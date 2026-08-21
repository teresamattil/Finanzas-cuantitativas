---
date: 2026-08-20
tags: [resumen, módulos-1-6, econometría, simulación, series-temporales, volatilidad]
---

# Resumen — Módulos 1 a 6

> Estos módulos son la base metodológica del máster. El hilo que los conecta es OLS: cada módulo o resuelve uno de sus supuestos violados o añade una dimensión que OLS no puede capturar.

---

## Hilo conductor — OLS y sus extensiones

OLS como punto de partida: `yₜ = α + βxₜ + uₜ` → `β̂ = (X'X)⁻¹X'y`

Cada supuesto Gauss-Markov que falla remite a un módulo concreto:

| Supuesto violado | Consecuencia | Módulo / solución |
|---|---|---|
| A1 — No linealidad en parámetros | β̂ sesgado e inconsistente | M6 — Switching, transformaciones ln/x² |
| A2 — Exogeneidad violada (endogeneidad) | β̂ sesgado e inconsistente | M4 — IV, 2SLS, GMM, VAR |
| A3 — Multicolinealidad perfecta | (X'X)⁻¹ inestable, Var(β̂) muy alta | M1 — Ridge, Lasso, PCA |
| A4 — Heterocedasticidad | SE(β̂) erróneos, t y F no válidos | M5 — ARCH, GARCH, WLS, HC SE |
| A5 — Autocorrelación | β̂ ineficiente, inferencia incorrecta | M4 — ARIMA, GLS, Newey-West HAC |
| A5+1 — No estacionariedad | Regresión espuria, R² alto sin sentido | M4 — ARIMA, ECM, Johansen, VECM |

**Notas clave:**
- A5 y A5+1 son distintos: A5 = residuos del modelo correlados en el tiempo; A5+1 = la propia serie no tiene media o varianza fija.
- M2 (Monte Carlo / Bootstrap) se usa cuando no hay solución analítica — no responde a un supuesto concreto.
- M6 (Kalman Filter) aplica cuando los parámetros varían suavemente en el tiempo.

**Combinaciones frecuentes:**
- A5+1 + A4: ECM con errores GARCH — largo plazo más volatilidad dinámica en residuos.
- A5+1 + A1: Markov Switching + ECM — el ajuste al equilibrio cambia de régimen.
- A2 + A5+1: VECM con instrumentos — cointegración con endogeneidad simultánea.

---

## Módulo 1 — OLS y fundamentos econométricos

> El modelo lineal clásico. Todo lo demás del máster es una extensión o corrección de este punto de partida.

### El modelo y el estimador

```
y = Xβ + u    →    β̂ = (X'X)⁻¹ X'y

y  → vector (n×1) variable dependiente
X  → matriz (n×k) regresores  [col. de 1s para el intercepto]
β  → vector (k×1) parámetros a estimar
u  → perturbaciones  ~  N(0, σ²I)  bajo CLM completo

Residuos:  û = y − Xβ̂
Varianza:  σ̂² = û'û / (n−k)   [estimador insesgado de σ²]
```

β̂ minimiza Σûᵢ². Bajo A1–A5 es **BLUE**: Best Linear Unbiased Estimator (Gauss-Markov).

### Indicadores clave

| Indicador | Fórmula | Interpretación |
|---|---|---|
| **R²** | `SSR/SST = 1 − SSE/SST` | Fracción de varianza explicada. Nunca decrece al añadir regresores. |
| **R² ajustado** | `1 − (SSE/(n−k)) / (SST/(n−1))` | Penaliza regresores irrelevantes. Puede ser negativo. |
| **AIC** | `−2·ln(L̂) + 2k` | Menor = mejor. También en ARIMA y GARCH. |
| **BIC** | `−2·ln(L̂) + k·ln(n)` | Penaliza más que AIC cuando n es grande. |
| **F-test** | `(R²/(k−1)) / ((1−R²)/(n−k)) ~ F(k−1, n−k)` | Significatividad conjunta. F sig. + t no sig. → multicolinealidad. |
| **t-stat** | `β̂ⱼ / SE(β̂ⱼ) ~ t(n−k)` | Significatividad individual. Inválido con A4 o A5 violados. |
| **VIF** | `1 / (1 − R²ⱼ)` | VIF > 10 → multicolinealidad problemática. No sesga β̂, solo lo hace impreciso. |
| **Durbin-Watson** | `d ≈ 2(1−ρ̂)`; d≈2 → sin autocorr. | Solo detecta AR(1). No válido con retardos de y como regresor. |
| **Jarque-Bera** | `n/6 · [S² + (K−3)²/4] ~ χ²(2)` | Solo testa normalidad (A6). Independiente de DW. Irrelevante en n>100. |

### Supuestos CLM

| Supuesto | Definición | Si se viola | Tests | Solución |
|---|---|---|---|---|
| **A1** Linealidad | Modelo lineal en β (no en x) | β̂ sesgado — no es problema de muestra | RESET de Ramsey; gráfico û vs ŷ | Transformaciones ln/x²; Logit/Probit; NLS |
| **A2** Exogeneidad | E[u\|X]=0; Cov(xⱼ,u)=0 ∀j | β̂ sesgado e inconsistente incluso con n→∞. El más crítico. | Test Hausman; Wu-Hausman | IV / 2SLS; GMM; VAR (M4) |
| **A3** No multicolinealidad | rango(X)=k; X'X invertible | Perfecta: β̂ no existe. Alta: imprecisión, t pequeños, F grande | VIF>10; condition number X'X | Eliminar regresor; PCA; Ridge; regla n-1 dummies |
| **A4** Homocedasticidad | Var(u\|X) = σ²·I | SE(β̂) incorrectos → t y p-valores no fiables. β̂ correcto. | Breusch-Pagan; White; gráfico \|û\| vs ŷ | HC robustos (White); WLS; GARCH (M5) |
| **A5** No autocorrelación | Cov(uᵢ,uⱼ\|X)=0 para i≠j | β̂ ineficiente; t-stats inflados (SE subestimados) | Durbin-Watson (solo AR(1)); Breusch-Godfrey; ACF/PACF residuos | Newey-West HAC; GLS/FGLS; ARIMA (M4) |
| **A6** Normalidad | u\|X ~ N(0,σ²I) | En muestras pequeñas: p-valores aproximados. En n>100: irrelevante (TCL). | Jarque-Bera; Shapiro-Wilk; Q-Q plot | Bootstrap (M2); Box-Cox; distribución t |

---

## Módulo 2 — Modelos de Simulación

> Cuando no hay fórmula cerrada, se simula. Tres enfoques complementarios.

| Modelo | Ecuación | Uso |
|---|---|---|
| **Monte Carlo** | `yᵢ = f(θ, uᵢ)`, uᵢ ~ F; repetir N veces | Pricing opciones, critical values ADF, stress-testing |
| **Variantes antipéticos** | `Var(x̄) = ¼[Var(x₁)+Var(x₂)+2Cov(x₁,x₂)]` | Usar −u junto a u → covarianza negativa → menor error MC |
| **Control variates** | `x* = y + (x̂ – ŷ)`, y analíticamente conocida | Ej: opción asiática vs Black-Scholes analítico |
| **Bootstrap** | `θ̂* = θ̂(y*)`, y* = ŷ + û* (muestreo con reemplazo) | Sin supuesto distribucional. Falla con autocorrelación. |
| **VaR por simulación** | Percentil 90/95 de 2000 pérdidas máximas simuladas | Hsieh (1993): Bootstrap de residuos EGARCH |
| **Generación números aleatorios** | `yᵢ₊₁ = (ayᵢ + c) mod m → Rᵢ₊₁ = yᵢ₊₁/m` | Pseudo-aleatorios U(0,1) → transformar a N(0,1) |

Convergencia MC: `S_x = √(Var(x)/N)` — el error estándar decrece como 1/√N.

---

## Módulo 3 — ML Financiero

> Sin vista de detalle en el HTML de referencia. Contenido del máster: clasificación supervisada, clustering no supervisado y redes neuronales aplicadas a finanzas.

Técnicas estudiadas (inferidas del mapa global):
- **Clasificación:** modelos supervisados para predecir defaults, señales de trading, rating de crédito.
- **Clustering:** K-means y similares para segmentar carteras, bucketing de exposiciones (conecta con M9 riesgo de crédito).
- **Redes neuronales:** arquitecturas feedforward; aplicaciones en predicción de series y valoración.

---

## Módulo 4 — Series Temporales

> Cuando las observaciones están ordenadas en el tiempo y no son independientes.

| Modelo | Ecuación | Identificación |
|---|---|---|
| **Ruido blanco** | E(yₜ)=μ, Var(yₜ)=σ², Cov(yₜ,yₛ)=0 | Punto de referencia. Tests: Box-Pierce Q, Ljung-Box Q* |
| **MA(q)** | `yₜ = μ + uₜ + θ₁uₜ₋₁ + … + θquₜ₋q` | ACF truncada en lag q; PACF decae exponencialmente |
| **AR(p)** | `yₜ = μ + φ₁yₜ₋₁ + … + φₚyₜ₋ₚ + uₜ` | Estacionario si \|raíces\| > 1; PACF truncada en p |
| **ARMA(p,q)** | `yₜ = μ + Σφᵢyₜ₋ᵢ + Σθⱼuₜ₋ⱼ + uₜ` | Box-Jenkins: identificar → estimar → diagnosticar; AIC/BIC |
| **ARIMA(p,d,q)** | `Φ(L)(1−L)ᵈyₜ = μ + Θ(L)uₜ` | d diferencias para estacionarizar; tests ADF, PP, KPSS |
| **VAR(p)** | `yₜ = A₁yₜ₋₁ + … + Aₚyₜ₋ₚ + uₜ` | Sistema multivariante; IRF, descomposición varianza, causalidad Granger |
| **Cointegración** (Engle-Granger / Johansen) | `I(1) + I(1) = I(0)` → β'yₜ ~ I(0) | r vectores de cointegración; rango de Π en VECM |
| **ECM** | `Δyₜ = γ(yₜ₋₁−β₀−β₁xₜ₋₁) + δΔxₜ + uₜ` | γ < 0 → velocidad de ajuste al equilibrio de largo plazo |

---

## Módulo 5 — Volatilidad y Correlación

> El residuo uₜ tiene varianza condicional no constante. La volatilidad misma sigue un proceso dinámico.

Punto de partida: `uₜ = σₜεₜ`, εₜ ~ iid(0,1) — volatility clustering (Mandelbrot 1963): E[u²ₜ|Fₜ₋₁] no es constante.

| Modelo | Ecuación | Característica |
|---|---|---|
| **ARCH(q)** — Engle 1982 | `σ²ₜ = α₀ + α₁u²ₜ₋₁ + … + αqu²ₜ₋q` | Test ARCH-LM: T·R² ~ χ²(q) |
| **GARCH(p,q)** — Bollerslev 1986 | `σ²ₜ = ω + Σαᵢu²ₜ₋ᵢ + Σβⱼσ²ₜ₋ⱼ` | Persistencia: Σα+Σβ < 1; estimación MLE |
| **IGARCH / EWMA** | Σα + Σβ = 1 → shocks permanentes | RiskMetrics: EWMA λ=0.94 es caso especial de IGARCH |
| **GJR-GARCH** (leverage) | `σ²ₜ = ω + αu²ₜ₋₁ + γu²ₜ₋₁Iₜ₋₁ + βσ²ₜ₋₁` | Iₜ₋₁=1 si uₜ₋₁<0; caídas suben más volatilidad que subidas |
| **EGARCH** — Nelson 1991 | `ln(σ²ₜ) = ω + β ln(σ²ₜ₋₁) + γ\|zₜ₋₁\| + λzₜ₋₁` | λ<0 → leverage effect; sin restricciones de positividad |
| **GARCH-M** | `yₜ = μ + δσ²ₜ + uₜ` | Prima de riesgo proporcional a varianza condicional |
| **MGARCH / DCC** | `Hₜ = DₜRₜDₜ` (correlaciones dinámicas) | Rₜ = Q*ₜ⁻¹QₜQ*ₜ⁻¹; cobertura óptima time-varying |
| **Beta CAPM time-varying** | `βᵢₜ = Cov(rᵢ,rₘ\|Fₜ₋₁) / Var(rₘ\|Fₜ₋₁)` | Extraído de MGARCH; conecta M5 con gestión de carteras (M8) |

---

## Módulo 6 — Switching & State Space

> Los parámetros del modelo cambian en el tiempo o entre regímenes.

| Modelo | Ecuación | Característica |
|---|---|---|
| **Dummies estacionales / pendiente** | `yₜ = β₁ + γ₁D1 + γ₂D2 + γ₃D3 + β₂xₜ + uₜ` | n-1 dummies para n estaciones; cambio de intercepto o pendiente |
| **Markov Switching** (Hamilton) | `yₜ = μₛₜ + φyₜ₋₁ + uₜ`, sₜ ∈ {1,…,m} | P[sₜ=j\|sₜ₋₁=i]=pᵢⱼ; πₜ₊₁=πₜP; estimación MLE. Régimen latente. |
| **TAR** | `yₜ = μᵢ+φᵢyₜ₋₁+uₜ` si sₜ₋ₖ ≷ r | r = umbral; transición discreta; estimación NLS |
| **SETAR** | sₜ₋ₖ = yₜ₋ₖ; el propio y define el régimen | AIC por régimen; ej. FRF/DEM en ERM |
| **State Space — medición** | `yₜ = Hβₜ + uₜ`, uₜ ~ N(0,R) | Lo observable. Ej: yₜ = α + βₜxₜ + uₜ (CAPM TVP) |
| **State Space — transición** | `βₜ₊₁ = Tβₜ + ηₜ`, ηₜ ~ N(0,Q) | Lo latente. T=I → paseo aleatorio del parámetro |
| **Filtro de Kalman** | `β̂ₜ\|ₜ = β̂ₜ\|ₜ₋₁ + Kₜ(yₜ − Hβ̂ₜ\|ₜ₋₁)` | Kₜ = ganancia de Kalman. Recursivo → MLE para hiperparámetros |
| **¿Parámetros TVP o fijos?** | H₀: σ²η = 0 → β constante en el tiempo | Si σ²η/σ²u grande → parámetros evolucionan; test LM sobre residuos |

---

## Conexiones M1–M6 con módulos posteriores

| Concepto | Sale de | Entra en |
|---|---|---|
| OLS, β̂, R², t/F-stat | M1 | Base de todo — M4 (ARIMA), M9 (regresión en riesgo) |
| Bootstrap, Monte Carlo | M2 | Pricing opciones (M7 T19–T21), VaR MC (M9) |
| ARIMA, cointegración, ECM | M4 | Largo plazo en modelos de crédito (M9) |
| GARCH, volatilidad condicional | M5 | Black-Scholes (M7 T19), VaR (M9), filtrado previo a EVT (M10) |
| Beta time-varying (MGARCH) | M5 | Gestión de carteras (M8 T22–T24) |
| Markov Switching, State Space | M6 | CAPM con parámetros variables (M8), regímenes en riesgo (M9) |
