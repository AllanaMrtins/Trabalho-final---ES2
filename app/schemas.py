"""Schemas Pydantic: validação de entrada e formato das respostas da API."""
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator

EMAIL_RE = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
Perfil = Literal["aluno", "professor"]
Representacao = Literal["algebrica", "tabular", "grafica", "situacao_problema"]
TipoPergunta = Literal["valor_em_x", "raiz", "coef_angular", "coef_linear"]


class UsuarioIn(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    email: str = Field(pattern=EMAIL_RE, max_length=150)
    senha: str = Field(min_length=6, max_length=72)
    perfil: Perfil = "aluno"


class UsuarioOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome: str
    email: str
    perfil: Perfil


class LoginIn(BaseModel):
    email: str
    senha: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RepresentacaoIn(BaseModel):
    a: float = Field(allow_inf_nan=False, description="Coeficiente angular (a != 0)")
    b: float = Field(allow_inf_nan=False, description="Coeficiente linear")
    x_min: float = -3
    x_max: float = 3
    passo: float = Field(1, gt=0)

    @model_validator(mode="after")
    def validar(self):
        if self.a == 0:
            raise ValueError("O coeficiente 'a' deve ser diferente de zero em uma função afim.")
        if self.x_max <= self.x_min:
            raise ValueError("x_max deve ser maior que x_min.")
        if (self.x_max - self.x_min) / self.passo > 200:
            raise ValueError("O intervalo gera mais de 200 pontos; aumente o passo.")
        return self


class Ponto(BaseModel):
    x: float
    y: float


class Grafico(BaseModel):
    pontos: list[Ponto]
    intercepto_x: Ponto
    intercepto_y: Ponto


class RepresentacaoOut(BaseModel):
    expressao: str
    coeficiente_angular: float
    coeficiente_linear: float
    crescimento: str
    raiz: float
    tabela: list[Ponto]
    grafico: Grafico
    situacao_problema: str


class AtividadeIn(BaseModel):
    titulo: str = Field(min_length=3, max_length=150)
    enunciado: str = Field(min_length=5)
    nivel: int = Field(ge=1, le=3)
    representacao: Representacao
    tipo_pergunta: TipoPergunta
    coef_a: float = Field(allow_inf_nan=False)
    coef_b: float = Field(allow_inf_nan=False)
    x_dado: Optional[float] = Field(default=None, allow_inf_nan=False)

    @model_validator(mode="after")
    def validar(self):
        if self.coef_a == 0:
            raise ValueError("coef_a deve ser diferente de zero em uma função afim.")
        if self.tipo_pergunta == "valor_em_x" and self.x_dado is None:
            raise ValueError("x_dado é obrigatório para perguntas do tipo valor_em_x.")
        return self


class AtividadeOut(BaseModel):
    """Campos que revelam a resposta (coef_a, coef_b, resposta_esperada) só vão ao professor."""
    model_config = ConfigDict(from_attributes=True)
    id: int
    titulo: str
    enunciado: str
    nivel: int
    representacao: Representacao
    tipo_pergunta: TipoPergunta
    x_dado: Optional[float] = None
    coef_a: Optional[float] = None
    coef_b: Optional[float] = None
    resposta_esperada: Optional[float] = None


class RespostaIn(BaseModel):
    valor: float = Field(allow_inf_nan=False)


class RespostaOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    atividade_id: int
    valor_informado: float
    correta: bool
    respondido_em: datetime
    feedback: Optional[str] = None
    xp_ganho: Optional[int] = None


class NivelDesempenho(BaseModel):
    nivel: int
    total: int
    acertos: int


class DesempenhoOut(BaseModel):
    total_respostas: int
    acertos: int
    taxa_acerto: float
    por_nivel: list[NivelDesempenho]
    nivel_recomendado: int


class ConquistaOut(BaseModel):
    id: str
    nome: str
    descricao: str
    icone: str
    conquistada: bool


class GamificacaoOut(BaseModel):
    xp: int
    nivel_jogador: int
    xp_no_nivel: int
    xp_para_proximo: int
    sequencia_atual: int
    maior_sequencia: int
    atividades_concluidas: int
    conquistas: list[ConquistaOut]


class RankingItem(BaseModel):
    posicao: int
    nome: str
    xp: int
    nivel_jogador: int
