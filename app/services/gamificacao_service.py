from sqlalchemy.orm import Session

from app.domain import gamificacao as g
from app.models import Usuario
from app.repositories.resposta_repository import RespostaRepository
from app.schemas import ConquistaOut, GamificacaoOut, RankingItem


class GamificacaoService:
    def __init__(self, db: Session):
        self.repo = RespostaRepository(db)

    def perfil(self, aluno: Usuario) -> GamificacaoOut:
        resultados = self.repo.resultados_do_aluno(aluno.id)
        corretas = [ok for _, _, ok in resultados]
        concluidas: dict[int, int] = {}
        for atividade_id, nivel, ok in resultados:
            if ok:
                concluidas.setdefault(atividade_id, nivel)
        xp = sum(g.xp_da_atividade(n) for n in concluidas.values())
        maior = g.maior_sequencia(corretas)
        obtidas = g.conquistas_obtidas(
            acertos=len(concluidas),
            tentadas=len({a for a, _, _ in resultados}),
            maior_seq=maior,
            acertou_nivel3=3 in concluidas.values(),
        )
        return GamificacaoOut(
            xp=xp,
            nivel_jogador=g.nivel_do_jogador(xp),
            xp_no_nivel=xp % g.XP_POR_NIVEL_JOGADOR,
            xp_para_proximo=g.XP_POR_NIVEL_JOGADOR,
            sequencia_atual=g.sequencia_atual(corretas),
            maior_sequencia=maior,
            atividades_concluidas=len(concluidas),
            conquistas=[
                ConquistaOut(id=i, nome=n, descricao=d, icone=ic, conquistada=i in obtidas)
                for i, n, d, ic in g.CONQUISTAS
            ],
        )

    def ranking(self, limite: int = 10) -> list[RankingItem]:
        itens = []
        for pos, (nome, soma) in enumerate(self.repo.ranking(limite), start=1):
            xp = soma * g.XP_BASE
            # Só o primeiro nome é exibido, para proteger a identidade dos alunos.
            itens.append(RankingItem(posicao=pos, nome=nome.split()[0], xp=xp, nivel_jogador=g.nivel_do_jogador(xp)))
        return itens
