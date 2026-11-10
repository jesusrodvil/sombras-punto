"""Posición del sol vista desde un punto de la superficie terrestre."""

from dataclasses import dataclass

import pandas as pd
import pvlib

ZONA_HORARIA = "Europe/Madrid"

@dataclass(frozen=True)
class Punto:
    """Punto en cordenadas geográficas WGS84 (EPSG:4326, lat y lon)"""

    lat: float # grados decimales positivo al norte
    lon: float # grados decimales positivo al este
    altitud: float = 0.0 # m sobre nivel del mar

def posicion_solar(punto: Punto, instantes: pd.DatetimeIndex) -> pd.DataFrame:
    """Elevación y acimut del sol en cada instante
    acimut: coordenada horizontal que indica la dirección en la que se encuentra el Sol a lo largo del horizonte"""

    if instantes.tz is None: # si no tiene tz asignada, el sistema asume UTC
        raise ValueError(
            "Los instantes deben llevar zona horaria (p. ej. tz='Europe/Madrid')."
        )
    
    ubicacion = pvlib.location.Location(punto.lat, punto.lon, altitude=punto.altitud) # objeto de pvlib que representa un punto
    pos = ubicacion.get_solarposition(instantes) # ejecuta el algoritmo SPA y devuelve tabla con 6 columnas

    return pd.DataFrame(
        {
            "elevacion": pos["apparent_elevation"], # la elevación con la refracción de la atmósfera incluida, (la sombra proyecta la luz que llega de verdad)
            "acimut": pos["azimuth"], # medido desde el norte en sentido horario (N = 0°, E = 90°, S = 180°, O = 270°)
        },
        index=instantes,
    )

def instantes_del_dia(fecha: str, paso: str= "1h", zona: str = ZONA_HORARIA) -> pd.DatetimeIndex:
    """Devuelve instantes de un día completo en hora local, 'paso' indica cada cuanto se registra un instante
    Se usa DateOffset en vez de Timedelta para que los días de cambio horario no se vean afectados"""

    inicio = pd.Timestamp(fecha, tz=zona) # medianoche local de la fecha
    fin = inicio + pd.DateOffset(days=1) # justamente medianoche del día siguiente
    return pd.date_range(inicio, fin, freq=paso, inclusive="left") # inclusive="left" incluye el inicio pero no el final (24 instantes por día)

