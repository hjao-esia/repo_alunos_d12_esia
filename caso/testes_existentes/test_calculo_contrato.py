"""Testes de calcular_total derivados do contrato R1 (caso/regras.md), não do código.

Cada esperado foi calculado à mão a partir da regra citada. As entradas evitam
meio centavo e a fronteira de R$ 200, onde o código diverge do contrato; essas
divergências ficam em expectedFailure (ver caso/adr/0001-divergencias-r13-r15.md).
"""
import os
import unittest

from miniloja.calculo import calcular_total


def item(preco, qtd=1):
    return {"preco": preco, "qtd": qtd}


class TestSubtotalR11(unittest.TestCase):
    def test_subtotal_soma_preco_vezes_quantidade(self):
        # 10 × 3 + 25 × 2 = 80; (80 + 19,90) × 1,07 = 106,893 → 106,89
        self.assertEqual(calcular_total([item(10.0, 3), item(25.0, 2)], None, "SP"), 106.89)


class TestDescontoR12(unittest.TestCase):
    def tearDown(self):
        os.environ.pop("MINILOJA_PROMO_NATAL", None)

    def test_promo10_tira_dez_por_cento(self):
        # 150 × 0,9 = 135; (135 + 21,50) × 1,06 = 165,89
        self.assertEqual(calcular_total([item(150.0)], "PROMO10", "RJ"), 165.89)

    def test_vip15_tira_quinze_por_cento(self):
        # 100 × 0,85 = 85; (85 + 21,50) × 1,06 = 112,89
        self.assertEqual(calcular_total([item(100.0)], "VIP15", "RJ"), 112.89)

    def test_natal_com_campanha_ativa_tira_vinte_por_cento(self):
        # 100 × 0,8 = 80; (80 + 21,50) × 1,06 = 107,59
        os.environ["MINILOJA_PROMO_NATAL"] = "1"
        self.assertEqual(calcular_total([item(100.0)], "NATAL", "RJ"), 107.59)

    def test_natal_sem_campanha_nao_desconta(self):
        # (100 + 21,50) × 1,06 = 128,79
        os.environ["MINILOJA_PROMO_NATAL"] = "0"
        self.assertEqual(calcular_total([item(100.0)], "NATAL", "RJ"), 128.79)

    def test_cupom_desconhecido_e_ignorado(self):
        # sem desconto: (100 + 21,50) × 1,06 = 128,79
        self.assertEqual(calcular_total([item(100.0)], "XYZ", "RJ"), 128.79)


class TestFreteR13(unittest.TestCase):
    def test_fretegratis_zera_frete_sem_alterar_valor(self):
        # 50 × 1,07 = 53,50
        self.assertEqual(calcular_total([item(50.0)], "FRETEGRATIS", "SP"), 53.5)

    def test_frete_por_uf_abaixo_de_200(self):
        casos = [
            (37.5, "PE", 52.92),  # (37,50 + 12,90) × 1,05 = 52,92
            (60.0, "SP", 85.49),  # (60 + 19,90) × 1,07 = 85,493
            (40.0, "RJ", 65.19),  # (40 + 21,50) × 1,06 = 65,19
            (50.0, "XX", 86.29),  # (50 + 29,90) × 1,08 = 86,292
        ]
        for preco, uf, esperado in casos:
            with self.subTest(uf=uf):
                self.assertEqual(calcular_total([item(preco)], None, uf), esperado)

    def test_frete_gratis_acima_de_200(self):
        # 300 × 1,07 = 321,00
        self.assertEqual(calcular_total([item(300.0)], None, "SP"), 321.0)

    def test_limite_usa_subtotal_com_desconto_abaixo(self):
        # 220 × 0,9 = 198 < 200 → paga frete; (198 + 19,90) × 1,07 = 233,153
        self.assertEqual(calcular_total([item(220.0)], "PROMO10", "SP"), 233.15)

    def test_limite_usa_subtotal_com_desconto_acima(self):
        # 250 × 0,85 = 212,50 ≥ 200 → frete grátis; 212,50 × 1,06 = 225,25
        self.assertEqual(calcular_total([item(250.0)], "VIP15", "RJ"), 225.25)

    @unittest.expectedFailure
    def test_frete_gratis_com_subtotal_exatamente_200(self):
        # R1.3 "maior ou igual": 200 × 1,05 = 210,00. O código usa > 200 (ADR 0001).
        self.assertEqual(calcular_total([item(100.0, 2)], None, "PE"), 210.0)


class TestTaxaR14(unittest.TestCase):
    def test_taxa_por_uf_sobre_valor_sem_frete(self):
        # FRETEGRATIS isola a taxa: 100 × (1 + taxa da UF)
        for uf, esperado in [("PE", 105.0), ("SP", 107.0), ("RJ", 106.0), ("XX", 108.0)]:
            with self.subTest(uf=uf):
                self.assertEqual(calcular_total([item(100.0)], "FRETEGRATIS", uf), esperado)


class TestArredondamentoEOrdemR15R16(unittest.TestCase):
    def test_ordem_desconto_frete_taxa(self):
        # 100 × 0,9 = 90; (90 + 29,90) × 1,08 = 129,492 → 129,49
        self.assertEqual(calcular_total([item(100.0)], "PROMO10", "XX"), 129.49)

    @unittest.expectedFailure
    def test_meio_centavo_arredonda_para_cima(self):
        # Exemplo da R1.5: (2 + 12,90) × 1,05 = 15,645 → 15,65. O código dá 15,64 (ADR 0001).
        self.assertEqual(calcular_total([item(2.0)], None, "PE"), 15.65)


if __name__ == "__main__":
    unittest.main()
