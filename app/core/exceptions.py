"""Erros de domínio. A camada de API os converte em respostas HTTP padronizadas."""


class ErroDominio(Exception):
    status_code = 400

    def __init__(self, mensagem: str):
        super().__init__(mensagem)
        self.mensagem = mensagem


class NaoAutenticado(ErroDominio):
    status_code = 401


class NaoAutorizado(ErroDominio):
    status_code = 403


class NaoEncontrado(ErroDominio):
    status_code = 404


class Conflito(ErroDominio):
    status_code = 409
