# 0005 — Calcular mapas de sombra desplazando el MDS completo

## Estado
Aceptado (2026-11-12)

## Contexto
Aplicar la marcha de rayos celda a celda en Python cuesta unos 150 µs por celda: unos 100 s por ventana de 400 × 400 m y hora, y del orden de cuatro días por hora para todo el municipio de Madrid.

## Decisión
Intercambiar los bucles: en cada paso se avanzan los rayos de todas las celdas a la vez, desplazando el MDS completo con NumPy y comparándolo con la altura de los rayos (técnica de análisis ráster urbano descrita por Ratti y Richens, 2004, y usada por SOLWEIG). La implementación celda a celda (`hay_sombra`) se conserva como referencia.

## Consecuencias
+ Unas 275 veces más rápido (0,39 s por ventana y hora) sin código compilado.
+ Mismo resultado celda a celda que `hay_sombra`, comprobado con un test oráculo sobre escenas aleatorias.
− Sigue comparando celdas que ya están en sombra (trabajo redundante).
− Memoria proporcional a la ventana en cada paso: la ciudad entera exige trabajar por teselas con búfer.

## Alternativas consideradas
Compilar el bucle celda a celda con Numba o C++ (se reserva para cuando el rendimiento lo exija), paralelizar por ventanas (compatible con esta decisión).