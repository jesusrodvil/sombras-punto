"""Sombra proyectada sobre un punto a partir de un modelo digital de superficies."""

import math

import numpy as np

def hay_sombra(alturas, fila, col, acimut, elevacion, res=0.5, altura_observador=1.7, paso=0.25):
    """True si algo se interpone entre la celda (fila, col) y el sol.
    -. Alturas: el MDS de una ventana como un array normal
    -. Fila: fila del ráster dónde se encuentra el observador 
    -. Columna: columna del ráster dónde se encuentra el observador 
    -. Acimut: acimut del sol en e instante observado
    -. Elevación: elevación del sol en e instante observado
    -. Res: resolución de las casillas del ráster (en el MDS del IGN 0.5mx0.5m)
    -. Altura_observador: altura del observador (modificable)
    -. Paso: cuanto avanza el rayo de sol horizontalmente en cada iteración (necesario para el cálculo)"""
    if elevacion <= 0:
        return True  # de noche no hay sol

    z_obs = alturas[fila, col] + altura_observador # altura base del punto + altura del observador
    este = math.sin(math.radians(acimut)) # cuánto se mueve al este el rayo (seno del acimut)
    norte = math.cos(math.radians(acimut)) # cuánto se mueve al norte el rayo (coseno del acimut)
    subida = math.tan(math.radians(elevacion)) # cuánto se sube el rayo (tangente de la elevación)
    z_max = np.nanmax(alturas) # altura máxima en la ventana estudiada

    d = paso
    while True:
        f = round(fila - d * norte / res) # fila avanzada en esta iteración
        c = round(col + d * este / res) # columna avanzada en esta iteración
        if not (0 <= f < alturas.shape[0] and 0 <= c < alturas.shape[1]):
            return False  # el rayo sale de la ventana sin chocar
        z_rayo = z_obs + d * subida
        if z_rayo > z_max:
            return False  # el rayo ya está por encima de todo
        if alturas[f, c] > z_rayo:
            return True   # algo tapa el sol
        d += paso