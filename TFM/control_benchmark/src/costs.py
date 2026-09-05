"""Costes de transacción y financiación sobre las series de retorno de estrategia.

Grupo de control del TFM: Paso 8, sobre `wml_returns` (pura, Paso 4) y
`wml_returns_scaled_dailyvol` (escalada canónica, comprobación de vol diaria) — la versión
escalada con vol mensual del Paso 6 queda como diagnóstico, no se recalculan costes sobre
ella. Todos los parámetros de coste son argumentos con valores por defecto (no constantes
sueltas), pensados para variarse en el Paso 9 (sensibilidad).
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

DEFAULT_SPREAD_BPS = 10.0
DEFAULT_COMMISSION_BPS = 5.0
DEFAULT_SLIPPAGE_BPS = 0.0
DEFAULT_FUNDING_SPREAD_BPS = 50.0


def load_funding_rate(path: str | Path) -> pd.Series:
    """Carga el tipo de financiación de referencia desde un CSV diario, en fracción decimal.

    Fichero de referencia estático en `data/external/` (no forma parte del pipeline de
    descarga automática de `src/data_loader.py`): serie FRED `ECBMRRFR`, el tipo de
    referencia de las operaciones principales de financiación del BCE, con cobertura
    diaria 2008-presente. Se usa como proxy del EURIBOR a 1 mes porque no se consiguió
    una serie histórica fiable de EURIBOR 1M en este entorno — es una sustitución
    documentada, no el dato literal pedido, y debe tratarse como tal.
    """
    df = pd.read_csv(path, parse_dates=["observation_date"])
    valor_col = df.columns[1]
    return (df.set_index("observation_date")[valor_col] / 100.0).rename("funding_rate")


def portfolio_turnover(weights: pd.DataFrame) -> pd.Series:
    """Turnover mensual: suma de |cambio de peso| por ETF respecto al mes anterior.

    Los meses sin cartera formada (NaN en `weights`) se tratan como posición 0 (sin
    exposición) — así, entrar por primera vez en una cartera (o volver a entrar tras un
    hueco) se contabiliza como el turnover real de construirla desde cero, no como NaN ni
    como 0 por falta de mes anterior.
    """
    pesos = weights.fillna(0.0)
    pesos_anterior = pesos.shift(1).fillna(0.0)
    return (pesos - pesos_anterior).abs().sum(axis=1).rename("turnover")


def scaled_weights(weights: pd.DataFrame, multiplier: pd.Series) -> pd.DataFrame:
    """Pesos efectivamente mantenidos por la cartera escalada: `multiplicador_t * peso_i,t`."""
    return weights.mul(multiplier, axis=0)


def transaction_costs(
    turnover: pd.Series,
    spread_bps: float = DEFAULT_SPREAD_BPS,
    commission_bps: float = DEFAULT_COMMISSION_BPS,
    slippage_bps: float = DEFAULT_SLIPPAGE_BPS,
) -> pd.Series:
    """Coste de transacción mensual = turnover x (spread + comisión + slippage).

    Todo en puntos básicos (10 = 0.10%) sobre cada unidad de turnover. `turnover` ya suma
    el valor absoluto de cada operación, así que el coste no se duplica ni se divide entre
    compra/venta. `slippage_bps=0` por defecto (ETFs UCITS grandes y líquidos, tamaño de
    cartera de un TFM — sin impacto de mercado relevante); se deja como parámetro explícito
    en vez de asumirlo tácitamente, para poder activarlo en el análisis de sensibilidad.
    """
    coste_por_unidad = (spread_bps + commission_bps + slippage_bps) / 10_000
    return (turnover * coste_por_unidad).rename("coste_transaccion")


def leverage_financing_cost(
    multiplier: pd.Series,
    funding_rate_annual: pd.Series,
    funding_spread_bps: float = DEFAULT_FUNDING_SPREAD_BPS,
) -> pd.Series:
    """Coste de financiación mensual del apalancamiento cuando `multiplier` > 1.

    Se aplica solo sobre el EXCESO de exposición por encima de 1x (`multiplier - 1`,
    recortado a 0 si es negativo — no hay "ingreso" por infra-exposición), a la tasa
    `funding_rate_annual + funding_spread_bps` (anual, ya alineada al índice de
    `multiplier`), prorrateada a mensual (÷12).
    """
    exceso_exposicion = (multiplier - 1.0).clip(lower=0.0)
    tasa_anual = funding_rate_annual + funding_spread_bps / 10_000
    return (exceso_exposicion * tasa_anual / 12.0).rename("coste_financiacion")


def net_returns(
    gross_returns: pd.Series,
    turnover: pd.Series,
    spread_bps: float = DEFAULT_SPREAD_BPS,
    commission_bps: float = DEFAULT_COMMISSION_BPS,
    slippage_bps: float = DEFAULT_SLIPPAGE_BPS,
    financing_cost: pd.Series | None = None,
) -> pd.Series:
    """Retorno neto = retorno bruto − coste de transacción [− coste de financiación]."""
    neto = gross_returns - transaction_costs(turnover, spread_bps, commission_bps, slippage_bps)
    if financing_cost is not None:
        neto = neto - financing_cost
    return neto.rename("wml_return_net")


def average_annual_cost(gross_returns: pd.Series, net_returns: pd.Series) -> float:
    """Coste medio anualizado, en fracción decimal: media mensual de (bruto − neto) x 12."""
    return float((gross_returns - net_returns).dropna().mean() * 12)
