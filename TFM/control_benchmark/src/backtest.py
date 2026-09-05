"""Motor de backtest frictionless: aplica pesos mensuales a retornos realizados.

Grupo de control del TFM (volatility targeting sobre momentum): Paso 4, sobre el panel de
pesos ya construido en `src/portfolio.py`. Sin costes de transacción, sin métricas de
riesgo-retorno (Paso 5) ni volatility scaling (Paso 6) — el único objetivo es la serie de
retorno mensual de la estrategia (proxy de WML_t).
"""

from __future__ import annotations

import pandas as pd


def strategy_returns(
    weights: pd.DataFrame,
    forward_returns: pd.DataFrame,
    cartera_formada: pd.Series,
) -> pd.Series:
    """Retorno mensual de la estrategia: `sum_i peso_i,t * retorno_i,t+1`.

    Sin look-ahead: `weights` está indexado por la fecha de formación t (información
    disponible hasta t — la señal 12-1 ya excluye el último mes), y se multiplica por
    `forward_returns`, que representa el retorno YA REALIZADO de t a t+1
    (`port.forward_monthly_return`, construido con `shift(-1)`). El peso nunca ve datos
    posteriores a t; el retorno aplicado nunca es anterior a t+1.

    Meses sin cartera formada quedan en NaN (no en 0): no hay estrategia "plana" esos
    meses, hay ausencia de señal.
    """
    assert weights.index.isin(forward_returns.index).all(), (
        "El panel de pesos tiene fechas fuera del panel de retornos forward"
    )
    fwd = forward_returns.reindex(index=weights.index, columns=weights.columns)
    retorno = (weights * fwd).sum(axis=1, min_count=1)

    formada = cartera_formada.reindex(weights.index).fillna(False)
    return retorno.where(formada).rename("wml_return")


def cumulative_growth(returns: pd.Series, base: float = 1.0) -> pd.Series:
    """Valor liquidativo acumulado desde `base`, componiendo `(1 + retorno)`.

    Los meses sin retorno (NaN, sin cartera formada) se tratan como 0% solo a efectos de
    continuidad de la curva (`fillna(0.0)`) — no implica que la estrategia tuviera
    posición esos meses, solo evita que la curva se corte.
    """
    return base * (1.0 + returns.fillna(0.0)).cumprod()
