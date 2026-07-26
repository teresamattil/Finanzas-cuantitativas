# Módulo 7 — Temas 6, 7, 8, 9 y 10: Retornos, Riesgo y Diversificación

---

## Para qué sirve este bloque

Antes de poner precio a cualquier instrumento financiero — un bono, una acción, una opción — necesitas responder dos preguntas previas:

1. **¿Cuánto puedo esperar ganar?** (retorno)
2. **¿Cuánto puedo perder, y con qué probabilidad?** (riesgo)

Sin esas dos piezas, la valoración no tiene base. El CAPM, Black-Scholes, la curva de tipos: todos usan retorno esperado y volatilidad como inputs. Este bloque es el lenguaje que hace posible todo lo que viene después.

---

## Tema 6: Retornos — el lenguaje común del dinero

### La idea central

Para comparar inversiones distintas (un bono a 2 años, acciones, un inmueble) necesitas un denominador común. La respuesta es el **retorno**: cuánto ganas por cada euro invertido, expresado de forma que sea comparable.

### Valor temporal del dinero

El concepto más importante de las finanzas: **100€ hoy valen más que 100€ dentro de un año**, aunque la inflación fuera cero. ¿Por qué? Porque puedes invertirlos hoy y tener más mañana. Por tanto, para comparar cantidades en distintos momentos del tiempo necesitas descontarlas o capitalizarlas usando una tasa.

- **Valor presente (PV):** cuánto vale hoy un pago futuro → $PV = \frac{C}{(1+r)^T}$
- **Valor futuro (FV):** a cuánto crece tu dinero → $FV = PV \cdot (1+r)^T$

Todo el análisis de descuento de flujos de caja (DCF), que se usa para valorar acciones y bonos, descansa sobre esto.

### Compounding (interés compuesto)

La frecuencia con la que se capitaliza el interés cambia el resultado real:

$$FV = P\left(1 + \frac{r}{N}\right)^{NT}$$

En el límite (capitalización continua): $FV = Pe^{rT}$

Esta fórmula de capitalización continua aparece constantemente en los modelos de derivados (Black-Scholes usa $e^{rT}$ para descontar).

### Log-retornos

En la práctica, en vez de calcular la rentabilidad como:

$$R = \frac{P_t - P_{t-1}}{P_{t-1}}$$

se usan **log-retornos**:

$$r_t = \ln\left(\frac{P_t}{P_{t-1}}\right) = \ln(P_t) - \ln(P_{t-1})$$

La ventaja es que los log-retornos **se suman en el tiempo**, lo que simplifica los modelos. Si ganas un 5% en enero y un 3% en febrero, el retorno acumulado es simplemente $r_{enero} + r_{febrero}$. Con retornos simples eso no funciona. Los log-retornos son el estándar en finanzas cuantitativas.

### Tipos nominales vs. reales

- **Tipo nominal:** lo que promete el instrumento en euros corrientes.
- **Tipo real:** lo que ganas en poder adquisitivo real, corrigiendo por inflación.

Relación de Fisher (1930): $r_{nominal} \approx r_{real} + \text{inflación esperada}$

Importante para valorar bonos indexados a la inflación (TIPS) y para cualquier análisis de largo plazo.

---




## Tema 7: Riesgo vs. Retorno — los estadísticos que importan

### La idea central

Si los mercados incorporan información rápidamente, los precios se mueven de forma impredecible. El modelo matemático natural para eso es el **movimiento browniano geométrico**:

$$\frac{dS_t}{S_t} = \mu \, dt + \sigma \, dW_t$$

donde $\mu$ es la tendencia media y $\sigma$ es la volatilidad. Si este modelo fuera exactamente correcto, los log-retornos serían **normalmente distribuidos**. El problema es que no lo son — y eso es el tema 8.

### Estadísticos clave para caracterizar retornos

Para caracterizar la distribución de retornos, los cuatro momentos que importan:

