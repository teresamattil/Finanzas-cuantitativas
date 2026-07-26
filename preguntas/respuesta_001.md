---
date: 2026-07-25
tags: [distribuciones, retornos, normal, t-student, VaR, examen]
---

# Normal vs t-Student para retornos diarios: por qué importa la elección

## El hecho empírico de partida

Los retornos diarios tienen colas gruesas (*fat tails*) y skewness negativa. La normal asigna probabilidad casi cero a movimientos de más de 3σ. En la realidad ocurren con frecuencia. La t-Student los captura mejor porque tiene más masa en las colas, controlada por los grados de libertad ν.

## Consecuencias directas de elegir mal

**1. VaR paramétrico subestimado**
El cuantil 1% de una t con ν pequeño está más alejado de la media que el cuantil 1% de la normal. Si calculas VaR al 99% asumiendo normalidad, el banco subestima el capital regulatorio necesario.

**2. Expected Shortfall materialmente menor**
ES mide el promedio de pérdidas en ese 1% de cola. Con normalidad, ese promedio está artificialmente cerca del umbral. Con t-Student, la cola es más pesada y el ES es materialmente mayor — y ES es lo que exige Basilea desde 2016.

**3. Pricing de opciones y la sonrisa de volatilidad**
Black-Scholes asume lognormalidad (normal en retornos). Las colas gordas reales generan la sonrisa de volatilidad: el mercado implícitamente corrige la distribución usando volatilidades implícitas distintas por strike. La sonrisa es la huella de que la distribución real tiene más cola de lo que asume el modelo.

**4. Backtesting falla sistemáticamente**
Si el modelo es normal y los retornos son realmente t, las excepciones del VaR superan el umbral esperado. Bank of America en 2007: 14 excepciones observadas vs 2.6 esperadas al 99%.

**5. Conexión con EVT (M10)**
Cuando la EVT se aplica a colas financieras, siempre emerge la familia Fréchet — equivalente a una t-Student con pocos grados de libertad. La t-Student no es solo un ajuste empírico: es lo que la teoría predice que debe aparecer en las colas.

## So-what para el examen

Elegir t-Student no es una conveniencia estadística sino la distribución que tanto los datos empíricos como la teoría (EVT) predicen para retornos financieros en la zona que importa: las colas. Y es exactamente ahí donde cualquier modelo de riesgo tiene que ser correcto.

En el análisis gráfico y estadístico del examen: esperar Q-Q plot con desviaciones en ambos extremos (colas más pesadas que la normal), curtosis > 3, y p-valores < 0.05 en Jarque-Bera, Shapiro-Wilk y KS — todo apuntando a rechazar normalidad y favorecer t-Student.
