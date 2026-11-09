"""Testes de reprodução dos achados do PR do bloco 5 (exportação CSV).

Reprodução (cópia descartável, sem tocar em caso/):
  cp -r caso <copia>/caso && cd <copia> && git init -q && git add -A && git commit -qm base
  git apply <repo>/apoio/pr-bloco5/0001-Adiciona-exporta-o-de-vendas-em-CSV.patch
  python -B exercicios/aula-5/repro/test_repro_pr5.py <copia>/caso
Cada teste descreve o comportamento exigido pelo contrato/segurança;
um FAIL significa que o PR viola aquele requisito. Saída gravada: saida-pr.txt.
"""
import csv
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.abspath(sys.argv.pop(1)))

from miniloja import exportacao, formatacao, handlers  # noqa: E402
from miniloja.repositorio import RepositorioPedidos  # noqa: E402

ITENS = [{"sku": "BOLA-01", "preco": 50.0, "qtd": 1}]


class Base(unittest.TestCase):
    def setUp(self):
        # cada teste roda num diretório vazio, para não sujar o repositório
        self._cwd = os.getcwd()
        self.tmp = tempfile.mkdtemp()
        self.dentro = os.path.join(self.tmp, "app")
        os.makedirs(self.dentro)
        os.chdir(self.dentro)
        handlers._repo.__init__()  # repositório real, zerado

    def tearDown(self):
        os.chdir(self._cwd)


class TestAchados(Base):
    def test_a1_r4_exporta_apenas_pedidos_do_proprio_usuario(self):
        handlers.post_pedidos(1, {"itens": ITENS})
        handlers.post_pedidos(2, {"itens": ITENS})
        status, corpo = handlers.get_exportacao(1, "vendas.csv")
        with open(corpo["arquivo"], encoding="utf-8") as f:
            donos = {linha["usuario_id"] for linha in csv.DictReader(f)}
        self.assertEqual(donos, {"1"}, "CSV do usuário 1 contém pedidos de outros usuários")

    def test_a2_nome_com_dotdot_nao_escreve_fora_de_exports(self):
        status, _ = handlers.get_exportacao(1, "../fora.csv")
        self.assertFalse(os.path.exists(os.path.join(self.dentro, "fora.csv")),
                         "arquivo escrito fora de exports/")
        self.assertEqual(status, 400)

    def test_a2b_nome_absoluto_nao_escreve_fora_de_exports(self):
        alvo = os.path.join(self.tmp, "absoluto.csv")
        handlers.get_exportacao(1, alvo)
        self.assertFalse(os.path.exists(alvo), "caminho absoluto ignora EXPORT_DIR")

    def test_a3_falha_de_escrita_nao_responde_200(self):
        status, corpo = handlers.get_exportacao(1, "pasta_inexistente/vendas.csv")
        self.assertFalse(os.path.exists(corpo.get("arquivo", "")))
        self.assertNotEqual(status, 200, "erro de escrita engolido e 200 devolvido")


class TestTesteDoPR(Base):
    def test_a5_teste_do_pr_exige_linhas_2_para_usuario_1(self):
        # O teste do PR espera linhas == 2 com pedidos de usuários 1 e 2:
        # ele fixa a violação de R4 como comportamento esperado.
        handlers.post_pedidos(1, {"itens": ITENS})
        handlers.post_pedidos(2, {"itens": ITENS})
        _, corpo = handlers.get_exportacao(1, "v.csv")
        self.assertEqual(corpo["linhas"], 1)


class TestDuplicacao(unittest.TestCase):
    def test_a6_br_igual_a_formatar_moeda(self):
        for v in (0, 10, 1234.5, 1234567.891, -3.5):
            self.assertEqual(exportacao._br(v), formatacao.formatar_moeda(v))


if __name__ == "__main__":
    unittest.main(verbosity=2)
