# Módulo 9 — Temas 1 a 12: Gestión de Riesgos Financieros

## Para qué sirve este bloque

Este módulo es la base matemática y estadística del riesgo cuantitativo. No mide riesgos directamente: construye el lenguaje formal —probabilidades, distribuciones, series temporales, regresión— que hace posible modelar pérdidas, calcular VaR, estimar copulas y diseñar pruebas de estrés. Sin este bloque, los modelos de riesgo son cajas negras; con él, se entiende qué supuestos se están asumiendo y cuándo fallan.

Los temas no son independientes: los conceptos de probabilidad (T2–T3) alimentan las distribuciones (T4–T5), que a su vez son la base del VaR (T7) y los modelos de series temporales (T11). El análisis bayesiano (T6) y la regresión (T10) son marcos alternativos de estimación. Los factores de decaimiento (T12) son un refinamiento práctico de casi todo lo anterior.

---

## Tema 1: Matemáticas básicas

### La idea central

Los retornos y los factores de descuento son los bloques de construcción de cualquier modelo financiero. Antes de hacer estadística, hay que decidir cómo medir lo que varía.

### Retornos

Existen dos convenciones para medir la rentabilidad de un activo: el **retorno simple** $R_t = P_t/P_{t-1} - 1$ y el **retorno logarítmico** $r_t = \ln(P_t/P_{t-1})$. La diferencia importa porque los retornos logarítmicos son aditivos en el tiempo:

$$r_{n,t} = r_{1,t} + r_{1,t-1} + \cdots + r_{1,t-n+1}$$

lo que facilita el análisis de series temporales. Los retornos simples, en cambio, son multiplicativos: $(1+R_{n,t}) = (1+R_1)(1+R_2)\cdots$. Para horizontes cortos la diferencia es pequeña; para horizontes largos o retornos extremos, no.

La capitalización continua lleva al límite este razonamiento: cuando el periodo de capitalización tiende a cero, $R_\text{Annual} = e^r - 1$, donde $r$ es el retorno continuo.

### Factores de descuento

El **valor presente** de un pago futuro $V_{t+n}$ se obtiene descontando a la tasa $R$:

$$V_t = \frac{V_{t+n}}{(1+R)^n}$$

Esta fórmula es la base de la valoración de bonos, opciones y cualquier instrumento con flujos futuros.

### Series geométricas y combinatoria

Una **serie geométrica infinita** $\sum_{i=0}^\infty \delta^i = \frac{1}{1-\delta}$ (para $|\delta|<1$) aparece en los factores de decaimiento (T12). La **combinatoria** $C(n,k) = \frac{n!}{k!(n-k)!}$ es la base de la distribución binomial (T4).

---

## Tema 2: Probabilidades

### La idea central

La probabilidad es el lenguaje para hablar de incertidumbre. Este tema establece las definiciones operativas que se usan en toda la gestión de riesgos.

### Variables aleatorias discretas y continuas

Una **variable aleatoria discreta** toma un conjunto contable de valores, cada uno con una probabilidad $p_i$ tal que $\sum p_i = 1$. Una **variable aleatoria continua** tiene una **función de densidad de probabilidad** (PDF, *probability density function*) $f(x)$ que satisface $\int f(x)\,dx = 1$. La probabilidad de que $X$ caiga en un intervalo es el área bajo la PDF en ese intervalo.

La **función de distribución acumulada** (CDF, *cumulative distribution function*) $F(a) = P[X \leq a]$ resume toda la información probabilística en una función monótona creciente de 0 a 1. El VaR se lee directamente como un cuantil de esta función.

### Eventos independientes y probabilidad condicional

Dos eventos son **mutuamente excluyentes** si no pueden ocurrir simultáneamente: $P[A \cup B] = P[A] + P[B]$. Son **independientes** si la ocurrencia de uno no modifica la probabilidad del otro: $P[A \cap B] = P[A] \cdot P[B]$.

La **probabilidad condicional** $P[A|B] = P[A \cap B]/P[B]$ mide cuánto cambia la probabilidad de $A$ al saber que $B$ ocurrió. Esta distinción es central en riesgo: durante crisis, activos que parecían independientes resultan fuertemente correlacionados.

---

## Tema 3: Estadística básica

### La idea central

Dado que no se puede observar la distribución completa de los retornos, se estiman sus propiedades a partir de datos. Este tema cubre los estimadores estándar y sus propiedades.

