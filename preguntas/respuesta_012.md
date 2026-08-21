---
date: 2026-07-30
tags: [CAPM, APT, factores de riesgo, M7]
---

# APT vs CAPM

## La diferencia en una línea

CAPM dice que **un solo factor** (el mercado) explica todos los retornos. APT dice que pueden ser **varios factores**, sin especificar cuáles.

## CAPM

$$E(r_i) = r_f + \beta_i \cdot [E(r_m) - r_f]$$

- Un factor: el mercado
- β mide la exposición a ese único factor
- Derivado de equilibrio general (todos los inversores tienen la misma cartera arriesgada → tangency portfolio = mercado)
- Testeable en teoría, pero el "mercado" es inobservable (problema de Roll)

## APT (Ross, 1976)

$$E(r_i) = r_f + \beta_{i1} \cdot \lambda_1 + \beta_{i2} \cdot \lambda_2 + \dots + \beta_{ik} \cdot \lambda_k$$

- `βᵢⱼ` = sensibilidad del activo al factor `j`
- `λⱼ` = prima de riesgo del factor `j` (cuánto te pagan por exposición a ese factor)
- No especifica qué son los factores — los determina empíricamente
- Derivado de ausencia de arbitraje, no de equilibrio general → supuesto más débil y más creíble

## Comparación directa

| | CAPM | APT |
|--|------|-----|
| Número de factores | 1 (mercado) | k (libre) |
| Supuesto base | Equilibrio general | No arbitraje |
| Factores especificados | Sí (el mercado) | No — empíricos |
| Ejemplo aplicado | — | Fama-French (3 o 5 factores) |
| Problema práctico | El mercado es inobservable | ¿Qué factores elegir? |

## Fama-French como APT aplicado

Fama-French es APT con factores concretos:
- **Mkt-Rf**: exceso de retorno del mercado (= CAPM)
- **SMB** (Small Minus Big): prima por tamaño
- **HML** (High Minus Low): prima por valor (book-to-market alto)

Añaden HML y SMB porque empíricamente explican retornos que el CAPM solo no captura.

## Qué es una prima y diferencia entre las tres de Fama-French

**Prima = retorno extra que el mercado paga por asumir un riesgo específico.** Si un activo tiene más riesgo, nadie lo compra al mismo precio → el mercado lo abarata hasta que ofrece más retorno. Esa diferencia es la prima.

| Prima | Fórmula | Qué riesgo compensa |
|-------|---------|---------------------|
| **Mkt-Rf** | `E(rₘ) − rƒ` | Estar en renta variable en vez de deuda soberana. No diversificable |
| **SMB** | `E(rₛₘₐₗₗ) − E(rᵦᵢᵍ)` | Tamaño: small caps son más frágiles e ilíquidas |
| **HML** | `E(rₕᵢᵍₕ B/M) − E(rₗₒw B/M)` | Value vs growth: empresas value tienen mayor riesgo de distress |

Una cartera de small caps value cobra las tres primas simultáneamente — pero asume los tres riesgos.

## So-what para el examen

CAPM es un caso especial de APT con k=1. APT es más flexible pero requiere decidir los factores — esa decisión es donde vive todo el debate empírico en gestión de carteras. Si el examen pregunta por qué usar APT sobre CAPM: supuesto más débil (no arbitraje vs. equilibrio) y más capacidad explicativa.
