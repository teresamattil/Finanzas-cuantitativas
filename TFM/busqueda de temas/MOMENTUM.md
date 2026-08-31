MOMENTUM

Bloque 2 del Módulo 7, Tema 15 (T15) — Factores de riesgo multifactoriales

Eficiencia de mercado --> temas 11 a 17


# 1 -Momentum 
---

**Qué es el momentum**

El momentum es una anomalía de mercado bien documentada: los activos que más han subido en los últimos 3-12 meses tienden a seguir subiendo en el corto plazo, y los que más han caído tienden a seguir cayendo. Contradice directamente la hipótesis débil de eficiencia de mercado — si los precios pasados no deberían predecir retornos futuros, el momentum no debería existir. Lleva documentado desde Jegadeesh & Titman (1993) y sigue siendo, décadas después, uno de los factores más robustos y replicados en la literatura empírica, presente en prácticamente cualquier clase de activo (acciones, divisas, materias primas, y más recientemente cripto).

**Por qué es relevante / necesario**

El momentum no es solo una curiosidad académica: es una de las estrategias sistemáticas más utilizadas por fondos cuantitativos reales (CTA, hedge funds de "managed futures", etc.). Pero tiene un defecto grave y conocido: sufre **crashes** — periodos cortos y extremos donde pierde una fracción enorme de su valor. El caso más citado es 2009: tras el rebote brusco posterior a la crisis de Lehman, las carteras momentum perdieron más del 70% en semanas. Esto hace que, pese a tener un Sharpe atractivo en media, sea una estrategia poco invertible para un gestor real sin algún mecanismo de control de riesgo.

**Qué se hace en la práctica**

En la industria, la respuesta habitual no es abandonar el momentum sino **gestionar dinámicamente el tamaño de la posición** según el riesgo estimado — lo que se conoce como *volatility targeting* o *risk scaling*: cuando la volatilidad reciente del activo o de la cartera sube, se reduce la exposición; cuando baja, se amplía. Es una práctica extendida en gestión de CTAs y fondos de volatilidad controlada, pero su justificación empírica específica para el caso del momentum —¿realmente elimina los crashes, o solo diluye el retorno junto con el riesgo?— no siempre está bien separada de la intuición.

**Estado del arte (mini resumen)**

- **Barroso & Santa-Clara (2015)**, *"Momentum has its moments"* (JFE): demuestran, con datos de EEUU, que escalar la posición momentum por volatilidad realizada reciente casi duplica el Sharpe ratio y reduce drásticamente el riesgo de cola, sin sacrificar apenas retorno medio.
- **Moreira & Muir (2017)**, *"Volatility-Managed Portfolios"* (JoF): generalizan la idea — el *volatility timing* mejora el Sharpe de prácticamente cualquier factor, no solo momentum, porque el riesgo predice mal el retorno pero sí predice bien el riesgo futuro.
- **Daniel & Moskowitz (2016)**, *"Momentum Crashes"* (JFE): caracterizan cuándo y por qué ocurren los crashes — coinciden con reversiones bruscas de mercado tras periodos bajistas, cuando el momentum queda "atrapado" en el lado corto equivocado.

**Qué aporto yo / cuál es el problema / por qué este TFM**

La literatura existente se centra casi exclusivamente en mercados de acciones estadounidenses de gran capitalización, con décadas de datos. Lo que no está bien probado es si el resultado se sostiene en: (a) mercados con menos profundidad y más costes de fricción, o (b) activos de comportamiento estructuralmente distinto, como cripto, donde el momentum tiene documentación mucho más reciente y limitada, y donde la volatilidad es órdenes de magnitud mayor y más persistente. El problema que delimita este TFM es: **¿el volatility targeting mejora igual de bien el perfil riesgo-retorno del momentum fuera de EEUU/large-caps, en concreto en [ETFs sectoriales europeos / cripto], y esa mejora se mantiene una vez se incluyen costes de transacción realistas?**

**Mini resumen de metodología propuesta**

1. Construcción de la estrategia momentum clásica (ranking por retorno 12-1 meses, formación de carteras long-short o long-only según universo).
2. Cálculo de una versión con *volatility scaling*: tamaño de posición inversamente proporcional a la volatilidad reciente (rolling realizada y, como extensión, estimada vía GARCH). [ Esta es la de barroso y santa Clara creo]
3. Backtest out-of-sample con costes de transacción explícitos.
4. Comparación momentum puro vs. escalado: Sharpe, máximo drawdown, asimetría/curtosis de retornos, y en particular el comportamiento durante los periodos de crash conocidos del universo elegido.
5. Test de robustez: ¿el resultado se sostiene con distintas ventanas de formación y distintos periodos de rebalanceo?




