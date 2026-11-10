import pytest

from sombras.sol import instantes_del_dia

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
