---
date: 2026-08-20
tags: [TFM, propuestas, finanzas-cuantitativas]
---

# TFM — Propuestas de tema

> Cinco preguntas que viven en el mismo espacio: la brecha entre lo que los modelos asumen y lo que los mercados hacen.

---

## Hilo conductor

Los modelos financieros están construidos sobre supuestos que los mercados violan sistemáticamente: normalidad, estacionariedad, parámetros fijos. Sabemos que fallan. La pregunta que organiza estas propuestas es: **¿cuánto importa que fallen, y en qué circunstancias?**

---

## Propuesta 1 — Estimación de riesgo de cola: ¿cuánto infraestiman los modelos estándar?

### Por qué

El VaR con normalidad es el modelo de riesgo más usado en la industria y en regulación (Basilea). La crisis de 2008 demostró que subestima sistemáticamente las pérdidas de cola. El regulador respondió: Basilea IV reemplaza VaR 99% por Expected Shortfall 97.5% precisamente para capturar mejor las colas.

Lo que no está bien cuantificado empíricamente es **cuánto importa la elección del modelo según el activo y el periodo**. Un modelo que falla el 2% del tiempo en renta variable puede fallar el 10% en cripto o en un activo emergente. La respuesta no es universal. El TFM que contesta esta pregunta — con datos reales, backtesting riguroso y comparación explícita — tiene respuesta directa a una decisión que toman los gestores de riesgo cada día.

### Metodología

**Datos:** retornos diarios de 3 activos con perfil de cola distinto — ej. IBEX35 (índice), EUR/USD (divisa), Bitcoin (cripto). Periodo: 2015–2025, ventana de estimación rolling de 500 días.

**Pipeline:**

1. **Preprocesado:** log-retornos, test ADF (estacionariedad), test ARCH-LM (heteroscedasticidad condicional).

2. **Filtrado GARCH:** estimar GARCH(1,1) con distribución t de Student. Extraer residuos estandarizados `zₜ = uₜ/σₜ` — aproximadamente i.i.d.

3. **Ajuste EVT:** aplicar método POT (Peak Over Threshold) a la cola izquierda de `zₜ`. Seleccionar umbral u con Hill plot. Ajustar distribución GPD(ξ, σ) por MLE.

4. **Cálculo de medidas de riesgo:**
   - VaR(α) y ES(α) para α ∈ {95%, 99%, 99.5%}
   - Cuatro métodos: normal paramétrico · histórico · GARCH-normal · GARCH-EVT

5. **Backtesting out-of-sample:**
   - Test de Kupiec: contrasta si la tasa de fallos observada coincide con α
   - Test de Christoffersen: contrasta independencia de las violaciones
   - Comparar número de excepciones por método y activo

6. **Análisis de resultados:** ¿En qué activos y periodos abre más el diferencial GARCH-normal vs GARCH-EVT? ¿El coste de complejidad se justifica empíricamente?

**Módulos del máster:** M5 (GARCH), M10 (EVT, GPD, backtesting), M9 (VaR, ES, Kupiec)

---

## Propuesta 2 — Beta dinámica: ¿por qué los gestores siguen usando un número que sabemos incorrecto?

### Por qué

Desde los años 70 sabemos que la beta de CAPM no es constante. Cambia con el ciclo económico, con la volatilidad del mercado, con la estructura del balance de la empresa. Sin embargo, la mayoría de los sistemas de gestión de carteras siguen usando betas estimadas por OLS sobre ventanas rolling de 3–5 años.

El gap no es teórico — está resuelto con DCC-GARCH. El gap es **práctico**: ¿mejora realmente la cobertura si usas beta dinámica en lugar de beta estática? ¿O el coste de mayor complejidad no se traduce en menor error de seguimiento? Esa pregunta tiene implicaciones directas para cómo se gestiona el riesgo de una cartera institucional y todavía no tiene una respuesta empírica clara para mercados europeos.

### Metodología

**Datos:** retornos diarios de 5–8 acciones del Eurostoxx50 (distintos sectores) vs. Eurostoxx50 como índice de mercado. Periodo: 2010–2025.

**Pipeline:**

1. **Beta estática (benchmark):** OLS rolling con ventana de 252 días. `βᵢ = Cov(rᵢ,rₘ)/Var(rₘ)` — recalculada cada día.

2. **Beta dinámica:** estimar DCC-GARCH(1,1) bivariante para cada par (acción, índice). Extraer `βᵢₜ = H₁₂ₜ / H₂₂ₜ` donde `Hₜ` es la matriz de covarianzas condicionales.

3. **Evaluación del hedge:** simular estrategia de cobertura — posición larga en la acción, corta en el índice por un importe `βₜ` × nocional. Calcular varianza del portfolio cubierto con cada método de beta.