| Estadístico | Qué mide | Normal |
|---|---|---|
| **Media** ($\mu$) | Retorno esperado | cualquier valor |
| **Varianza** ($\sigma^2$) | Dispersión cuadrática | cualquier valor |
| **Skewness** ($\gamma$) | Asimetría — ¿más sorpresas malas o buenas? | 0 |
| **Kurtosis** ($\kappa$) | Peso de las colas — ¿qué tan extremos son los extremos? | 3 |

Para escalar a datos anuales (con 250 días de trading):
- $\sigma_{anual} = \sqrt{250} \cdot \sigma_{diaria}$
- Skewness y kurtosis no escalan — son invariantes al período de medición.

### Riesgo y prima de riesgo

El mercado compensa por asumir riesgo. El exceso de retorno respecto al activo libre de riesgo se llama **prima de riesgo**:

$$\text{Prima de riesgo} = E(r_i) - r_f$$

Para acciones estadounidenses, históricamente ~6–8% anual sobre el bono del Tesoro. No es constante: varía entre 3–15% dependiendo del período y el entorno macro.

La **utilidad esperada** de un inversor averso al riesgo bajo normalidad:

$$U = E(r) - \frac{\lambda}{2}\sigma^2$$

donde $\lambda$ es el coeficiente de aversión al riesgo ($\lambda \in [2, 4]$ en la práctica). A mayor $\lambda$, más penaliza la varianza.

---




## Tema 8: Distribuciones No Normales — cuando los modelos estándar fallan

### La idea central

Los retornos reales tienen **colas más gordas que la normal** (kurtosis > 3) y **asimetría negativa**. Datos de 14 mercados desarrollados lo confirman: índices de acciones muestran kurtosis 5-7; activos como gas natural o trigo alcanzan 31-60. Un modelo que asume normalidad asigna probabilidad casi cero a caídas del 5-sigma — que en mercados reales ocurren una vez por década.

### Distribuciones alternativas

**Estable Paretiana** — parámetro clave $\alpha \in (0,2)$: para $\alpha < 2$ la varianza es **infinita** y el análisis media-varianza de Markowitz pierde su base. Fama (1965) estimó $\alpha \approx 1.7$ para acciones diarias.

**t de Student** — captura leptocurtosis con varianza finita. Kurtosis $= 6/(\nu-4)$; converge a la normal para $\nu \to \infty$. Alternativa práctica a la estable Paretiana.

**Mezcla de normales** — el mercado alterna entre regímenes (calma/pánico); cada régimen es normal pero la mezcla produce colas gordas. Versión discreta (Kon 1984) y secuencial con rupturas estructurales (Kim y Kon 1996).

**Jump-diffusion** — movimiento browniano + saltos de Poisson para modelar shocks de noticias inesperadas. Base de extensiones de Black-Scholes que explican el "volatility smile".

**Lognormal** — si los log-retornos son normales, los retornos simples son lognormales: $E(1+r_t) = e^{\dot{\mu} + \frac{1}{2}\dot{\sigma}^2}$. Incorpora la asimetría por responsabilidad limitada. El CAPM sigue siendo válido bajo lognormalidad.

### Resumen comparativo

| Distribución | Varianza finita | Captura skewness | Captura fat tails | Uso en práctica |
|---|---|---|---|---|
| Normal | Sí | No | No | Base teórica |
| Estable Paretiana | No (si $\alpha<2$) | Sí | Sí | Investigación académica |
| t de Student | Sí | No | Sí | Riesgo de mercado, opciones |
| Mezcla de normales | Sí | Sí | Sí | Modelos de régimen |
| Jump-diffusion | Sí | Sí | Sí | Opciones avanzadas |
| Lognormal | Sí | Sí (positiva) | Moderado | Precios de acciones, B-S |

---

## Tema 9: Diversificación — cómo construir carteras

### La idea central

Mezclar activos que no se mueven igual reduce el riesgo sin reducir el retorno esperado. Esta es la única forma conocida de reducir riesgo sin coste.

### Dos tipos de riesgo

