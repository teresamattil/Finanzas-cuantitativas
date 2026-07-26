# ¿Cómo se mide el riesgo?

La varianza es **una medida** del riesgo, no el riesgo en sí. Y tiene limitaciones importantes.

---

## Qué es el riesgo en finanzas

Riesgo = **incertidumbre sobre el retorno futuro**. No sabes lo que vas a ganar. El problema es que esa incertidumbre no es simétrica — a un inversor le importa mucho más perder que ganar lo equivalente.

---

## Cómo se mide

### 1. Varianza / desviación típica (volatilidad)

$$\sigma^2 = E[(r - \mu)^2]$$

Mide dispersión total alrededor de la media — tanto subidas como bajadas. Es el estándar de Markowitz y el CAPM.

**Problema:** penaliza igual las sorpresas buenas y las malas. Un activo que sube mucho de forma irregular tiene "mucho riesgo" según este criterio, aunque nadie se queja de las subidas.

### 2. Semi-varianza (downside risk)

$$\text{SV} = E[\min(r - \mu, 0)^2]$$

Solo penaliza los retornos por debajo de la media. Más intuitivo para inversores reales. Base del ratio de Sortino.

### 3. Value at Risk (VaR)

"¿Cuánto puedo perder como máximo con un 95% de probabilidad en un día?"

$$\text{VaR}_{95\%} = \text{cuantil}_{5\%}\text{ de la distribución de pérdidas}$$

Estándar regulatorio. **Problema:** no dice nada sobre qué pasa en el 5% peor — solo marca la frontera.

### 4. CVaR / Expected Shortfall

"¿Cuánto pierdo **en promedio** en el peor 5% de los casos?"

$$\text{CVaR}_{95\%} = E[r \mid r < \text{VaR}_{95\%}]$$

Más conservador que el VaR. Es el estándar de Basilea III/IV para banca. Captura el comportamiento de la cola, no solo su umbral.

### 5. Beta

Riesgo **relativo al mercado**. No mide dispersión absoluta sino cuánto se mueve un activo cuando el mercado se mueve. Aparece en el CAPM (tema 14).

---

## La jerarquía práctica

| Medida | Qué captura | Dónde se usa |
|---|---|---|
| Varianza $\sigma^2$ | Dispersión total (simétrica) | Markowitz, CAPM |
| Semi-varianza | Solo pérdidas | Ratio de Sortino |
| VaR | Umbral de pérdida máxima | Regulación, gestoras |
| CVaR / Expected Shortfall | Pérdida media en la cola | Basilea III/IV, banca |
| Beta $\beta$ | Riesgo relativo al mercado | CAPM, factor models |

---

## So-what

Cuando el guía habla de $\sigma^2$ como riesgo, está usando el supuesto de normalidad implícito — si los retornos son simétricos, varianza y downside risk son equivalentes. En cuanto los retornos tienen skewness negativa (que es siempre, tema 8), la varianza **subestima el riesgo real de pérdida**. Por eso el CVaR existe.
