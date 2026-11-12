# sombras-punto

Prototipo que calcula a qué horas está a la sombra un punto de Madrid, a partir
del Modelo Digital de Superficies del IGN y la posición del sol.

## Cómo funciona

1. **Posición del sol** (`sombras.sol`): elevación y acimut en cada instante, con el algoritmo SPA a través de pvlib.
2. **Geometría** (`sombras.mds`): recorte del MDS de 0,5 m alrededor del punto.
3. **Sombra** (`sombras.sombra`): se lanza un rayo desde cada celda hacia el sol; si choca con el MDS, la celda está a la sombra. Para mapas completos, los rayos de todas las celdas avanzan a la vez desplazando el MDS.

A partir de ahí se obtienen mapas de sombra de un instante y mapas de horas de sol de un día.

## Estructura

```
src/sombras/        código del paquete
  sol.py            posición solar
  mds.py            lectura de ventanas del MDS
  sombra.py         cálculo de sombras y horas de sol
tests/              tests (pytest)
docs/decisiones/    registro de decisiones de arquitectura (ADR)
data/README.md      registro de datos externos y cómo obtenerlos
data/raw/           datos descargados (no se versionan)
```

## Instalación

Requiere [pixi](https://pixi.sh):

```bash
pixi install
```

Instala Python, las librerías y sus dependencias nativas (GDAL, PROJ) en las versiones exactas de `pixi.lock`. Ver [ADR 0001](docs/decisiones/0001-gestor-entorno.md).

## Datos

El MDS no está en el repositorio. Descarga la hoja indicada en [`data/README.md`](data/README.md), guárdala en `data/raw/` y comprueba que es la misma versión:

```bash
sha256sum data/raw/MDS50CM-ETRS89-H30_0559-5-5-COB3-V1.tif
```

El resultado debe coincidir con el SHA-256 de `data/README.md`

## Tests

```bash
pixi run -e test test
```

Las funciones de sombra se validan con escenas sintéticas cuyo resultado se conoce por geometría, y la versión rápida (`mapa_sombra`) contra la de referencia (`hay_sombra`) celda a celda.

## Decisiones

Las decisiones de diseño están en [`docs/decisiones/`](docs/decisiones/):

- [0001](docs/decisiones/0001-gestor-entorno.md) — pixi como gestor de entorno
- [0002](docs/decisiones/0002-posicion-solar-pvlib.md) — posición solar con pvlib
- [0003](docs/decisiones/0003-fuente-mds.md) — MDS de 0,5 m del IGN
- [0004](docs/decisiones/0004-modelo-de-sombra.md) — modelo geométrico de sombra
- [0005](docs/decisiones/0005-mapa-por-desplazamiento.md) — mapas por desplazamiento del MDS

## Limitaciones conocidas

- Edificios y árboles se tratan igual: los árboles dan sombra total (ADR 0003).
- Los objetos fuera de la ventana se ignoran: cerca de los bordes hay más sol del real (ADR 0004).
- `sombras.mds` no tiene tests: se ha validado manualmente; hay que probar la transformación de coordenadas antes de reutilizarlo en el precálculo.

## Licencia y atribución

Los datos del MDS son © Instituto Geográfico Nacional (PNOA-LiDAR), con licencia compatible con CC BY 4.0.