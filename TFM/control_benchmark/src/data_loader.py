"""Descarga, almacenamiento y control de calidad de precios de ETFs sectoriales.

Grupo de control del TFM (volatility targeting sobre momentum): universo de
ETFs iShares STOXX Europe 600 Sector UCITS, listados en Xetra.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
import yfinance as yf

LONG_COLUMNS = ["fecha", "ticker", "sector", "adj_close", "volume"]


@dataclass
class DownloadResult:
    ticker: str
    sector: str
    status: str  # "ok" | "empty" | "error"
    n_obs: int
    message: str = ""


def load_universe(csv_path: str | Path) -> pd.DataFrame:
    """Carga el universo de ETFs desde el CSV editable."""
    df = pd.read_csv(csv_path)
    required = {"sector", "ticker", "yahoo_ticker", "isin", "fecha_inception"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas en {csv_path}: {missing}")
    return df


def download_etf_history(
    yahoo_ticker: str,
    max_retries: int = 3,
    retry_wait_seconds: float = 2.0,
) -> pd.DataFrame:
    """Descarga el histórico diario completo (ajustado) de un ticker con yfinance.

    Devuelve un DataFrame con columnas [fecha, adj_close, volume], vacío si
    el ticker no tiene datos tras los reintentos.
    """
    last_error = ""
    for attempt in range(1, max_retries + 1):
        try:
            hist = yf.Ticker(yahoo_ticker).history(
                period="max", auto_adjust=True, actions=False
            )
        except Exception as exc:  # noqa: BLE001 - red de descarga externa
            last_error = str(exc)
            time.sleep(retry_wait_seconds)
            continue

        if hist.empty:
            last_error = "respuesta vacía"
            time.sleep(retry_wait_seconds)
            continue

        out = hist.reset_index()[["Date", "Close", "Volume"]].rename(
            columns={"Date": "fecha", "Close": "adj_close", "Volume": "volume"}
        )
        out["fecha"] = pd.to_datetime(out["fecha"]).dt.tz_localize(None)
        return out

    raise RuntimeError(last_error or "descarga fallida")


def download_universe(
    universe: pd.DataFrame,
    raw_dir: str | Path,
    log_path: str | Path,
    save_per_ticker: bool = True,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Descarga todo el universo y persiste en `raw_dir` en formato parquet.

    - Guarda un parquet por ETF (si `save_per_ticker`) y uno consolidado
      `precios_long.parquet` con formato long (fecha, ticker, sector,
      adj_close, volume).
    - Registra el resultado de cada descarga (ok/empty/error) en `log_path`
      en vez de fallar silenciosamente ante tickers no encontrados.

    Devuelve (df_long, log_df).
    """
    raw_dir = Path(raw_dir)
    raw_dir.mkdir(parents=True, exist_ok=True)

    frames: list[pd.DataFrame] = []
    results: list[DownloadResult] = []

    for row in universe.itertuples(index=False):
        try:
            hist = download_etf_history(row.yahoo_ticker)
        except Exception as exc:  # noqa: BLE001
            results.append(
                DownloadResult(row.ticker, row.sector, "error", 0, str(exc))
            )
            continue

        if hist.empty:
            results.append(
                DownloadResult(row.ticker, row.sector, "empty", 0, "sin observaciones")
            )
            continue

        hist["ticker"] = row.ticker
        hist["sector"] = row.sector
        hist = hist[LONG_COLUMNS]
        frames.append(hist)
        results.append(DownloadResult(row.ticker, row.sector, "ok", len(hist)))

        if save_per_ticker:
            hist.to_parquet(raw_dir / f"{row.ticker}.parquet", index=False)

    log_df = pd.DataFrame([r.__dict__ for r in results])
    Path(log_path).parent.mkdir(parents=True, exist_ok=True)
    log_df.to_csv(log_path, index=False)

    df_long = (
        pd.concat(frames, ignore_index=True)
        if frames
        else pd.DataFrame(columns=LONG_COLUMNS)
    )
    if not df_long.empty:
        df_long = df_long.sort_values(["ticker", "fecha"]).reset_index(drop=True)
        df_long.to_parquet(raw_dir / "precios_long.parquet", index=False)

    return df_long, log_df


def load_raw_long(raw_dir: str | Path) -> pd.DataFrame:
    """Carga el parquet consolidado en formato long ya descargado."""
    path = Path(raw_dir) / "precios_long.parquet"
    df = pd.read_parquet(path)
    df["fecha"] = pd.to_datetime(df["fecha"])
    return df


def count_business_day_gaps(fechas: pd.Series) -> int:
    """Cuenta días hábiles sin dato entre la primera y la última fecha de la serie."""
    if fechas.empty:
        return 0
    calendario = pd.bdate_range(fechas.min(), fechas.max())
    return int(len(calendario) - fechas.nunique())


def quality_summary(df_long: pd.DataFrame) -> pd.DataFrame:
    """Construye la tabla resumen de control de calidad por ETF.

    Para cada ticker: sector, primera y última fecha disponible, número de
    observaciones, huecos en días hábiles y volumen medio diario.
    """
    rows = []
    for (ticker, sector), g in df_long.groupby(["ticker", "sector"]):
        g = g.sort_values("fecha")
        rows.append(
            {
                "ticker": ticker,
                "sector": sector,
                "fecha_inicio": g["fecha"].min(),
                "fecha_fin": g["fecha"].max(),
                "n_obs": len(g),
                "n_huecos_dias_habiles": count_business_day_gaps(g["fecha"]),
                "volumen_medio_diario": g["volume"].mean(),
            }
        )
    return (
        pd.DataFrame(rows)
        .sort_values("fecha_inicio")
        .reset_index(drop=True)
    )


def monthly_coverage(df_long: pd.DataFrame) -> pd.Series:
    """Número de ETFs con datos vivos (entre su primera y última fecha) cada mes."""
    ranges = df_long.groupby("ticker")["fecha"].agg(["min", "max"])
    meses = pd.period_range(
        df_long["fecha"].min().to_period("M"),
        df_long["fecha"].max().to_period("M"),
        freq="M",
    )
    vivos = pd.Series(
        [
            ((ranges["min"].dt.to_period("M") <= m) & (ranges["max"].dt.to_period("M") >= m)).sum()
            for m in meses
        ],
        index=meses.to_timestamp(),
        name="n_etfs_vivos",
    )
    return vivos


def normalized_prices_common_origin(df_long: pd.DataFrame, base: float = 100.0) -> pd.DataFrame:
    """Precios normalizados a `base` desde el origen común (fecha en la que
    todos los ETFs del universo ya tienen datos).

    Devuelve un DataFrame ancho (fecha x ticker).
    """
    wide = df_long.pivot(index="fecha", columns="ticker", values="adj_close").sort_index()
    common_start = wide.dropna(how="any").index.min()
    if pd.isna(common_start):
        raise ValueError("No hay una fecha en la que coincidan todos los ETFs del universo")
    wide = wide.loc[common_start:]
    return wide.div(wide.iloc[0]).mul(base)
