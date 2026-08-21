---
date: 2026-08-20
tags: [navegación, outline, finanzas-cuantitativas, módulos-1-10]
---

# Outline — Finanzas Cuantitativas (M1–M10)

> **Cómo leer este archivo:** es un mapa de navegación. Cada sección es un bloque del curso con sus conceptos clave y los archivos de detalle donde se desarrolla el contenido. No repite lo que ya está en esos archivos.

---

## M1–M6 — Métodos Computacionales y Econométricos

**Resumen completo:** [`resumen_modulos_1_a_6.md`](resumen_modulos_1_a_6.md)

El hilo conductor es OLS: cada módulo resuelve un supuesto violado o añade una dimensión que OLS no puede capturar.

| Módulo | Contenido | Supuesto OLS que resuelve |
|---|---|---|
| M1 | OLS, β̂=(X'X)⁻¹X'y, R², AIC/BIC, t/F, VIF, DW, JB, 6 supuestos CLM | Base — define el problema |
| M2 | Monte Carlo, Bootstrap, variantes antipéticos, control variates, VaR por sim. | A6 sin supuesto distribucional |
| M3 | ML Financiero — clasificación, clustering, redes neuronales | Complemento no paramétrico |
| M4 | MA, AR, ARMA, ARIMA, VAR, cointegración (E-G/Johansen), ECM | A5 autocorrelación; A5+1 no estacionariedad |
| M5 | ARCH, GARCH, IGARCH/EWMA, GJR-GARCH, EGARCH, GARCH-M, MGARCH/DCC | A4 heterocedasticidad |
| M6 | Dummies, Markov Switching, TAR, SETAR, State Space, Filtro de Kalman | A1 no linealidad; parámetros variables |

---

## Hilo conductor

Los cuatro módulos son la misma historia contada con más honestidad cada vez:
> Los modelos asumen normalidad. Los mercados no son normales. Todo lo demás es gestionar esa contradicción.

| Módulo | Pregunta central | Herramienta clave |
|---|---|---|
| M7 | ¿Cuánto vale este activo? | Descuento de flujos, Black-Scholes |
| M8 | ¿Cómo gestiono el riesgo de tenerlo? | Delta hedging, superficie de volatilidad |
| M9 | ¿Cuánto puedo perder? | VaR, ES, modelos de crédito y liquidez |
| M10 | ¿Qué pasa en el 1% que el VaR ignora? | EVT, GPD, GEV |

---

## M7 — Valoración de Instrumentos Financieros

**Resumen completo:** [`resumen_modulo07.md`](7%20-%20Valoración%20de%20instrumentos%20financieros/resumen_modulo07.md)

Estructura interna en tres bloques:

### Bloque 1: Medición (T6–T10)
**Detalle:** [`Resumen_Temas_6-9.md`](7%20-%20Valoración%20de%20instrumentos%20financieros/temas%2006%20a%2010%20-%20Medición/Resumen_Temas_6-9.md)

| Tema | Concepto clave |
|---|---|
| T6 | Log-retornos aditivos; valor temporal del dinero; capitalización continua |
| T7 | 4 momentos (media, varianza, skewness, kurtosis); prima de riesgo; utilidad esperada |
| T8 | Distribuciones no normales: t de Student, Estable Paretiana, mezcla de normales, jump-diffusion, lognormal |
| T9 | Frontera eficiente Markowitz; $\sigma_P^2 = \mathbf{w}^T\Sigma\mathbf{w}$; Sharpe ratio; CAL |
| T10 | GMR, Safety-First (Roy/Kataoka/Telser), Dominancia Estocástica (FSD/SSD/TSD) |

**Python:** retornos, covarianza, frontera eficiente, Sharpe máximo
`temas 06 a 10 - Medición/01. measuring investmen risks/` y `02. Portfolio Allocation/`

---

### Bloque 2: Valoración I — Bonos, Acciones y Factores de Riesgo (T11–T17)
**Detalle:** [`resumen_temas_11_17_v2.md`](7%20-%20Valoración%20de%20instrumentos%20financieros/temas%2011%20a%2017%20-%20Valoración%20I/resumen_temas_11_17_v2.md)

| Tema | Concepto clave |
|---|---|
| T11 | Precio de bono, YTM, duration modificada $D^*$, convexidad, credit spread, repo |
| T12 | Spot/forward/short rates; bootstrapping; formas de curva y señal macro; Vasicek, Nelson-Siegel |
| T13 | DDM Gordon-Shapiro; FCFF/WACC; PVGO; P/E; corrección de Jensen |
| T14 | CAPM: $E(r_i)-r_f = \beta_i[E(r_M)-r_f]$; Single-Index Model; SML; betas ajustados |
| T15 | APT (Ross 1976); factores macro Chen-Roll-Ross; Fama-French 3F/4F/5F; liquidez Acharya-Pedersen |
| T16–T17 | No disponibles en el PDF del curso |

**Python:** beta por OLS, retorno esperado CAPM, Fama-French con datos reales
`temas 11 a 17 - Valoración I/03. CAPM modelo/` y `04. Multi factor models/`

---

### Bloque 3: Valoración II — Derivados y Pricing de Opciones (T18–T21)
**Detalle:** [`resumen_temas_18_21.md`](7%20-%20Valoración%20de%20instrumentos%20financieros/temas%2018%20a%2021%20-%20Valoración%20II/resumen_temas_18_21.md)

| Tema | Concepto clave |
|---|---|
| T18 | Forward, futuro, opción (derecho unilateral), swap — diferencias estructurales |
| T19 | Black-Scholes: $C = SN(d_1) - Ke^{-rT}N(d_2)$; paridad put-call; $\sigma$ = único input no observable |
| T20 | Monte Carlo directo sobre GBM: $S_T = S_0 e^{(r-\sigma^2/2)T + \sigma\sqrt{T}Z}$ |
| T21 | Euler: trayectoria paso a paso $\Delta t$ → generaliza a opciones path-dependent; no requiere solución analítica |

**Python:** B-S + MC sobre P&G ($S$=88.12, $K$=110, $\sigma$=0.176), Euler con 10k sim × 250 días
`temas 18 a 21 - Valoración II/05. Option pricing/` y `06. Euler discretization/`

---

## M8 — Gestión de Carteras de Inversión

**Resumen completo:** [`resumen_modulo08.md`](8%20-%20Gestión%20de%20carteras%20de%20inversión/resumen_modulo08.md)

| Tema | Concepto clave |
|---|---|
| T22 — Dynamic Hedging | $\Delta$: fracción de subyacente por opción vendida; $\Gamma$: coste de reajuste; Vega/Theta/Rho |
| T23 — Sonrisa de volatilidad | B-S como calculadora, no modelo; sesgo post-1987 en acciones; superficie 2D (strike × vencimiento) |
| T24 — Gestión activa | IR = $IC \times \sqrt{BR}$; Treynor-Black (bottom-up), Black-Litterman (bayesiano top-down), Risk Parity |

**Python:**

| Notebook | Qué hace |
|---|---|
| `1 - Treynor-Black.ipynb` | Alpha por activo → pesos óptimos activo/mercado |
| `2 - Black Litterman.ipynb` | Prior CAPM + views con Bayes → pesos posteriores |
| `3 - Risk Parity.ipynb` | Pesos $\propto$ 1/volatilidad; descarga precios con yfinance |

`Aplicaciones pyhton/`

---

## M9 — Gestión de Riesgos

**Resumen aplicado:** [`resumen_modulo09.md`](9%20-%20Gestión%20de%20riesgos/resumen_modulo09.md)
**Marco matemático T1–T12:** [`mates_de_detras.md`](9%20-%20Gestión%20de%20riesgos/mates_de_detras.md)

### Marco matemático (T1–T12) — base de todo lo que viene
| Bloque | Temas | Conceptos clave |
|---|---|---|
| Probabilidad y estadística | T1–T3 | Log-retornos, descuento, varianza, covarianza, $h^* = -\rho\sigma_A/\sigma_B$, skewness, kurtosis |
| Distribuciones | T4–T5 | Normal, lognormal, t, Poisson, binomial; cópulas (Clayton, Frank) para dependencia no lineal |
| Inferencia | T6–T7 | Bayes (prior → posterior), redes bayesianas; VaR como cuantil; backtesting binomial; ES subaditivo |
| Álgebra y simulación | T8–T9 | Cholesky para Monte Carlo multivariante; matrices de transición para ratings; PCA (3 factores = 95% curva tipos) |
| Regresión y series temporales | T10–T12 | OLS: $\hat{\beta}=(X'X)^{-1}X'Y$; GARCH(1,1); factores de decaimiento; Hybrid VaR |

### Aplicaciones prácticas
**Riesgo de mercado:** VaR paramétrico, histórico, Monte Carlo + Expected Shortfall
**Riesgo de crédito:** PD×LGD×EAD; K-means bucketing; logística con SMOTEENN; ROC-AUC
**Riesgo de liquidez:** 11 medidas (spread, Amihud, Florackis…) + GMM + GMCM + PCA por régimen

**Python:**

| Notebook | Qué hace |
|---|---|
| `Value at Risk.ipynb` | VaR paramétrico e histórico |
| `Expected Shortfall.ipynb` | ES paramétrico e histórico |
| `1 - MarketRISK.ipynb` | Pipeline completo: retornos → VaR → ES → backtesting |
| `CreditRisk.ipynb` | K-means → logística → SMOTEENN → ROC-AUC (`credit_data_risk.csv`) |
| `4 - Credit Risk Modelling in Python.ipynb` | Pipeline ampliado con UCI Credit Card |
| `LiquidityRisk.ipynb` | 11 medidas de liquidez → GMM → GMCM → PCA (`bid_ask.csv`) |

`Aplicaciones python/1 - Market Risk/`, `2 - Credit Risk/`, `3 - Liquidity Risk/`

---

## M10 — Teoría del Valor Extremo (EVT)

**Resumen completo:** [`resumen_modulo10.md`](10%20-%20Teoría%20del%20valor%20extremo/resumen_modulo10.md)

| Bloque | Concepto clave |
|---|---|
| T1 — Dos marcos | Block Maximum → GEV; POT → GPD. $\xi>0$ (Fréchet) = colas gruesas = finanzas |
| T2 — Estimación | MLE (Nelder-Mead); Hill (solo $\xi>0$, Hill plot); Pickands; De Haan-Resnick + corrección Huisman |
| T3 — VaR con EVT | VaR-Hill, VaR-POT, VaR-Block; EVT domina para cuantiles 99.9%+; normal puede errar hasta 16.000× |
| T4 — Avanzado | GARCH → residuos → EVT (i.i.d. requirement); EVT multivariante con cópulas; IC para VaR |

**Python:** `VaR_calculation.py` sobre S&P500 — 4 métodos secuenciales: normal (`norm.ppf`) → histórico (`quantile`) → Hill ($\hat{\xi}$, VaR≈-3.2%) → MLE GPD ($\hat{\xi}$=0.388, $\hat{\sigma}$=0.0075, VaR=-2.60%)
`Aplicaciones python/`

---

## Conexiones clave entre módulos

| Concepto | Sale de | Entra en |
|---|---|---|
| Log-retornos, $\sigma$ | M7 T6–7 | B-S (M7 T19), VaR paramétrico (M9) |
| Fat tails, distribuciones no normales | M7 T8 | Limitaciones B-S (M7), motivación EVT (M10) |
| Frontera eficiente, Sharpe | M7 T9 | CAPM (M7 T14), Risk Parity (M8) |
| $\beta$, prima de riesgo | M7 T14 | APT (M7 T15), Treynor-Black (M8), WACC en FCFF |
| Delta y griegas | M7 T19 + M8 T22 | Cobertura dinámica |
| Volatilidad implícita, superficie | M8 T23 | Pricing opciones (M7 T19) |
| VaR y sus limitaciones | M9 T7 | EVT como mejora (M10) |
| GARCH, clusters de volatilidad | M9 T11 | Filtrado previo a EVT (M10 T4) |
| Cópulas | M9 T5, liquidez | EVT multivariante (M10 T4) |
