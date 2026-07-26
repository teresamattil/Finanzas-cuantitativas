# Módulo 10 — Teoría del Valor Extremo (EVT)

## Para qué sirve este bloque

La estadística clásica se centra en el comportamiento promedio de una serie. Los modelos de riesgo basados en distribución normal estiman bien la media y la varianza, pero sistemáticamente subestiman la probabilidad de eventos extremos porque la normal tiene colas demasiado delgadas respecto a los datos financieros reales. La **Teoría del Valor Extremo** (EVT) resuelve exactamente ese problema: en lugar de modelar toda la distribución, modela solo las colas, donde ocurren las pérdidas graves.

El módulo es la continuación natural del Módulo 9: si el VaR paramétrico falla porque asume normalidad, EVT proporciona la herramienta para calcular un VaR más preciso en el extremo de la distribución sin ese supuesto.

Ilustración del problema: retornos mensuales de bonos corporativos A-rated (1980-2008). La peor observación fue -10.84%. Con distribución normal, la probabilidad de un retorno así en 30 años es 0.00008%. Con EVT, es 1.4% — más de 16.000 veces mayor. El evento ocurrió en la muestra; la normal lo consideraba imposible en diez milenios.

---

## Tema 1: Los dos marcos de EVT

### La idea central

EVT no es un modelo único: es una familia de resultados teóricos que garantizan que, bajo ciertas condiciones, los valores extremos de cualquier distribución convergen a una de solo tres distribuciones posibles. El resultado es válido independientemente de cuál sea la distribución subyacente de los datos.

### Marco 1: Block Maximum (máximos por bloque)

Se divide la serie de $T$ observaciones en $m$ bloques de longitud $n$ ($m \times n = T$) y se toma el máximo de cada bloque: $M_k = \max(y_{n(k-1)+1}, \ldots, y_{nk})$. El resultado teórico (Fisher-Tippett 1928, Gnedenko 1943) es que la distribución de los máximos normalizados converge a una **distribución generalizada de valores extremos (GEV)**, que engloba tres casos según el parámetro de forma $\xi$:

- $\xi > 0$: **Fréchet** — colas gruesas. Es la distribución relevante en finanzas, porque los retornos son leptocúrticos. Engloba como caso especial la distribución t de Student.
- $\xi = 0$: **Gumbel** — colas de grosor medio, decaimiento exponencial. Engloba la normal y la log-normal.
- $\xi < 0$: **Weibull** — colas cortas con punto final finito; la PDF es exactamente cero más allá de ese punto.

La CDF unificada de la GEV es:

$$H_{\xi,\mu,\sigma}(y_t) = \begin{cases} \exp\left[-(1 + \xi(y_t-\mu)/\sigma)^{-1/\xi}\right] & \text{si } \xi \neq 0 \\ \exp\left[-\exp(-(y_t-\mu)/\sigma)\right] & \text{si } \xi = 0 \end{cases}$$

donde $\mu$ es el parámetro de localización, $\sigma$ es el de escala, y $\xi$ es el de forma (determina el grosor de las colas).

El **problema práctico** del enfoque de bloques es la ineficiencia: si hay varios extremos en un bloque, solo se usa el máximo y el resto se descarta. Hay además un trade-off: bloques largos → menos sesgo pero más varianza; bloques cortos → menos varianza pero más sesgo.

### Marco 2: Peaks Over Threshold (POT)

Es el enfoque preferido en la práctica. Se especifica un umbral $U$ y se modelan las excedencias: $\tilde{y}_t = y_t - U \mid y_t > U$. Cuando $U \to \infty$, la distribución de las excedencias normalizadas converge a la **distribución generalizada de Pareto (GPD)**:

$$G_{\xi,\sigma}(\tilde{y}_t) = \begin{cases} 1 - (1 + \xi \tilde{y}_t/\sigma)^{-1/\xi} & \text{si } \xi \neq 0 \\ 1 - \exp(-\tilde{y}_t/\sigma) & \text{si } \xi = 0 \end{cases}$$

Los tres casos (Fréchet, Gumbel, Weibull en block maximum) corresponden en el POT a las distribuciones **Pareto ordinaria, exponencial y beta**, respectivamente. El parámetro $\xi$ es el mismo en ambos marcos, lo que permite transferir estimaciones entre los dos enfoques.

