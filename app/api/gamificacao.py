from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import exige_perfil, usuario_atual
from app.core.database import get_db
from app.models import Usuario
from app.schemas import GamificacaoOut, RankingItem
from app.services.gamificacao_service import GamificacaoService

router = APIRouter(tags=["Gamificação"])


@router.get("/gamificacao", response_model=GamificacaoOut)  # RF08
def meu_perfil(aluno: Usuario = Depends(exige_perfil("aluno")), db: Session = Depends(get_db)):
    return GamificacaoService(db).perfil(aluno)


@router.get("/ranking", response_model=list[RankingItem])  # RF08
def ranking(_: Usuario = Depends(usuario_atual), db: Session = Depends(get_db)):
    return GamificacaoService(db).ranking()
