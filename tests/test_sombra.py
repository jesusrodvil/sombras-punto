import math

import numpy as np
import pytest

from sombras.sombra import hay_sombra

RES = 0.5  # metros por celda, como el MDS del IGN
OBS = 1.7  # altura del observador usada en los tests

def escena_muro(distancia, altura, n=101):
    """Suelo plano a 0 m y un muro de altura m que empieza distancia m al sur.
    Devuelve la matriz de alturas y el índice de la celda central"""
    alturas = np.zeros((n, n))
    centro = n // 2
    fila_muro = centro + round(distancia / RES) # fila donde empieza el muro
    alturas[fila_muro:, :] = altura
    return alturas, centro

@pytest.mark.parametrize(
    "elevacion, esperado",
    [
        (50, True),   # sol bajo: el muro lo tapa
        (70, False),  # sol alto: el rayo pasa por encima
    ],
)
def test_muro_al_sur_tapa_el_sol_bajo(elevacion, esperado):
    alturas, centro = escena_muro(distancia=5, altura=10)
    resultado = hay_sombra(alturas, centro, centro, acimut=180, elevacion=elevacion,
                           res=RES, altura_observador=OBS)
    assert resultado == esperado

def test_muro_detras_del_observador_no_tapa_el_sol():
    alturas, centro = escena_muro(distancia=5, altura=10)
    assert not hay_sombra(alturas, centro, centro, acimut=0, elevacion=30,
                          res=RES, altura_observador=OBS)