**Elección del umbral $U$:** es el punto crítico del enfoque POT. Si $U$ es demasiado bajo, observaciones no extremas se clasifican como extremas → sesgo en los parámetros. Si $U$ es demasiado alto, quedan muy pocas observaciones en la cola → alta varianza de las estimaciones. La solución práctica más habitual es estimar los parámetros para valores crecientes de $U$ hasta que los estimados se estabilicen.

---

## Tema 2: Estimación de parámetros

### Estimación por máxima verosimilitud (ML)

La PDF de las excedencias sobre el umbral (para $\xi \neq 0$) es:

$$g_{\xi,\sigma}(\tilde{y}_t) = \frac{1}{\sigma}\left(1 + \frac{\xi \tilde{y}_t}{\sigma}\right)^{-(1/\xi + 1)}$$

La log-verosimilitud conjunta para $N_U$ observaciones sobre el umbral es:

$$\text{LLF}(\xi, \sigma) = -N_U \ln(\sigma) - \left(\frac{1}{\xi} + 1\right)\sum_{i=1}^{N_U} \ln\left(1 + \frac{\xi \tilde{y}_i}{\sigma}\right)$$

Siempre que $\xi > -0.5$, los estimadores ML son consistentes y asintóticamente normales. Sin embargo, **no existe solución analítica**: hay que usar un optimizador numérico (en Python, `scipy.optimize.minimize` con Nelder-Mead). Aplicado a datos del S&P500 con umbral $-0.025$, los parámetros estimados son $\hat{\xi} \approx 0.388$ y $\hat{\sigma} \approx 0.0075$.

### Estimador de Hill (no paramétrico)

Más simple que ML. Aplicable solo al caso de colas gruesas (Fréchet, $\xi > 0$). Se ordenan las excedencias de mayor a menor: $\tilde{y}_{(1)} \geq \tilde{y}_{(2)} \geq \cdots \geq \tilde{y}_{(T)}$. El estimador de Hill es:

$$\hat{\xi} = \frac{1}{k-1} \sum_{i=1}^{k-1} \left[\ln(\tilde{y}_{(i)}) - \ln(\tilde{y}_{(k)})\right]$$

donde $k$ es el número de observaciones clasificadas como extremas. Intuitivamente, promedia los logaritmos de los ratios entre valores extremos consecutivos: estima la velocidad a la que decae la cola. El **Hill plot** representa $\hat{\xi}$ frente a $k$ y se elige el menor $k$ para el que el estimado se estabiliza.

### Estimadores de Pickands y De Haan-Resnick

Dos variantes alternativas del enfoque no paramétrico:

$$\hat{\xi}_{\text{Pickands}} = \frac{1}{\ln 2} \ln\left(\frac{\tilde{y}_{(k)} - \tilde{y}_{(2k)}}{\tilde{y}_{(2k)} - \tilde{y}_{(4k)}}\right)$$

$$\hat{\xi}_{\text{De Haan-Resnick}} = \frac{\ln(\tilde{y}_{(1)}) - \ln(\tilde{y}_{(k)})}{\ln(k)}$$

Pickands es consistente y asintóticamente normal pero menos eficiente que Hill. Una corrección del sesgo de muestra pequeña (Huisman et al. 2001) consiste en regresar las estimaciones de $\xi$ sobre una constante y el valor de $k$ utilizado; el intercepto de esa regresión es el estimado corregido $\hat{\xi}$ que corresponde al límite cuando $k \to 0$.

### Estimación del parámetro de escala $\sigma$

Una vez estimado $\xi$ por un método no paramétrico, $\sigma$ se puede obtener: (a) sustituyendo $\hat{\xi}$ en la log-verosimilitud y optimizando solo sobre $\sigma$; o (b) usando la fórmula analítica que existe bajo el supuesto Fréchet (Brooks et al. 2005).

---

## Tema 3: VaR con EVT

### La idea central

Los tres métodos estándar de VaR (paramétrico normal, histórico y Monte Carlo) fueron cubiertos en el Módulo 9. EVT añade un cuarto método que es más preciso en el extremo profundo de la cola porque usa explícitamente la forma de esa cola, en lugar de extrapolar desde el centro de la distribución.

