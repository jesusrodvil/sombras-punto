## MDS 0,5 m — hoja MDS50CM

- Producto: Modelo Digital de Superficies 0,5 m, PNOA-LiDAR 3ª cobertura, versión 1 (provisional)
- Origen: Centro de Descargas del CNIG — Modelos Digitales de Elevaciones
- Fecha de descarga: 2026-11-11
- Vuelo: Comunidad de Madrid, marzo–mayo 2024
- Sistema de referencia: EPSG:3042 (ETRS89 / UTM 30N, ejes N-E), declarado en la cabecera del GeoTIFF; misma proyección que EPSG:25830
- Licencia: uso libre compatible con CC BY 4.0, citando al IGN
- Ubicación local: data/raw/

## Cartografía municipal 1:1000

- Producto: Cartografía municipal a escala 1:1000 del Ayuntamiento de Madrid, versión 2016
- Origen: Portal de datos abiertos del Ayuntamiento de Madrid — "Cartografía municipal por distritos a escala 1:1000, formato SHP, ETRS89"
- Fichero descargado: 03.Retiro.zip
- Fecha de descarga: 2026-11-13
- Capas usadas:
  - `acera_p`: aceras (polígonos)
  - `acera_nivel_p`: aceras al mismo nivel que la calzada (polígonos)
  - `acera_isleta_L`: contorno de isletas (líneas; no se usa por ahora)
- Campos: objectid, nivel, id_cd, shape_star (área, m²), shape_stle (perímetro, m). Los dos últimos son Shape_STArea y Shape_STLength truncados por el límite de 10 caracteres del formato Shapefile.
- Sistema de referencia: EPSG:25830 (ETRS89 / UTM 30N), comprobado en QGIS para las tres capas
- Licencia: licencia propia del portal de datos abiertos del Ayuntamiento de Madrid; exige citar el origen de los datos y la fecha de su última actualización
- Ubicación local: data/raw/aceras
- Validación: encaja con la ortofoto del PNOA y con el MDS