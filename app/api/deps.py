"""Dependências de autenticação e autorização (RBAC por perfil)."""
import jwt
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import NaoAutenticado, NaoAutorizado
from app.core.security import decodificar_token
from app.models import Usuario
from app.repositories.usuario_repository import UsuarioRepository

bearer = HTTPBearer(auto_error=False)


def usuario_atual(cred: HTTPAuthorizationCredentials | None = Depends(bearer), db: Session = Depends(get_db)) -> Usuario:
    if cred is None:
        raise NaoAutenticado("Token de acesso ausente.")
    try:
        payload = decodificar_token(cred.credentials)
        usuario = UsuarioRepository(db).obter(int(payload["sub"]))
    except (jwt.PyJWTError, KeyError, ValueError):
        raise NaoAutenticado("Token inválido ou expirado.")
    if usuario is None:
        raise NaoAutenticado("Token inválido ou expirado.")
    return usuario


def exige_perfil(perfil: str):
    def dependencia(usuario: Usuario = Depends(usuario_atual)) -> Usuario:
        if usuario.perfil != perfil:
            raise NaoAutorizado(f"Acesso restrito ao perfil '{perfil}'.")
        return usuario

    return dependencia
