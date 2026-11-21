from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Atividade


class AtividadeRepository:
    def __init__(self, db: Session):
        self.db = db

    def obter(self, atividade_id: int) -> Atividade | None:
        return self.db.get(Atividade, atividade_id)

    def listar(self, nivel=None, representacao=None, tipo_pergunta=None, limit=20, offset=0):
        stmt = select(Atividade).order_by(Atividade.id)
        if nivel is not None:
            stmt = stmt.where(Atividade.nivel == nivel)
        if representacao is not None:
            stmt = stmt.where(Atividade.representacao == representacao)
        if tipo_pergunta is not None:
            stmt = stmt.where(Atividade.tipo_pergunta == tipo_pergunta)
        return list(self.db.scalars(stmt.limit(limit).offset(offset)))

    def salvar(self, atividade: Atividade) -> Atividade:
        self.db.add(atividade)
        self.db.commit()
        self.db.refresh(atividade)
        return atividade

    def excluir(self, atividade: Atividade) -> None:
        self.db.delete(atividade)
        self.db.commit()
