"""Configurações da aplicação (podem ser sobrescritas por variáveis de ambiente)."""
import os

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-troque-em-producao-0123456789")
ALGORITHM = "HS256"
TOKEN_MINUTES = int(os.getenv("TOKEN_MINUTES", "60"))
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./funcao_afim.db")
