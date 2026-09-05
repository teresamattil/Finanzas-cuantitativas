"""Tests de robustez del grupo de control: bandas de no-operación, sensibilidad a costes,
a la ventana de formación/rebalanceo, y por sub-periodo.

Paso 9, el último de la fase de control. Reutiliza los módulos de los pasos anteriores
(`momentum`, `portfolio`, `backtest`, `vol_scaling`, `metrics`, `costs`) para poder repetir
el pipeline completo (Pasos 2-8) con parámetros distintos sin duplicar su lógica.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from src import backtest as bt
from src import costs as cst
from src import metrics as met
from src import momentum as mom
from src import portfolio as port
from src import vol_scaling as vs


def apply_no_trade_band(multiplier: pd.Series, threshold: float = 0.15) -> pd.Series:
    """Multiplicador con banda de no-operación de `threshold` (0.15 = ±15%).

    Solo se actualiza el multiplicador aplicado (y por tanto solo se retradea) cuando el
    multiplicador bruto se desvía más de `threshold` respecto al último aplicado — si no,
    se mantiene el anterior. Un hueco de NaN rompe la cadena: al reaparecer dato, se
    re-ancla al primer valor bruto disponible (no se arrastra un multiplicador de antes
    del hueco).
    """
    aplicado = None
    salida = []
    for m in multiplier.to_numpy():
        if np.isnan(m):
            salida.append(np.nan)
            aplicado = None
            continue
        if aplicado is None or abs(m / aplicado - 1.0) > threshold:
            aplicado = m
        salida.append(aplicado)
    return pd.Series(salida, index=multiplier.index, name="multiplicador_banda")


def scale_with_multiplier(returns: pd.Series, multiplier: pd.Series) -> pd.Series:
    """r_t * multiplicador_t, cuando el multiplicador ya está calculado (p. ej. con banda)
    en vez de partir de `sigma_hat`/`sigma_target` (eso es `vol_scaling.scale_returns`)."""
    return (multiplier * returns).rename("wml_return_scaled_band")


def resample_rebalance(weights: pd.DataFrame, every_n_months: int) -> pd.DataFrame:
    """Mantiene el peso fijo `every_n_months` meses en vez de recalcularlo cada mes.

    Se queda con la fila de `weights` cada `every_n_months` posiciones (contando desde el
    principio del panel) como fecha de reforma, y arrastra ese mismo peso (`ffill`) en los
    meses intermedios hasta la siguiente reforma.
    """
    resultado = weights.copy()
    es_reforma = (np.arange(len(weights)) % every_n_months) == 0
    resultado.loc[~es_reforma] = np.nan
    return resultado.ffill()


def run_scenario(
    df_long: pd.DataFrame,
    daily_prices: pd.DataFrame,
    funding_rate_monthly: pd.Series,
    sigma_target: float,
    lookback: int = 12,
    skip: int = 2,
    n_groups: int = 3,
    rebalance_every_n_months: int = 1,
    vol_window_daily: int = 126,
    spread_bps: float = cst.DEFAULT_SPREAD_BPS,
    commission_bps: float = cst.DEFAULT_COMMISSION_BPS,
    funding_spread_bps: float = cst.DEFAULT_FUNDING_SPREAD_BPS,
) -> dict[str, float]:
    """Ejecuta el pipeline completo (Pasos 2-8: señal -> ranking -> pesos -> backtest ->
    vol scaling diario -> costes) para una combinación de parámetros, y devuelve solo las
    métricas finales netas — para barridos de sensibilidad, no para inspección paso a paso
    (esa ya se hizo para la especificación base en los Pasos 2-8).

    `sigma_target` se mantiene fijo entre escenarios (el de la especificación base, Paso 5)
    para que las comparaciones aíslen el efecto de cada parámetro, no el del propio target.
    """
    monthly_prices = mom.monthly_close_wide(df_long)
    signal = mom.momentum_12_1(monthly_prices, lookback=lookback, skip=skip)
    rank = mom.cross_sectional_percentile_rank(signal)
    groups = port.assign_groups(rank, n_groups=n_groups)
    weights = port.build_group_weights(groups, n_groups, long_short=True)

    if rebalance_every_n_months > 1:
        weights = resample_rebalance(weights, rebalance_every_n_months)

    forward_returns = port.forward_monthly_return(monthly_prices)
    cartera_formada = weights.notna().any(axis=1)
    wml_returns = bt.strategy_returns(weights, forward_returns, cartera_formada)

    wml_daily = vs.daily_portfolio_returns(daily_prices, weights)
    sigma_hat_daily = vs.rolling_realized_vol_daily(wml_daily, window=vol_window_daily)
    sigma_hat_mensual = vs.sample_at_month_end(sigma_hat_daily, wml_returns.index)
    wml_scaled = vs.scale_returns(wml_returns, sigma_hat_mensual, sigma_target)

    turnover_pura = cst.portfolio_turnover(weights)
    multiplicador = vs.scaling_multiplier(sigma_hat_mensual, sigma_target)
    turnover_escalada = cst.portfolio_turnover(cst.scaled_weights(weights, multiplicador))

    wml_returns_net = cst.net_returns(wml_returns, turnover_pura, spread_bps, commission_bps)
    coste_financiacion = cst.leverage_financing_cost(multiplicador, funding_rate_monthly, funding_spread_bps)
    wml_scaled_net = cst.net_returns(
        wml_scaled, turnover_escalada, spread_bps, commission_bps, financing_cost=coste_financiacion
    )

    return {
        "sharpe_pura_neto": met.sharpe_ratio(wml_returns_net),
        "sortino_pura_neto": met.sortino_ratio(wml_returns_net),
        "sharpe_escalada_neto": met.sharpe_ratio(wml_scaled_net),
        "sortino_escalada_neto": met.sortino_ratio(wml_scaled_net),
        "turnover_medio_pura": float(turnover_pura.mean()),
        "turnover_medio_escalada": float(turnover_escalada.mean()),
    }
