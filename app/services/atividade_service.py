from sqlalchemy.orm import Session

from app.core.exceptions import NaoAutorizado, NaoEncontrado
from app.domain.funcao_afim import calcular_resposta_esperada
from app.models import Atividade, Usuario
from app.repositories.atividade_repository import AtividadeRepository
from app.schemas import AtividadeIn


class AtividadeService:
    def __init__(self, db: Session):
        self.repo = AtividadeRepository(db)

    def criar(self, professor: Usuario, dados: AtividadeIn) -> Atividade:
        atividade = Atividade(**dados.model_dump(), professor_id=professor.id, resposta_esperada=self._esperada(dados))
        return self.repo.salvar(atividade)

    def obter(self, atividade_id: int) -> Atividade:
        atividade = self.repo.obter(atividade_id)
        if not atividade:
            raise NaoEncontrado("Atividade não encontrada.")
        return atividade

    def listar(self, **filtros) -> list[Atividade]:
        return self.repo.listar(**filtros)

    def atualizar(self, professor: Usuario, atividade_id: int, dados: AtividadeIn) -> Atividade:
        atividade = self._do_professor(professor, atividade_id)
        for campo, valor in dados.model_dump().items():
            setattr(atividade, campo, valor)
        atividade.resposta_esperada = self._esperada(dados)
        return self.repo.salvar(atividade)

    def excluir(self, professor: Usuario, atividade_id: int) -> None:
        self.repo.excluir(self._do_professor(professor, atividade_id))

    def _do_professor(self, professor: Usuario, atividade_id: int) -> Atividade:
        atividade = self.obter(atividade_id)
        if atividade.professor_id != professor.id:
            raise NaoAutorizado("Somente o professor autor pode alterar esta atividade.")
        return atividade

    @staticmethod
    def _esperada(dados: AtividadeIn) -> float:
        return calcular_resposta_esperada(dados.tipo_pergunta, dados.coef_a, dados.coef_b, dados.x_dado)
