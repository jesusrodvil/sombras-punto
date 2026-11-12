import math

import numpy as np
import pytest

from sombras.sombra import hay_sombra, mapa_sombra, horas_de_sol

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

def ciudad_aleatoria(n, semilla):
    """Escena de n × n celdas con suelo algo irregular y bloques de 5 a 45 m."""
    rng = np.random.default_rng(semilla)
    alturas = rng.normal(0, 0.05, size=(n, n))
    for _ in range(n // 7):
        f, c = rng.integers(0, n - 5, size=2)
        alto, ancho = rng.integers(5, 30, size=2)
        alturas[f:f + alto, c:c + ancho] = rng.uniform(5, 45)
    alturas[3, 7] = np.nan  # una celda sin dato
    return alturas


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


def test_de_noche_siempre_hay_sombra():
    alturas = np.zeros((11, 11))
    assert hay_sombra(alturas, 5, 5, acimut=180, elevacion=-10,
                      res=RES, altura_observador=OBS)


@pytest.mark.parametrize(
    "distancia, altura",
    [
        (5, 10),   # muro medio
        (3, 20),   # muro alto y cercano: límite muy vertical
        (10, 6),   # muro bajo y lejano: límite casi horizontal
    ],
)
def test_limite_de_sombra_coincide_con_la_geometria(distancia, altura):
    alturas, centro = escena_muro(distancia=distancia, altura=altura)
    sube = altura - OBS # cuánto tiene que subir el rayo para superar el muro
    lim_inf = math.degrees(math.atan(sube / distancia))
    lim_sup = math.degrees(math.atan(sube / (distancia - RES / 2)))

    assert hay_sombra(alturas, centro, centro, acimut=180, elevacion=lim_inf - 0.5,
                      res=RES, altura_observador=OBS)
    assert not hay_sombra(alturas, centro, centro, acimut=180, elevacion=lim_sup + 0.5,
                          res=RES, altura_observador=OBS)


@pytest.mark.parametrize("acimut", [0, 90, 180, 270])
def test_siempre_sol_con_altura_max(acimut):
    alturas = np.zeros((11, 11))
    assert not hay_sombra(alturas,  5, 5, acimut, elevacion=10,
                              res=RES, altura_observador=OBS)


@pytest.mark.parametrize("acimut", [0, 90, 180, 270])
def test_rayo_sale_por_el_borde(acimut):
    alturas = np.zeros((101, 101))
    alturas[0, 10] = 1000  # pilar fuera del camino: solo sirve para que z_max sea alto
    assert not hay_sombra(alturas, 50, 50, acimut=acimut, elevacion=30,
                          res=RES, altura_observador=OBS)


@pytest.mark.parametrize(
    "acimut, elevacion",
    [
        (180, 32), 
        (135, 15), 
        (220, 8), 
        (0, 30), 
        (90, 20), 
        (45, 10), 
        (300, 5), 
        (17.3, 22.2)
    ],
)
def test_mapa_coincide_con_hay_sombra(acimut, elevacion):
    alturas = ciudad_aleatoria(41, semilla=1) # tamaño acotado 41x41, un tamaño más grande alargaría el tiempo que toman los tests
    mapa = mapa_sombra(alturas, acimut, elevacion, res=RES, altura_observador=OBS) # intento con mapa_sombra
    referencia = np.array([ # intento con hay_sombra para cada celda 1 a 1
        [hay_sombra(alturas, f, c, acimut, elevacion, res=RES, altura_observador=OBS) for c in range(alturas.shape[1])]
        for f in range(alturas.shape[0])
    ])
    np.testing.assert_array_equal(mapa, referencia) # comprueba que sean iguales


def test_horas_de_sol_en_suelo_plano_son_las_horas_de_dia():
    alturas = np.zeros((11, 11))
    elevaciones = [-10, 5, 30, 50, 30, 5, -10]  # noche, día, noche
    acimuts = [90, 110, 150, 180, 210, 250, 270]
    horas = horas_de_sol(alturas, acimuts, elevaciones, horas_por_instante=1, res=RES, altura_observador=OBS)
    assert (horas == 5).all()


def test_horas_de_sol_detras_de_un_muro():
    alturas, centro = escena_muro(distancia=5, altura=10)
    acimuts = [180, 180, 180]
    elevaciones = [50, 70, -5]  # sombra, sol, noche
    horas = horas_de_sol(alturas, acimuts, elevaciones, horas_por_instante=0.25, res=RES, altura_observador=OBS) # cada 15 min
    assert horas[centro, centro] == 0.25

