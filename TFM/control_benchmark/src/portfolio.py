"""Validación de la señal momentum y construcción de pesos de cartera por tercil.

Grupo de control del TFM (volatility targeting sobre momentum): Paso 3, sobre los
paneles de señal y ranking ya construidos en `src/momentum.py`. Aquí termina el paso:
solo se genera un panel de PESOS, no una serie de retornos de estrategia (eso es el
motor de backtest del Paso 4).
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm


def forward_monthly_return(monthly_prices: pd.DataFrame) -> pd.DataFrame:
    """Retorno REAL del mes siguiente: `P(t+1) / P(t) - 1`.

    A diferencia de la señal momentum (que mira hacia atrás desde t), esto mira
    hacia delante — es lo que se usa para validar si la señal predice algo.
    """
    return monthly_prices.shift(-1) / monthly_prices - 1.0


def assign_groups(rank_pct: pd.DataFrame, n_groups: int = 3) -> pd.DataFrame:
    """Agrupa el percentil de ranking transversal en `n_groups` grupos de igual tamaño.

    Grupo 0 = peor (percentil más bajo), grupo `n_groups - 1` = mejor. Como el
    percentil ya está normalizado por mes (Paso 2), los cortes son fijos en [0, 1] y
    no hace falta recalcular nada por mes. NaN se mantiene como NaN (sin grupo).
    """
    edges = np.linspace(0.0, 1.0, n_groups + 1)
    codes = pd.cut(rank_pct.to_numpy().ravel(), bins=edges, labels=False, include_lowest=True)
    return pd.DataFrame(
        codes.reshape(rank_pct.shape), index=rank_pct.index, columns=rank_pct.columns
    )


def group_forward_returns(fwd_returns: pd.DataFrame, groups: pd.DataFrame) -> pd.DataFrame:
    """Retorno forward medio por grupo y mes (columnas = código de grupo 0..n_groups-1)."""
    rows = {}
    for date in groups.index:
        pair = pd.concat(
            [groups.loc[date].rename("grupo"), fwd_returns.loc[date].rename("fwd_ret")],
            axis=1,
        ).dropna()
        if not pair.empty:
            rows[date] = pair.groupby("grupo")["fwd_ret"].mean()
    return pd.DataFrame(rows).T.sort_index()


def winner_loser_spread(group_returns: pd.DataFrame, n_groups: int) -> pd.Series:
    """Retorno forward medio del grupo ganador menos el del grupo perdedor, mes a mes."""
    return (group_returns[n_groups - 1] - group_returns[0]).rename("spread_ganador_perdedor")


def t_stat(series: pd.Series) -> float:
    """t-estadístico de la media de `series` frente a cero (t = media / (std / sqrt(n)))."""
    serie = series.dropna()
    return float(serie.mean() / (serie.std(ddof=1) / np.sqrt(len(serie))))


def find_signal_outliers(signal: pd.DataFrame, threshold: float = 0.75) -> pd.DataFrame:
    """Observaciones (fecha, ticker, señal) por encima de `threshold`, de mayor a menor."""
    stacked = signal.stack().dropna()
    out = stacked[stacked > threshold].rename("senal").reset_index()
    out.columns = ["fecha", "ticker", "senal"]
    return out.sort_values("senal", ascending=False).reset_index(drop=True)


def price_window(
    df_long: pd.DataFrame, ticker: str, center_date, n_days: int = 10
) -> pd.DataFrame:
    """Precios diarios ajustados de `ticker` en +/- `n_days` sesiones alrededor de `center_date`."""
    serie = (
        df_long.loc[df_long["ticker"] == ticker]
        .set_index("fecha")["adj_close"]
        .sort_index()
    )
    pos = serie.index.searchsorted(pd.Timestamp(center_date))
    lo, hi = max(pos - n_days, 0), min(pos + n_days + 1, len(serie))
    return serie.iloc[lo:hi].to_frame(name="adj_close")


def inspect_signal_outlier(
    df_long: pd.DataFrame,
    monthly_index: pd.DatetimeIndex,
    fecha: pd.Timestamp,
    ticker: str,
    lookback: int = 12,
    skip: int = 2,
    n_days: int = 10,
) -> dict[str, pd.DataFrame]:
    """Ventanas de precio diario alrededor de los dos meses (t-lookback y t-skip) que
    componen la señal momentum en (fecha, ticker) — son los dos puntos donde un salto
    real o un artefacto de ajuste haría saltar el valor de la señal.
    """
    pos = monthly_index.get_loc(fecha)
    fecha_lejana = monthly_index[pos - lookback]
    fecha_cercana = monthly_index[pos - skip]
    return {
        f"t-{lookback} ({fecha_lejana.date()})": price_window(df_long, ticker, fecha_lejana, n_days),
        f"t-{skip} ({fecha_cercana.date()})": price_window(df_long, ticker, fecha_cercana, n_days),
    }


def build_group_weights(
    groups: pd.DataFrame, n_groups: int, long_short: bool = True
) -> pd.DataFrame:
    """Pesos equal-weight por mes a partir de los grupos de tercil.

    Long en el grupo ganador (`n_groups - 1`), con pesos que suman +1 ese mes. Si
    `long_short=True`, además short en el grupo perdedor (grupo 0) con pesos que suman
    -1, dejando la cartera auto-financiada (exposición neta ~0); si no, solo hay
    posiciones largas. Solo se implementa equal-weight dentro de cada tercil (no
    ponderación por score). Meses sin grupo ganador (o perdedor, si `long_short`)
    formable quedan enteros en NaN — no se puede construir cartera ese mes.
    """
    winner = groups == (n_groups - 1)
    loser = groups == 0
    if long_short and (winner & loser).to_numpy().any():
        raise AssertionError("Un ETF no puede estar simultáneamente en el grupo ganador y perdedor")

    n_winner = winner.sum(axis=1)
    weights = winner.div(n_winner.replace(0, np.nan), axis=0).fillna(0.0)
    valid = n_winner > 0

    if long_short:
        n_loser = loser.sum(axis=1)
        w_loser = loser.div(n_loser.replace(0, np.nan), axis=0).fillna(0.0)
        weights = weights - w_loser
        valid = valid & (n_loser > 0)

    weights.loc[~valid] = np.nan
    return weights


def validate_weights(weights: pd.DataFrame, long_short: bool = True, atol: float = 1e-8) -> pd.DataFrame:
    """Por mes: suma de pesos largos, suma de pesos cortos y si hay cartera formada.

    Lanza `AssertionError` si en algún mes con cartera formada la suma de largos no es
    1 (o la de cortos no es -1, cuando `long_short=True`).
    """
    long_sum = weights.where(weights > 0, 0.0).sum(axis=1)
    short_sum = weights.where(weights < 0, 0.0).sum(axis=1)
    formada = weights.notna().any(axis=1)

    check = pd.DataFrame(
        {
            "suma_pesos_largos": long_sum,
            "suma_pesos_cortos": short_sum,
            "cartera_formada": formada,
        }
    )

    formados = check.loc[check["cartera_formada"]]
    assert np.allclose(formados["suma_pesos_largos"], 1.0, atol=atol), (
        "La suma de pesos largos no es 1 en algún mes con cartera formada"
    )
    if long_short:
        assert np.allclose(formados["suma_pesos_cortos"], -1.0, atol=atol), (
            "La suma de pesos cortos no es -1 en algún mes con cartera formada"
        )

    return check


def spread_summary(series: pd.Series) -> dict[str, float]:
    """Media, desviación estándar, t-stat (frente a cero) y nº de meses de `series`."""
    serie = series.dropna()
    return {
        "media": float(serie.mean()),
        "std": float(serie.std(ddof=1)),
        "t_stat": t_stat(serie),
        "n": int(len(serie)),
    }


def most_extreme_months(series: pd.Series, n: int = 5) -> pd.DataFrame:
    """Los `n` meses con mayor valor absoluto de `series`, de más a menos extremo."""
    serie = series.dropna()
    idx = serie.abs().sort_values(ascending=False).index[:n]
    out = serie.loc[idx].rename("spread").reset_index()
    out.columns = ["fecha", "spread"]
    return out.sort_values("spread", key=lambda s: s.abs(), ascending=False).reset_index(drop=True)


def group_members(groups: pd.DataFrame, date, n_groups: int) -> dict[str, list[str]]:
    """Tickers del tercil ganador y perdedor en `date` (grupo `n_groups - 1` y grupo 0)."""
    fila = groups.loc[date]
    return {
        "ganador": sorted(fila.index[fila == (n_groups - 1)]),
        "perdedor": sorted(fila.index[fila == 0]),
    }


def newey_west_tstat(series: pd.Series, maxlags: int) -> tuple[float, float]:
    """Media y t-stat de `series` (frente a cero) con errores estándar HAC (Newey-West).

    Regresión OLS de la serie sobre una constante con `cov_type="HAC"`: el coeficiente
    es la media simple, pero el error estándar (y por tanto el t-stat) es robusto a
    autocorrelación y heterocedasticidad hasta `maxlags` retardos.
    """
    serie = series.dropna()
    modelo = sm.OLS(serie.to_numpy(), np.ones(len(serie)))
    resultado = modelo.fit(cov_type="HAC", cov_kwds={"maxlags": maxlags})
    return float(resultado.params[0]), float(resultado.tvalues[0])
