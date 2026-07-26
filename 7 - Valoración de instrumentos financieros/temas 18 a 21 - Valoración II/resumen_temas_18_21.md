---
date: 2026-07-22
tags: [resumen, valoración, derivados, finanzas-cuantitativas, módulo-7]
---

# Módulo 7 — Temas 18 a 21: Valoración II — Derivados y Pricing de Opciones

## Para qué sirve este bloque

Los temas anteriores del módulo establecieron cómo medir el riesgo (temas 6-10) y cómo valorar activos bajo modelos de equilibrio como CAPM (temas 11-17). Este bloque da el siguiente paso: cómo valorar instrumentos cuyo precio no depende directamente de un activo, sino del derecho a comprarlo o venderlo en el futuro. Eso es un **derivado financiero**: un contrato cuyo valor se deriva del comportamiento de otro activo subyacente.

La pregunta central que responde este bloque es: ¿cuánto vale hoy la posibilidad de comprar una acción a un precio fijado dentro de un año? La respuesta requiere dos herramientas: la **fórmula de Black-Scholes** (solución analítica) y la **discretización de Euler con Monte Carlo** (solución numérica). Ambas producen el mismo resultado por caminos distintos, lo que refuerza la robustez del resultado.

---

## Tema 18: Introducción a los contratos derivados

### La idea central

Un derivado no tiene valor propio: su precio depende del comportamiento de un activo subyacente (una acción, un índice, un tipo de cambio). Surgieron como instrumentos de cobertura — para proteger posiciones ante movimientos adversos de precios — pero hoy los usan también especuladores y arbitrajistas.

### Los cuatro tipos principales

**Forward**: contrato privado entre dos partes para intercambiar un activo en una fecha futura a un precio pactado hoy. No cotiza en bolsa, no está estandarizado, y genera exposición de crédito bilateral (si una parte incumple, la otra sufre el daño). Se usa principalmente para cubrir riesgos de tipo de cambio o de materias primas.

**Futuro**: equivalente al forward pero estandarizado y negociado en mercados regulados. La estandarización reduce el riesgo de contraparte (la cámara de compensación actúa como intermediario), pero elimina flexibilidad. El comprador asume la obligación de adquirir el subyacente en la fecha de vencimiento; el vendedor, de entregarlo.

**Opción**: a diferencia del forward y el futuro, la opción da un **derecho, no una obligación**. Una *call* (opción de compra) da al titular el derecho a comprar el subyacente al precio de ejercicio (*strike price*) antes o en la fecha de vencimiento. Una *put* (opción de venta) da el derecho a venderlo. El vendedor de la opción sí tiene la obligación de cumplir si el comprador ejerce. Por asumir esa obligación, el vendedor cobra una prima.

**Swap**: acuerdo para intercambiar flujos de caja futuros según condiciones pactadas. El caso más común es el *interest rate swap*: una parte paga tipo fijo y recibe tipo variable. Se usan para gestionar exposición a tipos de interés, divisas, o para aprovechar ventajas comparativas en distintos mercados de deuda.

La diferencia estructural entre estos cuatro contratos no es trivial: forward y futuros obligan a ambas partes; opciones dan flexibilidad unilateral al comprador a cambio de una prima; swaps redistribuyen flujos recurrentes en lugar de un único intercambio.

---

## Tema 19: Valoración de opciones — Fórmula de Black-Scholes

### La idea central

Black, Scholes y Merton (1973) resolvieron el problema de cuánto vale hoy una opción europea (solo ejercible al vencimiento). Su fórmula da un precio analítico exacto bajo un conjunto de supuestos: mercados eficientes, sin costes de transacción, sin dividendos, volatilidad y tasa libre de riesgo conocidas y constantes, y precios del subyacente que siguen una distribución lognormal.

### La fórmula

El precio de una *call* europea es:

$$C = S \cdot N(d_1) - K \cdot e^{-rT} \cdot N(d_2)$$

