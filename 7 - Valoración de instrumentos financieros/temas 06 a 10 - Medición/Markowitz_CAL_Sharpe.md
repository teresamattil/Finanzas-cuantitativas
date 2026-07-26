# Markowitz, CAL y Sharpe ratio

---

## Para qué sirve este bloque

Toda decisión de inversión tiene dos preguntas: cuánto puedo ganar y cuánto puedo perder. Markowitz formaliza eso. La CAL y el Sharpe ratio resuelven qué pasa cuando añades una opción sin riesgo a la mezcla.

---

## Markowitz: la nube de posibilidades

Tienes un universo de $m$ activos de riesgo. Quieres construir un portfolio eligiendo $n$ de ellos y asignando pesos $(w_1, w_2, ..., w_n)$ que sumen 100%.

Para cada combinación de activos y pesos puedes calcular:

- **Retorno esperado** del portfolio: media ponderada de los retornos individuales
- **Riesgo** del portfolio: varianza que depende de los pesos y de las correlaciones entre activos

$$\sigma_P^2 = \mathbf{w}^T \mathbf{\Sigma} \mathbf{w}$$
# Expected portfolio return
np.sum(weights * log_returns.mean())* 250
# Expected Portfolio Variance
np.dot(weights.T,np.dot(log_returns.cov()* 250,weights))
# Expected Portfolio Volatility
np.sqrt(np.dot(weights.T,np.dot(log_returns.cov()* 250,weights)))

Si simulas todas las combinaciones posibles de activos y pesos, obtienes una nube de puntos en el espacio (riesgo, retorno). Cada punto es un portfolio distinto.

```
E(r)
 |          * frontera eficiente
 |        *
 |      * *  (nube interior — posibles pero subóptimos)
 |    *
 |  * (mínima varianza)
 |___________________________
                            σ
```

La **frontera eficiente** es el borde superior de esa nube: para cada nivel de riesgo, el portfolio con mayor retorno esperado. Todo lo que está por debajo de la frontera es dominado — mismo riesgo, menos retorno. Se descarta.

El resultado de Markowitz no es un portfolio único sino una frontera: una curva de opciones óptimas. Qué punto de esa curva eliges depende de tu aversión al riesgo.

### Por qué la frontera es curva

Cuando combinas dos activos de riesgo, la varianza del resultado no es la suma de sus varianzas: depende de la correlación entre ellos. Esa dependencia no lineal es lo que hace que la frontera sea curva, no una recta. A menor correlación entre activos, más a la izquierda puede llegar la frontera — menor riesgo para el mismo retorno. Eso es la diversificación.

---

## Añades un activo sin riesgo — y el problema cambia de forma

Un bono del Estado o una cuenta garantizada paga un tipo fijo $r_f$ con riesgo cero: $\sigma = 0$, correlación 0 con todo. En la práctica, $r_f$ no es algo que elijas — es el tipo que fija el banco central (BCE, Fed), observable y disponible para todos. Representa el coste de oportunidad de invertir: si no haces nada, el mercado ya te da $r_f$ gratis. Cualquier activo de riesgo tiene que justificar el riesgo adicional frente a ese punto de referencia.

Ahora tu decisión ya no es solo "qué mezcla de activos de riesgo elijo" sino:

> **¿Cuánto de mi dinero pongo en activos de riesgo y cuánto en el activo sin riesgo?**

Podrías meter el activo sin riesgo directamente en Markowitz, pero matemáticamente el modelo colapsa: como el bono tiene varianza y covarianza cero, la no-linealidad que generaba la curva desaparece. Cualquier mezcla entre el bono y un portfolio de riesgo escala de forma perfectamente lineal — en retorno y en riesgo. El resultado no es una curva sino una recta.

---

## La CAL: la línea bono–portfolio

Elige un portfolio cualquiera $P$ de la frontera eficiente. En el gráfico está en el punto $(\sigma_P,\ E(r_P))$, por ejemplo $(15\%,\ 9\%)$.

El bono está en el eje Y, en el punto $(0,\ r_f)$, por ejemplo $(0,\ 3\%)$ — riesgo cero, retorno garantizado.

Si mezclas bono y $P$ en distintas proporciones, obtienes todos los puntos entre esos dos extremos. Como ambos escalan linealmente, forman una **recta**. Esa recta es la **Capital Allocation Line (CAL)** para el portfolio $P$.

```
E(r)
 |
9%|              * P
 |            /
 |          /
3%|* bono  /
 |      /
 |____/___________
      0%    15%    σ
```

Moviéndote a lo largo de esta recta:
- En el extremo izquierdo (todo en bono): $r_f$, riesgo 0
- En el extremo derecho (todo en $P$): retorno y riesgo de $P$
- En el medio: proporcional al peso que pones en cada uno
- Más allá de $P$ (apalancamiento): pides prestado al tipo $r_f$ e inviertes más del 100% en $P$

---

## El Sharpe ratio: la pendiente de la recta

Puedes trazar esa recta desde el bono hacia cualquier portfolio de la frontera eficiente. Cada uno da una recta distinta. La pregunta es: ¿cuál es mejor?

La más empinada. Para cualquier nivel de riesgo que decidas asumir, la recta más empinada te da más retorno. Y como todas las rectas salen del mismo punto (el bono), "más empinada" equivale exactamente a "más retorno por unidad de riesgo añadida".

Eso es el **Sharpe ratio**: la pendiente de la recta bono–$P$.

$$S_P = \frac{E(r_P) - r_f}{\sigma_P}$$

El numerador es el retorno en exceso sobre el bono — lo que ganas de más por asumir riesgo. El denominador es la unidad de riesgo. Sharpe ratio = precio del riesgo para ese portfolio.

---

## Dos decisiones separadas

Aquí está la distinción clave:

**Decisión 1 — ¿Qué portfolio de riesgo elijo?**
De todos los portfolios en la frontera eficiente, el mejor es el de mayor Sharpe ratio. Es el punto donde la recta desde el bono es tangente a la curva de Markowitz — la recta más empinada posible que todavía toca la frontera.

```
E(r)
 |            / ← recta óptima (tangente a la frontera en T)
 |          T ← portfolio tangente
 |        * /\
 |      *  /  P2 ← otra recta, menos empinada
 |    *   /
3%|*   /
 |/__________________
  0                 σ
```

**Decisión 2 — ¿Cuánto pongo en $T$ vs. en el bono?**
Una vez elegido el portfolio tangente $T$, tu aversión al riesgo determina en qué punto de la recta te sitúas:

$$y^* = \frac{E(r_T) - r_f}{\lambda \cdot \sigma_T^2}$$

- Inversor conservador ($\lambda$ alto): $y^*$ pequeño → mucho en bono, poco en $T$
- Inversor agresivo ($\lambda$ bajo): $y^*$ grande → mucho en $T$, puede llegar al apalancamiento

### El resultado más poderoso

Todos los inversores racionales mantienen el **mismo portfolio de activos de riesgo** — el tangente $T$. Lo que varía entre inversores es cuánto ponen ahí. Esto es el **Teorema de Separación de Tobin**: la elección del portfolio de riesgo óptimo es independiente de la aversión al riesgo.

---

## Conexión con lo que viene

| Concepto | Aparece después en |
|---|---|
| Portfolio tangente $T$ | Si el CAPM es cierto, $T$ = índice de mercado (Tema 14) |
| Sharpe ratio | Evaluación de gestores, alpha de Jensen |
| $\lambda$ y el reparto $y^*$ | Base del modelo de utilidad esperada |
| Activo libre de riesgo $r_f$ | Input directo de Black-Scholes ($e^{-r_f T}$) |
