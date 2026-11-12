# 0004 — Modelo geométrico de sombra: marcha de rayos sobre el MDS

## Estado
Aceptado (2026-11-11)

## Contexto
Hay que decidir qué significa que un punto "está a la sombra" y cómo se calcula sobre un ráster. El sombreado del relieve (hillshade) no sirve: solo depende de la orientación de cada celda y no detecta obstáculos.

## Decisión
Un punto está a la sombra si un rayo lanzado desde él hacia el sol choca con el MDS. El rayo avanza en pasos fijos y en cada uno compara su altura con la del terreno. Supuestos:
- observador a 1,7 m sobre el suelo, media de altura de un adulto; 
- paso de media celda (0,25 m), para no saltarse celdas;
- vecino más próximo, redondeando solo el desplazamiento (no la posición absoluta) para que el resultado no dependa de la paridad de la celda;
- sombra binaria: sin penumbra ni transmisión de luz por la vegetación;
- de noche (elevación ≤ 0) todo está a la sombra;
- un rayo que sale de la ventana sin chocar llega al sol;
- las celdas sin dato (NaN) nunca tapan el sol.

## Consecuencias
+ Modelo sencillo y verificable con geometría: los tests comparan el límite de sombra con atan(altura / distancia).
+ Mismo enfoque que el cálculo de sombras de SOLWEIG.
− La discretización introduce una incertidumbre de media celda en las distancias; pesa más con obstáculos cercanos (hasta 1,3° a 5 m).
− Los objetos fuera de la ventana se ignoran: la ventana necesita un margen mayor que la sombra más larga que se quiera captar.
− Resultado sensible a la altura del observador, que es una elección de modelo, no un dato.

## Alternativas consideradas
Hillshade (no proyecta sombras), interpolación bilineal entre celdas (posible mejora, sin evaluar), sombra parcial de la vegetación (requiere separar árboles: ver 0003).