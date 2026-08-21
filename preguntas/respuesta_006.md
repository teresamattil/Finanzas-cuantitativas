---
date: 2026-07-26
tags: [Markowitz, transaction-costs, rebalanceo, Black-Litterman, módulo-7, módulo-8]
---

# ¿Qué son los transaction costs en Markowitz? ¿Por qué importan?

## Qué son

Los costes de ejecutar las operaciones necesarias para construir o rebalancear el portfolio óptimo: comisiones de intermediación, bid-ask spread, e impacto en precio para órdenes grandes.

## Por qué importan

La frontera eficiente de Markowitz asume mercados perfectos — sin fricciones, sin costes. En la práctica, el optimizador produce pesos muy específicos (p.ej. 3.7% en un activo, 12.3% en otro). Rebalancear a esos pesos exactos cada periodo genera costes que erosionan el retorno esperado. El problema se agrava por dos razones:

1. **Inestabilidad de la optimización:** pequeños cambios en los inputs (retornos esperados, covarianzas) producen carteras radicalmente distintas, forzando rebalanceos frecuentes y costosos.
2. **Pesos extremos:** con muchos activos, la optimización tiende a concentrar posiciones o generar posiciones cortas — órdenes de gran tamaño con alto impacto en precio.

## So-what para el examen

Los transaction costs son uno de los argumentos empíricos centrales contra la implementación directa de Markowitz, y una de las motivaciones de los modelos que vienen después:

- **Black-Litterman** ancla en el portfolio de mercado y reduce el turnover necesario → menos costes de rebalanceo.
- **Risk Parity** produce pesos más estables en el tiempo → rebalanceos menos frecuentes.
- En implementaciones prácticas se añade un término de penalización al optimizador que desincentiva alejarse demasiado de la cartera actual: $\max \; E(r_P) - \frac{\lambda}{2}\sigma_P^2 - c \cdot \|\mathbf{w} - \mathbf{w}_0\|$, donde $c$ es el coste por unidad de cambio en pesos y $\mathbf{w}_0$ la cartera actual.