4. **Criterios de comparación:**
   - Ratio de reducción de varianza: `1 − Var(cubierto)/Var(sin cubrir)`
   - Hedge ratio error: desviación de β estimada vs. realizada (ventana ex-post)
   - Número de rebalanceos necesarios (coste implícito de transacción)

5. **Análisis:** ¿Varía la ventaja de la beta dinámica según el sector? ¿En periodos de stress (2020 COVID, 2022 tipos) la diferencia es más pronunciada?

**Módulos del máster:** M5 (MGARCH, DCC), M7 (CAPM, beta), M8 (hedging, delta)

---

## Propuesta 3 — Pairs trading: ¿es la cointegración alfa real o compensación por riesgo?

### Por qué

La hipótesis de mercados eficientes dice que no hay estrategias sistemáticas que generen alfa persistente. Las estrategias de pares explotan relaciones estructurales entre activos — regulatorias, sectoriales, de propiedad cruzada — que no deberían desaparecer con el arbitraje.

La pregunta relevante es: **¿la rentabilidad de la estrategia cae cuando más gente la usa, o el equilibrio persiste porque hay un riesgo latente que la justifica?** En España hay sectores (banca, utilities) donde estas relaciones estructurales son muy estables y están poco analizados en la literatura reciente. Un TFM que lo pruebe con datos recientes aporta evidencia en un debate abierto sobre la naturaleza del alfa estadístico.

### Metodología

**Datos:** retornos diarios de acciones dentro de 2–3 sectores homogéneos — ej. banca española (BBVA, SAN, SAB, BKT) y utilities europeas. Periodo: 2015–2025. División train (2015–2021) / test (2022–2025).

**Pipeline:**

1. **Selección de pares:** test de cointegración Engle-Granger en todas las combinaciones del universo. Filtrar pares con p-valor < 0.05 y residuo estacionario (test ADF sobre spread).

2. **Modelado del spread:** estimar ECM para cada par seleccionado. Verificar `γ < 0` — velocidad de ajuste negativa confirma reversión a la media. Interpretar la semivida del spread: `t½ = −ln(2)/ln(1+γ)`.

3. **Regla de trading:** abrir posición larga/corta cuando `spread > μ ± 2σ`. Cerrar al cruzar la media. Stops en `±3σ`. Simular con datos out-of-sample (2022–2025).

4. **Evaluación:**
   - P&L acumulado, Sharpe ratio, máximo drawdown
   - Número de operaciones, ratio de acierto, duración media de posición
   - Comparación vs. buy-and-hold del sector y vs. estrategia aleatoria (Bootstrap del spread para IC)

5. **Análisis de persistencia:** ¿se deteriora la estrategia en el periodo test respecto al train? ¿En qué pares y por qué? Eso responde si el alfa es estructural o ya ha sido arbitrado.

**Módulos del máster:** M4 (cointegración, ECM), M2 (Bootstrap para intervalos de confianza)

---

## Propuesta 4 — Detección de regímenes: ¿puede un modelo estadístico anticipar crisis antes que los indicadores macro?

### Por qué

Los bancos centrales, los gestores macro y los modelos de asset allocation trabajan con la idea de que los mercados tienen regímenes diferenciados: expansión/recesión, alta/baja volatilidad, risk-on/risk-off. El problema es que casi todos los indicadores que se usan para detectar esos regímenes son **macroeconómicos y van con retraso** — el NBER tarda meses en declarar una recesión.

Un modelo de Markov Switching estimado sobre precios de mercado — que son instantáneos — podría detectar cambios de régimen antes que los indicadores convencionales. El TFM que contrasta esa hipótesis tiene implicaciones para gestión táctica y para la pregunta más amplia de si el mercado "sabe" algo que los datos macro no revelan todavía.

### Metodología

**Datos:** retornos mensuales del S&P500 (o Eurostoxx50). Periodo: 2000–2025 — incluye dot-com, GFC 2008, COVID 2020, ciclo de tipos 2022. Fechas de recesión NBER / CEPR como ground truth.

**Pipeline:**

1. **Estimación MS-AR(2):** modelo Markov Switching con 2 regímenes sobre retorno mensual. Parámetros: `μᵢ` (media por régimen), `σᵢ` (volatilidad por régimen), `pᵢⱼ` (probabilidades de transición). Estimación por MLE con algoritmo de Hamilton (filtro de probabilidades).

2. **Interpretación de regímenes:** verificar que régimen 1 = expansión (`μ₁ > 0`, `σ₁` baja) y régimen 2 = contracción (`μ₂ < 0`, `σ₂` alta). Calcular duración media esperada de cada régimen: `E[d] = 1/(1−pᵢᵢ)`.

