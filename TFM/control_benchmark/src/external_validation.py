"""Validación externa: réplica del análisis núcleo sobre el factor Europe Momentum (WML) de
la librería de datos de Kenneth French — benchmark académico independiente, construido sobre
cientos de acciones de 16 países europeos, frente al universo pequeño y concentrado de 19
ETFs sectoriales del grupo de control.

Reutiliza `src/metrics.py` y `src/vol_scaling.py` tal cual (no se reimplementa nada de
métricas ni de escalado). No se repite el Paso 8 (costes de transacción): el factor de
French no trae turnover ni composición de cartera real, así que aplicar un supuesto de
coste aquí sería inventarlo sin base — esta sección se queda deliberadamente en bruto.
"""

from __future__ import annotations

import pandas as pd
import pandas_datareader.data as web

MISSING_CODE = -99.99

DATASET_NAMES = {
    "monthly": "Europe_Mom_Factor",
    "daily": "Europe_Mom_Factor_Daily",
}


def download_europe_momentum_factor(frequency: str) -> pd.Series:
    """Descarga el factor WML (Europe Mom, Kenneth French) en fracción decimal.

    `frequency`: "monthly" o "daily" (nombres de dataset confirmados con
    `pandas_datareader.famafrench.get_available_datasets()`, no de memoria:
    `Europe_Mom_Factor` y `Europe_Mom_Factor_Daily`).

    French publica el factor en PORCENTAJE (p. ej. 2.45 = 2.45%) y usa -99.99 como código
    de dato faltante — ambas cosas se corrigen aquí explícitamente antes de devolver la
    serie, para no mezclar por error unidades distintas con las series propias (que están
    en fracción decimal desde el Paso 4).
    """
    dataset = DATASET_NAMES[frequency]
    datos = web.DataReader(dataset, "famafrench", start="1900-01-01")
    serie = datos[0]["WML"].replace(MISSING_CODE, pd.NA).astype(float) / 100.0

    if isinstance(serie.index, pd.PeriodIndex):
        how = "end" if frequency == "monthly" else "start"
        serie.index = serie.index.to_timestamp(how=how).normalize()
    else:
        serie.index = pd.to_datetime(serie.index)

    return serie.rename("europe_mom")
