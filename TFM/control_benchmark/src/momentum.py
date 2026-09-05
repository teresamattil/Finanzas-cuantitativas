"""Construcción de la señal momentum (12-1) y su ranking transversal.

Grupo de control del TFM (volatility targeting sobre momentum): Paso 2, sobre
el panel de precios ya descargado y validado en `src/data_loader.py`.
"""

from __future__ import annotations

import pandas as pd


def monthly_close_wide(df_long: pd.DataFrame) -> pd.DataFrame:
    """Precios mensualizados en panel ancho (fecha fin de mes x ticker).

    Convención: último precio de calendario disponible en cada mes
    (`resample("ME").last()`), no el último día hábil teórico del mes. Un mes
    sin ninguna observación queda como NaN, no se interpola.
    """
    wide = df_long.pivot(index="fecha", columns="ticker", values="adj_close").sort_index()
    return wide.resample("ME").last()


def monthly_continuity_mask(monthly_prices: pd.DataFrame, lookback: int) -> pd.DataFrame:
    """True en (t, ticker) si hay dato mensual ininterrumpido en t-1 ... t-lookback.

    Exige `lookback` observaciones mensuales consecutivas inmediatamente
    anteriores a t; un solo mes con NaN en esa ventana invalida el mes t.
    """
    present = monthly_prices.notna()
    window_count = present.shift(1).rolling(lookback).sum()
    return window_count == lookback


def momentum_12_1(
    monthly_prices: pd.DataFrame, lookback: int = 12, skip: int = 2
) -> pd.DataFrame:
    """Señal momentum: retorno acumulado entre t-lookback y t-skip meses.

    Por defecto (`lookback=12, skip=2`): `P(t-2) / P(t-12) - 1`, es decir, el
    retorno acumulado excluyendo el último mes disponible (t-1), para evitar
    contaminar la señal con el efecto de reversión a corto plazo.

    Un ETF solo tiene señal válida en el mes t si tiene los `lookback` meses
    anteriores sin huecos (ver `monthly_continuity_mask`); si no, queda NaN.
    """
    far = monthly_prices.shift(lookback)
    near = monthly_prices.shift(skip)
    signal = near / far - 1.0
    valid = monthly_continuity_mask(monthly_prices, lookback)
    return signal.where(valid)


def cross_sectional_percentile_rank(signal: pd.DataFrame) -> pd.DataFrame:
    """Percentil (0-1) de cada ETF entre los que tienen señal válida ese mes.

    Ranking transversal (por fila/mes, no a lo largo del tiempo), así es
    comparable entre meses con distinto número de ETFs disponibles. NaN se
    mantiene como NaN (no participa en el ranking).
    """
    return signal.rank(axis=1, pct=True, na_option="keep")


def valid_signal_count(signal: pd.DataFrame) -> pd.Series:
    """Número de ETFs con señal momentum válida (no NaN) en cada mes."""
    return signal.notna().sum(axis=1).rename("n_etfs_con_senal")


def rank_month_over_month_autocorrelation(rank: pd.DataFrame) -> pd.Series:
    """Correlación transversal entre el ranking de t y el de t-1, mes a mes.

    Para cada mes t, correla (por Pearson, sobre percentiles) el ranking de
    los ETFs que tienen señal válida tanto en t como en t-1. Es una
    comprobación informal de persistencia del ranking: valores altos y
    estables sugieren que el orden de un mes predice el del siguiente.
    """
    corr = {}
    prev = None
    for date, row in rank.iterrows():
        if prev is not None:
            pair = pd.concat([prev, row], axis=1, keys=["t_1", "t"]).dropna()
            if len(pair) >= 2:
                corr[date] = pair["t_1"].corr(pair["t"])
        prev = row
    return pd.Series(corr, name="autocorr_rank_t_vs_t_1")