-------------------------
# Puntos que tendré que definir en mi TFM 
Define "perfil riesgo-retorno" de forma operativa: ¿Sharpe? ¿Sortino? ¿max drawdown / Calmar? ¿asimetría y curtosis de los retornos? Vol targeting típicamente mejora Sharpe y reduce crashes de cola izquierda, pero no siempre mejora el retorno total — si no especificas la métrica, la pregunta es ambigua.



Esto no sabía que era una decisión, pero entiendo que tendré que hablar de ello en mi TFM y comparar varias métricas?



"Costes de transacción realistas" necesita números concretos: spread bid-ask, comisión, slippage/impacto de mercado, y si hay financiación de posiciones apalancadas (el vol targeting suele implicar leverage variable). En cripto además hay que decidir si usas spot, futuros perpetuos (funding rate) — cambia mucho el resultado.

Ventana temporal y frecuencia de rebalanceo: la cripto tiene historia corta y regímenes muy distintos (2017, 2021, 2022); especifica si controlas por régimen o no.


# Criptos o EFTs?

Por qué cripto da resultados más interesantes:

La tensión de la pregunta es más aguda. En cripto el momentum es muy fuerte (documentado por Liu & Tsyvinski, retornos brutos altísimos) pero también los "crashes" de momentum son brutales (2018, mayo 2021, 2022) por la volatilidad extrema y su clustering. Es el escenario ideal para que el vol targeting realmente demuestre su valor — o para que los costes se lo coman entero. En ETFs sectoriales europeos el efecto probablemente sea positivo pero modesto (como en EEUU), así que el resultado es más previsible y menos publicable.
Los costes son la historia real. En cripto, spread + slippage + funding rate (si usas perpetuos) pueden ser 5-10x los de un ETF líquido. Es muy plausible que encuentres: "vol targeting mejora el Sharpe bruto un X%, pero tras costes realistas el edge desaparece o se invierte" — esa es una conclusión con gancho, no una confirmación tibia de literatura ya conocida.
Contribución más original. Momentum + vol targeting en equities está muy trillado (Barroso & Santa-Clara, Moskowitz et al.). En cripto hay bastante menos evidencia sobre la interacción específica con vol targeting, así que tu aportación marginal es mayor.

El riesgo real que tienes que gestionar:

Poder estadístico limitado: la cripto solo tiene ~2-3 ciclos completos (2017-18, 2020-21, 2022-23). Cualquier resultado puede estar dominado por régimen, no por el efecto que estudias. Tendrás que reportarlo con honestidad (bootstrap por bloques, o al menos mostrar resultados por sub-período).
Survivorship bias: si usas el universo actual de criptos "grandes", estás sesgando hacia las que sobrevivieron. Necesitas un universo histórico correcto (ej. top-N por market cap en cada fecha de rebalanceo, no top-N de hoy).
Calidad de datos: spreads y volumen reales por exchange son más difíciles de conseguir que en ETFs (donde tienes NAV, spread bid-ask consolidado, etc.)

Mi recomendación práctica: quédate con cripto como el estudio principal (es donde está el resultado interesante), pero usa ETFs sectoriales europeos como benchmark de sanidad — si tu metodología no reproduce el efecto conocido de EEUU/vol targeting en un mercado "fácil" y líquido, sabes que algo falla en tu pipeline antes de fiarte de lo que veas en cripto.

¿Quieres que diseñemos la metodología completa (universo, ventanas de formación/holding, cálculo del target de vol, estimación de costes) para el estudio de cripto?


# Revisitando el Outline

Vamos por partes, tu razonamiento va bien encaminado pero hay matices importantes que conviene afinar.

## 1. El momentum como factor en un modelo multifactorial

Lo que probablemente tienes en mente es el **modelo de Carhart (1997)**, que añade el momentum al modelo de tres factores de Fama-French:

$$R_{i,t} - R_{f,t} = \alpha_i + \beta_{MKT}\,MKT_t + \beta_{SMB}\,SMB_t + \beta_{HML}\,HML_t + \beta_{UMD}\,UMD_t + \varepsilon_{i,t}$$

Donde **UMD** (*Up Minus Down*, a veces llamado WML, *Winners Minus Losers*) es el propio factor momentum, construido así (Jegadeesh & Titman, 1993):

1. Cada mes $t$, rankea los activos por su retorno acumulado entre $t-12$ y $t-2$ (se salta el último mes por el efecto de reversión a corto plazo / microestructura).
2. Forma una cartera long en el decil ganador y short en el decil perdedor.
3. El factor es simplemente el retorno de esa cartera long-short:

$$WML_t = R_{winners,t} - R_{losers,t}$$

Esa serie temporal $WML_t$ es la que luego usas como factor de riesgo (regresor) en el modelo de Carhart, o como estrategia standalone (que es tu caso).

**Intuición**: no es un "parámetro" en el sentido de un input calibrado, es el retorno de una estrategia replicable. Su $\beta_{UMD}$ en la regresión te dice cuánta exposición tiene un activo/cartera al factor momentum.