### VaR delta-normal y VaR histórico (referencia)

**Delta-normal:** $\text{VaR}_{\text{normal}} = \sigma Z_\alpha$. Usa la desviación típica de toda la muestra y un cuantil de la normal estándar. Simple pero subestima el riesgo en las colas.

**Histórico:** ordena los retornos y toma el percentil correspondiente: `data['ret'].quantile(0.05)`. No asume distribución pero usa un único punto de la distribución empírica e ignora toda la información de la forma de la cola.

En datos del S&P500: VaR 99% histórico = -2.60%, VaR 99% normal = -2.21%. El histórico es mayor en valor absoluto porque capta las colas gruesas que la normal no puede.

### VaR con el estimador de Hill

$$\text{VaR}_{\text{Hill}} = \tilde{y}_{(k)} \cdot \left(\frac{N}{N_U} \alpha\right)^{-\hat{\xi}}$$

donde $\tilde{y}_{(k)}$ es la observación en el umbral, $N$ es el tamaño total de la muestra, $N_U$ es el número de observaciones sobre el umbral, y $\alpha$ es el nivel de significación (1% para VaR al 99%).

### VaR con el enfoque POT (GPD)

$$\text{VaR}_{\text{POT}} = U + \frac{\hat{\sigma}}{\hat{\xi}}\left[\left(\frac{N}{N_U}\alpha\right)^{-\hat{\xi}} - 1\right]$$

### VaR con el enfoque de bloques (GEV)

$$\text{VaR}_{\text{Block}} = \hat{\mu} + \frac{\hat{\sigma}}{\hat{\xi}}\left[1 - (-m\ln\alpha)^{-\hat{\xi}}\right]$$

donde $m$ es la longitud del bloque.

Aplicado a S&P500 con umbral -0.025 y ML: $\text{VaR}_{\text{MLE}} \approx -2.60\%$, consistente con el histórico pero con base estadística más sólida para cuantiles más extremos.

### Comparación empírica: mercados emergentes (Gençay y Selçuk 2004)

Estudio con datos diarios de índices de Argentina, Brasil, Hong Kong, Indonesia, Corea, México, Singapur, Taiwán y Turquía (~1993-2000). Conclusión principal: **EVT supera a todos los enfoques alternativos a medida que nos adentramos más en las colas**.

- Para cuantiles del 5% o 2.5% (VaR 95%-97.5%): la t de Student o la simulación histórica son competitivas.
- Para el cuantil del 0.1% (VaR 99.9%): EVT es el mejor método para todos los países excepto uno.
- Las colas superior e inferior tienen **formas distintas** — los modelos que asumen simetría (como la normal) están mal especificados por construcción.

Los parámetros de forma estimados oscilan entre 0.03 (Corea, colas casi normales) y 0.60 (Taiwán, colas extremadamente gruesas con varianza que no existe). Para Taiwán, $\hat{\xi} = 0.60$ implica un índice de cola de $1/\hat{\xi} \approx 1.67$, lo que significa que el segundo momento (varianza) no existe: la distribución tiene tanta masa en las colas que la varianza diverge.

---

## Tema 4: Cuestiones avanzadas

### Dependencia temporal y filtrado ARMA-GARCH

EVT asume que los datos son i.i.d., supuesto que los retornos financieros violan (GARCH, autocorrelación). La solución estándar es: ajustar un modelo ARMA-GARCH, recoger los **residuos estandarizados** (que son más cercanos a i.i.d.) y aplicar EVT sobre esos residuos. Esto combina el modelado de la dinámica temporal con la estimación precisa de los extremos.

### EVT multivariante

EVT se puede extender al caso multivariante para medir dependencia conjunta y spillovers entre series. Se usan funciones **cópula** para conectar las distribuciones marginales extremas de cada serie. Tanto el enfoque de bloques como el POT admiten esta extensión, aunque la complejidad aumenta considerablemente y no existe una definición única de "extremo multivariante".

Complicación práctica: debido a efectos de diversificación o cobertura, movimientos extremos simultáneos en activos individuales pueden no constituir un extremo para el portfolio — los movimientos se atenúan o se cancelan entre sí.

