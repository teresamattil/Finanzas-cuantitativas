Investigación sobre Momentum

# Qué es? Donde entra en juego en el día a día de un fondo de inversión? Situemoslo en el mapa
Vale, vamos a bajarlo a tierra con un ejemplo concreto.

## Un fondo cuant básico: la rutina

Imagina un fondo long-only que invierte en las 500 acciones del S&P 500, con un proceso sistemático (no discrecional — nadie "decide a ojo", todo sale de un modelo). Su rutina, a grandes rasgos, es esta:

**1. Universo de inversión**
Define qué activos son candidatos: por ejemplo, todas las acciones del S&P 500 con liquidez suficiente (volumen diario mínimo, sin restricciones regulatorias, etc.).

**2. Cálculo de señales (aquí es donde entra el momentum)**
Cada cierto tiempo (mensual es lo típico), el fondo calcula, para cada acción, uno o varios **factores** — variables numéricas que intentan predecir qué activos lo van a hacer mejor que otros. El momentum es uno de los factores más usados y clásicos: mide la rentabilidad acumulada de un activo en los últimos N meses (típicamente 12 meses, a veces excluyendo el último mes para evitar el efecto de reversión a corto plazo). La idea empírica detrás: **los activos que lo han hecho bien recientemente tienden a seguir haciéndolo bien un tiempo más** (y viceversa con los que lo han hecho mal). No es la única señal — normalmente se combina con otras: value (barato vs. caro), calidad (rentabilidad, deuda), volatilidad baja, tamaño, etc. Cada modelo pesa estos factores de forma distinta.

**3. Ranking y selección**
Con la señal de momentum (y quizás otras) calculada, el fondo ordena todo el universo de mejor a peor y selecciona, por ejemplo, el 20% superior (long) — o construye una cartera long-short si también apuesta contra el 20% inferior.

**4. Construcción de la cartera (position sizing)**
No todos los activos seleccionados entran con el mismo peso. Aquí es donde el riesgo entra en juego: puede pesar más los activos con mayor score de momentum, o ajustar el peso según su volatilidad individual (menos peso a los más volátiles), o aplicar restricciones (máximo % por sector, por activo, etc.).

**5. Overlay de riesgo**
Antes de ejecutar, se revisa la cartera contra límites de riesgo: volatilidad total esperada, exposición sectorial, VaR, etc. Si algo se sale de los límites, se recorta.

**6. Rebalanceo y ejecución**
Se ejecutan las operaciones necesarias para pasar de la cartera actual a la nueva cartera objetivo, típicamente con algo de cuidado para minimizar costes de transacción (trading escalonado, límites de participación en volumen, etc.).

**7. Vuelta a empezar**
Un mes después, se repite todo el proceso desde el paso 2 con datos actualizados.## Entonces, ¿el momentum es "un parámetro más"?

Sí, exactamente — es **una señal de entrada al modelo**, no el modelo entero. En un fondo real casi nunca se usa solo: se combina con otros factores (value, calidad, baja volatilidad...) y el peso que se le da a cada uno depende de la filosofía del fondo. Algunos fondos son "puramente momentum" (apuestan casi todo a esa señal), otros lo usan como un factor más entre cinco o seis.

Para tu TFM, esto te da una pista útil: el paso 2 (cálculo de señales) y el paso 4 (construcción con overlay de riesgo) son exactamente donde se sitúan tus temas favoritos (2 y 3 de mi lista anterior — riesgo y carteras). Un TFM de "momentum + volatility targeting" es literalmente construir ese pipeline completo: implementas el paso 2 (momentum), el paso 4 (ajuste por volatilidad) y el paso 5 (backtesting con costes), y comparas contra una versión sin ese ajuste de riesgo.



# Qué tiene que ver los modelos de multifcator con CAPM?
Buena pregunta, porque son cosas relacionadas pero que operan en planos distintos — no son "estrategias competidoras", es más bien que el momentum (y los demás factores) nacieron **como una crítica empírica al CAPM**.

**CAPM: qué predice**

CAPM dice que el único factor que explica el retorno esperado de un activo es su beta (sensibilidad al mercado):

E(Rᵢ) = Rf + βᵢ(E(Rm) − Rf)

Es decir: si dos activos tienen el mismo beta, deberían tener el mismo retorno esperado. No debería haber ninguna otra variable que añada poder explicativo.

