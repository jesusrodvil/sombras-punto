"""pixi run -e test test -v"""
import pandas as pd
import pytest
import pvlib

from sombras.sol import Punto, instantes_del_dia, posicion_solar
from typing import Literal

PUNTO = Punto(lat=40.402639, lon=-3.680472, altitud=650)
OBLICUIDAD = 23.44  # inclinación del eje terrestre, en grados

def momento_solar(fecha: str, momento: Literal["sunrise", "sunset", "transit"]) -> pd.DatetimeIndex:
    dia = pd.DatetimeIndex([pd.Timestamp(fecha, tz="Europe/Madrid")]) # se pasa como lista porque DatetineIndex necesita que sea así
    transito = pvlib.solarposition.sun_rise_set_transit_spa(dia, PUNTO.lat, PUNTO.lon) # transito: mediodia solar. solarposition.sun_rise_set_transit_spa devuelve salida (sunrise), puesta (sunset) y mediodía (transit)
    return pd.DatetimeIndex(transito[momento])

@pytest.mark.parametrize(
    "fecha", 
    [
        "2026-06-21", # días cualesquiera
        "2026-11-10", 
        "2026-12-21"
    ]
)

def test_sol_al_este_y_oeste(fecha):
    pos_salida = posicion_solar(PUNTO, momento_solar(fecha, "sunrise")).iloc[0] # iloc[0]: toma la primera fila por posición (integer location)
    pos_puesta = posicion_solar(PUNTO, momento_solar(fecha, "sunset")).iloc[0]
    assert 0 < pos_salida.acimut < 180    # mitad este del horizonte. El sol sale por el este
    assert 180 < pos_puesta.acimut < 360  # mitad oeste del horizonte. El sol sale por el oeste

@pytest.mark.parametrize(
    "fecha, horas",
    [
        ("2026-11-10", 24),  # día normal
        ("2026-03-29", 23),  # cambio a horario de verano
        ("2026-10-25", 25),  # cambio a horario de invierno
    ],
)

def test_instantes_por_dia(fecha, horas):
    assert len(instantes_del_dia(fecha)) == horas

@pytest.mark.parametrize(
    "fecha, declinacion", # declinación: latitud a la que el sol cae en vertical. +23.44 en verano, -23.44 en invierno
    [
        ("2026-06-21", +OBLICUIDAD), # verano
        ("2026-12-21", -OBLICUIDAD) # invierno
    ],
)

def test_elevacion_en_mediodia_de_solsticio(fecha, declinacion):
    pos = posicion_solar(PUNTO, momento_solar(fecha, "transit")).iloc[0]
    esperada = 90 - PUNTO.lat + declinacion # si estuvieramos en el ecuador (latitud 0) en un equinoccio (declinación 0), el sol pasaría justo por encima de nosotros 90°
    assert pos.elevacion == pytest.approx(esperada, abs=0.05) # margen absoluto de 0.05º
    assert pos.acimut == pytest.approx(180, abs=0.1) # margen absoluto de 0.1º. En el mediodía solar, el sol está exactamente al sur: 180° en nuestro convenio (N = 0°, E = 90°, S = 180°)

