"""Testes unitários das regras de negócio (sem banco nem HTTP)."""
import pytest

from app.domain import funcao_afim as fa


def test_raiz_e_valor():
    assert fa.raiz(2, -4) == 2
    assert fa.valor_em_x(3, 1, 2) == 7


def test_raiz_com_a_zero_levanta_erro():
    with pytest.raises(ValueError):
        fa.raiz(0, 5)


@pytest.mark.parametrize(
    "a,b,esperado",
    [(2, 3, "f(x) = 2x + 3"), (-1, 0, "f(x) = -x"), (1, -2.5, "f(x) = x - 2.5")],
)
def test_expressao(a, b, esperado):
    assert fa.expressao(a, b) == esperado


def test_tabela():
    assert [p["y"] for p in fa.tabela(2, -4, -1, 3, 1)] == [-6, -4, -2, 0, 2]


def test_corrigir_com_tolerancia():
    assert fa.corrigir(0.3333, 0.33)
    assert not fa.corrigir(2, 3)


def test_recomendar_nivel():
    assert fa.recomendar_nivel([]) == 1
    assert fa.recomendar_nivel([(1, True), (1, True), (1, True)]) == 2
    assert fa.recomendar_nivel([(2, False), (2, False), (2, True)]) == 1
    assert fa.recomendar_nivel([(3, True), (3, True), (3, True)]) == 3
