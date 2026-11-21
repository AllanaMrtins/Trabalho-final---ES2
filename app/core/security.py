"""Hash de senha (PBKDF2 + salt) e tokens JWT."""
import hashlib
import hmac
import os
from datetime import datetime, timedelta, timezone

import jwt

from app.core.config import ALGORITHM, SECRET_KEY, TOKEN_MINUTES

_ITERACOES = 120_000


def _derivar(senha: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", senha.encode(), salt, _ITERACOES)


def hash_senha(senha: str) -> str:
    salt = os.urandom(16)
    return f"{salt.hex()}${_derivar(senha, salt).hex()}"


def verificar_senha(senha: str, armazenado: str) -> bool:
    salt_hex, hash_hex = armazenado.split("$")
    return hmac.compare_digest(_derivar(senha, bytes.fromhex(salt_hex)).hex(), hash_hex)


def criar_token(usuario_id: int, perfil: str) -> str:
    expira = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_MINUTES)
    return jwt.encode(
        {"sub": str(usuario_id), "perfil": perfil, "exp": expira}, SECRET_KEY, algorithm=ALGORITHM
    )


def decodificar_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