**El problema: no se sostiene empíricamente**

Desde los 80-90 se acumuló evidencia de que hay variables que predicen retorno *más allá* de lo que explica el beta: tamaño (size), book-to-market (value), y momentum (Jegadeesh & Titman, 1993) fueron de las primeras "anomalías" documentadas. Si CAPM fuera cierto, controlando por beta, el momentum no debería aportar nada — y sin embargo aporta, de forma robusta y persistente en el tiempo y en distintos mercados.

**De ahí surgen los modelos multifactor como extensión/sustitución de CAPM:**

- Fama-French 3 factores (1993): mercado + size (SMB) + value (HML)
- Carhart 4 factores (1997): añade momentum (UMD/WML) — este es el que formaliza momentum como factor de asset pricing
- Fama-French 5 factores (2015): añade profitability e investment (y momentum sigue vivo fuera del modelo, algo debatido)

Estos modelos son literalmente CAPM extendido: mismo esquema (retorno esperado = suma de sensibilidades a factores × sus primas de riesgo), pero con más variables explicativas que el beta de mercado solo.

**Entonces, ¿es lo mismo que lo que te expliqué antes del fondo?**

Aquí está el matiz clave — hay dos usos del mismo armazón matemático:

1. **Uso académico/explicativo (asset pricing):** el modelo se usa *ex post*, para explicar por qué un fondo o activo tuvo el retorno que tuvo, y si ese retorno es "alpha genuino" o simplemente exposición a factores conocidos (beta disfrazado de alpha). Aquí momentum es una prima de riesgo sistemática, al mismo nivel conceptual que el beta de mercado en CAPM.

2. **Uso práctico/predictivo (lo que describimos del fondo):** el mismo factor se usa *ex ante*, como señal cross-sectional para rankear activos y construir cartera. No estás testando si CAPM es cierto — estás explotando la anomalía que CAPM no explica.

**Resumen de la relación:** no son estrategias distintas en competencia, es una jerarquía. CAPM es el modelo base de un solo factor (mercado). Los modelos multifactor (Carhart, etc.) son extensiones que incluyen momentum como una prima de riesgo adicional porque CAPM, empíricamente, deja "alpha residual" sin explicar que resulta estar correlacionado con estas variables. Un fondo momentum es, en el fondo, una apuesta a que esa prima de riesgo (o ineficiencia, según la escuela) sigue siendo real y explotable — algo que CAPM en su forma pura dice que no debería existir.

# Por qué el momentum sufre crashes? Por qué es especialmente doloroso? Cómo evitarlo?

Vale, vamos a desengranarlo pieza a pieza, empezando por lo más básico y subiendo en complejidad.

**Paso 1: qué es una "posición"**

Una posición es simplemente la cantidad de un activo que tienes en cartera, con signo y tamaño. Hay dos dimensiones:

- **Dirección**: *long* (compras el activo, ganas si sube) o *short* (vendes algo que no tienes prestado, ganas si baja — es apostar a la caída).
- **Tamaño/peso**: cuánto capital (o cuánto riesgo) le asignas. No es lo mismo tener un 2% de la cartera en Apple que un 20%.

Una estrategia momentum "pura" en su forma académica es **long-short**: compras los activos con mejor rentabilidad pasada (los "ganadores") y vendes en corto los peores (los "perdedores"). No apuestas por la dirección del mercado en general — apuestas por que los ganadores sigan ganando *relativo* a los perdedores. Esto se llama una cartera market-neutral (en teoría, el riesgo de mercado se cancela porque tienes long y short a la vez).

**Paso 2: qué significa "escalar" una posición**

Cuando hablamos de *tamaño de posición según riesgo*, la idea es: no metes el mismo dinero en un activo tranquilo (poca volatilidad) que en uno que se mueve muchísimo. Si Nvidia se mueve un 5% diario y una utility se mueve un 0.5% diario, meter el mismo importe en ambas significa que tu riesgo real está dominado por Nvidia. Para igualar el riesgo, reduces el tamaño en el activo volátil y aumentas en el tranquilo. Eso es "risk scaling" a nivel de activo individual — y lo mismo se puede aplicar a nivel de cartera entera: si la volatilidad de toda la estrategia sube, reduces el apalancamiento global.

