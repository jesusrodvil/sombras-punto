"""Sombra proyectada sobre un punto a partir de un modelo digital de superficies."""

import math

import numpy as np

def desplazar(a, df, dc, relleno=-np.inf):
    """Devuelve una matriz en la que cada celda (f, c) contiene a[f + df, c + dc].
    Las celdas cuyo origen queda fuera de a se rellenan."""
    n_f, n_c = a.shape # número de filas y columnas
    salida = np.full(a.shape, relleno, dtype=float)
    if abs(df) >= n_f or abs(dc) >= n_c:
        return salida  # el desplazamiento saca todo fuera de la matriz

    origen_f = slice(max(0, df), n_f - max(0, -df)) # filas que se leen del original
    destino_f = slice(max(0, -df), n_f - max(0, df)) # filas de la salida donde se escriben
    origen_c = slice(max(0, dc), n_c - max(0, -dc)) # columnas que se leen del original
    destino_c = slice(max(0, -dc), n_c - max(0, dc)) # columnas de la salida donde se escriben

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


def mapa_sombra(alturas, acimut, elevacion, res=0.5, altura_observador=1.7, paso=0.25):
    """Matriz booleana: True en las celdas de alturas que están a la sombra.
    Equivale a llamar a hay_sombra en cada celda, pero avanza los rayos de
    todas las celdas a la vez desplazando la matriz completa en cada paso"""

    if elevacion <= 0:
        return np.ones(alturas.shape, dtype=bool) # si es de noche todo está a la sombra

    z_obs = alturas + altura_observador # en este caso se suma al altura de observador a todos los puntos de cada celda
    este = math.sin(math.radians(acimut))
    norte = math.cos(math.radians(acimut))
    subida = math.tan(math.radians(elevacion))
    desnivel = np.nanmax(alturas) - np.nanmin(z_obs) # medida para atajo si todos nos rayos superan el desnivel
    n_f, n_c = alturas.shape

    sombra = np.zeros(alturas.shape, dtype=bool) # inicializa la matriz en 0
    d = paso
    while d * subida <= desnivel:
        df = -round(d * norte / res) # avance en filas
        dc = round(d * este / res) # avance en columnas

        if abs(df) >= n_f or abs(dc) >= n_c:
            break  # todos los rayos han salido de la ventana

        terreno = desplazar(alturas, df, dc) # altura del terreno en cada casilla tras desplazamiento
        sombra |= (terreno > z_obs + d * subida) # compara y comprueba todas las celdas (si un casilla = True: el terreno supera al rayo y hay un obstáculo a esa distancia) Luego hace or con sombra
        d += paso
    return sombra


def sombra_en_celdas(alturas, filas, cols, acimut, elevacion, res=0.5, altura_observador=1.7, paso=0.25):
    """Sombra en una lista de celdas: True si la celda (filas[i], cols[i]) está a la sombra.
    Equivale a mapa_sombra(...)[filas, cols], pero solo lanza rayos desde esas
    celdas y deja de calcular cada una en cuanto su resultado está decidido.
    Los obstáculos siguen siendo todo alturas."""

    sombra = np.zeros(len(filas), dtype=bool)
    if elevacion <= 0:
        sombra[:] = True  # de noche, todas a la sombra
        return sombra

    n_f, n_c = alturas.shape
    este = math.sin(math.radians(acimut))
    norte = math.cos(math.radians(acimut))
    subida = math.tan(math.radians(elevacion))
    z_max = np.nanmax(alturas)
    z_obs = alturas[filas, cols] + altura_observador

    vivas = np.arange(len(filas))  # posiciones en la lista de las celdas aún sin decidir
    d = paso
    while vivas.size > 0:
        df = -round(d * norte / res)
        dc = round(d * este / res)
        f = filas[vivas] + df
        c = cols[vivas] + dc
        z_rayo = z_obs[vivas] + d * subida

        dentro = (f >= 0) & (f < n_f) & (c >= 0) & (c < n_c)
        sigue = dentro & (z_rayo <= z_max)
        choca = np.zeros(vivas.size, dtype=bool)
        choca[sigue] = alturas[f[sigue], c[sigue]] > z_rayo[sigue]

        sombra[vivas[choca]] = True
        vivas = vivas[sigue & ~choca]
        d += paso
    return sombra


def horas_de_sol(alturas, acimuts, elevaciones, horas_por_instante, res=0.5, altura_observador=1.7, paso=0.25):
    """Horas de sol directo de cada celda de alturas a lo largo de varios instantes.
    acimuts y elevaciones dan la posición del sol en cada instante, y cada instante cuenta como horas_por_instante horas (0.25 si se muestrea cada 15 minutos)"""
    total = np.zeros(alturas.shape)
    for acimut, elevacion in zip(acimuts, elevaciones):
        if elevacion > 0:
            al_sol = ~mapa_sombra(alturas, acimut, elevacion, res=res, altura_observador=altura_observador, paso=paso)
            total += al_sol
    return total * horas_por_instante

def horas_de_sol_en_celdas(alturas, filas, cols, acimuts, elevaciones, horas_por_instante, res=0.5, altura_observador=1.7, paso=0.25):
    """Horas de sol directo de cada celda (filas[i], cols[i]) a lo largo de varios instantes."""
    total = np.zeros(len(filas))
    for acimut, elevacion in zip(acimuts, elevaciones):
        if elevacion > 0:
            total += ~sombra_en_celdas(alturas, filas, cols, acimut, elevacion, res=res, altura_observador=altura_observador, paso=paso)
    return total * horas_por_instante