donde:

$$d_1 = \frac{\ln(S/K) + (r + \sigma^2/2) \cdot T}{\sigma \sqrt{T}}, \qquad d_2 = d_1 - \sigma\sqrt{T}$$

Los símbolos son: $S$ = precio actual del subyacente, $K$ = precio de ejercicio (*strike*), $r$ = tasa libre de riesgo, $\sigma$ = volatilidad anualizada del subyacente, $T$ = tiempo hasta vencimiento en años, $N(\cdot)$ = función de distribución acumulada normal estándar.

**¿Qué calcula cada parte?** El término $S \cdot N(d_1)$ es el valor esperado de lo que recibes si ejerces la opción (el activo, ponderado por la probabilidad de que valga la pena ejercerla). El término $K \cdot e^{-rT} \cdot N(d_2)$ es el valor presente de lo que pagas al ejercerla. La diferencia es el valor neto de la opción hoy.

$N(d_1)$ y $N(d_2)$ son probabilidades, obtenidas con la función de distribución acumulada normal (en Python, `scipy.stats.norm.cdf()`). $N(d_2)$ es la probabilidad de que la opción termine *in the money* (precio de mercado > strike al vencimiento). $N(d_1)$ pondera adicionalmente el tamaño del beneficio.

### Implementación en Python

```python
import numpy as np
from scipy.stats import norm

def d1(S, K, r, stdev, T):
    return (np.log(S / K) + (r + stdev**2 / 2) * T) / (stdev * np.sqrt(T))

def d2(S, K, r, stdev, T):
    return (np.log(S / K) + (r - stdev**2 / 2) * T) / (stdev * np.sqrt(T))

def BSM(S, K, r, stdev, T):
    return S * norm.cdf(d1(S, K, r, stdev, T)) - K * np.exp(-r * T) * norm.cdf(d2(S, K, r, stdev, T))
```

Para Procter & Gamble en abril 2017: $S = 88.12$, $K = 110$, $r = 2.5\%$, $\sigma = 0.176$, $T = 1$ año → precio de la call ≈ **$1.13**.

La diferencia entre $d_1$ y $d_2$ en el código es que $d_1$ suma $\sigma^2/2$ y $d_2$ la resta. Esto corresponde al ajuste de Itô en el logaritmo del precio esperado.

---

## Tema 20: Monte Carlo con Black-Scholes

### La idea central

Antes de pasar a Euler, el material presenta Monte Carlo aplicado directamente al movimiento browniano geométrico que subyace a Black-Scholes. El objetivo es simular miles de trayectorias del precio del subyacente y estimar el precio de la opción como el promedio descontado de los payoffs simulados. Es conceptualmente más intuitivo que la fórmula cerrada, aunque computacionalmente más costoso.

El precio del subyacente evoluciona como movimiento browniano geométrico:

$$S_T = S_0 \cdot e^{(r - \frac{\sigma^2}{2})T + \sigma\sqrt{T} \cdot Z}$$

donde $Z \sim N(0,1)$ es un shock aleatorio. Se generan miles de valores de $Z$, se calcula $S_T$ para cada uno, y el precio de la call es:

$$C = e^{-rT} \cdot \mathbb{E}[\max(S_T - K, 0)]$$

El resultado converge al valor de Black-Scholes a medida que aumenta el número de simulaciones.

---

## Tema 21: Discretización de Euler con Monte Carlo

### La idea central

La fórmula cerrada de Black-Scholes funciona para opciones europeas simples. Para instrumentos más complejos (opciones americanas, opciones barrera, productos estructurados con condiciones path-dependent), no existe solución analítica. La **discretización de Euler** resuelve esto simulando la trayectoria completa del precio paso a paso, no solo el valor final.

### La fórmula de Euler

En lugar de simular directamente $S_T$, se aproxima la evolución del precio en pequeños intervalos de tiempo $\Delta t$:

