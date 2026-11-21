from sqlalchemy.orm import Session

from app.core.exceptions import Conflito, NaoAutenticado
from app.core.security import criar_token, hash_senha, verificar_senha
from app.models import Usuario
from app.repositories.usuario_repository import UsuarioRepository
from app.schemas import TokenOut, UsuarioIn


class UsuarioService:
    def __init__(self, db: Session):
        self.repo = UsuarioRepository(db)

    def cadastrar(self, dados: UsuarioIn) -> Usuario:
        email = dados.email.strip().lower()
        if self.repo.obter_por_email(email):
            raise Conflito("Já existe um usuário cadastrado com este e-mail.")
        return self.repo.salvar(
            Usuario(nome=dados.nome.strip(), email=email, senha_hash=hash_senha(dados.senha), perfil=dados.perfil)
        )

    def autenticar(self, email: str, senha: str) -> TokenOut:
        usuario = self.repo.obter_por_email(email.strip().lower())
        # Mensagem única evita revelar se o e-mail existe.
        if not usuario or not verificar_senha(senha, usuario.senha_hash):
            raise NaoAutenticado("E-mail ou senha inválidos.")
        return TokenOut(access_token=criar_token(usuario.id, usuario.perfil))