### Media, varianza y desviación típica

La **media** de una variable aleatoria $\mu = E[X]$ mide el valor central esperado. La **varianza** $\sigma^2 = E[(X-\mu)^2]$ cuantifica la dispersión alrededor de esa media. La **desviación típica** $\sigma = \sqrt{\sigma^2}$ tiene las mismas unidades que la variable original y es la medida de riesgo más básica.

Regla clave para combinar variables: $\text{Var}[cX] = c^2 \text{Var}[X]$, y $E[X^2] \neq (E[X])^2$ en general —la varianza nunca es cero salvo que la variable sea constante.

### Covarianza, correlación y cobertura

La **covarianza** $\sigma_{XY} = E[(X-\mu_X)(Y-\mu_Y)]$ mide si dos variables se mueven juntas. La **correlación** $\rho_{XY} = \sigma_{XY}/(\sigma_X \sigma_Y)$ normaliza esa medida al intervalo $[-1, 1]$, haciendo comparable la dependencia entre pares de activos.

La varianza de un **portfolio** de dos activos $A$ y $B$ es:

$$\sigma_P^2 = \sigma_A^2 + h^2\sigma_B^2 + 2h\rho_{AB}\sigma_A\sigma_B$$

El ratio de cobertura óptimo que minimiza esta varianza es:

$$h^* = -\rho_{AB}\frac{\sigma_A}{\sigma_B}$$

Esta fórmula conecta directamente con la gestión práctica: dice cuántas unidades de $B$ hay que vender por cada unidad de $A$ para minimizar la varianza del portfolio.

### Momentos, asimetría y curtosis

Los **momentos** de orden superior caracterizan la forma de la distribución más allá de la media y la varianza. La **asimetría** (*skewness*) es el momento central estandarizado de orden 3: valores negativos indican una cola larga a la izquierda (pérdidas extremas más probables de lo que sugiere la normal). La **curtosis** es el momento de orden 4: valores superiores a 3 (*fat tails* o colas gruesas) indican más eventos extremos de los que predice la normal.

La **coscewness** y la **cokurtosis** son extensiones multivariantes: miden si los retornos extremos de dos activos tienden a coincidir. Su problema práctico es que generan un número muy elevado de estadísticos cruzados, lo que dificulta su uso en portfolios grandes.

### BLUE

El **estimador BLUE** (*Best Linear Unbiased Estimator*) es el estimador lineal de varianza mínima entre todos los insesgados. La relevancia práctica: bajo los supuestos de OLS (T10), el estimador de mínimos cuadrados es BLUE.

---

## Tema 4: Distribuciones

### La idea central

Las distribuciones paramétricas son modelos compactos para la incertidumbre: en lugar de almacenar miles de observaciones, se estiman dos o tres parámetros y se trabaja con la distribución completa. El coste es que si el modelo paramétrico es incorrecto, las estimaciones de riesgo pueden fallar sistemáticamente.

### Distribuciones clave

La **distribución uniforme** asigna probabilidad igual a todos los valores en $[b_1, b_2]$. Es el punto de partida de la simulación Monte Carlo: se genera una uniforme estándar y se transforma.

La **distribución de Bernoulli** modela un resultado binario (impago/no impago, subida/bajada). La **distribución binomial** extiende esto a $n$ ensayos independientes: $P[K=k] = C(n,k)p^k(1-p)^{n-k}$. Es la base del backtesting del VaR: si el modelo es correcto al 99%, el número de excepciones en $n$ días sigue una binomial con $p=0.01$.

La **distribución de Poisson** $P[X=n] = e^{-\lambda}\lambda^n/n!$ modela el número de eventos raros por unidad de tiempo (defaults, saltos en precios). El parámetro $\lambda$ es simultáneamente la media y la varianza.

La **distribución normal** $N(\mu, \sigma^2)$ es el pilar del riesgo cuantitativo clásico. Su PDF es simétrica y completamente determinada por media y varianza. Su principal limitación para riesgo: subestima la probabilidad de eventos extremos (colas más delgadas que las observadas en mercados).

La **distribución lognormal** modela precios (no retornos): si $r_t \sim N(\mu, \sigma^2)$, entonces $P_t = P_{t-1} e^{r_t}$ sigue una lognormal. Garantiza que los precios sean positivos.

