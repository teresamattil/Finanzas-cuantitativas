---
date: 2026-07-24
tags: [resumen, valoración, módulo-7, finanzas-cuantitativas]
---

# Módulo 7 — Valoración de Instrumentos Financieros

El módulo responde tres preguntas en secuencia: cómo medir retorno y riesgo (T6-10), cómo usar esas medidas para valorar bonos y acciones (T11-17), y cómo extender esa valoración a instrumentos derivados (T18-21).

---

## Bloque 1 — Medición: Retorno, Riesgo y Diversificación (T6-10)

### T6: Retornos

El denominador común para comparar inversiones es el retorno. Los **log-retornos** son el estándar cuantitativo porque se suman en el tiempo:

$$r_t = \ln(P_t / P_{t-1})$$

El valor temporal del dinero es la base de toda la valoración: $PV = C/(1+r)^T$. En el límite (capitalización continua): $FV = Pe^{rT}$, que aparece directamente en Black-Scholes. La **relación de Fisher** separa tipo nominal de tipo real: $r_{nominal} \approx r_{real} + \pi^e$.

### T7: Estadísticos de riesgo

Los cuatro momentos que importan para describir retornos:

| Estadístico | Normal |
|---|---|
| Media $\mu$ | cualquier valor |
| Varianza $\sigma^2$ | cualquier valor |
| Skewness $\gamma$ | 0 |
| Kurtosis $\kappa$ | 3 |

Escalado a datos anuales (250 días): $\sigma_{anual} = \sqrt{250}\,\sigma_{diaria}$. La **utilidad esperada** de un inversor averso al riesgo: $U = E(r) - \frac{\lambda}{2}\sigma^2$.

### T8: Distribuciones no normales

Los retornos reales tienen skewness negativa y kurtosis > 3. Alternativas:

- **t de Student:** colas gruesas con varianza finita. $\kappa = 6/(\nu-4)$.
- **Estable Paretiana:** varianza infinita para $\alpha < 2$; invalida el análisis media-varianza.
- **Mezcla de normales:** regímenes de calma/pánico producen colas gordas aunque cada régimen sea normal.
- **Jump-diffusion:** browniano + saltos de Poisson; explica el volatility smile de opciones.
- **Lognormal:** si log-retornos son normales, precios son lognormales. Base de Black-Scholes.

### T9: Diversificación de Markowitz

Dos tipos de riesgo en cartera: **idiosincrático** (diversificable) y **sistemático** (no diversificable). Con $n$ activos iguales y correlación $\rho$:

$$\sigma_P^2 = \frac{\sigma^2}{n} + \frac{n-1}{n}\rho\sigma^2 \xrightarrow{n\to\infty} \rho\sigma^2$$

La varianza de cartera en forma matricial: $\sigma_P^2 = \mathbf{w}^T\boldsymbol{\Sigma}\mathbf{w}$. La **frontera eficiente** es el conjunto de portfolios que maximizan retorno para cada nivel de riesgo. El **Sharpe ratio** mide retorno en exceso por unidad de riesgo:

$$S_P = \frac{E(r_P) - r_f}{\sigma_P}$$

El portfolio completo óptimo asigna fracción $y^* = (E(r_P) - r_f)/(\lambda\sigma_P^2)$ a activos de riesgo.

### T10: Más allá de media-varianza

Tres criterios alternativos cuando la distribución no es normal:

1. **Media Geométrica (GMR):** $r_g \approx \bar{r} - \frac{1}{2}\sigma^2$. Captura el efecto del compounding; penaliza la volatilidad automáticamente.
2. **Safety-First:** fijan retorno mínimo $r_L$ y/o probabilidad máxima de caer bajo él. Roy ($r_L = r_f$) produce el mismo portfolio que Sharpe ratio.
3. **Dominancia Estocástica (FSD/SSD/TSD):** compara CDFs completas sin asumir distribución; conceptualmente más general pero computacionalmente prohibitivo con muchos activos.

---

## Bloque 2 — Valoración I: Bonos, Acciones y Factores de Riesgo (T11-17)

### T11: Renta fija (Fixed Income)

**Precio de un bono** (cupón anual, yield constante $r$, vencimiento $T$):

$$P = \frac{\text{par}}{(1+r)^T} + \frac{\text{cupón}}{r}\left[1 - \frac{1}{(1+r)^T}\right]$$

