"""Posición del sol vista desde un punto de la superficie terrestre."""

from dataclasses import dataclass

import pandas as pd
import pvlib

@dataclass(frozen=True)
class Punto:
    """Punto en cordenadas geográficas WGS84 (EPSG:4326, lat y lon)"""

    lat: float # grados decimales positivo al norte
    lon: float # grados decimales positivo al este
    altitud: float = 0.0 # m sobre nivel del mar

def posicion_solar(punto: Punto, instantes: pd.DatetimeIndex) -> pd.DataFrame:
    """Elevación y acimut del sol en cada instante"""
    """acimut: coordenada horizontal que indica la dirección en la que se encuentra el Sol a lo largo del horizonte"""

    if instantes.tz is None: # si no tiene tz asignada, el sistema asume UTC
        raise ValueError(
            "Los instantes deben llevar zona horaria (p. ej. tz='Europe/Madrid')."
        )
    
    ubicacion = pvlib.location.Location(punto.lat, punto.lon, altitude=punto.altitud) # objeto de pvlib que representa un punto
    pos = ubicacion.get_solarposition(instantes) # ejecuta el algoritmo SPA y devuelve tabla con 6 columnas

    return pd.DataFrame(
        {
            "elevacion": pos["apparent_elevation"], # la elevación con la refracción de la atmósfera incluida, (la sombra la proyecta la luz que llega de verdad)
            "acimut": pos["azimuth"], # medido desde el norte en sentido horario (N = 0°, E = 90°, S = 180°, O = 270°)
        },
        index=instantes,
    )