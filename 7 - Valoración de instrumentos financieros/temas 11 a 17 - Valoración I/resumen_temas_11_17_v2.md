# Módulo 7 — Valoración de Instrumentos Financieros
## Resumen Temas 11–17 (Valoración I)

> **Fuente:** Guía Didáctica Módulo 7 (UNED, curso 2025/26), páginas 186–310  
> **Nota:** Los temas 16 y 17 (*Extensions of the Standard CAPM* y *Continuous Time Asset Price Model*) no están incluidos en este PDF.

---

## Tema 11 — Fixed Income

### Terminología y estructura de un bono
- **Par (face value):** importe del préstamo, devuelto en su totalidad al vencimiento.
- **Cupón:** pago periódico de intereses = tasa cupón × par.
- **Zero-coupon bond:** solo paga el par al vencimiento (p.ej. T-bills, strips).
- Los detalles constan en el **bond indenture**.

### Características del bono
| Tipo | Beneficia a | Mecanismo |
|---|---|---|
| Floating rate | Inversor | Interés ligado a tasas actuales → menor sensibilidad a tipos |
| Indexed bond | Inversor | Par varía con inflación |
| Interest rate put | Inversor | Fuerza recompra si tipos suben |
| Convertible | Inversor | Reembolso en equity a elección del inversor |
| Interest rate call | Emisor | Rescata el bono si tipos bajan |
| Sinking fund | Emisor | Amortiza parcialmente a lo largo del tiempo |
| Asset-backed | Emisor | Traslada riesgo de préstamos a inversores (p.ej. MBS) |
| Catastrophe bond | Emisor | Paga menos si ocurre un evento catastrófico |

### Valoración
**Precio justo** (pago anual, tasa constante r, vencimiento T):

$$\text{Bond value} = \frac{\text{par}}{(1+r)^T} + \frac{\text{cupón}}{r}\left[1 - \frac{1}{(1+r)^T}\right]$$

- **Dirty price** = precio limpio + interés acumulado (accrued interest).
- **Accrued interest** = cupón × (días desde último cupón / días entre cupones).
- Convención daycount: 30/360 (deuda soberana EE.UU.) o Actual/365 (corporativos, algunos países).

### Yields
- **YTM (Yield to Maturity):** retorno anual si se mantiene hasta vencimiento; es el r que iguala precio de mercado con precio teórico.
- **Current yield** = cupón anual / precio actual.
- Otras: yield to call, yield to put.

### Sensibilidad a tipos de interés
- Tipos ↑ → precios ↓ (relación inversa).
- Bonos de mayor vencimiento son más sensibles.
- **DV01:** cambio en precio por 1 bp de variación en yield.
- **Duration (Macaulay):** media ponderada (por PV) de los flujos de caja — proxy de la sensibilidad.
- **Modified duration D\*:** % de variación del precio ante variación en yield.
- **Convexidad:** segunda derivada del precio respecto al yield; cuantifica la no-linealidad. Permite ajuste de Taylor de orden 2:

$$\frac{\Delta P}{P_0} \approx -D^* \Delta y + \frac{\text{convexity}}{2}(\Delta y)^2$$

- **Convexidad negativa:** bonos callable (el emisor los rescata si tipos bajan → el precio tiene techo).

### Riesgos y elementos de mercado
- **Default:** insolvencia de balance, insolvencia de flujo de caja o default estratégico.
- **Covenants protectores:** subordinación, cross-default, restricciones de dividendos, restricciones de activos.
- **Credit spread:** diferencia de yield respecto a deuda soberana equivalente. TED spread > 50 bp → señal de crisis.
- **High yield (junk):** bonos sub-investment grade; se comportan parcialmente como equity.
- **Liquidez:** bonos on-the-run vs off-the-run; diferencia de yield puede ser decenas de bp.
- **Repo:** venta + recompra de activos como garantía de un préstamo de cash. Haircut = margen de seguridad del prestamista.

---

## Tema 12 — Yield Curves

### Estructura temporal y tipos de tasas
- **Spot rates (zero rates):** yield de bonos cupón-cero a cada plazo.
- **Forward rates:** tipos acordados hoy para un préstamo que empieza en el futuro.
- **Short rates:** tasas a corto plazo vigentes hoy.
- La curva de rendimiento (*yield curve*) representa yields vs plazos para deuda soberana.

### Formas de la curva y señales macro
| Forma | Señal habitual |
|---|---|
| Upward sloping (suave) | Economía estable, crecimiento |
| Inverted | Expectativas de desaceleración/recesión |
| Humped | Defensa de divisa; gobierno sube tipos medios para retener inversores |

- Factores Litterman-Scheinkman: **nivel**, **pendiente**, **curvatura** (shift, twist, bow).

### Bootstrapping
Para construir la curva zero a partir de bonos con cupón: usar spot rates conocidos para despejar el siguiente spot rate desconocido iterativamente (de corto a largo plazo).

### Teorías de la estructura temporal
1. **Expectations hypothesis:** las tasas forward predicen las tasas cortas futuras.
2. **Liquidity preference:** los inversores exigen prima por comprometer liquidez → forward rates > E(tasas cortas).
3. **Market segmentation:** inversores con horizontes distintos y sin sustitución entre tramos.
4. **Preferred habitat:** como la anterior, pero con sustitución si hay precio suficiente.

