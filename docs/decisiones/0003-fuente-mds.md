# 0003 — Usar el MDS de 0,5 m del IGN como fuente de geometría

## Estado
Aceptado (2026-11-11)

## Contexto
Para saber qué tapa el sol hace falta la altura de edificios y árboles alrededor del punto. El PNOA-LiDAR (3ª cobertura, vuelo de Madrid en marzo–mayo de 2024, 5 puntos/m²) permite obtenerla de dos formas: usar el Modelo Digital de Superficies que publica el IGN o generarlo desde la nube de puntos.

## Decisión
Usar el MDS de 0,5 m del IGN (versión 1, provisional), leído con rasterio. El sistema de referencia se lee siempre de la cabecera del fichero, nunca se supone a partir del nombre.

## Consecuencias
+ Un solo ráster listo para usar: el algoritmo de sombra se puede validar sin depender del procesado del LiDAR.
+ Resolución de 0,5 m, suficiente para distinguir aceras.
− Edificios y vegetación en una sola superficie: los árboles dan sombra total y constante, aunque en la realidad dejan pasar luz y algunos pierden la hoja en invierno.
− Modelo 2,5D: una sola altura por celda (no hay soportales ni huecos bajo las copas).
− Fachadas interpoladas: los bordes se difuminan entre 1,5 y 3 m.
− Es una foto de la primavera de 2024: incluye coches, grúas y el follaje de esas semanas.
− Versión provisional: la definitiva puede cambiar los valores (se registra el SHA-256 en `data/README.md`).
− La cabecera declara EPSG:3042 (ejes N-E), no EPSG:25830 como sugiere el nombre.

## Alternativas consideradas
Generar el MDS desde la nube de puntos con PDAL, separando edificios (clase 6) y vegetación (clase 5): queda como evolución futura. MDS de 5 m (MDS05): resolución insuficiente para calles estrechas.