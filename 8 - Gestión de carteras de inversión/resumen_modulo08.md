---
date: 2026-07-22
tags: [resumen, gestión-carteras, derivados, volatilidad, módulo-8]
---

# Módulo 8 — Temas 22 a 24: Gestión de Carteras de Inversión

## Para qué sirve este bloque

El módulo 7 terminó con cómo valorar una opción: Black-Scholes y Euler dan su precio teórico. Este bloque responde las preguntas que siguen: ¿cómo gestionas el riesgo de una posición en opciones una vez que la has vendido? (T22), ¿cómo funciona la volatilidad en los mercados reales, donde el supuesto de BSM claramente falla? (T23), y ¿cómo construyes y gestionas activamente un portfolio buscando rentabilidad por encima del benchmark? (T24).

Los tres temas son independientes en su técnica pero comparten un eje común: la distancia entre los modelos teóricos y cómo operan los mercados de verdad.

### Recall: definición Opción
Una opción es un contrato que te da el **derecho** (pero no la obligación) de comprar o vender un activo a un precio fijado de antemano, en una fecha futura.

Por ejemplo: hoy una acción de Repsol vale 15€. Compras una opción que te da derecho a comprarla a 15€ dentro de tres meses. Si dentro de tres meses la acción vale 20€, ejerces la opción — la compras a 15€ y ganas 5€. Si vale 12€, no la ejerces y pierdes solo lo que pagaste por la opción.

Hay dos tipos básicos:
- **Call:** derecho a comprar.
- **Put:** derecho a vender.

Y quien vende la opción (la institución financiera del Tema 22) asume la obligación contraria: tiene que venderte la acción a 15€ aunque valga 20€. Por eso necesita cubrir ese riesgo — ahí es donde entran las griegas.

---

## Tema 22: Dynamic Hedging — Cobertura con Opciones

### La idea central

Cuando una institución financiera vende una opción a un cliente que no corresponde a ningún contrato estandarizado en bolsa, no puede cubrirse comprando exactamente la misma opción en el mercado. Tiene que cubrirse de forma **dinámica**: reajustando continuamente una posición en el activo subyacente para neutralizar el riesgo de la opción. El marco teórico para hacer esto son las **griegas** — un conjunto de sensibilidades que miden cómo cambia el valor de la opción ante cambios en distintos factores de mercado.


### EJEMPLO:

Piénsalo así: si vendes una opción call a alguien (le das el derecho a comprarte Repsol a 15€), y la acción sube a 25€, tienes que venderle la acción a 15€ aunque te cueste 25€ en el mercado. Pierdes 10€ por acción.

Para no estar expuesto a esa pérdida, la institución financiera **compra acciones de Repsol mientras espera**. Si tiene las acciones, cuando el cliente ejerza la opción simplemente se las entrega — no tiene que salir a comprarlas al precio alto.

El problema es que no sabe si el cliente va a ejercer o no. Si compra todas las acciones desde el principio y el precio baja a 10€, ha perdido dinero en las acciones sin necesidad. Y si no compra nada y el precio sube mucho, pierde al tener que comprarlas caras al final.

La cobertura dinámica resuelve esto comprando **una fracción** de las acciones — no todas, no ninguna. Esa fracción es exactamente la **delta**: si delta es 0.6, compras 0.6 acciones por cada opción vendida. Si el precio sube y la probabilidad de que el cliente ejerza aumenta, delta sube a 0.8 y compras más. Si el precio baja y es menos probable que se ejerza, delta baja y vendes parte.

Vas ajustando esa posición continuamente según cómo evoluciona el precio — de ahí lo de "dinámica". El objetivo es que en cualquier momento, las ganancias o pérdidas en las acciones que tienes compradas compensen exactamente las pérdidas o ganancias en la opción que vendiste.

### Las griegas

Cada griega mide una dimensión diferente del riesgo de una posición en opciones. El objetivo del gestor es mantenerlas dentro de rangos aceptables.

**Delta** ($\Delta$): sensibilidad del precio de la opción respecto al precio del subyacente. Una delta de 0.6 significa que si el subyacente sube 1€, la opción sube 0.6€. Cubrir el delta — mantenerlo en cero — es la cobertura básica. Para ello, el emisor de la call compra $\Delta$ acciones por cada opción vendida. Como delta cambia constantemente con el precio del subyacente, la cobertura requiere reajustes continuos.

**Gamma** ($\Gamma$): sensibilidad del delta respecto al precio del subyacente. Mide cuánto cambia la cobertura necesaria cuando se mueve el mercado. Una posición con gamma alta es más difícil de cubrir porque el delta se desplaza rápidamente y hay que reajustar con más frecuencia.

**Vega**: sensibilidad del precio de la opción respecto a la volatilidad implícita. Cubrir el vega requiere comprar otras opciones, no solo el subyacente. Una posición vendida en opciones tiene vega negativa: pierde valor si la volatilidad sube.

