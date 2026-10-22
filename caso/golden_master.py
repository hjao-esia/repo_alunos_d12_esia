"""Compara calcular_total com o golden master gravado na AV1.2.

Uso, da raiz do repositório:
  python -B caso/golden_master.py [--codigo DIR]

--codigo seleciona a pasta com o pacote miniloja (padrão: caso), como em
testes/test_miniloja.py. Igualdade exata (==), sem tolerância. Lista os id
divergentes e sai com código 1 se houver algum; 0 se todos forem iguais.
"""
import argparse
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
GOLDEN = os.path.join(AQUI, "dados", "golden-master.json")


def comparar(codigo):
    sys.path.insert(0, os.path.abspath(codigo))
    from miniloja.calculo import calcular_total

    with open(GOLDEN, encoding="utf-8") as f:
        casos = json.load(f)["casos"]

    anterior = os.environ.get("MINILOJA_PROMO_NATAL")
    divergentes = []
    try:
        for caso in casos:
            os.environ["MINILOJA_PROMO_NATAL"] = "1" if caso["natal"] else "0"
            obtido = calcular_total(caso["carrinho"], caso["cupom"], caso["uf"])
            if obtido != caso["saida"]:
                divergentes.append((caso["id"], caso["saida"], obtido))
    finally:
        if anterior is None:
            os.environ.pop("MINILOJA_PROMO_NATAL", None)
        else:
            os.environ["MINILOJA_PROMO_NATAL"] = anterior

    for id_, esperado, obtido in divergentes:
        print(f"DIVERGE {id_}: gravado {esperado!r}, obtido {obtido!r}")
    print(f"{len(casos) - len(divergentes)}/{len(casos)} iguais")
    return 1 if divergentes else 0


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--codigo", default=os.path.join("caso"))
    sys.exit(comparar(p.parse_args().codigo))
