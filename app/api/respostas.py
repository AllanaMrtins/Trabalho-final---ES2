from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import exige_perfil
from app.core.database import get_db
from app.models import Usuario
from app.schemas import DesempenhoOut, RespostaIn, RespostaOut
from app.services.resposta_service import RespostaService

router = APIRouter(tags=["Respostas e desempenho"])
aluno_only = exige_perfil("aluno")


@router.post("/atividades/{atividade_id}/respostas", response_model=RespostaOut, status_code=201)  # RF05
def responder(atividade_id: int, dados: RespostaIn, aluno: Usuario = Depends(aluno_only), db: Session = Depends(get_db)):
    resposta, feedback, xp = RespostaService(db).responder(aluno, atividade_id, dados.valor)
    out = RespostaOut.model_validate(resposta)
    out.feedback = feedback
    out.xp_ganho = xp
    return out


@router.get("/respostas", response_model=list[RespostaOut])  # RF06
def historico(atividade_id: Optional[int] = None, aluno: Usuario = Depends(aluno_only), db: Session = Depends(get_db)):
    return RespostaService(db).historico(aluno, atividade_id)


@router.get("/desempenho", response_model=DesempenhoOut)  # RF07
def desempenho(aluno: Usuario = Depends(aluno_only), db: Session = Depends(get_db)):
    return RespostaService(db).desempenho(aluno)
