---
date: 2026-07-26
tags: [utilidad, media-varianza, Markowitz, aversión-al-riesgo, módulo-7]
---

# ¿Qué es la utilidad media-varianza (mean-variance utility)?

## Dónde aparece

M7 — Bloque 1, Tema 7 (Riesgo vs. Retorno). Es el supuesto de fondo de toda la teoría de Markowitz y del CAPM.

## La función

$$U = E(r) - \frac{\lambda}{2}\sigma^2$$

El inversor maximiza $U$: quiere más retorno esperado $E(r)$ y menos varianza $\sigma^2$. El parámetro $\lambda$ es el **coeficiente de aversión al riesgo** — en la práctica $\lambda \in [2, 4]$. A mayor $\lambda$, más penaliza la varianza relativa al retorno.

## Por qué importa

Es el supuesto de fondo de toda la teoría de Markowitz. La frontera eficiente y el portfolio óptimo se derivan exactamente de que los inversores maximizan esta función. También justifica el CAPM: si todos los inversores tienen utilidad media-varianza y expectativas homogéneas, todos acaban en el mismo portfolio de mercado.

## So-what para el examen

Si te preguntan por qué Markowitz asume normalidad: la utilidad media-varianza solo describe completamente las preferencias del inversor cuando la distribución está caracterizada por media y varianza, lo que solo ocurre bajo normalidad (o preferencias cuadráticas). Si los retornos tienen fat tails, $U$ ignora skewness y kurtosis — el portfolio "óptimo" puede ser subóptimo en la práctica. Esa es la motivación de los criterios alternativos del T10 (GMR, safety-first, dominancia estocástica).
