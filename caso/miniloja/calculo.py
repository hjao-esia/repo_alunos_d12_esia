"""Cálculo de totais de pedido."""
from miniloja import flags

FRETE_POR_UF = {"PE": 12.9, "SP": 19.9, "RJ": 21.5}
TAXA_POR_UF = {"PE": 0.05, "SP": 0.07, "RJ": 0.06}


def _aplicar_desconto(total, cupom):
    """Aplica o desconto do cupom ao subtotal (R1.2).

    FRETEGRATIS não altera o valor (o frete é zerado em _calcular_frete);
    cupom desconhecido é ignorado; NATAL só vale com a flag ligada.
    """
    if cupom == "PROMO10":
        total = total * 0.9
    elif cupom == "VIP15":
        total = total * 0.85
    elif cupom == "NATAL" and flags.promo_natal_ativa():
        total = total * 0.8
    return total


def _calcular_frete(total, cupom, uf):
    """Frete sobre o total já com desconto."""
    frete = 0
    if cupom == "FRETEGRATIS":
        frete = 0
    else:
        if total > 200:
            frete = 0
        else:
            if uf == "PE":
                frete = 12.9
            elif uf == "SP":
                frete = 19.9
            elif uf == "RJ":
                frete = 21.5
            else:
                frete = 29.9
    return frete


def _aplicar_taxa(total, uf):
    """Soma a taxa de serviço por UF ao total (desconto + frete)."""
    if uf == "PE":
        taxa = 0.05
    elif uf == "SP":
        taxa = 0.07
    elif uf == "RJ":
        taxa = 0.06
    else:
        taxa = 0.08
    imposto = total * taxa
    total = total + imposto
    return total


def calcular_total(itens, cupom=None, uf="PE"):
    """Calcula o total do pedido conforme R1 de caso/regras.md.

    Ordem (R1.6): subtotal (soma de preço × quantidade) → desconto do cupom
    → frete sobre o subtotal com desconto → taxa de serviço por UF sobre
    (subtotal com desconto + frete) → arredondamento em duas casas.

    Divergências conhecidas com o contrato, mantidas de propósito porque
    esta função está sob refatoração com igualdade exata ao golden master
    (caso/dados/golden-master.json): o frete só é grátis com total > 200
    (R1.3 pede >= 200) e round() sobre float não arredonda meio para cima
    (R1.5). A correção é uma mudança de comportamento separada; ver
    caso/adr/0001-divergencias-r13-r15.md.
    """
    total = 0
    for i in itens:
        preco = i["preco"]
        qtd = i["qtd"]
        total = total + preco * qtd

    total = _aplicar_desconto(total, cupom)
    total = total + _calcular_frete(total, cupom, uf)
    total = _aplicar_taxa(total, uf)

    return round(total, 2)
