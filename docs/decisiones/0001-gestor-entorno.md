# 0001 — Usar pixi como gestor de entorno

## Estado
Aceptado (2026-11-10)

## Contexto
El proyecto depende de librerías geoespaciales nativas (GDAL, PDAL) y puede necesitar compiladores de C++ para núcleos de alto rendimiento. Debe reproducirse de forma idéntica en el portátil y en las máquinas de cómputo, y ser verificable por el tribunal.

## Decisión
Usar pixi, con conda-forge como canal principal y PyPI solo para paquetes Python puros no disponibles en conda-forge.

## Consecuencias
+ Librerías nativas y compiladores gestionados por el mismo lockfile.
+ Entorno local al proyecto; tareas integradas (pixi run ...).
− Herramienta joven, menos conocida que conda o uv.
− Para el paso 1 (pvlib + numpy) uv habría bastado.

## Alternativas consideradas
uv (sin soporte de librerías nativas), conda (entornos globales, lockfile aparte), pip + venv (ni nativas ni lockfile).