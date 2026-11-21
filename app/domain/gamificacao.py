"""Regras puras de gamificação: XP, nível do jogador, sequência de acertos e conquistas."""

XP_BASE = 10  # XP = 10 x nível da atividade (só no primeiro acerto de cada atividade)
XP_POR_NIVEL_JOGADOR = 100

CONQUISTAS = [
    ("primeiro_acerto", "Primeiro Passo", "Acertou a primeira missão", "🌱"),
    ("sequencia_3", "Em Chamas", "3 acertos seguidos", "🔥"),
    ("sequencia_5", "Imparável", "5 acertos seguidos", "⚡"),
    ("explorador", "Explorador", "Tentou 5 missões diferentes", "🧭"),
    ("mestre", "Mestre da Reta", "Acertou uma missão de nível 3", "👑"),
]


def xp_da_atividade(nivel: int) -> int:
    return XP_BASE * nivel


def nivel_do_jogador(xp: int) -> int:
    return xp // XP_POR_NIVEL_JOGADOR + 1


def maior_sequencia(corretas: list[bool]) -> int:
    """Corretas em ordem cronológica."""
    melhor = atual = 0
    for ok in corretas:
        atual = atual + 1 if ok else 0
        melhor = max(melhor, atual)
    return melhor


def sequencia_atual(corretas: list[bool]) -> int:
    n = 0
    for ok in reversed(corretas):
        if not ok:
            break
        n += 1
    return n


def conquistas_obtidas(acertos: int, tentadas: int, maior_seq: int, acertou_nivel3: bool) -> set[str]:
    obtidas = set()
    if acertos >= 1:
        obtidas.add("primeiro_acerto")
    if maior_seq >= 3:
        obtidas.add("sequencia_3")
    if maior_seq >= 5:
        obtidas.add("sequencia_5")
    if tentadas >= 5:
        obtidas.add("explorador")
    if acertou_nivel3:
        obtidas.add("mestre")
    return obtidas