### Política monetaria
- Los bancos centrales operan principalmente sobre el extremo corto de la curva (tipo overnight).
- Desde 2008: operaciones de mercado abierto en tramos largos (QE) y activos de riesgo.
- **Doble mandato Fed:** estabilidad de precios + máximo empleo (post-2008 añade estabilidad financiera).

### Modelos de curva
- **Vasicek:** proceso Ornstein-Uhlenbeck para la tasa corta: $dr_t = \kappa(\bar{r} - r_t)dt + \sigma dW_t$
- **Nelson-Siegel / Svensson:** factores de nivel, pendiente y curvatura (uno o dos jorobas).

---

## Tema 13 — Equity Valuation

### Análisis sectorial e industrial
- **DOL (Degree of Operating Leverage)** = 1 + costes fijos / beneficios → mide sensibilidad al ciclo.
- Software: DOL alto (costes fijos altos, variables bajos). Construcción: DOL bajo.
- **Sector rotation:** sobreponderar defensivos / infraponderar cíclicos al entrar en contracción.
- Codificaciones de industria: NAICS, UKSIC, NACE, ISIC.

### Análisis fundamental y comparables
- Ratios: **P/E**, **P/B** (book), **P/CF** (cashflow), **P/S** (sales).
- Limitaciones del P/E: earnings gestionables, no sirve para startups, inestable en cíclicas.
- **Tobin's q** = precio de mercado / coste de reposición de activos → tiende a 1 por competencia.

### Modelos de valoración por descuento

**DDM básico** (H años):
$$V_0 = \sum_{t=1}^{H} \frac{D_t}{(1+k)^t} + \frac{P_H}{(1+k)^H}$$

**Gordon-Shapiro (crecimiento constante g)**:
$$V_0 = \frac{D_1}{k - g} \quad \Rightarrow \quad k = \frac{D_1}{P_0} + g$$

- Reinversión: si ROE > k, tiene sentido no pagar todo como dividendo.
- $g = b \times \text{ROE}$ donde $b$ = fracción de beneficios retenida.
- **DuPont:** ROE = margen neto × rotación de activos × multiplicador de equity.
- **DDM multiestage:** modela el ciclo de vida de la empresa (crecimiento alto → madurez → terminal).

**Free Cashflow to the Firm (FCFF)**:
$$\text{FCFF} = \text{EBIT}(1-\tau) + \text{amortización} - \text{capex} - \Delta\text{NWC}$$
$$V_0^{\text{firma}} = \sum_t \frac{\text{FCFF}_t}{(1+\text{WACC})^t}$$

$$\text{WACC} = w_e r_e + (w_b r_b + w_l r_l)(1-\tau)$$

**FCFE** (Free Cashflow to Equity) = FCFF − intereses(1−τ) + variación neta de deuda.

**Comparación de modelos:** en teoría (Modigliani-Miller) todos dan el mismo valor; divergen por incertidumbre en inputs, impuestos, fricciones y no-constancia de rf.

### Corrección por desigualdad de Jensen
Cuando se estiman $\hat{k}$ y $\hat{g}$ con incertidumbre, la valoración debe corregirse:
$$\hat{V}_0 \approx \frac{\hat{D}}{\hat{k}-\hat{g}} + \frac{\hat{D}}{(\hat{k}-\hat{g})^3}(\sigma^2_k + \sigma^2_g - 2\,\text{Cov}(\hat{k},\hat{g}))$$

### PVGO y P/E
$$\text{PVGO} = P_0 - \frac{E_1}{k} \quad;\quad \frac{P_0}{E_1} = \frac{1}{k}\left(1 + \frac{\text{PVGO}}{E_1/k}\right)$$

- Si PVGO = 0, la acción se valora como una renta perpetua.
- Regla rápida: P/E / g < 1 → acción atractiva.

---

## Tema 14 — Capital Asset Pricing Model (CAPM)

### Notación
| Símbolo | Significado |
|---|---|
| $r_i$ | retorno del activo i |
| $r_M$ | retorno del portfolio de mercado |
| $r_f$ | tasa libre de riesgo |
| $R_i = r_i - r_f$ | exceso de retorno |
| $\beta_i$ | sensibilidad al factor de mercado |
| $\alpha_i$ | retorno anormal / inexplicado |

### Single-Index Model
$$R_{i,t} = \alpha_i + \beta_i R_{M,t} + \varepsilon_{i,t}$$

- **Ventaja:** reduce inputs de $\frac{n(n+3)}{2}$ a $3n+3$ (para 50 activos: 1.325 → 153 estimaciones).
- **Limitación:** no captura correlaciones idiosincrásicas entre pares.

### CAPM (Sharpe-Lintner-Mossin, 1964-1966)
**Supuestos:** muchos inversores price-takers, sin impuestos ni costes, horizonte único, maximización media-varianza, expectativas homogéneas.

