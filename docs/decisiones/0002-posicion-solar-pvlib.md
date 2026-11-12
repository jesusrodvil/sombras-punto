# 0002 — Calcular la posición solar con pvlib (algoritmo SPA)

## Estado
Aceptado (2026-11-10)

## Contexto
El cálculo de sombras necesita la elevación y el acimut del sol para un lugar e instante dados. Es un problema astronómico resuelto, pero con detalles delicados (tiempo astronómico, nutación, refracción) en los que es fácil equivocarse.

## Decisión
Usar `pvlib.location.Location.get_solarposition`, que por defecto implementa el SPA del NREL (Reda y Andreas, 2004), encapsulado en `sombras.sol`. Convenios:
- elevación aparente (con refracción), porque la sombra la proyecta la luz
  que llega realmente;
- acimut en grados desde el norte en sentido horario;
- instantes obligatoriamente con zona horaria (pvlib asume UTC si no la tienen).

## Consecuencias
+ Precisión de ±0,0003° (años −2000 a 6000), muy por encima de lo necesario.
+ Algoritmo publicado y citable; cálculo determinista y sin conexión.
+ pvlib queda aislado en un módulo: cambiarlo solo afecta a `sol.py`.
− Refracción calculada con atmósfera estándar y 12 °C, no con datos reales; el efecto solo es apreciable cerca del horizonte.

## Alternativas consideradas
Implementar el SPA a mano (riesgo de errores sin beneficio), fórmulas
simplificadas de declinación y ecuación del tiempo (error de décimas de grado).