3. **Comparación temporal con indicadores macro:** alinear las probabilidades filtradas `P(sₜ=2)` con las fechas de recesión declaradas. Calcular adelanto/retraso promedio del modelo respecto a la declaración oficial.

4. **Aplicación táctica:** definir regla de asignación — renta variable si `P(régimen expansión) > 0.6`, monetario si `P(régimen contracción) > 0.6`, mixto en zona intermedia. Simular rentabilidad vs. buy-and-hold y vs. indicador macro equivalente (ej. curva de tipos invertida).

5. **Extensión:** ¿mejora el modelo si se añade volatilidad implícita (VIX) como variable adicional? Comparar AIC/BIC de MS-AR(2) univariante vs. con VIX.

**Módulos del máster:** M6 (Markov Switching), M8 (gestión activa, IR)

---

## Propuesta 5 — Asimetría en volatilidad: ¿importa modelar el efecto leverage para medir riesgo?

### Por qué

Hay un hecho empírico bien documentado: las malas noticias aumentan la volatilidad más que las buenas del mismo tamaño — el efecto leverage. Lo capturan GJR-GARCH y EGARCH; el GARCH estándar no.

La pregunta que no tiene respuesta universal es **si esa asimetría importa para las decisiones prácticas** — no para el ajuste in-sample, donde GJR siempre gana, sino para la estimación de riesgo out-of-sample. Si la diferencia es estadísticamente significativa pero económicamente irrelevante, el modelo más simple gana por parsimonia. Si no lo es, los reguladores y gestores deberían usar siempre especificaciones asimétricas. El TFM que contesta esto con un criterio de evaluación externo toca un debate metodológico con consecuencias directas en cómo se mide riesgo en la práctica.

### Metodología

**Datos:** retornos diarios de activos con perfiles distintos de asimetría esperada — ej. índice de acciones (asimetría negativa documentada), índice de bonos (asimetría baja), commodity (asimetría mixta). Periodo: 2010–2025. Split 70/30 train/test.

**Pipeline:**

1. **Estimación de 4 modelos:** GARCH(1,1), GJR-GARCH(1,1), EGARCH(1,1), GARCH-M(1,1). Todos con distribución de error t de Student (fat tails). Criterios in-sample: AIC, BIC, log-verosimilitud.

2. **Test de asimetría:** en GJR-GARCH, `γ > 0` confirma leverage. En EGARCH, `λ < 0`. Test de significatividad del parámetro de asimetría para cuantificar su relevancia estadística por activo.

3. **Evaluación out-of-sample:** comparar `σ̂²ₜ` de cada modelo contra volatilidad realizada (suma de retornos al cuadrado en ventana de 5 días o datos intradía si disponibles). Métricas: RMSE, MAE, QLIKE (asimétrica, penaliza más infraestimación). Test Diebold-Mariano para significatividad de las diferencias entre modelos.

4. **Implicación para VaR:** calcular VaR 99% con cada especificación GARCH. Comparar tasas de excepción out-of-sample. ¿El modelo asimétrico reduce excepciones en mercados bajistas?

5. **Conclusión estructurada:** separar "asimetría estadísticamente presente" de "asimetría económicamente relevante para riesgo". La respuesta puede diferir por activo.

¿De dónde sale el "presentimiento" de que en la práctica no importa?

Es una hipótesis razonable, no un hecho comprobado — por eso es una buena pregunta de TFM. La lógica es:

In-sample, GJR/EGARCH van a ganar casi siempre — por la razón matemática de arriba (más parámetros).
Pero out-of-sample, el parámetro de asimetría se estima con ruido (con datos limitados, sobre todo si el asset no tiene mucha asimetría real). Ese ruido puede hacer que el modelo complejo sobreajuste el pasado y prediga peor el futuro que el modelo simple — el clásico problema de bias-variance.
Además, aunque el modelo complejo prediga ligeramente mejor, la diferencia puede ser tan pequeña que no cambie ninguna decisión real (ej. el VaR al 99% da prácticamente el mismo número, o el número de excepciones en el backtest es igual).

En resumen, lo que compara la propuesta 5 es:

	Pregunta que responde
Comparación in-sample (AIC/BIC)	¿El modelo asimétrico ajusta mejor el pasado? (Casi seguro sí, poco interesante)
Comparación out-of-sample (RMSE, QLIKE, Diebold-Mariano)	¿Predice mejor la volatilidad futura? (No obvio)
Comparación en VaR (excepciones, Kupiec)	¿Esa diferencia estadística se traduce en menos pérdidas mal estimadas? (La pregunta que de verdad le importa a un gestor de riesgo)