**Paso 3: por qué el momentum long-short es especialmente peligroso**

Aquí está el núcleo del problema. Piensa qué pasa en una recesión severa, tipo 2008:

- Los activos que más caen durante la crisis (bancos, cíclicos) se convierten en los "perdedores" de tu ranking momentum → tu estrategia los pone **short**.
- Los activos defensivos que aguantan mejor se convierten en "ganadores" → los pone **long**.

Hasta aquí todo normal. El problema es qué pasa cuando el mercado, tras tocar fondo, **rebota con violencia** — que es exactamente lo que pasó en marzo-abril de 2009. Los activos más castigados (justo los que tu estrategia tiene en corto) son los que más rebotan, porque venían de estar más sobrevendidos. Tu pata corta se dispara en tu contra al mismo tiempo que tu pata larga (los defensivos) se queda rezagada porque ya no hace falta refugio.

Deja que te lo muestre de forma visual antes de seguir con por qué esto genera un crash tan extremo y qué papel juega el apalancamiento aquí.**Paso 4: por qué esto no es un simple "mala suerte, activo bajó"**

Lo que hace único al momentum crash frente a otras pérdidas de mercado es que **las dos patas fallan a la vez**, cuando normalmente la gracia de una cartera long-short es que se compensan. En una caída de mercado "normal", si tu long baja, tu short (que también baja, porque baja todo) te protege parcialmente. Aquí ocurre lo contrario: el mercado sube y ambas patas contribuyen a la pérdida — el short porque el activo sube fuerte, el long porque no acompaña el rally. Es un fallo correlacionado, no diversificado, y ocurre justo en el peor momento: después de que ya llevas un tiempo con exposición grande a esos "perdedores" en corto.

**Paso 5: dónde entra la volatilidad como variable clave**

Aquí conecta con el paper de Daniel & Moskowitz que mencionas: el patrón no es aleatorio. Los crashes de momentum tienden a ocurrir específicamente cuando:
1. El mercado lleva un tiempo bajista (así se ha formado la pata short con activos muy castigados).
2. La volatilidad implícita/realizada está elevada (señal de pánico, pero también de que el rebote potencial es más violento).
3. Se produce un cambio brusco de régimen — la parte corta pasa de "sigue cayendo" a "rebota con fuerza" en cuestión de días.

Es decir: el propio riesgo de la estrategia sube *antes* del crash — hay una señal observable (volatilidad reciente elevada) que precede al desastre. Eso es exactamente lo que explota el volatility targeting de Barroso & Santa-Clara: si reduces tu exposición cuando la volatilidad reciente sube (que es precisamente cuando el riesgo de reversión es mayor), estás reduciendo tamaño de posición justo antes de que llegue el golpe, sin necesidad de predecir el rebote en sí — solo predices que "ahora mismo hay más riesgo de que algo raro pase".

¿Quieres que sigamos con el mecanismo concreto de cómo se calcula ese escalado por volatilidad (la fórmula de Barroso & Santa-Clara) o prefieres primero entender por qué Moreira & Muir dicen que esto funciona para "casi cualquier factor" y no es exclusivo del momentum?



# sigue mereciendo la pena el volatility targeting una vez restas los costes reales de ejecutarlo

Sí, has dado exactamente en el clavo — esa es la tensión central que plantea el propio texto que has pegado. Vamos a desmenuzarlo.

**Tienes razón: la fórmula en sí es "gratis" sobre el papel**

Barroso & Santa-Clara proponen algo matemáticamente simple: cada mes (o cada período que sea), miras la volatilidad reciente y recalculas cuánto debes apostar. Si en el modelo teórico no metes costes de transacción, ajustar el tamaño de la posición es instantáneo y sin fricción — un excel que recalcula un número.

**El problema: cada ajuste implica operar de verdad**

Cada vez que "escalas la posición" — sea para arriba o para abajo — tienes que **comprar o vender activos de verdad** para llegar al nuevo tamaño. Y eso no es gratis:

- **Spread**: la diferencia entre el precio al que puedes comprar y al que puedes vender. Nunca compras y vendes al mismo precio exacto — siempre hay un pequeño margen que se queda el mercado
- **Slippage**: cuando ejecutas una orden grande, el propio hecho de comprar/vender mueve el precio en tu contra antes de que termines de ejecutar toda la orden
- **Funding rate** (mencionan esto para futuros perpetuos, típico en cripto): un coste periódico que pagas o cobras por mantener la posición abierta, dependiendo del desequilibrio entre largos y cortos en el mercado