**Theta** ($\Theta$): decaimiento del valor de la opción con el paso del tiempo. Una posición corta en opciones tiene theta positivo (el tiempo juega a favor del emisor).

**Rho** ($\rho$): sensibilidad respecto al tipo de interés libre de riesgo. En general es la griega menos relevante para horizontes cortos.

### Posición descubierta vs. posición cubierta

Una **posición descubierta** (*naked*) significa no hacer nada: si la opción expira out-of-the-money, el emisor se queda la prima. Si expira in-the-money, asume la pérdida total. Una **posición cubierta** estática consiste en comprar desde el inicio el subyacente para poder entregarlo si es necesario, pero esto sobre-cubre cuando la opción no se ejerce. La cobertura dinámica con delta es el término medio: cubre el riesgo de forma continua al coste de las comisiones de reajuste.

---

## Tema 23: Trading de Volatilidad — La Sonrisa de Volatilidad

### La idea central

Black-Scholes asume que la volatilidad es constante y que los precios del subyacente siguen una distribución lognormal. Ninguna de las dos cosas se cumple en los mercados reales. Los operadores lo saben y lo ajustan: usan una volatilidad diferente para cada opción según su precio de ejercicio y su vencimiento. La representación gráfica de esta volatilidad implícita en función del precio de ejercicio se llama **sonrisa de volatilidad**.

### Opciones sobre divisas: la sonrisa simétrica

Para opciones sobre tipos de cambio, la volatilidad implícita es más alta en opciones muy dentro o muy fuera del dinero (*deep ITM/OTM*) y más baja para opciones *at-the-money*. El resultado es una curva en forma de U — la sonrisa.

Esto refleja que la distribución real de los tipos de cambio tiene **colas más pesadas** que la lognormal (mayor kurtosis): los movimientos extremos son más frecuentes de lo que el modelo predice. Los datos lo confirman: los tipos de cambio superan 3 desviaciones estándar diarias el 1.34% de los días; el modelo lognormal predice solo el 0.27%.

Las causas son dos: la volatilidad no es constante (varía a lo largo del tiempo) y los tipos de cambio sufren saltos discretos en respuesta a noticias o intervenciones de bancos centrales.

### Opciones sobre acciones: el sesgo de volatilidad

Para acciones e índices, la curva no es simétrica: la volatilidad implícita decrece a medida que aumenta el precio de ejercicio. Las opciones de venta *out-of-the-money* (puts baratas que se disparan en un crash) tienen volatilidad implícita muy alta; las calls *out-of-the-money* tienen volatilidad baja. Esto se llama **sesgo de volatilidad** (*volatility skew*), no sonrisa.

Este patrón no existía antes del crash de octubre de 1987. La explicación más directa es el **apalancamiento**: cuando el precio de una acción cae, el ratio deuda/capital sube y la acción se vuelve más arriesgada, lo que aumenta su volatilidad. Otra explicación es la **fobia a los crash**: los operadores asignan una probabilidad subjetiva mayor a desplomes extremos que la que implica la lognormal, y valoran las puts protectoras en consecuencia.

### Superficie de volatilidad

Cuando se combinan la sonrisa (variación por strike) con la **estructura de plazos de la volatilidad** (variación por vencimiento), se obtiene una **superficie de volatilidad**: una función bidimensional que da la volatilidad implícita apropiada para cualquier combinación de precio de ejercicio y plazo. Los operadores usan esta superficie como input real en la fórmula de BSM, reemplazando el supuesto de volatilidad constante por una que se ajusta al mercado.

La volatilidad implícita tiende a ser creciente con el plazo cuando las volatilidades de corto plazo están históricamente bajas (el mercado espera una reversión al alza), y decreciente cuando están altas. La sonrisa se aplana a medida que aumenta el vencimiento.

---

## Tema 24: Active Portfolio Management — Gestión Activa de Carteras

### La idea central

Un gestor **pasivo** replica un índice. Un gestor **activo** toma posiciones que se desvían del índice apostando a que sus señales de información generan rentabilidad adicional (**alpha**). El tema cubre tres marcos para construir portfolios activos y una forma de medir si la gestión activa añade valor.

### Treynor-Black (bottom-up)

El enfoque de Treynor-Black construye el portfolio activo desde los activos individuales hacia arriba. El analista genera señales de alpha para un subconjunto de activos (los que cree que están mal valorados). El modelo combina esas señales con el portfolio de mercado de forma óptima: pondera cada activo en el portfolio activo según su ratio alpha/riesgo idiosincrático ($\alpha_i / \sigma^2(\epsilon_i)$). El peso del portfolio activo respecto al de mercado depende de cuánto alpha total se espera y de cuánto riesgo no sistemático introduce.

Es un enfoque bottom-up porque parte de valoraciones individuales de activos y agrega hacia el portfolio.

