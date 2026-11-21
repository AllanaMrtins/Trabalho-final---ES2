from sqlalchemy import case, func, select
from sqlalchemy.orm import Session

from app.models import Atividade, Resposta


class RespostaRepository:
    def __init__(self, db: Session):
        self.db = db

    def salvar(self, resposta: Resposta) -> Resposta:
        self.db.add(resposta)
        self.db.commit()
        self.db.refresh(resposta)
        return resposta

    def listar_do_aluno(self, usuario_id: int, atividade_id: int | None = None):
        stmt = select(Resposta).where(Resposta.usuario_id == usuario_id).order_by(Resposta.id.desc())
        if atividade_id is not None:
            stmt = stmt.where(Resposta.atividade_id == atividade_id)
        return list(self.db.scalars(stmt))

    def agregar_por_nivel(self, usuario_id: int) -> list[tuple[int, int, int]]:
        stmt = (
            select(
                Atividade.nivel,
                func.count(Resposta.id),
                func.sum(case((Resposta.correta, 1), else_=0)),
            )
            .select_from(Resposta)
            .join(Atividade, Atividade.id == Resposta.atividade_id)
            .where(Resposta.usuario_id == usuario_id)
            .group_by(Atividade.nivel)
            .order_by(Atividade.nivel)
        )
        return [(n, int(t), int(a or 0)) for n, t, a in self.db.execute(stmt)]

    def ultimas(self, usuario_id: int, quantidade: int = 5) -> list[tuple[int, bool]]:
        stmt = (
            select(Atividade.nivel, Resposta.correta)
            .select_from(Resposta)
            .join(Atividade, Atividade.id == Resposta.atividade_id)
            .where(Resposta.usuario_id == usuario_id)
            .order_by(Resposta.id.desc())
            .limit(quantidade)
        )
        return [(n, bool(c)) for n, c in self.db.execute(stmt)]

    def ja_acertou(self, usuario_id: int, atividade_id: int) -> bool:
        stmt = select(Resposta.id).where(
            Resposta.usuario_id == usuario_id, Resposta.atividade_id == atividade_id, Resposta.correta.is_(True)
        ).limit(1)
        return self.db.scalar(stmt) is not None

    def resultados_do_aluno(self, usuario_id: int) -> list[tuple[int, int, bool]]:
        """[(atividade_id, nivel, correta)] em ordem cronológica."""
        stmt = (
            select(Resposta.atividade_id, Atividade.nivel, Resposta.correta)
            .select_from(Resposta)
            .join(Atividade, Atividade.id == Resposta.atividade_id)
            .where(Resposta.usuario_id == usuario_id)
            .order_by(Resposta.id)
        )
        return [(a, n, bool(c)) for a, n, c in self.db.execute(stmt)]

    def ranking(self, limite: int = 10) -> list[tuple[str, int]]:
        """[(nome, soma dos níveis das atividades acertadas)] - cada atividade conta uma vez."""
        from app.models import Usuario

        sub = (
            select(Resposta.usuario_id, Resposta.atividade_id, Atividade.nivel)
            .join(Atividade, Atividade.id == Resposta.atividade_id)
            .where(Resposta.correta.is_(True))
            .distinct()
            .subquery()
        )
        total = func.sum(sub.c.nivel)
        stmt = (
            select(Usuario.nome, total)
            .join(sub, sub.c.usuario_id == Usuario.id)
            .group_by(Usuario.id)
            .order_by(total.desc(), Usuario.id)
            .limit(limite)
        )
        return [(nome, int(t)) for nome, t in self.db.execute(stmt)]
