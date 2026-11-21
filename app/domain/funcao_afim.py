"""Regras de negócio puras sobre Função Afim f(x) = ax + b (sem dependência de framework/BD)."""

TOLERANCIA_CORRECAO = 0.01
FEEDBACKS_ERRO = {
    "valor_em_x": "Substitua o valor de x na expressão f(x) = ax + b e calcule.",
    "raiz": "A raiz é o x em que f(x) = 0, ou seja, x = -b/a.",
    "coef_angular": "O coeficiente angular (a) é a taxa de variação: quanto y muda quando x aumenta 1.",
    "coef_linear": "O coeficiente linear (b) é o valor de f(0), onde a reta corta o eixo y.",
}


def _n(v: float) -> str:
    return f"{v:g}"


def valor_em_x(a: float, b: float, x: float) -> float:
    return a * x + b


def raiz(a: float, b: float) -> float:
    if a == 0:
        raise ValueError("Função afim exige a != 0 para ter uma única raiz.")
    return -b / a + 0.0


def crescimento(a: float) -> str:
    return "crescente" if a > 0 else "decrescente" if a < 0 else "constante"


def expressao(a: float, b: float) -> str:
    termo_a = "x" if a == 1 else "-x" if a == -1 else f"{_n(a)}x"
    if b == 0:
        return f"f(x) = {termo_a}"
    return f"f(x) = {termo_a} {'+' if b > 0 else '-'} {_n(abs(b))}"


def tabela(a: float, b: float, x_min: float, x_max: float, passo: float) -> list[dict]:
    n = int(round((x_max - x_min) / passo))
    pontos = []
    for i in range(n + 1):
        x = x_min + i * passo
        pontos.append({"x": round(x, 10) + 0.0, "y": round(valor_em_x(a, b, x), 10) + 0.0})
    return pontos


def situacao_problema(a: float, b: float) -> str:
    variacao = "aumenta" if a > 0 else "diminui"
    return (
        f"Uma grandeza começa em {_n(b)} (quando x = 0) e, a cada 1 unidade acrescentada em x, "
        f"o valor de y {variacao} {_n(abs(a))}."
    )


def representar(a: float, b: float, x_min: float, x_max: float, passo: float) -> dict:
    """Mostra a MESMA função em quatro representações: algébrica, tabular, gráfica e situação-problema."""
    r = raiz(a, b)
    return {
        "expressao": expressao(a, b),
        "coeficiente_angular": a,
        "coeficiente_linear": b,
        "crescimento": crescimento(a),
        "raiz": r,
        "tabela": tabela(a, b, x_min, x_max, passo),
        "grafico": {
            "pontos": tabela(a, b, x_min, x_max, passo),
            "intercepto_x": {"x": r, "y": 0.0},
            "intercepto_y": {"x": 0.0, "y": b},
        },
        "situacao_problema": situacao_problema(a, b),
    }


def calcular_resposta_esperada(tipo: str, a: float, b: float, x: float | None) -> float:
    if tipo == "valor_em_x":
        if x is None:
            raise ValueError("x_dado é obrigatório para perguntas do tipo valor_em_x.")
        return valor_em_x(a, b, x)
    if tipo == "raiz":
        return raiz(a, b)
    if tipo == "coef_angular":
        return a
    if tipo == "coef_linear":
        return b
    raise ValueError(f"Tipo de pergunta desconhecido: {tipo}")


def corrigir(esperada: float, informada: float) -> bool:
    return abs(esperada - informada) <= TOLERANCIA_CORRECAO


def gerar_feedback(tipo: str, correta: bool) -> str:
    return "Correto! Muito bem." if correta else f"Resposta incorreta. Dica: {FEEDBACKS_ERRO[tipo]}"


def recomendar_nivel(ultimas: list[tuple[int, bool]]) -> int:
    """Recebe as últimas respostas [(nivel, correta)] da mais recente para a mais antiga."""
    if not ultimas:
        return 1
    nivel_atual = ultimas[0][0]
    taxa = sum(1 for _, ok in ultimas if ok) / len(ultimas)
    if len(ultimas) >= 3 and taxa >= 0.8:
        return min(3, nivel_atual + 1)
    if len(ultimas) >= 3 and taxa <= 0.4:
        return max(1, nivel_atual - 1)
    return nivel_atual
