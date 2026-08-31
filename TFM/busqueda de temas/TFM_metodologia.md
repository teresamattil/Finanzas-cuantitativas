Roadmap por pasos (grupo de control: ETFs)

Para que cada paso refuerce lo anterior y puedas verificar que entiendes cada pieza antes de avanzar:

Universo + datos — definir los ETFs sectoriales, descargar precios, verificar calidad (huecos, fechas de inicio, splits/dividendos). (Empezamos aquí)
Señal momentum — calcular retorno acumulado 12-1 meses por ETF, ver cómo varía el ranking en el tiempo.
Construcción de cartera — pasar de "ranking" a "pesos de cartera" (long-only vs. long-short, equal-weight), sin costes todavía.
Backtest frictionless — motor que convierte pesos + retornos en una serie temporal de retorno de estrategia (esto es tu WML).
Métricas de performance — Sharpe, Sortino, max drawdown, skew/kurtosis sobre esa serie.
Volatility scaling — implementar la fórmula de Barroso & Santa-Clara sobre tu propia serie WML.
Comparación pura vs. escalada — ¿tu pipeline reproduce el efecto que reporta el paper? Este es el checkpoint de sanidad que justifica todo el diseño.
Costes de transacción — meter spread/comisión realistas (en ETFs es sencillo comparado con cripto).
Robustez — distintas ventanas de formación y frecuencias de rebalanceo, sub-periodos.