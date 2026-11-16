"""Lectura de ventanas del Modelo Digital de Superficies alrededor de un punto."""

from dataclasses import dataclass
from rasterio.crs import CRS
from rasterio.transform import Affine
from rasterio.merge import merge
from shapely.geometry import box
from shapely.ops import unary_union

import numpy as np
import rasterio
from pyproj import Transformer
from rasterio.windows import Window

@dataclass(frozen=True)
class Ventana:
    """Recorte cuadrado del MDS centrado en un punto."""

    alturas: np.ndarray  # altitudes en metros, NaN donde no hay dato
    fila: int  # fila del punto dentro de alturas
    col: int  # columna del punto dentro de alturas
    res: float  # lado de cada celda, en metros
    transformacion: Affine  # de (fila, columna) de la ventana a coordenadas del MDS
    crs: CRS  # sistema de referencia del MDS

def leer_ventana(rutas, lon, lat, radio):
    """Lee la ventana del MDS de ruta con radio metros alrededor de (lon, lat).
    Las coordenadas son WGS84 (EPSG:4326). Lanza ValueError si la ventana no cabe entera dentro del ráster"""
    if isinstance(rutas, str):
        rutas = [rutas]
    
    with rasterio.open(rutas[0]) as mds:
        crs, res, nodata = mds.crs, mds.res[0], mds.nodata
        a_mds = Transformer.from_crs("EPSG:4326", crs, always_xy=True) # transformador de coordenadas. Origen: EPSG:4326, destino: mds.crs (sistema del fichero)
        x, y = a_mds.transform(lon, lat) # transformación de coordenadas
        fila, col = mds.index(x, y) # convierte posición en fila y columna
        oeste_celda, norte_celda = mds.transform * (col, fila)

    huellas = []
    for ruta in rutas:
        with rasterio.open(ruta) as hoja:
            if hoja.crs != crs or hoja.res[0] != res or hoja.nodata != nodata:
                raise ValueError(f"{ruta} no es compatible con {rutas[0]}")
            huellas.append(box(*hoja.bounds))

    r = round(radio / res)
    oeste = oeste_celda - r * res
    norte = norte_celda + r * res
    este = oeste + (2 * r + 1) * res
    sur = norte - (2 * r + 1) * res

    if not box(oeste, sur, este, norte).within(unary_union(huellas)):
        raise ValueError(
            f"Las hojas no cubren la ventana de {radio} m: falta alguna hoja vecina."
        )

    datos, transformacion = merge(rutas, bounds=(oeste, sur, este, norte), res=res, nodata=nodata)
    alturas = datos[0].astype(float)
    alturas[alturas == nodata] = np.nan

    return Ventana(alturas=alturas, fila=r, col=r, res=res,
                   transformacion=transformacion, crs=crs)