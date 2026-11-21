from sqlalchemy.orm import Session

from app.domain.funcao_afim import corrigir, gerar_feedback, recomendar_nivel
from app.domain.gamificacao import xp_da_atividade
from app.models import Resposta, Usuario
from app.repositories.resposta_repository import RespostaRepository
from app.schemas import DesempenhoOut, NivelDesempenho
from app.services.atividade_service import AtividadeService


class RespostaService:
    def __init__(self, db: Session):
        self.repo = RespostaRepository(db)
        self.atividades = AtividadeService(db)

    def responder(self, aluno: Usuario, atividade_id: int, valor: float) -> tuple[Resposta, str, int]:
        atividade = self.atividades.obter(atividade_id)
        correta = corrigir(atividade.resposta_esperada, valor)
        primeira_vez = correta and not self.repo.ja_acertou(aluno.id, atividade.id)
        resposta = self.repo.salvar(
            Resposta(usuario_id=aluno.id, atividade_id=atividade.id, valor_informado=valor, correta=correta)
        )
        xp = xp_da_atividade(atividade.nivel) if primeira_vez else 0
        return resposta, gerar_feedback(atividade.tipo_pergunta, correta), xp

    def historico(self, aluno: Usuario, atividade_id: int | None = None) -> list[Resposta]:
        return self.repo.listar_do_aluno(aluno.id, atividade_id)

    def desempenho(self, aluno: Usuario) -> DesempenhoOut:
        linhas = self.repo.agregar_por_nivel(aluno.id)
        total = sum(t for _, t, _ in linhas)
        acertos = sum(a for _, _, a in linhas)
        return DesempenhoOut(
            total_respostas=total,
            acertos=acertos,
            taxa_acerto=round(acertos / total, 4) if total else 0.0,
            por_nivel=[NivelDesempenho(nivel=n, total=t, acertos=a) for n, t, a in linhas],
            nivel_recomendado=recomendar_nivel(self.repo.ultimas(aluno.id)),
        )