**Resultado de equilibrio:** todos los inversores sostienen el mismo portfolio de riesgo = portfolio de mercado M. La Capital Market Line (CML) = Capital Allocation Line (CAL).

**Ecuación CAPM:**
$$E(r_i) - r_f = \beta_i [E(r_M) - r_f] \quad ;\quad \beta_i = \frac{\text{Cov}(r_i, r_M)}{\sigma^2_M}$$

- **Security Market Line (SML):** plot de $E(r_i)$ vs $\beta_i$. Activos por encima → alpha positivo (infravalorados). Por debajo → alpha negativo.

### Limitaciones del CAPM
- **Teóricas:** un solo factor de riesgo es insuficiente; los inversores no son todos media-varianza; equilibrio puede no existir.
- **Empíricas:** el portfolio de mercado verdadero es desconocido; heteroscedasticidad; correlación serial; betas pasados predicen mal betas futuros.

### Mejoras del CAPM
- **Betas ajustados:** Blume ($\hat{\beta}_i = \frac{1}{3} + \frac{2}{3}\hat{\beta}_i^{\text{hist}}$) o Vasicek (shrinkage bayesiano).
- **Conditional CAPM:** betas varían con el ciclo macroeconómico (Rothschild-Harvey).
- **Intertemporal CAPM (ICAPM, Merton):** añade factor de estado económico.
- Incluir capital humano o empresas privadas mejora el ajuste.

### Hedging y alpha portátil
- Portfolio de tracking T replica el $\beta$ de P usando el índice + T-bills.
- Posición larga en P + corta en T → market neutral → aísla el alpha.
- **Zero-beta portfolio (Black):** cuando no hay activo libre de riesgo, la tangente a la frontera en M define una tasa implícita $r_z$ → versión Black del CAPM.

---

## Tema 15 — Factor Models y Arbitrage Pricing Theory (APT)

### Motivación
Un solo factor de mercado es insuficiente → modelos multifactor.

**Modelo general multifactor:**
$$R_i = \alpha_i + \beta_{i,1}F_1 + \beta_{i,2}F_2 + \ldots + \beta_{i,k}F_k + \varepsilon_i$$

### APT (Ross, 1976)
Tres supuestos:
1. Los retornos se describen por un modelo factorial.
2. El riesgo idiosincrásico se puede diversificar.
3. Los mercados no permiten arbitraje persistente.

**Implicación:** $R_i \approx \beta_{i,1}F_1 + \ldots + \beta_{i,k}F_k$ (sin alpha en equilibrio).

**Arbitraje:**
- *Relativo:* dos portfolios bien diversificados con igual exposición a factores pero diferente retorno esperado → comprar barato, vender caro.
- *Absoluto:* un portfolio con retorno observado mayor que el predicado por los factores → construir portfolio arb con T-bills y tracking portfolios.

**Dominancia vs arbitraje:** el APT se apoya en pocos agentes que toman posiciones grandes (cierre rápido del desequilibrio), más robusto que el argumento de dominancia del CAPM.

### Factores macro
**Chen-Roll-Ross (5 factores):**
- Crecimiento producción industrial (%IP)
- Inflación esperada E(i)
- Sorpresa de inflación (Δi − E(i))
- Cambio en credit spread corporativo (CMG)
- Cambio en pendiente de la curva (LMS)

**Modelos para hedge funds:** Hasanhodzic-Lo (6 factores), Fung-Hsieh (7 y 8 factores).

### Factores micro
- **ARCH/GARCH-in-mean:** volatilidad actual afecta a retornos.
- **Liquidity CAPM (Acharya-Pedersen):** diferencial bid-ask como factor de riesgo.
- **Pastor-Stambaugh:** sorpresa en volumen en dólares como proxy de liquidez.

### Factores de estilo
- **Fama-French 3 factores:** mercado (RM), tamaño (SMB: small minus big), valor (HML: high minus low book/price).
- **Carhart 4 factores:** añade momentum (WML: winners minus losers).
- **Fama-French 5 factores:** añade rentabilidad (RMW) e inversión (CMA).

**¿Son reales estos factores?**
- SMB probablemente relacionado con credit spreads y small-cap.
- HML activo principalmente alrededor de anuncios de beneficios.
- WML posiblemente news sentiment o sorpresa en desempleo.
- Harvey-Liu-Zhu: solo son robustos estadísticamente el mercado, HML, momentum, consumo duradero, volatilidad a corto plazo y liquidez.

### Límites del arbitraje
- **Huberman-Stanzl:** los mercados no permiten quasi-arbitraje (coste de entrada ≈ coste de salida).
- **"Siamese Twin" shares:** evidencia de que el APT no es exacto.
- Otros frenos: model risk, fundamental risk, restricciones de crédito, segmentación de mercado.

---

## Temas 16 y 17 — No disponibles en este PDF

| Tema | Título | Estado |
|---|---|---|
| 16 | Extensions of the Standard CAPM | No incluido en la guía didáctica PDF |
| 17 | Continuous Time Asset Price Model | No incluido en la guía didáctica PDF |

Estos temas corresponden a la 3ª semana del módulo (4–11 junio) y deberían buscarse en el material docente adicional del curso.
