"""Cadastro de clientes."""
import re

_CLIENTES = []


def _cpf_valido(cpf):
    """Confere formato, dígitos iguais e dígitos verificadores do CPF."""
    if not isinstance(cpf, str) or not re.fullmatch(r"\d{3}\.\d{3}\.\d{3}-\d{2}|\d{11}", cpf):
        return False
    d = [int(c) for c in cpf if c.isdigit()]
    if len(set(d)) == 1:
        return False
    for n in (9, 10):
        resto = sum(d[i] * (n + 1 - i) for i in range(n)) * 10 % 11
        if resto % 10 != d[n]:
            return False
    return True


def cadastrar_cliente(payload):
    """Cadastra um cliente; se inválido, responde 422 com todos os erros."""
    erros = []
    for campo in ("nome", "email", "cpf"):
        if not payload.get(campo):
            erros.append({"campo": campo, "erro": "obrigatório"})
    email = payload.get("email")
    if email and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", str(email)):
        erros.append({"campo": "email", "erro": "formato inválido"})
    cpf = payload.get("cpf")
    if cpf and not _cpf_valido(cpf):
        erros.append({"campo": "cpf", "erro": "cpf inválido"})
    if erros:
        return 422, {"erros": erros}
    cliente = dict(payload, id=len(_CLIENTES) + 1)
    _CLIENTES.append(cliente)
    return 201, cliente


def limpar():
    _CLIENTES.clear()
