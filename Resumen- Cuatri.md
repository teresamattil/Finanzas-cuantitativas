# Mapa de los Módulos 7-10: Finanzas Cuantitativas

---

## La pregunta que responden los cuatro módulos

> *¿Cuánto vale algo que depende del futuro, y cuánto puedo perder si me equivoco?*

Hay una tensión que recorre los cuatro módulos y que nunca se dice explícitamente:

> **Los modelos asumen normalidad. Los mercados no son normales. Todo lo demás es gestionar esa contradicción.**

- M7 construye los modelos asumiendo normalidad (o lognormalidad)
- M8 muestra que el mercado *sabe* que eso falla y lo corrige con la sonrisa de volatilidad
- M9 mide el riesgo con esos modelos imperfectos
- M10 dice "olvidemos la normalidad en las colas y modelémoslas directamente"

Es la misma historia contada cuatro veces, cada vez con más honestidad sobre lo que los modelos no pueden hacer.

---

## Módulo 7 — ¿Cómo valoro activos financieros?

**La clave que conecta todo:** el valor presente. Todo activo financiero vale lo que te va a dar en el futuro, descontado al hoy. La diferencia entre bono, acción y opción es solo cuán incierto es ese flujo futuro y quién asume esa incertidumbre.

**Bloque 1 — Conceptos base**

Antes de valorar nada, hay que medir. El módulo construye el lenguaje: retornos, riesgo, distribuciones y diversificación (Markowitz). Los retornos no son normales en la realidad — tienen colas gordas y skewness negativa — pero los modelos que vienen después asumen normalidad de todas formas. Esa tensión recorre todo lo que sigue.

**Bloque 2 — Valoración de bonos y acciones**

Todo activo vale el descuento de sus flujos futuros. La diferencia es cuán predecibles son esos flujos: un bono tiene cupones fijos (fácil), una acción tiene dividendos inciertos (más difícil). Los **factores de riesgo** (CAPM, APT, Fama-French) no son una tercera categoría de valoración: son la respuesta a *"¿qué tasa de descuento uso?"*. Son la fontanería del denominador.

**Bloque 3 — Valoración de opciones y derivados**

Una opción es el instrumento donde la incertidumbre es más extrema: el comprador tiene el derecho pero no la obligación, así que el valor depende de toda la distribución futura del precio. Black-Scholes convierte esa distribución futura en un precio presente. El único input no observable es la volatilidad — pequeñas diferencias en ella generan grandes diferencias de precio.

---

## Módulo 8 — ¿Cómo gestiono el riesgo de tener opciones en cartera?

El módulo tiene tres temas que comparten un eje: la distancia entre los modelos teóricos y cómo operan los mercados de verdad.

**Dynamic Hedging — gestionar el riesgo de haber vendido una opción**

Cuando vendes una opción, asumes la obligación contraria a quien la compra. Si vendiste una call de Repsol a 15€ y el precio sube a 25€, tienes que venderla a 15€ aunque en el mercado cueste 25€. Para cubrirte, compras acciones de Repsol directamente: si el precio sube, ganas en las acciones lo que pierdes en la opción.

El problema es que no sabes si van a ejercer la opción o no, así que no compras todas las acciones — compras una fracción. Esa fracción es la **delta**. Si la probabilidad de que ejerzan es del 60%, compras 0.6 acciones por cada opción vendida. Esa fracción cambia cada día según cómo evoluciona el precio, por eso hay que reajustar continuamente. El coste de esos reajustes es el coste real de la cobertura. Las demás griegas (gamma, vega, theta) miden otras dimensiones del mismo riesgo: cuánto cambia la delta, cuánto afecta la volatilidad, cuánto afecta el paso del tiempo.

**La sonrisa de volatilidad — Black-Scholes falla, y el mercado lo sabe**

Black-Scholes asume volatilidad constante. No es verdad. Los traders lo saben y han desarrollado un *hack*: usan Black-Scholes igualmente, pero en vez de meterle una volatilidad fija le meten una volatilidad diferente para cada opción según su precio de ejercicio y su vencimiento. La "sonrisa" es el mapa de qué volatilidad usar en cada caso. Black-Scholes pasa de ser un modelo a ser una **calculadora con parámetros ajustables**.

En acciones e índices la curva no es simétrica sino sesgada: las puts baratas (protección contra crash) tienen volatilidad implícita muy alta. Este sesgo no existía antes de 1987 — el mercado aprendió que los desplomes extremos son más probables de lo que implica el modelo y desde entonces incorpora esa prima.

**Gestión activa de carteras — tres filosofías para desviarte del índice**

Un gestor pasivo replica un índice. Un gestor activo toma posiciones que se desvían apostando a que sus señales generan rentabilidad adicional (alpha). Hay tres respuestas distintas a cómo hacerlo:

