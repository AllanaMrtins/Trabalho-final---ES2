"""Testes de integração da API (rotas + serviços + banco em memória)."""


# --- TC01: cadastro de usuário (RF01) ---
def test_tc01_cadastro_valido_nao_expoe_senha(client):
    r = client.post("/usuarios", json={"nome": "Ana", "email": "ana@x.com", "senha": "123456"})
    assert r.status_code == 201
    assert r.json()["perfil"] == "aluno"
    assert "senha" not in r.json() and "senha_hash" not in r.json()


def test_tc01_email_duplicado_retorna_409(client):
    dados = {"nome": "Ana", "email": "ana@x.com", "senha": "123456"}
    client.post("/usuarios", json=dados)
    assert client.post("/usuarios", json=dados).status_code == 409


def test_tc01_email_invalido_retorna_422(client):
    r = client.post("/usuarios", json={"nome": "Ana", "email": "invalido", "senha": "123456"})
    assert r.status_code == 422 and r.json()["erro"] == "Dados inválidos."


# --- TC02: autenticação (RF02) ---
def test_tc02_login_valido_e_invalido(client):
    client.post("/usuarios", json={"nome": "Ana", "email": "ana@x.com", "senha": "123456"})
    ok = client.post("/login", json={"email": "ana@x.com", "senha": "123456"})
    assert ok.status_code == 200 and ok.json()["token_type"] == "bearer"
    assert client.post("/login", json={"email": "ana@x.com", "senha": "errada"}).status_code == 401


def test_tc02_rota_protegida_sem_token_retorna_401(client):
    assert client.get("/atividades").status_code == 401


# --- TC03: representações da função (RF04) ---
def test_tc03_representacoes(client):
    r = client.post("/funcoes/representacoes", json={"a": 2, "b": -4, "x_min": -1, "x_max": 3, "passo": 1})
    corpo = r.json()
    assert r.status_code == 200
    assert corpo["expressao"] == "f(x) = 2x - 4"
    assert corpo["raiz"] == 2 and corpo["crescimento"] == "crescente"
    assert [p["y"] for p in corpo["tabela"]] == [-6, -4, -2, 0, 2]


def test_tc03_a_zero_retorna_422(client):
    assert client.post("/funcoes/representacoes", json={"a": 0, "b": 1}).status_code == 422


# --- TC04: gestão de atividades e autorização (RF03) ---
def test_tc04_professor_cria_aluno_nao(client, prof, aluno, atividade_payload):
    assert client.post("/atividades", json=atividade_payload, headers=aluno).status_code == 403
    r = client.post("/atividades", json=atividade_payload, headers=prof)
    assert r.status_code == 201 and r.json()["resposta_esperada"] == 7


def test_tc04_aluno_nao_ve_gabarito(client, prof, aluno, atividade_payload):
    id_ = client.post("/atividades", json=atividade_payload, headers=prof).json()["id"]
    corpo = client.get(f"/atividades/{id_}", headers=aluno).json()
    assert "resposta_esperada" not in corpo and "coef_a" not in corpo


def test_tc04_crud_atualizar_excluir_e_404(client, prof, atividade_payload):
    id_ = client.post("/atividades", json=atividade_payload, headers=prof).json()["id"]
    novo = {**atividade_payload, "x_dado": 10}
    assert client.put(f"/atividades/{id_}", json=novo, headers=prof).json()["resposta_esperada"] == 21
    assert client.delete(f"/atividades/{id_}", headers=prof).status_code == 204
    assert client.get(f"/atividades/{id_}", headers=prof).status_code == 404


def test_tc04_validacao_x_dado_obrigatorio(client, prof, atividade_payload):
    atividade_payload.pop("x_dado")
    assert client.post("/atividades", json=atividade_payload, headers=prof).status_code == 422


# --- TC05: resolução, histórico e desempenho (RF05, RF06, RF07) ---
def test_tc05_resposta_correta_e_incorreta(client, prof, aluno, atividade_payload):
    id_ = client.post("/atividades", json=atividade_payload, headers=prof).json()["id"]
    certa = client.post(f"/atividades/{id_}/respostas", json={"valor": 7}, headers=aluno)
    errada = client.post(f"/atividades/{id_}/respostas", json={"valor": 5}, headers=aluno)
    assert certa.json()["correta"] is True
    assert errada.json()["correta"] is False and "Dica" in errada.json()["feedback"]


def test_tc05_historico_e_desempenho(client, prof, aluno, atividade_payload):
    id_ = client.post("/atividades", json=atividade_payload, headers=prof).json()["id"]
    for valor in (7, 7, 7, 0):
        client.post(f"/atividades/{id_}/respostas", json={"valor": valor}, headers=aluno)
    assert len(client.get("/respostas", headers=aluno).json()) == 4
    d = client.get("/desempenho", headers=aluno).json()
    assert d["total_respostas"] == 4 and d["acertos"] == 3 and d["taxa_acerto"] == 0.75
    assert d["por_nivel"] == [{"nivel": 1, "total": 4, "acertos": 3}]


def test_tc05_responder_atividade_inexistente_404(client, aluno):
    assert client.post("/atividades/999/respostas", json={"valor": 1}, headers=aluno).status_code == 404