### Intervalos de confianza para el VaR de EVT

Es posible construirlos aunque no es trivial. Son útiles para evaluar si las estimaciones de VaR son suficientemente precisas o si la escasez de datos extremos hace el estimado demasiado impreciso para ser accionable.

---

## Aplicación Python: `VaR_calculation.py`

Script directo sobre datos diarios del S&P500 (`sp500_daily.xlsx`). Tres métodos en secuencia sobre los mismos datos:

**1. VaR paramétrico normal** — `norm.ppf(1-alpha, mean, std_dev)`. Resultados: VaR 90% = -1.21%, VaR 95% = -1.56%, VaR 99% = -2.21%.

**2. VaR histórico** — `data['ret'].quantile(alpha)`. Resultados: VaR 90% = -0.99%, VaR 95% = -1.44%, VaR 99% = -2.60%. El 99% histórico es mayor en valor absoluto que el normal, confirmando que los retornos tienen colas más gruesas de lo que predice la normal.

**3. Estimador de Hill** — umbral = -0.025, $\alpha = 0.01$. Filtra observaciones bajo el umbral, ordena, aplica la fórmula de Hill para $\hat{\xi}$, calcula VaR con la fórmula $\tilde{y}_{(k)} \cdot (N/N_U \cdot \alpha)^{-\hat{\xi}}$. El Hill plot muestra que el VaR converge a -3.2% aproximadamente.

**4. MLE de la GPD** — mismos umbral y $\alpha$. Construye la log-verosimilitud de la GPD como función negativa (para usar `scipy.optimize.minimize` con Nelder-Mead). Estimados: $\hat{\xi} = 0.388$, $\hat{\sigma} = 0.0075$. VaR resultante: -2.60%, consistente con el histórico pero con base distribucional explícita que permite extrapolar a cuantiles más extremos.

---

## Lo más importante para recordar

1. **EVT es el único enfoque estadísticamente válido para cuantiles muy extremos (99.9%+).** El VaR normal los subestima por un factor de hasta 16.000x. El histórico mejora pero usa un solo punto de la distribución empírica, sin aprovechar la forma de la cola.

2. **El parámetro $\xi$ lo determina todo.** Si $\xi > 0$ (Fréchet), las colas son gruesas y los momentos de orden $1/\xi$ o superior no existen. Para retornos financieros típicos, $\xi \approx 0.1$-$0.2$, lo que implica colas equivalentes a una t con 5-10 grados de libertad.

3. **La elección del umbral $U$ es el punto débil del POT.** No hay una regla objetiva universalmente aceptada. El criterio pragmático (estimar para $U$ creciente hasta que $\hat{\xi}$ se estabilice) funciona razonablemente, pero introduce subjetividad.

4. **EVT asume i.i.d.: en datos financieros, hay que filtrar primero con GARCH.** Aplicar EVT directamente sobre retornos con clusters de volatilidad da estimaciones sesgadas. El flujo correcto es ARMA-GARCH → residuos estandarizados → EVT.

5. **EVT solo gana claramente en cuantiles muy extremos.** Para VaR al 95% o 97.5%, la t de Student o el histórico son competitivos. La ventaja de EVT es decisiva para el 99.9%, que es donde el regulador (Basilea) y los gestores de riesgo de cola necesitan precisión.

6. **Las colas superior e inferior son asimétricas.** Modelarlas por separado es necesario; asumir simetría (como hace la normal) introduce sesgo sistemático en al menos una de las dos colas.

---

## Conexión con el resto del módulo

| Concepto | Módulo relacionado |
|---|---|
| VaR paramétrico y sus limitaciones | Módulo 9 — T1: Riesgo de mercado |
| Expected Shortfall como alternativa al VaR | Módulo 9 — T1 (ES es más coherente, EVT lo estima mejor en la cola) |
| GARCH para filtrar dependencia temporal | Módulo 5 — Modelos de volatilidad y correlación |
| Cópulas para EVT multivariante | Módulo 9 — T3 (GMCM en liquidez) |
| MLE y optimización numérica | Módulo 9 — guía matemática (T6-T7) |
| Distribución t de Student como caso especial de Fréchet | Módulo 9 — guía matemática (T4) |