**Riesgo idiosincrático (específico)** — propio de un activo concreto. Si inviertes solo en Repsol y Repsol tiene un accidente, pierdes. Al añadir más activos descorrelacionados, este riesgo se diluye hasta casi desaparecer.

**Riesgo sistemático (de mercado)** — común a todos los activos: recesiones, guerras, pandemias. No desaparece diversificando porque todos los activos caen a la vez. Este es el riesgo que el CAPM (tema 14) va a medir y a pagar.

En el límite, con $n$ activos iguales con correlación $\rho$:

$$\sigma_P^2 = \frac{\sigma^2}{n} + \frac{n-1}{n}\rho\sigma^2 \xrightarrow{n\to\infty} \rho\sigma^2$$

El primer término desaparece (riesgo específico eliminado). El segundo persiste (riesgo sistemático).

### Varianza de cartera

Para una cartera con pesos $w_i$:

$$\sigma_P^2 = \mathbf{w}^T \mathbf{\Sigma} \mathbf{w}$$

Expandido para dos activos B y E:

$$\sigma_P^2 = w_B^2\sigma_B^2 + w_E^2\sigma_E^2 + 2w_Bw_E\,\text{Cov}(r_B, r_E)$$

El término clave es la **covarianza**. Si $\rho_{BE} < 0$, la varianza de la cartera puede caer por debajo de la varianza de cualquiera de los activos individuales. Por eso los bonos y las acciones se han combinado históricamente bien.

### Frontera eficiente de Markowitz (1952)

Al variar los pesos de todos los activos disponibles, obtienes el **conjunto de oportunidades de activos de riesgo (OSRA)**: todos los portfolios posibles en el espacio ($\sigma_P$, $E(r_P)$).

Dentro del OSRA:
- **Frontera eficiente:** la parte superior. Para cada nivel de riesgo, el portfolio con máximo retorno esperado.
- **Portfolio de mínima varianza (MV):** el punto más a la izquierda.
- **Frontera ineficiente:** la parte inferior — mismo riesgo, menos retorno.

### Capital Allocation Line (CAL) y Sharpe ratio

Combinando el portfolio de riesgo $P$ con el activo libre de riesgo:

$$E(r_C) = r_f + \frac{E(r_P) - r_f}{\sigma_P} \cdot \sigma_C = r_f + S_P \cdot \sigma_C$$

La pendiente de esta línea es el **Sharpe ratio**:

$$S_P = \frac{E(r_P) - r_f}{\sigma_P}$$

Retorno en exceso por unidad de riesgo. La métrica más usada en la industria para comparar gestores y fondos. El portfolio óptimo maximiza el Sharpe ratio.

### Portfolio completo óptimo

El inversor reparte entre el portfolio óptimo $P$ y el activo libre de riesgo en proporción:

$$y^* = \frac{E(r_P) - r_f}{\lambda \sigma_P^2}$$

A mayor aversión al riesgo ($\lambda$ alto), menor fracción en activos de riesgo.

---

## Tema 10: Inversión Más Allá de Media-Varianza

### La idea central

Media y varianza describen completamente la distribución solo bajo normalidad. El tema 8 demostró que los retornos no lo son. Tres criterios alternativos que no dependen de ese supuesto.

### 1. Criterio de la Media Geométrica (GMR)

La media aritmética sobreestima el crecimiento real porque ignora el compounding. La corrección:

$$r_g \approx \bar{r} - \frac{1}{2}\sigma^2$$

Un activo con $\bar{r} = 18.4\%$ y volatilidad alta puede tener $r_g = 2.9\%$ — el crecimiento real anual. Maximizar la GMR equivale a maximizar la utilidad logarítmica en contexto multiperiodo.

### 2. Criterios de Seguridad Primero (Safety-First)

Fijan un retorno mínimo tolerable $r_L$ y/o probabilidad máxima de caer bajo él ($\alpha$). Los tres criterios bajo normalidad:

