"""Lectura de ventanas del Modelo Digital de Superficies alrededor de un punto."""

from dataclasses import dataclass

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

def leer_ventana(ruta, lon, lat, radio):
    """Lee la ventana del MDS de ruta con radio metros alrededor de (lon, lat).
    Las coordenadas son WGS84 (EPSG:4326). Lanza ValueError si la ventana no cabe entera dentro del ráster"""
    with rasterio.open(ruta) as mds:
        a_mds = Transformer.from_crs("EPSG:4326", mds.crs, always_xy=True) # transformador de coordenadas. Origen: EPSG:4326, destino: mds.crs (sistema del fichero)
        x, y = a_mds.transform(lon, lat) # transformación de coordenadas
        fila, col = mds.index(x, y) # convierte posición en fila y columna
        res = mds.res[0] # mds.res contiene (ancho, alto) de una celda en m
        r = round(radio / res) # pasa radio a celdas

        if col - r < 0 or fila - r < 0 or col + r >= mds.width or fila + r >= mds.height: # verifica si la ventana se sale por alguno de los cuatro lados
            raise ValueError(
                f"La ventana de {radio} m se sale del ráster: el punto está demasiado cerca del borde de la hoja."
            )

        ventana = Window(col_off=col - r, row_off=fila - r, width=2 * r + 1, height=2 * r + 1) # descripción de la ventana a aleer
        alturas = mds.read(1, window=ventana, masked=True).filled(np.nan)

    return Ventana(alturas=alturas, fila=r, col=r, res=res)