# Módulo 9 — Gestión de Riesgos Financieros

## Para qué sirve este bloque

El módulo responde a una pregunta concreta: dado que los mercados pueden moverse en tu contra, ¿cómo cuantificas cuánto puedes perder y de qué fuente viene ese riesgo? Cubre tres tipos de riesgo que afectan a cualquier institución financiera —mercado, crédito y liquidez— y para cada uno proporciona tanto el marco teórico como la implementación cuantitativa. El hilo conductor es que cada tipo de riesgo necesita sus propias métricas: usar VaR para riesgo de liquidez o bid-ask spread para riesgo de mercado sería un error conceptual, no solo técnico.

---

## Tema 1: Riesgo de mercado

### La idea central

El **riesgo de mercado** es la pérdida potencial que surge de movimientos adversos en precios de mercado: tipos de interés, tipos de cambio, precios de acciones o materias primas. Las dos métricas dominantes para cuantificarlo son el **VaR** (*Value at Risk*) y el **Expected Shortfall** (ES). Históricamente surgieron de una necesidad práctica: JP Morgan necesitaba un único número que resumiera la exposición diaria de toda la institución.

### Value at Risk (VaR)

El VaR al nivel de confianza $\alpha$ responde a: ¿cuál es la pérdida máxima que no se superará con probabilidad $\alpha$ durante un horizonte temporal dado? Si el VaR diario al 95% es 1M€, hay un 5% de probabilidad de perder más de 1M€ ese día.

Sus tres ingredientes son invariables independientemente del método de cálculo: el **intervalo de confianza** (95% o 99%), el **horizonte temporal** (1 día para trading, 10 días para regulación), y la **desviación típica** de los retornos del portfolio.

El VaR escala con el tiempo según la raíz cuadrada: $\text{VaR}_{n\text{ días}} = \text{VaR}_{1\text{ día}} \times \sqrt{n}$. Esto asume retornos i.i.d., supuesto que rara vez se cumple en periodos de estrés.

### Los tres métodos de cálculo del VaR

**Varianza-covarianza (paramétrico).** Asume que los retornos siguen una distribución normal. La fórmula para un portfolio es:

$$\text{VaR} = V \cdot \sigma_p \cdot Z_\alpha$$

donde $V$ es el valor del portfolio, $\sigma_p = \sqrt{w_1^2\sigma_1^2 + w_2^2\sigma_2^2 + 2\rho w_1 w_2 \sigma_1 \sigma_2}$ es la desviación típica del portfolio, y $Z_\alpha$ es el cuantil de la normal estándar al nivel $\alpha$. En Python: `norm.ppf(1 - conf_level, mean, std)`.

Ventaja: fácil de calcular, requiere pocos datos. Limitación crítica: los retornos financieros tienen colas más gruesas que la normal (*fat tails*), por lo que este método subestima el riesgo en periodos de crisis.

**Simulación histórica.** No asume ninguna distribución. Se toman los retornos históricos del portfolio, se ordenan, y el VaR es el percentil correspondiente al nivel de confianza: si el intervalo es 95%, el VaR es el percentil 5 de los retornos históricos multiplicado por la inversión inicial. En Python: `np.percentile(returns, 5)`.

Ventaja: captura asimetría, colas gruesas y efectos GARCH implícitamente. Limitación: asume que el pasado es representativo del futuro; requiere muestra grande; es computacionalmente intensivo.

**Monte Carlo.** Genera miles de escenarios de retornos aleatorios desde una distribución especificada, calcula la pérdida en cada escenario, y toma el percentil correspondiente. La lógica es la misma que en simulación histórica, pero con datos sintéticos en lugar de históricos. Permite modelar distribuciones no normales y dependencias no lineales.

Ventaja: máxima flexibilidad. Limitación: depende enteramente de cuán bien se especifique la distribución generadora.

### VaR como medida de riesgo coherente

Una medida de riesgo es **coherente** si cumple cuatro axiomas: invarianza a la traslación, subaditividad, homogeneidad positiva y monotonicidad. El VaR **no es coherente** porque viola la **subaditividad**: puede ocurrir que $\text{VaR}(A+B) > \text{VaR}(A) + \text{VaR}(B)$. Esto es conceptualmente problemático porque implica que combinar dos portfolios puede aumentar el riesgo medido, penalizando la diversificación.

