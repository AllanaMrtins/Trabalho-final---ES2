from typing import Optional

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from app.api.deps import exige_perfil, usuario_atual
from app.core.database import get_db
from app.models import Atividade, Usuario
from app.schemas import AtividadeIn, AtividadeOut, Representacao, TipoPergunta
from app.services.atividade_service import AtividadeService

router = APIRouter(prefix="/atividades", tags=["Atividades"])
professor_only = exige_perfil("professor")


def _saida(atividade: Atividade, usuario: Usuario) -> AtividadeOut:
    out = AtividadeOut.model_validate(atividade)
    if usuario.perfil != "professor":  # aluno não pode ver o gabarito
        out.coef_a = out.coef_b = out.resposta_esperada = None
    return out


@router.post("", response_model=AtividadeOut, response_model_exclude_none=True, status_code=201)  # RF03
def criar(dados: AtividadeIn, prof: Usuario = Depends(professor_only), db: Session = Depends(get_db)):
    return _saida(AtividadeService(db).criar(prof, dados), prof)


@router.get("", response_model=list[AtividadeOut], response_model_exclude_none=True)  # RF03
def listar(
    nivel: Optional[int] = Query(None, ge=1, le=3),
    representacao: Optional[Representacao] = None,
    tipo_pergunta: Optional[TipoPergunta] = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    usuario: Usuario = Depends(usuario_atual),
    db: Session = Depends(get_db),
):
    itens = AtividadeService(db).listar(
        nivel=nivel, representacao=representacao, tipo_pergunta=tipo_pergunta, limit=limit, offset=offset
    )
    return [_saida(a, usuario) for a in itens]


@router.get("/{atividade_id}", response_model=AtividadeOut, response_model_exclude_none=True)
def obter(atividade_id: int, usuario: Usuario = Depends(usuario_atual), db: Session = Depends(get_db)):
    return _saida(AtividadeService(db).obter(atividade_id), usuario)


@router.put("/{atividade_id}", response_model=AtividadeOut, response_model_exclude_none=True)
def atualizar(atividade_id: int, dados: AtividadeIn, prof: Usuario = Depends(professor_only), db: Session = Depends(get_db)):
    return _saida(AtividadeService(db).atualizar(prof, atividade_id, dados), prof)


@router.delete("/{atividade_id}", status_code=204)
def excluir(atividade_id: int, prof: Usuario = Depends(professor_only), db: Session = Depends(get_db)):
    AtividadeService(db).excluir(prof, atividade_id)
    return Response(status_code=204)