**Por qué esto es especialmente grave justo cuando más lo necesitas**

Aquí está la ironía que probablemente explora el paper: **la volatilidad targeting te pide reajustar más veces, y más agresivamente, precisamente cuando el mercado está revuelto** (que es cuando la volatilidad cambia rápido). Pero **la volatilidad alta también suele venir con spreads más anchos y slippage peor** — precisamente porque hay pánico, menos liquidez, más incertidumbre.

Es decir: la estrategia te exige operar más justo en los momentos en que operar sale más caro. Doble penalización.

**Por qué esto es aún peor en cripto (que es lo que evalúa el paper)**

- Los costes de fricción en cripto son "órdenes de magnitud mayores" que en acciones grandes de EEUU (como dice el texto) — mercados menos maduros, menos líquidos en muchos casos
- El "funding rate" de los futuros perpetuos es un coste recurrente que no existe en acciones — pagas por mantener la posición abierta, encima del propio ajuste de tamaño
- Y el momentum en cripto es "especialmente fuerte pero especialmente volátil" → significa que la fórmula de Barroso & Santa-Clara te va a pedir reajustes más frecuentes y más bruscos que en acciones, exactamente donde más caro sale hacerlo

**Entonces, ¿qué está probando realmente el paper?**

Tu intuición es la pregunta de investigación central, literalmente: **¿sigue mereciendo la pena el volatility targeting una vez restas los costes reales de ejecutarlo, o esos costes se comen (o incluso revierten) la mejora que Barroso & Santa-Clara encontraron en un entorno mucho más barato de operar (acciones grandes, líquidas, EEUU)?**

Por eso usan los **ETFs sectoriales europeos como control**: primero comprueban que su metodología replica el resultado conocido (mejora de Sharpe) en un mercado líquido y barato de operar, para asegurarse de que el método está bien implementado. Solo después miran si ese mismo método sigue funcionando en cripto, donde los costes son mucho más altos — que es donde tu pregunta se vuelve decisiva.

En una frase: **tienes toda la razón — el valor añadido teórico de la fórmula puede quedar total o parcialmente anulado por el coste real de ejecutarla, y ese es precisamente el hueco en la literatura que el paper dice llenar.**


# Por qué usar ETFs (exchange- Traded Funds)

**Qué es un ETF (Exchange-Traded Fund)**

Es un fondo que agrupa muchos activos (acciones, bonos, materias primas...) en una sola "cesta", y esa cesta se compra y vende en bolsa **como si fuera una sola acción**. 

Ejemplo: en vez de comprar tú misma las 500 acciones que componen el S&P 500 una por una, compras **un solo ticket** (una participación del ETF) que replica ese índice entero. Si el S&P 500 sube un 1%, tu ETF sube aproximadamente un 1%.

Ventajas frente a comprar activos sueltos:
- **Diversificación instantánea**: un solo producto, muchas empresas dentro
- **Liquidez**: se compra/vende en cualquier momento del día en el mercado, como una acción normal
- **Coste bajo**: comisiones de gestión mucho más baratas que un fondo tradicional

**Qué es un ETF sectorial**

Es un ETF que, en vez de replicar todo un mercado (como el S&P 500 entero), replica **solo un sector concreto** de la economía. Por ejemplo:
- ETF de tecnología (solo empresas tech)
- ETF de energía (solo petroleras, gas, renovables)
- ETF de salud (farmacéuticas, biotech, hospitales)
- ETF de financieras (bancos, aseguradoras)

**"ETFs sectoriales europeos"** en tu texto = ETFs que replican sectores concretos de la economía europea (tecnología europea, energía europea, etc.), cotizados en bolsas europeas.

**¿Es donde Barroso & Santa-Clara aplicaron su fórmula originalmente?**

No exactamente — aquí hay un matiz importante que conviene aclarar.

- **Barroso & Santa-Clara (2015), el paper original**: aplicaron su fórmula sobre una cartera momentum construida con **acciones individuales estadounidenses de gran capitalización** (compra las acciones ganadoras, corto las perdedoras, una por una, no ETFs). Es el estudio clásico de momentum "stock-level" en EEUU.