$$S_t = S_{t-1} \cdot e^{(r - \frac{\sigma^2}{2})\Delta t + \sigma \sqrt{\Delta t} \cdot Z_t}$$

donde cada $Z_t \sim N(0,1)$ es independiente. Esto discretiza la ecuación diferencial estocástica de Black-Scholes en pasos diarios (o del tamaño que se elija).

### Implementación en Python

```python
T = 1.0
t_intervals = 250          # días de trading
delta_t = T / t_intervals
iterations = 10000         # simulaciones

Z = np.random.standard_normal((t_intervals + 1, iterations))
S = np.zeros_like(Z)
S[0] = S0                  # precio inicial

for t in range(1, t_intervals + 1):
    S[t] = S[t-1] * np.exp((r - 0.5 * stdev**2) * delta_t
                           + stdev * delta_t**0.5 * Z[t])

# Payoff y precio de la call
p = np.maximum(S[-1] - K, 0)
C = np.exp(-r * T) * np.sum(p) / iterations
```

Para los mismos parámetros de P&G: resultado ≈ **$1.16**, frente a $1.13 de Black-Scholes. La diferencia (~2.5%) es pequeña pero no nula: depende de la semilla aleatoria y del número de simulaciones. Con más iteraciones, converge.

### Por qué Euler es más potente

La diferencia no está en la precisión para opciones europeas simples (donde Black-Scholes es exacto), sino en la generalidad: Euler puede simular cualquier proceso estocástico, incluyendo varianza estocástica, saltos, o condiciones que dependen de toda la trayectoria del precio. Por eso se usa como base en modelos de riesgo avanzados.

---

## Lo más importante para recordar

1. **Un derivado vale por el derecho que otorga, no por el subyacente en sí.** Una call vale $\max(S_T - K, 0)$: solo tiene valor si el precio de mercado supera el strike. Este payoff asimétrico es la esencia de las opciones.

2. **Black-Scholes convierte la incertidumbre futura en un precio presente.** $N(d_1)$ y $N(d_2)$ son probabilidades que resumen toda la distribución de posibles precios futuros en dos números. La fórmula es exacta bajo sus supuestos, pero los supuestos (volatilidad constante, sin dividendos, mercados completos) son aproximaciones.

3. **Monte Carlo y Euler dan el mismo resultado que Black-Scholes para opciones europeas.** Que las tres rutas converjan al mismo número (~$1.13–1.16) es una validación, no una redundancia. En la práctica, se usa la solución analítica cuando existe y Euler cuando no.

4. **La discretización de Euler aproxima la EDE paso a paso.** Esto permite modelar cualquier proceso estocástico, no solo el lognormal. Es la base de los modelos de valoración de derivados exóticos y de la simulación de escenarios de riesgo.

5. **La volatilidad es el input más crítico de Black-Scholes.** El precio del subyacente y el strike son observables; la tasa libre de riesgo está dada por el mercado. La volatilidad ($\sigma$) hay que estimarla — históricamente o implícita del mercado — y pequeñas diferencias en $\sigma$ generan grandes diferencias en el precio de la opción.

---

## Conexión con el resto del módulo

| Concepto | Dónde aparece después |
|---|---|
| Movimiento browniano geométrico | Base de todos los modelos de simulación de precios en módulos posteriores |
| Volatilidad histórica (log-returns std) | Módulo 5 (modelos de volatilidad y correlación) |
| Monte Carlo | Módulo 2 (modelos de simulación); se retoma aquí aplicado a pricing |
| Tasa libre de riesgo como tasa de descuento | Temas 11-17 (CAPM y multifactor) usan el mismo concepto de descuento a tasa $r$ |
| Cobertura (hedging) con derivados | Módulo 8 (gestión de carteras) — el delta de una opción da el ratio de cobertura óptimo |
| Gestión del riesgo de opciones | Módulo 9 (gestión de riesgos financieros) — Greeks (delta, gamma, vega) |