**Módulos del máster:** M5 (ARCH, GARCH, GJR, EGARCH), M9 (VaR, backtesting)

---

## Propuesta 6 — Market Making: ¿explica el modelo teórico el comportamiento real de los spreads?

### Por qué

Un market maker es el agente que provee liquidez en un mercado: siempre cotiza precio de compra (bid) y de venta (ask), y gana el spread. Su problema no es predecir el precio — es gestionar el inventario acumulado mientras hace eso. Si compra demasiado y el precio cae, pierde. Si no compra, no gana el spread.

Es un problema de control óptimo bajo incertidumbre: ¿cómo fijar bid y ask dinámicamente para maximizar P&L y controlar el riesgo de inventario? El modelo de referencia es Avellaneda-Stoikov (2008) — el punto de partida de los desks de market making cuantitativos en renta fija, derivados y crypto. La brecha entre el modelo y los datos reales en mercados concretos (sobre todo en periodos de stress o mercados menos líquidos) no está bien documentada empíricamente.

El modelo da un resultado central: **el spread óptimo no es fijo, depende del inventario acumulado y del tiempo que queda**. Cuanto más inventario tienes, más asimétrico pones el spread para deshacerte de él. La pregunta empírica es si eso es lo que realmente hacen los spreads en el mercado.

### Metodología

**Datos:** datos de tick de un activo líquido — futuros sobre índice (Eurostoxx, ES) o crypto (Binance tiene API pública con book de órdenes histórico a nivel tick). Crypto tiene la ventaja de operar 24h y datos muy accesibles sin coste.

**Pipeline:**

1. **El modelo base — Avellaneda-Stoikov:** un market maker con aversión al riesgo CARA maximiza utilidad esperada sobre su riqueza terminal. La solución da spread óptimo:

   ```
   δ* = γσ²(T−t) + (2/γ)·ln(1 + γ/κ)

   γ  = aversión al riesgo
   σ  = volatilidad del activo
   T−t = tiempo hasta cierre de sesión
   κ  = intensidad de llegada de órdenes
   ```

2. **Estimación de parámetros:** calibrar σ con GARCH sobre el midprice (σ dinámica, no constante como asume el modelo original), κ como proceso de Poisson estimado del histórico de trades, γ calibrado a spreads observados.

3. **Simulación de estrategias (Monte Carlo):** simular el P&L del market maker bajo tres reglas:
   - Spread óptimo de Avellaneda-Stoikov con σ fija
   - Spread óptimo con σₜ dinámica (GARCH)
   - Spread fijo como benchmark pasivo

4. **Evaluación de cada estrategia:**
   - Sharpe del P&L acumulado
   - Máximo inventario acumulado (riesgo de posición)
   - Tasa de fill (cuántas órdenes se ejecutan)
   - Comparación de spreads simulados vs. spreads observados en el mercado

5. **Análisis de stress:** ¿cómo se comporta el market maker simulado en periodos de alta volatilidad? ¿El spread GARCH-dinámico reduce el drawdown de inventario respecto al modelo con σ fija?

**Módulos del máster:** M2 (simulación Monte Carlo del P&L), M5 (GARCH para σₜ dinámica), M7 (Black-Scholes y griegas si se extiende a opciones), M9 (bid-ask spread como medida de liquidez)

> **Nota:** Market Making no se estudia explícitamente en el máster, pero todos los bloques necesarios están cubiertos. Es el tema más cercano a la práctica de un desk quant y el que más diferencia frente al resto de propuestas.

---

## Comparativa de propuestas

| | Pregunta central | Dificultad técnica | Originalidad | Conexión con práctica de mercado |
|---|---|---|---|---|
| **1. GARCH–EVT** | ¿Cuánto importa la cola? | Media | Alta | Regulación Basilea — directa |
| **2. Beta dinámica** | ¿Vale la complejidad del hedge? | Media-alta | Alta | Gestión de carteras institucional |
| **3. Pairs trading** | ¿Es el alfa estructural o ya arbitrado? | Media | Media | Trading sistemático |
| **4. Markov Switching** | ¿Anticipa el mercado las crisis? | Media | Alta | Gestión macro táctica |
| **5. Asimetría GARCH** | ¿Importa el leverage para riesgo? | Baja-media | Media | Modelos internos de riesgo |
| **6. Market Making** | ¿Funciona el spread óptimo en la práctica? | Alta | Muy alta | Desks quant de market making |

Las propuestas 1, 2 y 4 tienen la motivación más sólida dentro del contenido del máster. La 6 es la más diferenciadora y la más cercana a un perfil quant de industria, pero también la más exigente en datos y en implementación.
