from fastapi import APIRouter

from app.domain.funcao_afim import representar
from app.schemas import RepresentacaoIn, RepresentacaoOut

router = APIRouter(prefix="/funcoes", tags=["Representações da Função Afim"])


@router.post("/representacoes", response_model=RepresentacaoOut)  # RF04
def representacoes(dados: RepresentacaoIn):
    """Dada f(x)=ax+b, devolve as formas algébrica, tabular, gráfica e de situação-problema."""
    return representar(dados.a, dados.b, dados.x_min, dados.x_max, dados.passo)
