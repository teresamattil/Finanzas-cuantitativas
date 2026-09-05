"""Métricas de riesgo-retorno sobre la serie de retornos de estrategia sin costes.

Grupo de control del TFM (volatility targeting sobre momentum): Paso 5, sobre `wml_returns`
y la curva de valor liquidativo ya construidos en `src/backtest.py` (Paso 4). Sin volatility
scaling (Paso 6) ni costes de transacción (Paso 8) — solo caracterización estadística de la
serie ya obtenida.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

MONTHS_PER_YEAR = 12


def annualized_return(returns: pd.Series) -> float:
    """Retorno medio mensual x 12 (anualización simple, no geométrica)."""
    return float(returns.dropna().mean() * MONTHS_PER_YEAR)


def annualized_vol(returns: pd.Series) -> float:
    """Volatilidad mensual (std, ddof=1) x sqrt(12)."""
    return float(returns.dropna().std(ddof=1) * np.sqrt(MONTHS_PER_YEAR))


def sharpe_ratio(returns: pd.Series) -> float:
    """Sharpe anualizado usando el retorno bruto de la cartera como "exceso de retorno".

    Convención estándar en la literatura de factores long-short autofinanciados
    (Barroso & Santa-Clara 2015, Fama-French): al tener exposición neta ~0 (ya
    validado en el Paso 3, suma pesos largos = +1 y cortos = -1), la cartera ya es
    una posición financiada con el propio short — no hace falta restar el tipo libre
    de riesgo, el retorno de la cartera ya es un exceso de retorno.
    """
    return annualized_return(returns) / annualized_vol(returns)


def sortino_ratio(returns: pd.Series) -> float:
    """Sortino anualizado: retorno anualizado / (std de los retornos negativos x sqrt(12)).

    El denominador es la desviación estándar (ddof=1) del subconjunto de meses con
    retorno negativo, anualizada — no la downside deviation completa respecto a un
    MAR distinto de cero.
    """
    serie = returns.dropna()
    negativos = serie[serie < 0]
    downside_vol = negativos.std(ddof=1) * np.sqrt(MONTHS_PER_YEAR)
    return annualized_return(returns) / downside_vol


def max_drawdown(cumulative: pd.Series) -> dict:
    """Máximo drawdown (valor negativo) sobre una curva de valor liquidativo, y su fecha."""
    curva = cumulative.dropna()
    drawdown = curva / curva.cummax() - 1.0
    fecha = drawdown.idxmin()
    return {"max_drawdown": float(drawdown.loc[fecha]), "fecha": fecha}


def calmar_ratio(annual_return: float, max_dd: float) -> float:
    """Retorno anualizado / |máximo drawdown|."""
    return annual_return / abs(max_dd)


def skew_kurtosis(returns: pd.Series) -> dict:
    """Asimetría y curtosis de `returns`.

    `kurtosis_exceso` usa la definición de Fisher (pandas `.kurt()`), donde una
    normal vale 0; `kurtosis_pearson` = `kurtosis_exceso + 3`, para comparar
    directamente con el valor de referencia clásico de una normal (3).
    """
    serie = returns.dropna()
    kurtosis_exceso = float(serie.kurt())
    return {
        "skew": float(serie.skew()),
        "kurtosis_exceso": kurtosis_exceso,
        "kurtosis_pearson": kurtosis_exceso + 3.0,
    }


def summary(returns: pd.Series, cumulative: pd.Series) -> pd.Series:
    """Tabla resumen (Series) con todas las métricas de riesgo-retorno del Paso 5."""
    ann_ret = annualized_return(returns)
    dd = max_drawdown(cumulative)
    sk = skew_kurtosis(returns)
    return pd.Series(
        {
            "retorno_medio_mensual": returns.dropna().mean(),
            "retorno_anualizado": ann_ret,
            "vol_mensual": returns.dropna().std(ddof=1),
            "vol_anualizada": annualized_vol(returns),
            "sharpe_anualizado": sharpe_ratio(returns),
            "sortino_anualizado": sortino_ratio(returns),
            "max_drawdown": dd["max_drawdown"],
            "fecha_max_drawdown": dd["fecha"],
            "calmar_ratio": calmar_ratio(ann_ret, dd["max_drawdown"]),
            "skew": sk["skew"],
            "kurtosis_exceso": sk["kurtosis_exceso"],
            "kurtosis_pearson": sk["kurtosis_pearson"],
        }
    )
