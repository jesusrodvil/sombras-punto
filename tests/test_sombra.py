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