"""Modelos ORM (entidades persistidas)."""
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


def agora() -> datetime:
    return datetime.now(timezone.utc)


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    senha_hash: Mapped[str] = mapped_column(String(200))
    perfil: Mapped[str] = mapped_column(String(20))  # aluno | professor
    criado_em: Mapped[datetime] = mapped_column(DateTime, default=agora)

    atividades: Mapped[list["Atividade"]] = relationship(back_populates="professor")
    respostas: Mapped[list["Resposta"]] = relationship(
        back_populates="aluno", cascade="all, delete-orphan"
    )


class Atividade(Base):
    __tablename__ = "atividades"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(150))
    enunciado: Mapped[str] = mapped_column(Text)
    nivel: Mapped[int] = mapped_column(Integer, index=True)  # 1, 2 ou 3
    representacao: Mapped[str] = mapped_column(String(30), index=True)
    tipo_pergunta: Mapped[str] = mapped_column(String(30))
    coef_a: Mapped[float] = mapped_column(Float)
    coef_b: Mapped[float] = mapped_column(Float)
    x_dado: Mapped[float | None] = mapped_column(Float, nullable=True)
    resposta_esperada: Mapped[float] = mapped_column(Float)
    professor_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))

    professor: Mapped[Usuario] = relationship(back_populates="atividades")
    respostas: Mapped[list["Resposta"]] = relationship(
        back_populates="atividade", cascade="all, delete-orphan"
    )


class Resposta(Base):
    __tablename__ = "respostas"

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), index=True)
    atividade_id: Mapped[int] = mapped_column(ForeignKey("atividades.id"), index=True)
    valor_informado: Mapped[float] = mapped_column(Float)
    correta: Mapped[bool] = mapped_column(Boolean)
    respondido_em: Mapped[datetime] = mapped_column(DateTime, default=agora)

    aluno: Mapped[Usuario] = relationship(back_populates="respostas")
    atividade: Mapped[Atividade] = relationship(back_populates="respostas")
