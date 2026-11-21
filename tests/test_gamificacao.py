"""Testes da gamificação (RF08): domínio puro e rotas."""
from app.domain import gamificacao as g


def test_xp_e_nivel_do_jogador():
    assert g.xp_da_atividade(3) == 30
    assert (g.nivel_do_jogador(0), g.nivel_do_jogador(99), g.nivel_do_jogador(100)) == (1, 1, 2)


def test_sequencias():
    assert g.maior_sequencia([True, True, False, True, True, True]) == 3
    assert g.sequencia_atual([True, False, True, True]) == 2
    assert g.sequencia_atual([True, False]) == 0


def test_conquistas():
    assert g.conquistas_obtidas(0, 0, 0, False) == set()
    assert g.conquistas_obtidas(5, 5, 5, True) == {"primeiro_acerto", "sequencia_3", "sequencia_5", "explorador", "mestre"}


def _nova(client, prof, payload):
    return client.post("/atividades", json=payload, headers=prof).json()["id"]


def test_xp_so_no_primeiro_acerto(client, prof, aluno, atividade_payload):
    id_ = _nova(client, prof, atividade_payload)
    url = f"/atividades/{id_}/respostas"
    assert client.post(url, json={"valor": 7}, headers=aluno).json()["xp_ganho"] == 10
    assert client.post(url, json={"valor": 7}, headers=aluno).json()["xp_ganho"] == 0
    perfil = client.get("/gamificacao", headers=aluno).json()
    assert perfil["xp"] == 10 and perfil["atividades_concluidas"] == 1
    assert [c["id"] for c in perfil["conquistas"] if c["conquistada"]] == ["primeiro_acerto"]


def test_erro_nao_gera_xp(client, prof, aluno, atividade_payload):
    id_ = _nova(client, prof, atividade_payload)
    assert client.post(f"/atividades/{id_}/respostas", json={"valor": 0}, headers=aluno).json()["xp_ganho"] == 0
    assert client.get("/gamificacao", headers=aluno).json()["xp"] == 0


def test_ranking_usa_primeiro_nome(client, prof, aluno, atividade_payload):
    id_ = _nova(client, prof, {**atividade_payload, "nivel": 2})
    client.post(f"/atividades/{id_}/respostas", json={"valor": 7}, headers=aluno)
    assert client.get("/ranking", headers=prof).json() == [{"posicao": 1, "nome": "Fulano", "xp": 20, "nivel_jogador": 1}]


def test_gamificacao_exige_perfil_aluno_e_login(client, prof):
    assert client.get("/gamificacao", headers=prof).status_code == 403
    assert client.get("/ranking").status_code == 401


def test_pagina_inicial_e_servida(client):
    r = client.get("/")
    assert r.status_code == 200 and "Afim Quest" in r.text
