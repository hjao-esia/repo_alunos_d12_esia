import unittest

from miniloja.descontos import aplicar_desconto


class TestDescontos(unittest.TestCase):
    def test_sem_cupom_retorna_total(self):
        self.assertEqual(aplicar_desconto(200.0, None), 200.0)

    def test_aplicar_desconto(self):
        total = 200.0
        esperado = total - (total * 10 / 100)
        self.assertEqual(aplicar_desconto(total, "PROMO10"), esperado)

    def test_vip15_aplica_quinze_por_cento(self):
        # R1.2: 200 - 15% = 170
        self.assertEqual(aplicar_desconto(200.0, "VIP15"), 170.0)