- **Treynor-Black**: tienes ideas sobre acciones concretas infravaloradas → construyes el portfolio desde abajo, ponderando cada apuesta por su ratio alpha/riesgo
- **Black-Litterman**: tienes ideas sobre sectores o mercados → partes de los pesos del índice (equilibrio CAPM) y los ajustas con tus creencias usando Bayes. Más estable que la optimización clásica porque ancla en el mercado
- **Risk Parity**: en vez de igualar dinero invertido, igualas riesgo aportado por cada activo. Sobrepondera activos de bajo riesgo (bonos) e infrapondera los de alto riesgo (acciones); en la práctica suele apalancar la parte de bonos para alcanzar la rentabilidad de un portfolio tradicional

Son tres filosofías distintas, no tres pasos de un proceso.

---

## Módulo 9 — ¿Cuánto puedo perder?

El módulo responde: *¿de cuántas formas distintas puedo perder dinero?* La respuesta tiene tres capítulos.

**Riesgo de mercado — el precio se mueve en tu contra**

Aquí vive el **VaR** (Value at Risk): un número que dice *"con 99% de probabilidad, mañana no pierdo más de X"*. Se puede calcular de tres formas:

- Asumiendo normalidad (rápido, pero miente en las colas)
- Con simulación histórica (usas datos reales, sin asumir distribución)
- Con Monte Carlo (simulas miles de escenarios)

El VaR tiene un problema estructural: no dice nada de lo que pasa en ese 1% malo, solo que existe. El **Expected Shortfall** sí: *"dado que estoy en ese 1% peor, ¿cuánto pierdo de media?"*. ES es el VaR mejorado y es lo que exige Basilea desde 2016. Aquí conecta directamente el Módulo 10: si el VaR paramétrico falla porque asume normalidad, EVT proporciona la herramienta para calcular ese extremo con más precisión.

**Riesgo de crédito — la contraparte no paga**

Dos problemas distintos bajo el mismo paraguas. Primero: ¿cuánto vale un bono que puede impagar? Los modelos estructurales (Merton) tratan el equity de una empresa como una call sobre sus activos — si el valor de los activos cae por debajo de la deuda, la empresa quiebra. Segundo: ¿cómo gestiono una cartera de créditos donde los defaults están correlacionados? Si quiebra una empresa, ¿quién más quiebra con ella? Aquí entran las cópulas, la misma herramienta que EVT usa para el caso multivariante.

**Riesgo de liquidez — el activo vale X en teoría pero no puedes venderlo a ese precio**

Dos dimensiones que se confunden pero son distintas. La **liquidez de mercado** es el coste de salir de una posición: el bid-ask spread. La **liquidez de financiación** es no tener cash para mantener una posición aunque tengas razón. Esta segunda mató a LTCM en 1998: tenían razón en sus apuestas pero no pudieron aguantar hasta que el mercado les diera la razón. Un activo puede ser ilíquido en mercado pero tener financiación, o viceversa; en una crisis, ambas se deterioran a la vez y se retroalimentan.

---

## Módulo 10 — ¿Qué pasa en ese 1% que el VaR ignora?

EVT no es un modelo alternativo al VaR. Es una mejora específica para el extremo de la cola. Para el 95% del tiempo, el VaR normal funciona bien. EVT solo importa cuando la pregunta es *"¿qué pasa en un crash de verdad?"* — y esa es exactamente la pregunta que los reguladores hacen después de cada crisis.

La estadística clásica modela el comportamiento promedio. EVT modela solo las colas, donde ocurren las pérdidas graves. El resultado teórico clave: bajo ciertas condiciones, los valores extremos de *cualquier* distribución convergen a una de solo tres distribuciones posibles. En finanzas siempre aparece la misma: colas gruesas (Fréchet), que es equivalente a una t de Student con pocos grados de libertad.

Hay dos formas de aplicarlo. El enfoque de **bloques** toma el máximo de cada periodo y modela esa serie de máximos. El enfoque **POT** (Peaks Over Threshold) modela directamente las observaciones que superan un umbral — es el preferido en la práctica porque aprovecha más datos. El punto débil de POT es elegir ese umbral: demasiado bajo introduce sesgo, demasiado alto deja muy pocas observaciones.

Una advertencia práctica importante: EVT asume que los datos son independientes entre sí. Los retornos financieros no lo son (hay clusters de volatilidad, autocorrelación). El flujo correcto es filtrar primero con un modelo GARCH, extraer los residuos estandarizados, y aplicar EVT sobre esos residuos.

---

## El hilo que une los cuatro

| Módulo | Pregunta | Herramienta clave |
|---|---|---|
| M7 | ¿Cuánto vale este activo? | Descuento de flujos, Black-Scholes |
| M8 | ¿Cómo gestiono el riesgo de tenerlo? | Delta hedging, superficie de volatilidad |
| M9 | ¿Cuánto puedo perder en total? | VaR, Expected Shortfall |
| M10 | ¿Qué pasa cuando los modelos de M9 se rompen? | EVT, GPD, GEV |