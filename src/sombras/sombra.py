"""Sombra proyectada sobre un punto a partir de un modelo digital de superficies."""

import math

import numpy as np

def desplazar(a, df, dc, relleno=-np.inf):
    """Devuelve una matriz en la que cada celda (f, c) contiene a[f + df, c + dc].
    Las celdas cuyo origen queda fuera de a se rellenan."""
    n_f, n_c = a.shape
    salida = np.full(a.shape, relleno, dtype=float)
    if abs(df) >= n_f or abs(dc) >= n_c:
        return salida  # el desplazamiento saca todo fuera de la matriz

    origen_f = slice(max(0, df), n_f - max(0, -df)) # filas de la matriz original a mover
    destino_f = slice(max(0, -df), n_f - max(0, df)) # filas de la matriz original donde se mueven
    origen_c = slice(max(0, dc), n_c - max(0, -dc)) # columnas de la matriz original a mover
    destino_c = slice(max(0, -dc), n_c - max(0, dc)) # columnas de la matriz original donde se mueven

    salida[destino_f, destino_c] = a[origen_f, origen_c] # hace el desplazamiento
    return salida


def hay_sombra(alturas, fila, col, acimut, elevacion, res=0.5, altura_observador=1.7, paso=0.25):
    """True si algo se interpone entre la celda (fila, col) y el sol.
    -. Alturas: el MDS de una ventana como un array normal en metros (celdas sin datos: NaN)
    -. Fila: fila del ráster dónde se encuentra el observador 
    -. Columna: columna del ráster dónde se encuentra el observador 
    -. Acimut: acimut del sol en e instante observado medido desde el norte
    -. Elevación: elevación del sol en e instante observado
    -. Res: resolución de las casillas del ráster (en el MDS del IGN 0.5mx0.5m)
    -. Altura_observador: altura del observador (modificable)
    -. Paso: cuanto avanza el rayo de sol horizontalmente en cada iteración (necesario para el cálculo)"""
    if elevacion <= 0:
        return True  # de noche no hay sol

    z_obs = alturas[fila, col] + altura_observador # altura base del punto + altura del observador
    este = math.sin(math.radians(acimut)) # cuánto se mueve al este el rayo por metro horizontal (seno del acimut)
    norte = math.cos(math.radians(acimut)) # cuánto se mueve al norte el rayo por metro horizontal (coseno del acimut)
    subida = math.tan(math.radians(elevacion)) # cuánto se sube el rayo por metro horizontal (tangente de la elevación)
    z_max = np.nanmax(alturas) # altura máxima en la ventana estudiada

    d = paso
    while True:
        f = fila - round(d * norte / res)  # fila donde está el rayo
        c = col + round(d * este / res)  # columna donde está el rayo
        if not (0 <= f < alturas.shape[0] and 0 <= c < alturas.shape[1]):
            return False  # el rayo sale de la ventana sin chocar
        z_rayo = z_obs + d * subida
        if z_rayo > z_max:
            return False  # el rayo ya está por encima de todo
        if alturas[f, c] > z_rayo:
            return True   # algo tapa el sol
        d += paso
