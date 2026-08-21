---
date: 2026-07-27
tags: [bonos, duración, renta-fija, sensibilidad, módulo-7]
---

# ¿Qué es la duración de un bono?

## Definición

La **duración** mide la sensibilidad del precio de un bono ante cambios en el tipo de interés. Tiene dos interpretaciones complementarias:

1. **Vencimiento medio ponderado de los flujos de caja:** promedio de los momentos en que el bono paga, ponderado por el valor presente de cada flujo.
2. **Elasticidad precio-tipo:** porcentaje de caída en precio por cada punto porcentual de subida en el tipo de descuento.

## Duración de Macaulay

$$D_{Mac} = \frac{\sum_{t=1}^{T} t \cdot \frac{C_t}{(1+y)^t}}{P} = \sum_{t=1}^{T} t \cdot \frac{PV_t}{P}$$

donde $C_t$ es el flujo en el periodo $t$, $y$ el yield to maturity, $P$ el precio del bono, y $PV_t = C_t/(1+y)^t$ el valor presente del flujo $t$. Las dos formas son equivalentes: la segunda es notación compacta que deja ver directamente que la duración es la media ponderada de los plazos, con pesos $PV_t/P$ (fracción del precio que representa cada flujo).

Para un bono cupón cero, $D_{Mac} = T$ (vencimiento). Para un bono con cupones, $D_{Mac} < T$ porque los cupones intermedios adelantan parte del cash flow.

## Duración modificada

Es la métrica operativa para medir sensibilidad:

$$D_{mod} = \frac{D_{Mac}}{1+y}$$

La aproximación lineal del cambio en precio es:

$$\frac{\Delta P}{P} \approx -D_{mod} \cdot \Delta y$$

Un bono con $D_{mod} = 5$ pierde aproximadamente un 5% de precio si el tipo sube 100 bps.

## Factores que determinan la duración

| Factor | Efecto sobre duración |
|---|---|
| Cupón más alto | Reduce (más flujos adelantados) |
| Vencimiento más largo | Aumenta |
| Yield más alto | Reduce (descuenta más los flujos lejanos) |
| Bono cupón cero | Duración = vencimiento (máxima para ese plazo) |

## DV01 (Dollar Value of a Basis Point)

El DV01 es el cambio en valor absoluto (en euros/dólares) ante un movimiento de 1 bp (0,01%) en el tipo, en cualquier dirección. Por convención se expresa como número positivo y representa la pérdida ante una subida de 1 bp — pero la magnitud es simétrica: una bajada de 1 bp produce una ganancia del mismo importe (a efectos de primer orden). La asimetría entre subidas y bajadas la captura la convexidad, no el DV01.

$$DV01 = D_{mod} \cdot P \cdot 0{,}0001$$

Es la versión monetaria de la duración modificada. Mientras $D_{mod}$ da la sensibilidad en términos porcentuales, el DV01 la da en unidades de precio — útil para agregar riesgo entre bonos de distinto nominal.

Ejemplo: bono con $P = 1.000.000$€, $D_{mod} = 5$ → $DV01 = 5 \times 1.000.000 \times 0{,}0001 = 500$€/bp.

En gestión de carteras y trading se usa el DV01 para dimensionar coberturas: si quieres neutralizar el riesgo de tipo de interés con futuros de bono, calculas cuántos contratos necesitas para igualar el DV01 de la posición.

## Convexidad: el término que Macaulay ignora

La duración es una aproximación de primer orden. Para movimientos grandes en tipos, hay que añadir el término de convexidad:

$$\frac{\Delta P}{P} \approx -D_{mod} \cdot \Delta y + \frac{1}{2} \cdot C \cdot (\Delta y)^2$$

La convexidad siempre es positiva para bonos ordinarios: el precio sube más de lo que baja ante movimientos simétricos de tipos — asimetría favorable al inversor.

## So-what para el examen

- La duración es el KPI central de riesgo de tipo de interés en renta fija; una cartera con $D_{mod}$ alta es muy vulnerable a subidas de tipos.
- En gestión de carteras, se usan duraciones objetivo: si anticipas subida de tipos, reduces duración (acortas vencimientos o aumentas peso de bonos con cupón alto).
- La duración de una cartera de bonos es la media ponderada de las duraciones individuales — propiedad que permite inmunización de carteras.
- Convexidad positiva = ventaja; en estrategias de "barbell" (bonos cortos + largos) se obtiene más convexidad que en "bullet" (bonos de plazo medio) con la misma duración.