- **YTM:** tasa $r$ que iguala precio de mercado con precio teórico.
- **Dirty price** = precio limpio + accrued interest.
- **Duration modificada $D^*$:** sensibilidad del precio al yield. Con corrección de convexidad:

$$\frac{\Delta P}{P} \approx -D^*\Delta y + \frac{\text{convexity}}{2}(\Delta y)^2$$

- Bonos callable tienen convexidad negativa (el emisor ejerce la call cuando tipos bajan → el precio tiene techo).
- **Credit spread** = yield corporativo − yield soberana. TED spread > 50 bp → señal de estrés.

Características relevantes: floating rate, indexed bonds, convertibles (a favor del inversor); callable, sinking fund, asset-backed (a favor del emisor).

### T12: Curvas de tipos

La **yield curve** (spot rates vs. plazos) resume las expectativas de mercado sobre tipos futuros. Factores clave: nivel, pendiente, curvatura (Litterman-Scheinkman). Construcción: **bootstrapping** iterativo de menor a mayor plazo.

Formas y señales: curva normal (crecimiento), invertida (recesión esperada), joroba (defensa de divisa). Cuatro teorías: expectations hypothesis, liquidity preference, segmentación de mercado, preferred habitat.

Modelos: **Vasicek** (proceso Ornstein-Uhlenbeck para la tasa corta), **Nelson-Siegel/Svensson** (factores de nivel, pendiente y curvatura).

### T13: Valoración de acciones (Equity Valuation)

**Modelos por descuento:**

- **DDM Gordon-Shapiro:** $V_0 = D_1/(k-g)$, donde $g = b \times \text{ROE}$ (fracción retenida × ROE).
- **FCFF:** $V_0^{firma} = \sum_t \text{FCFF}_t/(1+\text{WACC})^t$, con $\text{WACC} = w_e r_e + w_d r_d(1-\tau)$.
- **PVGO:** $P_0 = E_1/k + \text{PVGO}$. Si PVGO < 0, la empresa destruye valor reinvirtiendo.

**Múltiplos:** P/E, P/B, P/CF, P/S. Limitación: earnings gestionables, inútiles en pérdidas.

**Corrección de Jensen:** cuando $\hat{k}$ y $\hat{g}$ tienen incertidumbre, el precio justo incluye un término de segundo orden que depende de sus varianzas y covarianza.

### T14: CAPM

Bajo los supuestos estándar (muchos inversores price-takers, horizonte único, expectativas homogéneas, sin impuestos ni fricción), todos sostienen el portfolio de mercado M. La ecuación del CAPM:

$$E(r_i) - r_f = \beta_i[E(r_M) - r_f] \quad;\quad \beta_i = \frac{\text{Cov}(r_i, r_M)}{\sigma_M^2}$$

El **Single-Index Model** reduce inputs de $\frac{n(n+3)}{2}$ a $3n+3$ (para $n=50$: 1.325 → 153). La **SML** identifica activos infra/sobrevalorados según su alpha.

Limitaciones: un solo factor, beta histórico predice mal el futuro, portfolio de mercado teórico inobservable. Mejoras: betas ajustados (Blume/Vasicek), CAPM condicional (betas varían con el ciclo), ICAPM de Merton.

### T15: APT y modelos multifactor

**APT (Ross 1976):** sin arbitraje implica que el retorno esperado se explica solo por exposiciones a factores:

$$R_i \approx \beta_{i,1}F_1 + \ldots + \beta_{i,k}F_k$$

**Factores macro (Chen-Roll-Ross):** producción industrial, inflación esperada, sorpresa de inflación, credit spread corporativo, pendiente de la curva.

**Factores de estilo:** Fama-French 3F (mercado + SMB + HML), Carhart 4F (+momentum WML), Fama-French 5F (+RMW + CMA). Harvey-Liu-Zhu: solo son estadísticamente robustos mercado, HML, momentum, liquidez y volatilidad a corto plazo.

**Factores de liquidez:** Acharya-Pedersen (bid-ask spread como factor), Pastor-Stambaugh (volumen en dólares como proxy).

*(Temas 16 y 17 no disponibles en el PDF del curso.)*

---

## Bloque 3 — Valoración II: Derivados y Pricing de Opciones (T18-21)

### T18: Contratos derivados

Cuatro tipos fundamentales:

