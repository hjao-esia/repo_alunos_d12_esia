import unittest

from miniloja import handlers

ITENS = [{"sku": "BOLA-01", "preco": 50.0, "qtd": 1}]


class TestAcessoR4(unittest.TestCase):
    """R4.1: um usuário só pode ver os próprios pedidos."""

    def setUp(self):
        status, self.pedido = handlers.post_pedidos(20, {"itens": ITENS, "uf": "PE"})
        self.assertEqual(status, 201)

    def test_dono_ve_o_proprio_pedido(self):
        status, corpo = handlers.get_pedido(20, self.pedido["id"])
        self.assertEqual(status, 200)
        self.assertEqual(corpo["usuario_id"], 20)

    def test_outro_usuario_recebe_404(self):
        status, corpo = handlers.get_pedido(21, self.pedido["id"])
        self.assertEqual(status, 404)
        self.assertNotIn("usuario_id", corpo)

    def test_resposta_igual_a_de_pedido_inexistente(self):
        # não revela se o pedido existe: mesmo status e corpo de um id inexistente
        alheio = handlers.get_pedido(21, self.pedido["id"])
        inexistente = handlers.get_pedido(21, 999999)
        self.assertEqual(alheio, inexistente)


if __name__ == "__main__":
    unittest.main()