| Criterio | Qué fija | Qué optimiza | Ranking ejemplo |
|---|---|---|---|
| Roy | $r_L$ | Minimiza $\text{Prob}(r < r_L)$ | B > C > A > D |
| Kataoka | $\alpha$ | Maximiza $r_L$ | D > C > B > A |
| Telser | $r_L$ y $\alpha$ | Maximiza $E(r)$ | C > B |
| Sharpe ratio | — | Maximiza ratio exceso/riesgo | A > C > D > B |

Roy con $r_L = r_f$ produce exactamente el mismo portfolio óptimo que el Sharpe ratio. Los rankings divergen — la elección depende de qué define "desastre" para el inversor.

### 3. Dominancia Estocástica

Compara distribuciones completas sin asumir normalidad ni función de utilidad concreta.

- **FSD:** A domina a B si $F_A(r) \leq F_B(r)$ para todo $r$. Cualquier inversor prefiere A independientemente de su aversión al riesgo.
- **SSD:** integra las diferencias de CDFs; válido para inversores aversos al riesgo ($U'' < 0$). Bajo normalidad, el conjunto SSD-eficiente coincide con la frontera de Markowitz.
- **TSD:** añade aversión al riesgo absoluta decreciente. Reduce aún más el conjunto eficiente.

**Jerarquía:** FSD-eficiente ⊇ SSD-eficiente ⊇ TSD-eficiente. Ventaja: no asume distribución específica. Inconveniente: comparaciones por pares computacionalmente prohibitivas con muchos activos — uso principalmente académico.

---

## Lo más importante para recordar

**1. Los log-retornos son el lenguaje cuantitativo de las finanzas.**
Todo modelo de precios, backtesting y estimación de parámetros usa log-retornos. La capitalización continua conecta con Black-Scholes; la suma temporal conecta con la eficiencia computacional.

**2. Los retornos no son normales. Siempre.**
Skewness negativa y kurtosis > 3 son universales. Mezclas de normales y saltos de Poisson son las explicaciones más convincentes. La pregunta correcta ante cualquier modelo no es "¿funciona en promedio?" sino "¿qué pasa en el percentil 1%?".

**3. La diversificación elimina riesgo específico gratis — hasta el riesgo sistemático.**
Añadir activos descorrelacionados reduce el riesgo sin coste en retorno esperado. El riesgo sistemático no desaparece. Distinguir ambos tipos es la base del CAPM.

**4. El Sharpe ratio y la GMR son las dos métricas de comparación más usadas.**
Sharpe ratio para comparación en un período; media geométrica para evaluar estrategias multiperiodo. La GMR penaliza la volatilidad automáticamente — un activo muy volátil puede destruir riqueza aunque tenga media aritmética alta.

**5. Los criterios safety-first son el puente entre teoría y gestión de riesgo real.**
En la práctica, gestoras, pensiones y reguladores piensan en términos de pérdidas máximas tolerable (Roy/Kataoka) o retorno mínimo garantizado — no en utilidad abstracta. El criterio de Roy con $r_L = r_f$ produce exactamente el mismo portfolio óptimo que el Sharpe ratio.

**6. Media-varianza es el punto de partida, no el final.**
La dominancia estocástica demuestra que hay portfolios Markowitz-eficientes que no maximizan la utilidad esperada cuando los retornos son no normales. En la práctica, los modelos avanzados corrigen con CVaR, distribuciones t o mezclas.

---

## Conexión con el resto del módulo

| Concepto de este bloque | Dónde aparece después |
|---|---|
| Volatilidad $\sigma$ | Input #1 de Black-Scholes (Tema 21) |
| Retorno esperado $\mu$ | CAPM: $E(r_i) = r_f + \beta_i(E(r_m) - r_f)$ (Tema 14) |
| Jump-diffusion, fat tails | Complicaciones de Black-Scholes (Tema 21) |
| t de Student, mezclas | Modelos de volatilidad estocástica |
| Sharpe ratio | Evaluación de estrategias activas (Temas 14-15) |
| Safety-first / CVaR | Gestión de riesgos (regulación Basilea) |
| Dominancia estocástica | Marco teórico de comparación de fondos |
