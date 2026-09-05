"""Volatility targeting sobre la serie de retornos de estrategia (Barroso & Santa-Clara, 2015).

Grupo de control del TFM: Paso 6, sobre `wml_returns` (Paso 4) — estimación de `sigma_hat`
con retornos MENSUALES (ventana de 6 observaciones). Ampliado para una comprobación puntual
posterior al Paso 7: estimación de `sigma_hat` con retornos DIARIOS (ventana de 126 días,
la convención literal del paper) manteniendo el rebalanceo mensual de la cartera, para
aislar si el resultado mixto del Paso 7 se debe a la baja frecuencia de estimación o al
propio universo. Solo construye y verifica series escaladas — la tabla comparativa formal
de métricas es el Paso 7 (y su ampliación con la versión diaria), no este módulo.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

MONTHS_PER_YEAR = 12
TRADING_DAYS_PER_YEAR = 252


def rolling_realized_vol(returns: pd.Series, window: int = 6) -> pd.Series:
    """Volatilidad realizada anualizada, rolling de `window` meses, alineada sin look-ahead.

    El valor en el índice t usa solo retornos hasta t-1: `.rolling(window).std()` en la
    posición t cubre [t-window+1, t] (incluye t), así que se aplica `.shift(1)` para que
    el valor devuelto en t corresponda a la ventana [t-window, t-1] — nunca incluye el
    propio retorno de t. Anualizada x√12 para ser comparable con `sigma_target`.

    Adaptación explícita del paper: Barroso & Santa-Clara (2015) usan una ventana de ~126
    días de negociación diarios (~6 meses de calendario). Aquí solo hay datos mensuales
    (el universo de control no tiene frecuencia diaria de señal/retorno), así que la
    ventana se traduce directamente a 6 observaciones MENSUALES — no son estimaciones
    equivalentes en precisión estadística (6 puntos mensuales es una muestra muy pequeña
    para estimar una desviación estándar, frente a ~126 puntos diarios), es una limitación
    de este universo de control que hay que tener presente al interpretar los resultados.
    """
    return returns.rolling(window).std(ddof=1).mul(np.sqrt(MONTHS_PER_YEAR)).shift(1)


def assert_no_lookahead(
    sigma_hat: pd.Series,
    returns: pd.Series,
    window: int,
    annualization_factor: float = np.sqrt(MONTHS_PER_YEAR),
) -> int:
    """Verifica que `sigma_hat` en cada fecha t solo usa `returns` hasta t-1.

    Para cada fecha con `sigma_hat` no nulo, recalcula la std de la ventana
    [t-window, t-1] a partir de `returns` y comprueba que coincide exactamente. Lanza
    `AssertionError` en el primer desajuste. Devuelve el número de fechas comprobadas.
    `annualization_factor` debe coincidir con el usado para construir `sigma_hat`
    (√12 por defecto para la versión mensual del Paso 6; √252 para la versión diaria).
    """
    idx = returns.index
    comprobados = 0
    for i in range(window, len(idx)):
        t = idx[i]
        valor = sigma_hat.get(t, np.nan)
        if pd.isna(valor):
            continue
        ventana = returns.iloc[i - window : i]  # posiciones i-window .. i-1, es decir hasta t-1
        esperado = ventana.std(ddof=1) * annualization_factor
        if not np.isclose(valor, esperado, equal_nan=True):
            raise AssertionError(
                f"Look-ahead detectado: sigma_hat en {t} no coincide con la ventana hasta t-1"
            )
        comprobados += 1
    assert comprobados > 0, "No se pudo verificar ninguna fecha (revisar ventana/serie)"
    return comprobados


def scaling_multiplier(sigma_hat: pd.Series, sigma_target: float) -> pd.Series:
    """Multiplicador de exposición del volatility targeting: sigma_target / sigma_hat_{t-1}."""
    return sigma_target / sigma_hat


def scale_returns(returns: pd.Series, sigma_hat: pd.Series, sigma_target: float) -> pd.Series:
    """r_scaled_t = (sigma_target / sigma_hat_{t-1}) * r_t (Barroso & Santa-Clara, 2015).

    NaN donde `sigma_hat` es NaN (ventana rolling incompleta, primeros meses) o donde
    `returns` es NaN (sin cartera formada) — no se imputa nada.
    """
    multiplicador = scaling_multiplier(sigma_hat, sigma_target)
    return (multiplicador * returns).rename("wml_return_scaled")


def daily_portfolio_returns(daily_prices: pd.DataFrame, weights: pd.DataFrame) -> pd.Series:
    """Retorno diario de la cartera aplicando el peso formado el mes calendario anterior.

    Mismo timing que el backtest mensual (Paso 4): el peso fijado en el cierre del mes t-1
    (`weights`, panel del Paso 3) se aplica sin cambios a cada día de negociación del mes
    t — no hay rebalanceo intramés, solo cambia el retorno diario de cada ETF ponderado.
    NaN en los días cuyo mes de formación no tiene cartera formada (Paso 3), o antes de que
    exista ninguna fila de pesos.
    """
    daily_returns = daily_prices.pct_change()

    # Para cada día, el mes de formación es el mes calendario anterior (fin de ese mes).
    formation_month_end = (
        (pd.PeriodIndex(daily_returns.index, freq="M") - 1).to_timestamp(how="end").normalize()
    )
    pesos_por_dia = weights.reindex(formation_month_end)
    pesos_por_dia.index = daily_returns.index

    cols = daily_returns.columns.intersection(weights.columns)
    retorno = (pesos_por_dia[cols] * daily_returns[cols]).sum(axis=1, min_count=1)
    valid = pesos_por_dia[cols].notna().any(axis=1)
    return retorno.where(valid).rename("wml_return_daily")


def rolling_realized_vol_daily(daily_returns: pd.Series, window: int = 126) -> pd.Series:
    """Como `rolling_realized_vol`, pero a frecuencia diaria: ventana de `window` días de
    negociación (126 ≈ la convención literal de Barroso & Santa-Clara, 2015, frente a los 6
    meses/observaciones usados en el Paso 6), anualizada x√252. Mismo `.shift(1)` sin
    look-ahead, verificable con `assert_no_lookahead(..., annualization_factor=np.sqrt(252))`.
    """
    return daily_returns.rolling(window).std(ddof=1).mul(np.sqrt(TRADING_DAYS_PER_YEAR)).shift(1)


def sample_at_month_end(daily_series: pd.Series, month_end_index: pd.DatetimeIndex) -> pd.Series:
    """Muestrea `daily_series` en cada fecha de `month_end_index` (`ffill`).

    Las etiquetas de fin de mes calendario (p. ej. `momentum`/`wml_returns`, de
    `resample("ME")`) no siempre coinciden con un día de negociación real — `ffill` toma el
    último valor diario disponible en o antes de esa fecha, que es el vigente ese mes.
    """
    return daily_series.reindex(month_end_index, method="ffill")