### Expected Shortfall (ES)

El **Expected Shortfall** (también llamado CVaR o *Conditional VaR*) resuelve el problema de subaditividad del VaR. ES sí es coherente. Mientras el VaR es un cuantil, el ES es la **media de las pérdidas que superan el VaR**:

$$\text{ES}_\alpha = \mathbb{E}[L \mid L > \text{VaR}_\alpha] = \frac{1}{1-\alpha}\int_\alpha^1 \text{VaR}_u\, du$$

En distribución continua, ES es la media de las pérdidas en la cola. En distribución discreta:

$$\text{ES}_\alpha = \frac{1}{1-\alpha} \sum_n \max(L_n) \cdot P(L_n)$$

El ES paramétrico usa la esperanza de la normal truncada por encima del cuantil $\alpha$. El ES histórico toma la media de todos los retornos que caen por debajo del percentil 5. La diferencia práctica: si el VaR al 95% es 1M€, el ES al 95% podría ser 1.5M€ —dice que, en los días malos, la pérdida media es 1.5M€, no solo que se supera 1M€.

---

## Tema 2: Riesgo de crédito

### La idea central

El **riesgo de crédito** es la probabilidad de que un prestatario no cumpla sus obligaciones de pago. Es el mayor componente del capital económico de la mayoría de los bancos, superando al riesgo de mercado. El objetivo de su gestión es maximizar el retorno ajustado al riesgo manteniendo la exposición crediticia dentro de límites aceptables.

### Los tres componentes del riesgo de crédito

Todo modelo de riesgo de crédito se construye sobre tres variables:

- **PD** (*Probability of Default*): probabilidad de que el prestatario incumpla. Es el componente más difícil de estimar.
- **LGD** (*Loss Given Default*): fracción del crédito que no se recupera si hay impago, entre 0 y 1.
- **EAD** (*Exposure at Default*): importe total expuesto en el momento del impago.

La **pérdida esperada** del enfoque IRB (*Internal Ratings-Based*) de Basilea es:

$$\text{Expected Loss} = \text{EAD} \times \text{LGD} \times \text{PD}$$

### Los Acuerdos de Basilea

**Basilea I (1988):** primer sistema de requerimientos de capital. Clasifica activos por riesgo: 0% para activos libres de riesgo, 20% para préstamos interbancarios, 50% para hipotecas residenciales, 100% para deuda corporativa. Requiere capital mínimo del 8% de los activos ponderados por riesgo.

**Basilea II (1999):** introduce tres pilares — requerimientos mínimos de capital, revisión supervisora y disciplina de mercado. Permite a los bancos usar modelos internos (IRB) para estimar PD, LGD y EAD.

**Basilea III (2010):** respuesta a la crisis de 2007-2008. Introduce ratios adicionales de liquidez (LCR ≥ 100%, ratio de apalancamiento ≥ 3%) y requerimientos de capital de mayor calidad (Tier 1 capital ratio ≥ 4.5%).

### Risk bucketing: segmentación por riesgo

Estimar la PD con un único modelo para todos los clientes produce predicciones pobres porque la distribución del riesgo cambia entre segmentos. El **risk bucketing** agrupa prestatarios con características similares antes de modelar.

El método estándar es **K-means clustering** sobre variables financieras del prestatario. Para determinar el número óptimo de clusters se usan cuatro criterios:

- **Método del codo:** se busca el punto donde la inercia (suma de distancias al centroide) deja de decrecer significativamente.
- **Silhouette score:** mide separación entre clusters. Valor de 1 indica clasificación perfecta; -1 indica clasificación incorrecta. Fórmula: $(x - y) / \max(x, y)$ donde $x$ es distancia intercluster e $y$ distancia intracluster.
- **Calinski-Harabasz (CH):** cociente entre varianza entre-clusters ($SSB$) y varianza intra-cluster ($SSW$), escalado por $N$ y $k$. Mayor valor es mejor.
- **Gap analysis (Tibshirani):** compara la varianza intra-cluster observada con la esperada bajo distribución de referencia nula. Se elige $k$ que maximiza el gap statistic.

### Estimación de la PD: regresión logística