El **teorema central del límite** justifica el uso de la normal: la suma de $n$ variables independientes con media y varianza finitas converge en distribución a una normal cuando $n \to \infty$, independientemente de la distribución original.

La **distribución $\chi^2$** con $k$ grados de libertad es la suma de $k$ normales estándar al cuadrado. La **t de Student** surge de dividir una normal estándar por la raíz cuadrada de una $\chi^2$ normalizada; tiene colas más gruesas que la normal y se usa cuando la varianza es estimada, no conocida. La **distribución F** es el cociente de dos $\chi^2$ normalizadas; aparece en los tests de hipótesis sobre varianzas en regresión.

Las **distribuciones de mezcla** combinan dos o más distribuciones con pesos: pueden reproducir bimodalidad o colas gruesas sin asumir una forma paramétrica simple, a costa de añadir parámetros.

---

## Tema 5: Distribuciones multivariantes y cópulas

### La idea central

El riesgo de un portfolio depende no solo de la distribución marginal de cada activo sino de cómo se mueven conjuntamente. Las distribuciones multivariantes y las cópulas son las herramientas para modelar esa dependencia.

### Distribuciones multivariantes

La extensión natural de la normal univariante es la **normal multivariante**, caracterizada por un vector de medias y una matriz de covarianzas. La correlación captura la dependencia lineal, pero no la no-lineal: dos activos con correlación cero pueden ser estadísticamente dependientes.

### Cópulas

Una **cópula** es una función que une distribuciones marginales arbitrarias en una distribución conjunta, separando la estructura de dependencia de las distribuciones individuales. Formalmente, dado el teorema de Sklar, cualquier distribución conjunta puede descomponerse en sus marginales y una cópula.

La **cópula de Clayton** captura dependencia en la cola inferior (pérdidas conjuntas): dos activos pueden tener correlación baja en mercados normales pero alta dependencia cuando ambos caen. La **cópula de Frank** es más simétrica. La ventaja de las cópulas es su flexibilidad; el inconveniente es que la estimación y la interpretación son matemáticamente exigentes, y su uso masivo en CDOs durante 2006-2008 mostró que parametrizaciones incorrectas generan estimaciones de riesgo catastróficamente optimistas.

---

## Tema 6: Análisis bayesiano

### La idea central

El enfoque bayesiano trata los parámetros desconocidos como variables aleatorias con una distribución de probabilidad, en lugar de valores fijos a estimar. Esto permite incorporar información previa y actualizar creencias con datos nuevos de manera formal.

### Teorema de Bayes

$$P[A|B] = \frac{P[B|A] \cdot P[A]}{P[B]}$$

En notación bayesiana: **posterior** = (likelihood × prior) / evidencia. El **prior** $P[A]$ recoge la creencia antes de ver los datos. La **likelihood** $P[B|A]$ mide cuán probable es la evidencia dado el modelo. El **posterior** $P[A|B]$ actualiza la creencia tras observar los datos.

La fuente del prior es el mayor punto de controversia: puede venir de datos históricos, de opinión experta o de una distribución no informativa. Cuando el prior es una distribución Beta y los datos son ensayos de Bernoulli, el posterior también es Beta —esto se llama **distribución conjugada** y hace el cálculo tratable.

### Redes bayesianas

Una **red bayesiana** representa la estructura causal entre variables con un grafo dirigido. Cada nodo tiene una distribución condicional dados sus padres. La ventaja práctica es que es más fácil obtener probabilidades condicionales de expertos que probabilidades conjuntas. En riesgo financiero, se usan para modelar cadenas de eventos (burbuja inmobiliaria → caída MBS → quiebra bancaria → caída de bolsa) con datos escasos.

### Bayesianos vs frecuentistas

Los **frecuentistas** tratan los parámetros como constantes fijas y usan la frecuencia relativa de eventos para estimarlos. Los **bayesianos** asignan distribuciones de probabilidad a los parámetros. La diferencia práctica: los intervalos de confianza frecuentistas no son intervalos de probabilidad sobre el parámetro; los intervalos creíbles bayesianos sí lo son.

---

## Tema 7: Tests de hipótesis e intervalos de confianza

### La idea central

Estimar un parámetro puntualmente no basta: hay que cuantificar la incertidumbre de la estimación. Este tema conecta directamente con el VaR, que es esencialmente un cuantil estimado con cierta confianza.

### Media y varianza muestrales como variables aleatorias

