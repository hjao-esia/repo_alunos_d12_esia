import unittest

from miniloja.relatorios import resumo_vendas, simular_desconto


class TestRelatorios(unittest.TestCase):
    def test_resumo_vendas(self):
        r = resumo_vendas([{"total": 10.0}, {"total": 20.0}])
        self.assertEqual(r["quantidade"], 2)
        self.assertEqual(r["total"], 30.0)

    def test_simular_desconto(self):
        self.assertTrue(simular_desconto(100.0, "PROMO10").startswith("R$"))

    def test_simular_desconto_duas_casas(self):
        # R1.2 e R1.5: 12,34 * 0,9 = 11,106 -> 11,11
        self.assertEqual(simular_desconto(12.34, "PROMO10"), "R$ 11,11")