| Tipo | Obligación | Mercado | Uso principal |
|---|---|---|---|
| Forward | Ambas partes | OTC (bilateral) | Cobertura de FX/materias primas |
| Futuro | Ambas partes | Bolsa (estandarizado) | Cobertura con menor riesgo de contraparte |
| Opción | Solo el vendedor | Ambos | Cobertura + especulación; prima por la asimetría |
| Swap | Flujos recurrentes | OTC | Gestión de riesgo de tipos/divisas |

La diferencia estructural clave: forward/futuro obligan a ambas partes; la opción da flexibilidad unilateral al comprador a cambio de una prima.

### T19: Fórmula de Black-Scholes

Precio analítico de una call europea bajo lognormalidad, volatilidad y tasa constantes, sin dividendos:

$$C = S \cdot N(d_1) - K \cdot e^{-rT} \cdot N(d_2)$$

$$d_1 = \frac{\ln(S/K) + (r + \sigma^2/2)\,T}{\sigma\sqrt{T}}, \qquad d_2 = d_1 - \sigma\sqrt{T}$$

$N(d_2)$ = probabilidad de terminar in the money. $N(d_1)$ pondera además el tamaño del beneficio. En Python: `scipy.stats.norm.cdf()`.

Paridad put-call: $C - P = S - K e^{-rT}$ (permite valorar puts desde calls sin nueva derivación).

### T20-21: Monte Carlo y discretización de Euler

**Monte Carlo directo (T20):** simula el precio final del subyacente bajo GBM:

$$S_T = S_0 \cdot e^{(r - \sigma^2/2)T + \sigma\sqrt{T}\,Z}, \quad Z \sim N(0,1)$$

El precio de la call = $e^{-rT} \cdot \mathbb{E}[\max(S_T - K, 0)]$. Converge a Black-Scholes con suficientes iteraciones.

**Discretización de Euler (T21):** simula la trayectoria completa en pasos $\Delta t$:

$$S_t = S_{t-1} \cdot e^{(r - \sigma^2/2)\Delta t + \sigma\sqrt{\Delta t}\,Z_t}$$

Ventaja sobre la fórmula cerrada: funciona para opciones path-dependent (barrera, asiáticas, americanas) y cualquier proceso estocástico (varianza estocástica, saltos). Black-Scholes es exacto para opciones europeas simples; Euler es la herramienta general.

---

## Lo más importante para recordar

1. **Log-retornos son el lenguaje de trabajo.** Se suman en el tiempo, conectan con capitalización continua y son el input de todos los modelos del módulo.

2. **Los retornos no son normales.** Colas gordas y skewness negativa son universales. Las mezclas de normales y jump-diffusion son las explicaciones más convincentes. El modelo correcto depende del cuantil que importa.

3. **La diversificación elimina riesgo específico sin coste.** El riesgo sistemático persiste. El CAPM mide exactamente ese riesgo que no desaparece diversificando.

4. **CAPM es el punto de partida, no el final.** Un solo factor es insuficiente empíricamente. APT y modelos de estilo (Fama-French, Carhart) mejoran el ajuste; el coste es la interpretabilidad y el sobreajuste.

5. **Black-Scholes convierte distribución futura en precio presente.** La volatilidad $\sigma$ es el único input no observable: pequeñas diferencias en $\sigma$ generan grandes diferencias de precio. La volatilidad implícita del mercado es la métrica que realmente importa.

6. **Euler generaliza Black-Scholes a cualquier proceso.** Para opciones europeas, la fórmula cerrada es exacta y más eficiente. Euler es necesario cuando el payoff depende de la trayectoria o cuando el proceso es no-lognormal.

---

## Conexión entre bloques

| Concepto | Bloque origen | Aparece en |
|---|---|---|
| Volatilidad $\sigma$, log-retornos | T6-7 | Input #1 de Black-Scholes (T19) |
| Distribuciones no normales, fat tails | T8 | Limitaciones de B-S; EVT (M10) |
| Frontera eficiente, Sharpe ratio | T9 | CAPM como extensión (T14) |
| $\beta$, prima de riesgo | T14 | Factor de mercado en APT (T15); descuento en FCFF (T13) |
| Tasa libre de riesgo $r_f$ | T6 | CAPM, WACC, descuento en B-S |
| GBM, movimiento browniano | T7 | Base de B-S (T19) y Euler (T21) |
| VaR, ES | — | Módulo 9; la sensibilidad $\sigma$ viene de T6-T7 |