## 2. Sobre el "doble riesgo" — matiz importante

Tu intuición de que el riesgo viene de usar la señal tanto en el long como en el short es razonable pero no es exactamente el mecanismo que documentan Daniel & Moskowitz. Lo que ellos muestran es más sutil y más peligroso:

La pata **short (losers)** se comporta como una **opción call vendida sobre el mercado**. Los perdedores suelen ser acciones que han caído mucho, con betas altas y mucha sensibilidad a rebotes bruscos. Cuando el mercado ha estado en bajista y luego rebota con fuerza (como en 2009 post-Lehman), esos losers suben muchísimo más que el mercado general — y tú estás corto en ellos. La pérdida no está acotada de forma simétrica como en la pata long.

Además, esto ocurre justo en el peor momento posible: la volatilidad realizada *pasada* (la que usarías para dimensionar posición con una medida naive) suele estar todavía baja justo antes del crash, porque el crash coincide con el punto de inflexión del mercado. Por eso una medida de riesgo puramente backward-looking no te protege a tiempo — ese es precisamente el problema que atacan, cada uno a su manera, Barroso-Santa Clara y luego Daniel-Moskowitz de forma más fina.

## 3. Barroso & Santa-Clara (2015) — no es "volatility trading", es *volatility scaling / vol targeting*

Cuidado con el término: "volatility trading" normalmente se refiere a estrategias que operan la vol implícita vs. realizada (con opciones, VIX, etc.). Lo que hace este paper es **escalar el tamaño de posición de la estrategia momentum por su propia volatilidad reciente** — es *risk scaling*, no trading de volatilidad.

La reparametrización es:

$$r^{scaled}_{WML,t} = \frac{\sigma_{target}}{\hat\sigma_{WML,t-1}} \cdot r_{WML,t}$$

donde $\hat\sigma_{WML,t-1}$ es la volatilidad realizada de la propia serie $WML$, estimada con datos diarios de los últimos ~6 meses (126 días de trading):

$$\hat\sigma^2_{WML,t} = \frac{1}{21}\sum_{d=1}^{126} r^2_{WML,t-d}$$

(escalado a frecuencia mensual; el factor $1/21$ es una convención de anualización/reescalado, revisa el paper exacto para la convención que usan ellos).

**Intuición**: mismo signo de posición (long winners, short losers), pero el tamaño de la apuesta se reduce cuando la vol reciente del momentum sube, y se amplía cuando baja. El objetivo es mantener una volatilidad objetivo constante en el tiempo ($\sigma_{target}$).

Lo que encuentran: esto casi duplica el Sharpe y reduce la curtosis/asimetría negativa — porque, contraintuitivamente, la caída de volatilidad no predice bien la caída de retorno esperado (el retorno esperado del momentum no cae proporcionalmente cuando sube la vol), así que reducir tamaño en periodos de alta vol te ahorra riesgo sin sacrificar tanto retorno.

## 4. Moreira & Muir (2017) — generalización

Aplican exactamente la misma receta ($\sigma_{target}/\hat\sigma_{t-1}$) a **cualquier factor**, no solo momentum: mercado, value, size, etc. Su argumento central es que la varianza es mucho más predecible que el retorno esperado, así que escalar por volatilidad inversa mejora el Sharpe de forma casi mecánica en la mayoría de factores — no es algo específico del momentum.

## 5. Daniel & Moskowitz (2016) — el refinamiento

En vez de escalar solo por volatilidad realizada de $WML$, condicionan el riesgo a:
- Un indicador de si el mercado ha estado en bear market reciente (proxy de que los losers están "cargados" de opcionalidad).
- Una previsión de volatilidad del mercado (no solo del momentum).

Con eso construyen una versión que anticipa mejor los crashes específicamente, porque el mecanismo de Barroso-Santa Clara reacciona *después* de que la vol ya subió, mientras que el suyo intenta anticipar el régimen de crash antes de que se materialice en la vol realizada del propio factor.

## 6. Tu plan de TFM

Sí, es correcto: quieres replicar el enfoque de **Barroso & Santa-Clara (vol scaling del momentum)** — y opcionalmente comparar contra el enfoque más condicional de Daniel-Moskowitz — aplicado a un universo donde apenas está probado (cripto), con costes de transacción realistas. Es una extensión válida y bien delimitada: la pregunta no es "¿existe momentum en cripto?" (ya se ha documentado) sino "¿la corrección de vol scaling que funciona en US equities se sostiene en un universo con vol mucho más alta, persistente y con mayor coste de fricción?"

Un punto a decidir pronto para tu metodología: en cripto, ¿vas a usar vol realizada de alta frecuencia (datos horarios/diarios) para estimar $\hat\sigma_{t-1}$, dado que la vol cripto tiene clustering mucho más fuerte que en equities? Eso cambiará bastante tu ventana de estimación óptima frente al benchmark de 6 meses que usan Barroso-Santa Clara.