La **media muestral** $\hat{\mu}$ es en sí misma una variable aleatoria: tiene media $\mu$ y varianza $\sigma^2/n$. La **varianza muestral** $\hat{\sigma}^2$ con denominador $n-1$ es insesgada. La versión estandarizada $t = (\hat{\mu} - \mu) / (\hat{\sigma}/\sqrt{n})$ sigue una distribución $t$ de Student con $n-1$ grados de libertad, lo que permite construir intervalos de confianza sin conocer $\sigma$.

La **desigualdad de Chebyshev** proporciona un límite de probabilidad sin asumir ninguna distribución: $P[|X - \mu| \geq n\sigma] \leq 1/n^2$. Es menos precisa que asumir normalidad, pero más robusta.

### Value at Risk (VaR)

El **VaR** al nivel de confianza $\alpha$ es la pérdida máxima esperada en un horizonte dado, con probabilidad $1-\alpha$. Formalmente es el cuantil $\alpha$ de la distribución de pérdidas. Si el VaR diario al 99% es 10M€, significa que en el 99% de los días las pérdidas no superarán 10M€.

Ventajas: un único número, fácil de comunicar, ampliamente adoptado por reguladores (Basilea). Limitaciones sustanciales: no dice nada sobre la magnitud de las pérdidas en el 1% de los casos (**no captura la forma de la cola**), puede incentivar a concentrar riesgo justo por debajo del umbral, y no es **subaditivo** en general —el VaR del portfolio puede ser mayor que la suma de los VaR individuales, lo que viola la lógica de la diversificación.

El **backtesting** comprueba si el modelo VaR es consistente con los datos: al 99%, se esperan aproximadamente $0.01 \times n$ excepciones en $n$ días. El número de excepciones sigue una distribución binomial, lo que permite hacer tests formales. Los datos de 2007 mostraron que los modelos de los grandes bancos subestimaron sistemáticamente las excepciones (Bank of America: 14 excepciones observadas vs 2.6 esperadas).

---

## Tema 8: Álgebra matricial

### La idea central

Los portfolios son vectores, las covarianzas son matrices. El álgebra matricial es la sintaxis de la gestión de riesgos multivariante.

### Operaciones básicas

Las operaciones matriciales —suma, producto, transpuesta, inversa— permiten expresar en forma compacta sistemas de ecuaciones que de otro modo serían inmanejables. La fórmula de varianza del portfolio $\sigma_P^2 = \mathbf{w}'\Sigma\mathbf{w}$ (donde $\mathbf{w}$ es el vector de pesos y $\Sigma$ la matriz de covarianzas) es el ejemplo canónico.

### Matrices de transición

Una **matriz de transición** $T$ recoge las probabilidades de pasar de un estado a otro en un periodo. En riesgo de crédito, los estados son calificaciones crediticias (A, B, C, D=default). La probabilidad de transición a $n$ periodos es $T^n$: multiplicar la matriz por sí misma $n$ veces. Permite estimar la probabilidad de que un bono con rating A llegue a impago en 5 años.

### Descomposición de Cholesky y Monte Carlo

Para simular variables correlacionadas, se necesita descomponer la matriz de covarianzas $\Sigma = LL'$ (descomposición de **Cholesky**). El vector de variables correlacionadas se obtiene como $C = L\Phi$, donde $\Phi$ es un vector de normales estándar independientes. Esto es el motor de cualquier simulación Monte Carlo multivariante.

---

## Tema 9: Espacios vectoriales

### La idea central

Los rendimientos de activos financieros tienen estructura de espacio vectorial: se pueden descomponer en direcciones independientes (**componentes principales**) que explican la mayor parte de la varianza. Esto reduce dimensionalidad y facilita la interpretación del riesgo.

### Análisis de componentes principales (PCA)

El **PCA** (*Principal Component Analysis*) transforma un conjunto de variables correlacionadas en componentes ortogonales (no correlacionados) ordenados de mayor a menor varianza explicada. En la curva de tipos de interés, los tres primeros componentes principales corresponden a desplazamiento paralelo (*shift*), inclinación (*tilt*) y curvatura (*twist*) de la curva: con solo tres factores se explica más del 95% de los movimientos históricos. En renta variable global, los primeros componentes capturan el factor de mercado global y efectos sectoriales.

La aplicación práctica en riesgo: en lugar de modelar $n$ tipos de interés correlacionados, se modelan 3 factores independientes, lo que simplifica enormemente la estimación y la simulación.