### Black-Litterman (top-down, bayesiano)

Black-Litterman parte desde arriba: el **punto de partida son los pesos de mercado** (equilibrio CAPM), que implican un vector de rentabilidades esperadas. El gestor añade sus propias **views** — creencias sobre rentabilidades absolutas o relativas de activos o sectores — con un nivel de confianza asignado a cada una.

El modelo combina ambas fuentes mediante el **teorema de Bayes**: la distribución posterior de rentabilidades mezcla las rentabilidades de equilibrio (prior) con las views del gestor (likelihood), ponderadas por la confianza en cada una. Los pesos óptimos resultan de minimizar la varianza del portfolio sujeto a maximizar la rentabilidad esperada posterior.

La ventaja respecto a la optimización media-varianza clásica es la estabilidad: los pesos no dependen exclusivamente de las rentabilidades esperadas del analista (que tienen mucho error de estimación), sino de una combinación disciplinada con el equilibrio de mercado.

### Risk Parity

El portfolio de **riesgo paritario** asigna pesos de forma que cada activo o clase de activo **contribuya igual al riesgo total** del portfolio, en lugar de igualar los pesos de capital (1/N) o maximizar el Sharpe.

Para volatilidad como medida de riesgo, los pesos de riesgo paritario son proporcionales a la inversa de la volatilidad de cada activo (o, de forma más exacta, a la inversa de la suma de la fila correspondiente de la matriz de covarianzas). En la práctica, esto sobrepondera activos de bajo riesgo (bonos) e infrapondera activos de alto riesgo (acciones). Para alcanzar el nivel de rentabilidad de un portfolio tradicional 60/40, los fondos de risk parity suelen apalancar la parte de bonos.

La evidencia (PanAgora, Bridgewater) sugiere que outperforma para medidas de riesgo coherentes. El riesgo principal es el de estimación: si la volatilidad de un activo está subestimada, el portfolio le asigna más peso del que debería.

### Valoración de la gestión activa

El valor de la gestión activa se resume en el **ratio de información** (IR): alpha generado dividido entre el tracking error respecto al benchmark. La **ley fundamental de la gestión activa** establece que:

$$IR = IC \cdot \sqrt{BR}$$

donde $IC$ (*information coefficient*) es la correlación entre las señales del gestor y los retornos reales, y $BR$ (*breadth*) es el número de apuestas independientes al año. Un gestor con $IC$ modesto pero que opera con muchas apuestas independientes (diversificación de alpha) puede tener un IR alto. La implicación práctica: más diversificación de señales mejora el IR, incluso con habilidad moderada.

---

## Lo más importante para recordar

1. **Delta hedging es dinámico por definición.** La delta de una opción cambia continuamente con el precio del subyacente, por lo que la cobertura hay que reajustarla en cada periodo. El coste de ese reajuste es lo que el emisor "paga" por cubrir su exposición.

2. **La sonrisa de volatilidad demuestra que BSM es un modelo incompleto, no uno equivocado.** Los operadores lo usan como herramienta de interpolación: asignan la volatilidad implícita correcta para cada strike y vencimiento leyéndola de la superficie, y aplican la fórmula. El modelo sigue siendo útil como lenguaje común del mercado.

3. **El sesgo de volatilidad en acciones no existía antes de 1987.** Es un artefacto del crash: el mercado aprendió que los desplomes extremos son más probables de lo que implica la lognormal y desde entonces incorpora esa prima en las puts baratas.

4. **Black-Litterman resuelve el problema de inestabilidad de la optimización media-varianza.** Las pequeñas variaciones en las rentabilidades esperadas de entrada producen pesos óptimos radicalmente distintos. BL estabiliza el proceso anclando los pesos al equilibrio de mercado y dejando que las views del gestor los ajusten suavemente.

5. **Risk parity no es igual a mínima varianza.** Mínima varianza minimiza la volatilidad total; risk parity equilibra las contribuciones al riesgo. Son diferentes en composición y en objetivo.

6. **La ley fundamental de la gestión activa: el IR crece con la raíz del número de apuestas.** Diversificar señales (más activos, más estrategias) mejora el IR incluso sin mejorar la habilidad de cada señal individual.

---

## Conexión con el resto del módulo

| Concepto | Dónde aparece |
|---|---|
| Delta y cobertura dinámica | Directamente en las prácticas de derivados (M7 T21); base del risk management de opciones en M9 |
| Volatilidad implícita y superficie | Módulo 5 (modelos de volatilidad tipo GARCH); el tema 23 es su aplicación en pricing |
| Black-Litterman (Bayes) | Práctica 2 del módulo 8 |
| Risk parity | Práctica 3 del módulo 8 |
| Treynor-Black | Práctica 1 del módulo 8 |
| Information Ratio | Módulo 9 (gestión de riesgos) — la misma métrica se usa para evaluar estrategias de cobertura |