La **regresión logística** es el modelo estándar para predecir la PD porque la variable dependiente es binaria (impago/no impago). Transforma la probabilidad mediante la función logit para que el output esté en $[0, 1]$:

$$\log\frac{p}{1-p} = \beta_0 + \beta_1 x \implies p = \frac{e^{\beta_0 + \beta_1 x}}{1 + e^{\beta_0 + \beta_1 x}}$$

Un problema frecuente en datos de crédito es el **desbalance de clases**: los impagos son mucho menos frecuentes que los pagos correctos. La solución estándar es **SMOTEENN** (*Synthetic Minority Oversampling Technique + Edited Nearest Neighbors*): genera muestras sintéticas de la clase minoritaria y elimina observaciones ambiguas en la frontera de decisión.

La evaluación del modelo se hace con la **curva ROC-AUC** (*Receiver Operating Characteristic - Area Under the Curve*): mide la capacidad del modelo de separar defaults de no-defaults. Un AUC de 1 indica separación perfecta; de 0.5 indica que el modelo no tiene poder predictivo (equivale a lanzar una moneda).

---

## Tema 3: Riesgo de liquidez

### La idea central

El **riesgo de liquidez** es la incapacidad de convertir un activo en efectivo sin incurrir en pérdidas significativas de precio o de tiempo. Fue el gran ignorado antes de 2008: los modelos asumían que los activos siempre tenían compradores. La crisis hipotecaria demostró que en periodos de estrés la liquidez desaparece exactamente cuando más se necesita, creando un círculo vicioso entre liquidez de mercado y liquidez de financiación.

### Las cuatro dimensiones de la liquidez

La liquidez es multidimensional; cada dimensión captura un aspecto diferente y necesita sus propias métricas:

- **Tightness (estrechez):** coste de ejecutar una transacción. A mayor diferencia entre precio de compra y venta (bid-ask spread), menor liquidez.
- **Immediacy (inmediatez):** velocidad a la que se pueden ejecutar órdenes grandes. Malfuncionamiento en clearing o settlement reduce la inmediatez.
- **Depth (profundidad):** abundancia de compradores y vendedores capaces de absorber órdenes de gran tamaño sin mover el precio.
- **Resiliency (resiliencia):** capacidad del mercado de recuperar el precio de equilibrio tras un desequilibrio de órdenes.

### Medidas de liquidez por dimensión

**Basadas en volumen (dimensión: profundidad):**

El **ratio de liquidez** mide cuánto volumen se necesita para inducir un cambio de precio del 1%: $LR = \sum(P \cdot V) / \sum|PC|$. Mayor ratio implica mayor liquidez.

El **ratio Hui-Heubel** compara la variación de precio con el volumen relativo a capitalización: $LHH = (P_{max} - P_{min})/P_{min}$ dividido por $V/(P \times \text{shrout})$. Es aplicable a acciones individuales.

El **turnover ratio** es el ratio de volumen negociado sobre acciones en circulación: $TR = (1/D)\sum V / \sum \text{shrout}$. Alta rotación implica alta liquidez.

**Basadas en coste de transacción (dimensión: tightness e immediacy):**

El **porcentaje de spread cotizado** mide el coste directo de una transacción: $(P_{ask} - P_{bid}) / P_{mid}$.

El **spread efectivo** captura el caso donde las operaciones ocurren fuera de las cotizaciones: $2|P_t - P_{mid}|/P_{mid}$.

El **spread de Roll** usa la autocorrelación serial de cambios de precio como proxy del bid-ask spread implícito: $\text{Roll} = 2\sqrt{-\text{Cov}(\Delta p_t, \Delta p_{t-1})}$.

El **spread Corwin-Schultz** extrae el spread directamente de los precios máximos y mínimos diarios, basándose en que los precios altos son órdenes de compra y los bajos son órdenes de venta.

**Basadas en impacto en precio (dimensión: resiliencia):**

La **medida de iliquidez de Amihud** mide la sensibilidad del retorno al volumen en dólares: $\text{ILLIQ} = (1/D)\sum|R|/V$. Mayor ILLIQ implica mayor impacto de precio por dólar negociado, es decir, menor liquidez.

El **ratio RtoTR de Florackis** mejora a Amihud sustituyendo el volumen en dólares por el turnover ratio, eliminando el sesgo por capitalización: $\text{RtoTR} = (1/D)\sum|R|/TR$.