---

## Tema 10: Regresión lineal

### La idea central

La regresión descompone la variación de un activo en una parte explicada por factores sistemáticos y una parte idiosincrática. Esta descomposición es la base de los modelos de factor y las pruebas de estrés.

### OLS y sus supuestos

La regresión por **mínimos cuadrados ordinarios** (OLS, *Ordinary Least Squares*) estima $\beta$ minimizando la suma de residuos al cuadrado:

$$\hat{\beta} = (X'X)^{-1}X'Y$$

Los supuestos clave son: linealidad, $E[\varepsilon|X]=0$ (exogeneidad), $\text{Var}[\varepsilon|X]=\sigma^2$ (homocedasticidad) y $\text{Cov}[\varepsilon_i, \varepsilon_j]=0$ (no autocorrelación). Bajo estos supuestos, OLS es BLUE.

El ratio de cobertura óptimo $h^* = -\rho_{AB}\sigma_A/\sigma_B$ del T3 se obtiene directamente como el coeficiente de la regresión de los retornos de $A$ sobre los de $B$: OLS cancela sistemáticamente el riesgo sistemático.

### Modelos de factor

En la **regresión multivariante** $Y = X\beta + \varepsilon$, los regresores son factores de riesgo (mercado, sector, tipo de cambio). La varianza del portfolio se descompone en:

$$\sigma_\text{portfolio}^2 = \beta^2 \sigma_\text{factor}^2 + \sigma_\varepsilon^2$$

La ventaja es que $\beta$ (la exposición al factor) es aditiva entre activos, lo que permite agregar riesgo de forma consistente en un portfolio. El **stress testing** aplica shocks a los factores y observa el impacto en el portfolio; la limitación es que asume linealidad, que puede fallar en eventos extremos.

---

## Tema 11: Modelos de series temporales

### La idea central

Los precios y retornos financieros no son independientes en el tiempo. Modelar esa dependencia temporal es imprescindible para estimar la volatilidad futura y diseñar modelos de riesgo dinámicos.

### Random walk y drift-diffusion

Un **random walk** es una serie donde cada incremento es ruido blanco: $x_t = x_{t-1} + \varepsilon_t$ con $E[\varepsilon_t]=0$ y varianza constante. La varianza crece linealmente con el tiempo: $\text{Var}[x_t|x_0] = t\sigma^2$. El modelo de **drift-diffusion** añade una tendencia constante $\alpha$: $p_t = p_{t-1} + \alpha + \varepsilon_t$. Estos son los modelos de precios más simples; el modelo de Black-Scholes es su versión en tiempo continuo.

### Autoregresión y reversión a la media

El modelo **AR(1)** es $r_t = \alpha + \lambda r_{t-1} + \varepsilon_t$. Cuando $|\lambda| < 1$, la serie revierte a la media de largo plazo $\alpha/(1-\lambda)$: los tipos de interés y la volatilidad tienen esta propiedad empíricamente. Cuando $\lambda > 1$, la serie diverge. Cuando $\lambda = 1$, es un random walk.

### GARCH

Los mercados financieros exhiben **heterocedasticidad**: la volatilidad no es constante, se agrupa en el tiempo (periodos de alta volatilidad seguidos de alta volatilidad). El modelo **GARCH(1,1)** modela la varianza condicional:

$$\sigma_t^2 = \omega + \alpha \varepsilon_{t-1}^2 + \beta \sigma_{t-1}^2$$

donde $\varepsilon_{t-1}^2$ es el cuadrado del retorno del día anterior (shock reciente) y $\sigma_{t-1}^2$ es la varianza estimada ayer. Este modelo captura la persistencia de la volatilidad y es el estándar de la industria para estimar volatilidad dinámica.

### Jump-diffusion e modelos de tipo de interés

Los modelos de **jump-diffusion** añaden saltos discretos al proceso continuo: $r_t = \mu + \sigma\varepsilon_t + I_t u_t$, donde $I_t$ es un indicador de salto y $u_t$ la magnitud. Capturan mejor los movimientos bruscos de mercado.

Los modelos de tipo de interés son procesos de reversión a la media con formulaciones específicas: el **Vasicek** tiene reversión lineal y volatilidad constante; el **Cox-Ingersoll-Ross** añade un término $r_t^{1/2}$ que hace la volatilidad proporcional al nivel del tipo (impide tipos negativos).

---

## Tema 12: Factores de decaimiento

### La idea central

En la estimación de media y varianza con datos históricos, las observaciones antiguas pesan igual que las recientes. Los factores de decaimiento son un mecanismo para dar más peso a los datos recientes, capturando mejor el estado actual de los mercados.

### Media y varianza con decaimiento

En lugar de la media simple $\hat{\mu} = \frac{1}{n}\sum x_t$, se usa la media con pesos exponenciales:

$$\hat{\mu}_t = (1-\delta)x_t + \delta\hat{\mu}_{t-1}$$

donde $\delta \in (0,1)$ es el factor de decaimiento: cuanto más cercano a 1, más lento el olvido. El **half-life** es el número de periodos en que el peso de una observación se reduce a la mitad: $h = \ln(0.5)/\ln(\delta)$.

La varianza con decaimiento sigue la misma lógica: $\hat{\sigma}_t^2 = (1-\delta)(r_t - \hat{\mu}_t)^2 + \delta\hat{\sigma}_{t-1}^2$, que puede verse como un GARCH restringido.

### Mínimos cuadrados ponderados y Hybrid VaR

Los **mínimos cuadrados ponderados** (WLS, *Weighted Least Squares*) aplican la matriz de pesos $W$ en la estimación de regresión: $\tilde{\beta} = (X'WX)^{-1}X'WY$. Las observaciones recientes reciben mayor peso, lo que hace los coeficientes más sensibles a cambios estructurales.

El **Hybrid VaR** combina la simulación histórica (que reproduce colas gruesas, asimetría y autocorrelación sin asumir una distribución) con factores de decaimiento (que dan más relevancia a los datos recientes). Es el compromiso estándar en la práctica: no paramétrico en la forma de la distribución, pero adaptativo en el tiempo.

---

## Lo más importante para recordar

1. **Los retornos logarítmicos son aditivos en el tiempo; los simples no.** Esto hace los log-retornos más manejables para modelar series temporales, pero la diferencia solo es relevante para horizontes largos o retornos grandes.

2. **El VaR es un cuantil, no una pérdida máxima.** Dice que con probabilidad $1-\alpha$ las pérdidas no superarán cierto nivel; no dice nada sobre qué pasa en el otro $\alpha$%. El Expected Shortfall (ES) es la métrica que sí captura el riesgo de cola.

3. **Correlación no implica independencia, y correlación cero no implica independencia.** Las cópulas existen precisamente para modelar dependencia no lineal, que es la que aparece en crisis.

4. **La volatilidad agrupa en el tiempo (GARCH).** Usar una volatilidad histórica estática subestima el riesgo en periodos de alta volatilidad y lo sobreestima cuando el mercado está tranquilo. El factor de decaimiento y GARCH son las soluciones prácticas.

5. **Los supuestos de OLS son restrictivos.** Homocedasticidad, no autocorrelación y exogeneidad rara vez se cumplen en datos financieros. Violarlos no invalida necesariamente el modelo, pero sí invalida los errores estándar y los tests de hipótesis derivados.

6. **El análisis bayesiano y el frecuentista no son rivales en la práctica: son complementarios.** El prior bayesiano permite incorporar conocimiento experto cuando los datos son escasos (riesgo de crédito, riesgo operacional); el enfoque frecuentista es más robusto cuando los datos son abundantes y el prior difícil de justificar.

---

## Conexión con el resto del módulo

| Concepto | Dónde aparece después |
|---|---|
| Retornos logarítmicos | Base de todos los modelos de precios (T11) |
| Distribución normal | Supuesto implícito del VaR paramétrico (T7), OLS (T10) |
| Curtosis y colas gruesas | Motivación de distribuciones de mezcla (T4), copulas (T5), Hybrid VaR (T12) |
| Correlación y covarianza | Matriz de covarianzas en álgebra matricial (T8), PCA (T9) |
| Distribución binomial | Backtesting del VaR (T7) |
| Distribución t de Student | Inferencia en regresión cuando $\sigma$ es desconocida (T10) |
| Teorema de Bayes | Redes bayesianas para riesgo de crédito y stress testing (T6) |
| Cholesky | Simulación Monte Carlo multivariante (T8) |
| AR(1) con reversión | Modelos de tipo de interés Vasicek y CIR (T11) |
| Factores de decaimiento | Hybrid VaR como caso especial de simulación histórica ponderada (T12) |
