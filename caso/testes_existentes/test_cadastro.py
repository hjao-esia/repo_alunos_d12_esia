import unittest

from miniloja import cadastro


class TestCadastro(unittest.TestCase):
    def test_cadastro_sem_nome_e_rejeitado(self):
        cadastro.limpar()
        status, corpo = cadastro.cadastrar_cliente({"email": "a@b.com"})
        self.assertEqual(status, 422)
        self.assertIn("nome", [e["campo"] for e in corpo["erros"]])

    def test_cadastro_valido(self):
        cadastro.limpar()
        status, corpo = cadastro.cadastrar_cliente(
            {"nome": "Ana", "email": "ana@exemplo.com", "cpf": "529.982.247-25"}
        )
        self.assertEqual(status, 201)
        self.assertEqual(corpo["id"], 1)
