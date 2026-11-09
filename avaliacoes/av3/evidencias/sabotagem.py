"""Sabotagens da correção de R4 em get_pedido (AV3, B1).

Uso, da raiz do repositório: python -B avaliacoes/av3/evidencias/sabotagem.py
Copia caso/ para um diretório temporário, aplica cada variante errada da
correção e roda test_acesso.py. Toda sabotagem deve ser detectada (FAIL);
o código original em caso/ não é alterado.
"""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[3]
CORRECAO = 'if pedido is None or pedido["usuario_id"] != usuario_id:'

SABOTAGENS = [
    ("sem a checagem de dono (código anterior)", CORRECAO, "if pedido is None:"),
    ("checagem invertida (só o dono é barrado)", CORRECAO,
     'if pedido is None or pedido["usuario_id"] == usuario_id:'),
    ("403 em vez de 404 (revela que o pedido existe)", CORRECAO,
     'if pedido is not None and pedido["usuario_id"] != usuario_id:\n'
     '        return 403, {"erro": "acesso negado"}\n'
     "    if pedido is None:"),
    ("404 com corpo diferente do inexistente", CORRECAO,
     'if pedido is not None and pedido["usuario_id"] != usuario_id:\n'
     '        return 404, {"erro": "pedido de outro usuário"}\n'
     "    if pedido is None:"),
]


def rodar(caso):
    cmd = [sys.executable, "-B", "-m", "unittest", "testes_existentes.test_acesso"]
    return subprocess.run(cmd, cwd=caso, capture_output=True, text=True).returncode == 0


def main():
    detectadas = 0
    for nome, velho, novo in SABOTAGENS:
        with tempfile.TemporaryDirectory() as tmp:
            caso = Path(tmp) / "caso"
            shutil.copytree(RAIZ / "caso", caso, ignore=shutil.ignore_patterns("__pycache__"))
            arq = caso / "miniloja" / "handlers.py"
            texto = arq.read_text(encoding="utf-8")
            assert velho in texto, f"trecho não encontrado: {velho!r}"
            arq.write_text(texto.replace(velho, novo), encoding="utf-8")
            passou = rodar(caso)
        detectadas += not passou
        print(f"{'SOBREVIVEU' if passou else 'detectada '} | {nome}")
    print(f"Sabotagens: {len(SABOTAGENS)} | detectadas: {detectadas}")
    sys.exit(0 if detectadas == len(SABOTAGENS) else 1)


if __name__ == "__main__":
    main()
