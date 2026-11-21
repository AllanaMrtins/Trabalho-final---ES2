from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import usuario_atual
from app.core.database import get_db
from app.schemas import LoginIn, TokenOut, UsuarioIn, UsuarioOut
from app.services.usuario_service import UsuarioService

router = APIRouter(tags=["Usuários e autenticação"])


@router.post("/usuarios", response_model=UsuarioOut, status_code=201)  # RF01
def cadastrar(dados: UsuarioIn, db: Session = Depends(get_db)):
    return UsuarioService(db).cadastrar(dados)


@router.post("/login", response_model=TokenOut)  # RF02
def login(dados: LoginIn, db: Session = Depends(get_db)):
    return UsuarioService(db).autenticar(dados.email, dados.senha)


@router.get("/usuarios/me", response_model=UsuarioOut)
def perfil(usuario=Depends(usuario_atual)):
    return usuario
