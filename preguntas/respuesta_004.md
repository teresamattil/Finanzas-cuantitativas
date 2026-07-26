---
date: 2026-07-25
tags: [VaR, horizonte temporal, escalado, raíz cuadrada, i.i.d., examen]
---

# Intuición detrás de escalar el VaR con √n

## Por qué no es simplemente ×n

Si el riesgo fuera el mismo cada día y los días fueran independientes, perder 1% diario durante 10 días daría -10%. Pero el VaR no es una pérdida fija — es una medida de dispersión. Y la dispersión de una suma de variables aleatorias no crece linealmente, crece con la raíz cuadrada del número de términos.

## La intuición estadística

Si cada retorno diario tiene desviación típica σ, y los días son independientes entre sí, la desviación típica acumulada en n días es:

$$\sigma_n = \sigma \times \sqrt{n}$$

Esto viene de que la **varianza sí es aditiva**: Var_n = n · σ², y al sacar la raíz cuadrada aparece √n.

El VaR paramétrico es Z_α × σ, así que escala igual que σ: multiplicando por √n.

## La analogía física

Es la misma lógica que el movimiento browniano: una partícula que da pasos aleatorios no se aleja linealmente en el tiempo — se aleja proporcionalmente a √t. Si hoy puede ir 1 metro, en 100 pasos esperamos que esté a 10 metros del origen, no a 100. Los pasos en direcciones opuestas se cancelan parcialmente.

## Por qué es un supuesto fuerte

La regla √n asume retornos **i.i.d.** — independientes entre sí y con la misma distribución cada día. Eso falla en la práctica:
- Si hay un crash hoy, mañana la volatilidad es mayor (GARCH — los días no son independientes)
- En periodos de estrés, los retornos extremos se encadenan

Por eso Basilea exige el VaR a 10 días pero permite calcularlo como VaR diario × √10 solo como **aproximación regulatoria** — no como verdad estadística.
