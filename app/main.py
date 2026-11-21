"""Ponto de entrada da API: Plataforma Interativa para o Ensino de Função Afim."""
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from pathlib import Path

from fastapi.responses import FileResponse, JSONResponse

from app import models  # noqa: F401  (registra as tabelas)
from app.api import atividades, auth, funcoes, gamificacao, respostas
from app.core.database import Base, engine
from app.core.exceptions import ErroDominio


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(engine)
    yield


app = FastAPI(title="Plataforma Interativa - Função Afim", version="1.0.0", lifespan=lifespan)


@app.exception_handler(ErroDominio)
async def tratar_erro_dominio(_: Request, exc: ErroDominio):
    return JSONResponse(status_code=exc.status_code, content={"erro": exc.mensagem})


@app.exception_handler(RequestValidationError)
async def tratar_validacao(_: Request, exc: RequestValidationError):
    detalhes = [
        {"campo": ".".join(str(p) for p in e["loc"][1:]) or "corpo", "mensagem": e["msg"]} for e in exc.errors()
    ]
    return JSONResponse(status_code=422, content={"erro": "Dados inválidos.", "detalhes": detalhes})


@app.get("/", include_in_schema=False)
def pagina_inicial():
    return FileResponse(Path(__file__).parent / "static" / "index.html")


@app.get("/manus-routes.json", include_in_schema=False)
def manifesto_rotas():
    return JSONResponse(content={"routes": [{"path": "/", "title": "Afim Quest"}, {"path": "/docs", "title": "Documentação da API"}]})


@app.get("/saude", tags=["Saúde"])
def saude():
    return {"status": "ok"}


for r in (auth.router, funcoes.router, atividades.router, respostas.router, gamificacao.router):
    app.include_router(r)
