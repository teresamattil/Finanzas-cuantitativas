---
date: 2026-07-27
tags: [bonos, YTM, yield, renta-fija, valoración, módulo-7]
---

# ¿Qué es el YTM (Yield to Maturity)?

## Definición

El **YTM** es la tasa interna de retorno de un bono: el tipo de descuento $y$ que iguala el precio de mercado del bono con el valor presente de todos sus flujos futuros (cupones + principal).

$$P = \sum_{t=1}^{T} \frac{C_t}{(1+y)^t} + \frac{F}{(1+y)^T}$$

donde $P$ es el precio de mercado, $C_t$ el cupón del periodo $t$, $F$ el valor nominal (face value), y $T$ el vencimiento.

No tiene solución analítica cerrada — se obtiene numéricamente (bisección, Newton-Raphson).

## Qué representa

El YTM es el retorno anualizado que obtiene el inversor **si**:
- Mantiene el bono hasta vencimiento
- Reinvierte todos los cupones exactamente al mismo tipo $y$

Ambas condiciones rara vez se cumplen en la práctica, por lo que el YTM es una medida de rendimiento *esperado bajo supuestos*, no una promesa.

## Relación precio-YTM

| Situación | Precio vs Nominal | YTM vs Cupón |
|---|---|---|
| Bono a la par | $P = F$ | $y = c$ |
| Bono con descuento | $P < F$ | $y > c$ |
| Bono con prima | $P > F$ | $y < c$ |

La relación es inversa: si el precio sube, el YTM baja, y viceversa. Es la misma mecánica que explica la duración.

## YTM vs otras métricas de yield

- **Current yield:** $C/P$ — solo mide el cupón sobre el precio, ignora las ganancias/pérdidas de capital al vencimiento.
- **Yield to call (YTC):** como el YTM pero hasta la fecha de amortización anticipada, relevante en bonos callable.
- **Spot rate:** tipo de descuento para un flujo único en $t$, sin asumir reinversión. La curva de spot rates es más precisa que el YTM para valorar bonos con estructura de flujos compleja.

## Relación con la duración

El YTM entra directamente en el cálculo de la duración de Macaulay (ver [[respuesta_007]]): un YTM más alto reduce la duración porque descuenta más los flujos lejanos, dándoles menos peso relativo.

## So-what para el examen

- El YTM es el tipo de descuento implícito en el precio de mercado: si sabes el precio, tienes el YTM; si sabes el YTM, tienes el precio.
- En la curva de tipos, cada vencimiento tiene su YTM — eso es la curva de rendimientos (yield curve). Una curva invertida (YTM corto > YTM largo) históricamente anticipa recesión.
- Para comparar bonos con estructuras distintas, el YTM normaliza en una sola cifra, pero hay que tener presente el supuesto de reinversión — en entornos de tipos cambiantes, el YTM sobrestima o subestima el retorno real.