El **coeficiente de elasticidad del trading (CET)** mide la elasticidad del volumen respecto al precio: $\text{CET} = \%\Delta V / \%\Delta P$. Alta elasticidad implica mayor inmediatez.

**Basadas en impacto de mercado (dimensión: resiliencia):**

Se estima el riesgo idiosincrático de cada activo regresando el retorno sobre el retorno de mercado (CAPM), y luego regresando el cuadrado de los residuos sobre el porcentaje de cambio en volumen. El coeficiente $\gamma_2$ mide cuánto se mueve el precio idiosincrático ante cambios en volumen: mayor $\gamma_2$, menor liquidez.

### Modelización: GMM y GMCM

Con once medidas de liquidez construidas, el problema es que son multimodales (diferentes distribuciones según el régimen de mercado) y correlacionadas. El **Gaussian Mixture Model (GMM)** permite modelar datos con múltiples modos sin asumir una distribución paramétrica única. Identifica clusters probabilísticos: cada observación tiene una probabilidad de pertenecer a cada estado. El estado con mayor probabilidad media representa el régimen de liquidez dominante.

El **Gaussian Mixture Copula Model (GMCM)** extiende el GMM incorporando la estructura de correlación entre medidas mediante una cópula. Es el enfoque más completo porque reconoce que distintas dimensiones de liquidez no son independientes: en periodos de alta volatilidad, se deterioran simultáneamente.

Para interpretar qué medidas definen cada estado, se aplica **PCA sobre los componentes del GMM**: los loadings de cada componente principal identifican qué medidas de liquidez dominan en cada régimen. En periodos de alta liquidez predominan turnover ratio, spread cotizado y medidas de Amihud y Florackis; en periodos de iliquidez, cobran más peso las medidas de bid-ask spread basadas en Rolling windows.

---

## Lo más importante para recordar

1. **VaR paramétrico asume normalidad: eso es su mayor vulnerabilidad.** En crisis, los retornos tienen colas más gruesas. El VaR histórico y Monte Carlo evitan este supuesto pero requieren más datos y cómputo.

2. **VaR no es subaditivo: ES sí lo es.** El ES es la media de las pérdidas en la cola y es la métrica preferida regulatoriamente (Basilea IV migra a ES). Es siempre mayor que el VaR al mismo nivel de confianza.

3. **La pérdida esperada en crédito se descompone en PD × LGD × EAD.** La PD es el componente más difícil de estimar; se modela con regresión logística por segmentos (risk bucketing) para capturar la heterogeneidad entre prestatarios.

4. **El desbalance de clases en crédito es la regla, no la excepción.** Sin corrección (SMOTE, ENN), los modelos predicen siempre la clase mayoritaria (no-default) con alta accuracy pero cero capacidad predictiva. La curva ROC-AUC, no el accuracy, es la métrica relevante.

5. **La liquidez tiene cuatro dimensiones que se comportan diferente según el régimen de mercado.** No existe una única medida de liquidez válida para todos los contextos; el GMM permite identificar qué dimensión es dominante en cada periodo.

6. **Los tres tipos de riesgo interactúan.** Una crisis de liquidez puede convertirse en riesgo de crédito (si una empresa no puede financiarse, incumple sus obligaciones). El riesgo de mercado afecta al valor del colateral que respalda el crédito. Modelarlos de forma aislada subestima el riesgo sistémico.

---

## Conexión con el resto del módulo

| Concepto | Dónde aparece después |
|---|---|
| Distribución normal y cuantiles | Base del VaR paramétrico (T1) |
| Cópulas | Modelización de dependencia en liquidez: GMCM (T3) |
| PCA | Identificación de medidas de liquidez dominantes por régimen (T3) |
| K-means clustering | Risk bucketing en crédito (T2), clustering de medidas de liquidez (T3) |
| Regresión logística | Estimación de PD en crédito (T2) |
| CAPM / regresión OLS | Estimación de riesgo idiosincrático en medidas de impacto de mercado (T3) |
| Series temporales / GARCH | Implícito en el VaR histórico y en la modelización dinámica de liquidez |
| Gaussian Mixture Model | Clustering probabilístico de medidas de liquidez multidimensionales (T3) |
