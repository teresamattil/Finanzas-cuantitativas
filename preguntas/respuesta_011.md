---
date: 2026-07-30
tags: [MPT, Markowitz, Roy, Tobin, gestión de carteras, M7, M8]
---

# MPT — Modern Portfolio Theory (Markowitz / Roy)

## Idea central

No optimices activos individualmente: optimiza la **cartera**. Lo que importa no es el riesgo de cada activo sino su contribución al riesgo total, que depende de las correlaciones.

## El modelo y sus parámetros

### Inputs

Con `n` activos, el modelo necesita:

| Parámetro | Qué es | Cantidad |
|-----------|--------|----------|
| `μᵢ` | Retorno esperado de cada activo | n |
| `σᵢ²` | Varianza de cada activo | n |
| `σᵢⱼ` | Covarianza entre cada par | n(n−1)/2 |

Todo se resume en dos objetos: el vector de retornos **μ** (n×1) y la matriz de covarianzas **Σ** (n×n).

El problema de optimización:

$$\min_w \; w^\top \Sigma w \quad \text{s.t.} \quad w^\top \mu = \mu^* \;,\; \mathbf{1}^\top w = 1$$

Donde `w` es el vector de pesos y `μ*` es el retorno objetivo.

### El coste de escalar

Con 50 activos necesitas 50 retornos + 50 varianzas + 1.225 covarianzas = **1.325 parámetros**. El número de covarianzas crece como n²/2, lo que hace la estimación muy sensible al ruido muestral. Ese es el problema práctico de Markowitz: la matriz Σ estimada es inestable → los pesos óptimos se vuelven extremos y poco robustos.

## Los tres bloques

### 1. Markowitz (1952) — frontera eficiente

Para cada nivel de retorno esperado, existe la cartera de mínima varianza. El conjunto de esas carteras es la **frontera eficiente**.

El resultado clave: la diversificación reduce el riesgo **solo si las correlaciones son < 1**. La reducción de riesgo viene exactamente de los términos de covarianza cruzada en `w'Σw`.

### 2. Roy (1952) — Safety First

Contemporáneo de Markowitz, enfoque distinto. En vez de maximizar utilidad media-varianza, el inversor maximiza la probabilidad de no caer por debajo de un umbral de ruina (disaster level `d`):

$$\max \frac{\mu_p - d}{\sigma_p}$$

Esto es equivalente a maximizar el **ratio de Sharpe** con `d` = tipo libre de riesgo. La conexión no es obvia pero es directa: Sharpe y Roy llegan al mismo portfolio óptimo.

### 3. Tobin (1958) — Separación

Añade un activo sin riesgo (rf). Resultado: el problema se separa en dos decisiones independientes:

1. **Cuánto riesgo tomar** (mix entre rf y la cartera arriesgada)
2. **Qué cartera arriesgada** elegir → siempre la misma para todos: la **tangency portfolio**

La línea que va de rf hasta la tangency portfolio y más allá es la **Capital Market Line (CML)**. Todos los inversores están en esa línea; solo difieren en dónde.

## Diagrama conceptual

```
E[r]
 |                          / CML
 |                    [T] /        ← tangency portfolio
 |               /       
 |          [frontera eficiente]
 |      /
[rf]
 |_________________________________ σ
```

## El modelo de un factor: qué significa cada término

$$r_i = E(r_i) + \beta_i \cdot m + n_i$$

| Término | Qué es |
|---------|--------|
| `E(rᵢ)` | Retorno esperado — lo que ya descontabas |
| `m = rₘ − E(rₘ)` | **Sorpresa del mercado**: desviación del mercado respecto a lo esperado |
| `βᵢ · m` | Tu exposición a esa sorpresa, escalada por beta |
| `nᵢ` | Sorpresa idiosincrática del activo (ruido propio, media cero) |

`m` no es el retorno del mercado sino su parte inesperada. Si el mercado sube 10% pero se esperaba 7%, `m = +3%`. Un activo con β = 1.5 recibe un impacto de +4.5% solo por esa sorpresa.

## Descomposición de la varianza: sistemática vs. idiosincrática

En el modelo de un factor (CAPM), la varianza total de un activo se parte en dos:

$$\sigma^2_i = \beta^2_i \cdot \sigma^2_m + \sigma^2_\varepsilon$$

| Componente | Nombre | Diversificable |
|-----------|--------|---------------|
| `β²·σ²_m` | Varianza sistemática (mercado) | No — es riesgo compartido con el mercado |
| `σ²_ε` | Varianza idiosincrática | Sí — se cancela al combinar activos |

**Ejemplo:** β = 1.1, σ²_ε = 0.15, σ²_m = 0.1

$$\sigma^2_i = (1.1)^2 \times 0.1 + 0.15 = 0.121 + 0.15 = 0.271$$

En una cartera bien diversificada, σ²_ε → 0. Solo queda la parte sistemática, por eso el CAPM solo remunera beta.

## So-what para el examen

Los tres autores resuelven el mismo problema con ángulos distintos: Markowitz da la frontera, Roy justifica por qué el Sharpe ratio es la métrica correcta, Tobin dice que con un activo sin riesgo todos eligen la misma cartera arriesgada. Si el examen pregunta por MPT, el hilo es: correlaciones → frontera eficiente → tangency portfolio → CML.