- **El paper que tú me has pegado (el que evalúas tú)**: es un trabajo **distinto y posterior**, que coge esa misma idea (volatility targeting) y la pone a prueba en dos sitios nuevos:
  1. **ETFs sectoriales europeos** → como "universo de control", para comprobar que su metodología reproduce el efecto conocido en un entorno líquido y ya estudiado, antes de fiarse de resultados en un terreno nuevo
  2. **Criptoactivos** → el terreno realmente nuevo que quieren investigar, donde el momentum es fuerte pero los costes de operar son mucho más altos

**Por qué tiene sentido usar ETFs sectoriales como "control" en este nuevo estudio**

Porque son un término medio perfecto para validar la metodología: 
- Tienen **suficiente historia y liquidez** en Europa como para que el momentum se pueda medir bien (no son tan líquidos/estudiados como las acciones grandes de EEUU del paper original, pero se le parecen bastante)
- Al agrupar sectores enteros (en vez de acciones sueltas), reducen algo de "ruido" idiosincrático de empresas individuales
- Sirven de **puente metodológico**: si el investigador logra replicar la mejora de Sharpe de Barroso & Santa-Clara aquí, sabe que su código/metodología está bien implementada — y entonces puede aplicar esa misma metodología con confianza al terreno realmente interesante (cripto), sabiendo que si algo falla ahí, no es un error de implementación sino un efecto real de los costes/estructura de mercado cripto


# A INVESTIGAR!!

"La respuesta habitual de la industria no ha sido abandonar el momentum, sino gestionar dinámicamente el tamaño de la posición en función del riesgo estimado..." FALTA CITACIÓN

The good news is that researchers have uncovered strategies that have reduced crash risk—crashes are at least partly forecastable, tending to occur in “panic” states following market declines and when market volatility is high, and are contemporaneous with market rebounds. The authors of the 2015 study “Momentum Has Its Moments,” the 2016 study “Momentum Crashes,” the 2017 study “A Century of Evidence on Trend-Following Investing,” the 2018 study “The Impact of Volatility Targeting,” the 2019 study “Portfolio Management of Commodity Trading Advisors with Volatility Targeting,” and the 2020 studies “Conditional Volatility Targeting” and “Understanding Volatility-Managed Portfolios” have found:

Long-only momentum strategies are not subject to deep crashes.
Scaling momentum based on momentum’s mean and variance dramatically reduces the risk of crashes and greatly improves the Sharpe ratio of momentum strategies.
Scaling strategies could be improved upon by adjusting risk exposures conditional on (extreme) volatility states—it reduces risk exposures during high volatility states, increases risk exposures during low volatility states, and maintains an unscaled exposure otherwise.
In their May 2023 study “Momentum Turning Points,” Christian Goulding, Campbell Harvey, and Michele Mazzoleni found that momentum strategies could be improved on by dynamically blending slow and fast momentum strategies based on four-state cycle-conditional information. They partitioned an asset’s return history into four observable phases—Bull, Correction, Bear, and Rebound—by relying on the agreement or disagreement of slow and fast trailing momentum signals. They then examined the information content of these states for subsequent return behavior. They used this information to specify an implementable “dynamic” trend-following strategy that adjusts the weight it assigns to slow (such as 12 months) and fast (such as one month) momentum signals after observing market breaks (Corrections or Rebounds). If historical returns tended to be positive after Corrections (when the slow strategy goes long and the fast strategy goes short), then the strategy would tilt away (scale down) from the fast strategy. In contrast, if historical returns tended to be positive after Rebounds (when the slow strategy goes short and the fast strategy goes long), then the strategy would tilt toward the fast strategy. If historical returns were negative after such states, then the direction of the tilt reversed.

Among their key findings were:

When bets indicated by SLOW and FAST disagreed, the market was more likely to be at a turning point.
The agreement of SLOW and FAST to go long (short) was more likely to indicate the market was amid an uptrend (downtrend).
Intermediate-speed momentum strategies had higher Sharpe ratios than the average Sharpe ratios of SLOW or FAST. They also further reduced exposure to extreme downside events by scaling down after Corrections and Rebounds. They linked this behavior to the volatility of returns following turning-point states.