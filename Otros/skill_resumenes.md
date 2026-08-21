---
name: resumen-estudio
description: "Usa esta skill cuando el usuario pida resumir un PDF académico o de apuntes de curso. Produce resúmenes en markdown calibrados al nivel del usuario: conocimiento básico del dominio, pero sin vocabulario técnico previo."
---

# Skill: Resumen de material de estudio

## A quién va dirigido

Alguien con base media en el tema: inteligente, sin jerga del dominio. Define cada término técnico la primera vez que aparece, en lenguaje directo. No uses analogías ni metáforas para simplificar — resultan condescendientes. Define y sigue adelante.

## Estructura del resumen

```markdown
# Módulo X — Temas N a M: Título

## Para qué sirve este bloque
[Por qué existe este bloque en el temario. Qué pregunta responde.
Si cubre varios instrumentos o marcos, explica desde el principio
por qué difieren — no solo que difieren.]

## Tema N: Título

### La idea central
[El insight clave del tema. Qué problema resuelve.]

### [Subsección]
[Contenido]

## Lo más importante para recordar
[Lista numerada de 4–6 items. Cada uno: afirmación en negrita + por qué importa.
Insights, no definiciones.]

## Conexión con el resto del módulo
[Tabla: concepto → dónde aparece después]
```

## Reglas de formato

- **Prosa, no bullets.** Los bullets solo para listas de items nombrados o tablas comparativas. Nunca para explicar razonamientos.
- **Fórmulas en LaTeX** cuando clarifican. Siempre con una frase explicando qué calcula y qué significa cada símbolo.
- **Negrita** solo para introducir un término técnico por primera vez.
- **Idioma:** español. Los términos técnicos en inglés se mantienen si así aparecen en el material fuente (yield to maturity, free cash flow, etc.).

## Profundidad

Cada tema principal: 300–600 palabras. Cada subsección: 100–250 palabras. Sin ejemplos numéricos salvo que sean la única forma de explicar el concepto. Sin derivaciones — enuncia resultados y explica su significado.

## Tono — ejemplo

**Mal (demasiado técnico):** "El YTM es la TIR del flujo de caja del bono bajo el supuesto de curva plana."

**Mal (demasiado simple):** "Imagina que el bono es como un préstamo a un amigo."

**Bien:** "El YTM es la rentabilidad anual efectiva que obtienes si compras el bono hoy al precio de mercado y lo mantienes hasta el vencimiento. Es la inversa de la fórmula de precio: dado el precio actual, ¿qué tasa de descuento lo justifica?"