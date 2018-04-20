from No import No, PRETO, VERMELHO, NIL  
from Red_Black_Tree import RedBlackTree
import unittest

NIL_LEAF = RedBlackTree.NIL_LEAF

class Valida(unittest.TestCase):

    def test_functional_test_build_tree(self):
        rb_tree = RedBlackTree()
        
        # Testa Insercao do numero 2
        rb_tree.insere(2)
        
        self.assertEqual(rb_tree.raiz.valor, 2)
        self.assertEqual(rb_tree.raiz.cor, PRETO)
        node_2 = rb_tree.raiz

        valores_esperados = [2]
        values = list(rb_tree)
        self.assertEqual(values, valores_esperados)

        # Testa Insercao do numero 1
        rb_tree.insere(1)

        valores_esperados = [1, 2]
        values = list(rb_tree)
        self.assertEqual(values, valores_esperados)

        node_1 = rb_tree.raiz.esquerda
        self.assertEqual(node_1.valor, 1)
        self.assertEqual(node_1.cor, VERMELHO)

        # Testa Insercao do numero 4
        rb_tree.insere(4)

        valores_esperados = [1, 2, 4]
        values = list(rb_tree)
        self.assertEqual(values, valores_esperados)

        node_4 = rb_tree.raiz.direita
        self.assertEqual(node_4.valor, 4)
        self.assertEqual(node_4.cor, VERMELHO)
        self.assertEqual(node_4.esquerda, NIL_LEAF)
        self.assertEqual(node_4.direita, NIL_LEAF)

        # Testa Insercao do numero 5
        rb_tree.insere(5)

        valores_esperados = [1, 2, 4, 5]
        values = list(rb_tree)
        self.assertEqual(values, valores_esperados)

        # Valida Arvore
        node_5 = node_4.direita
        self.assertEqual(node_5.valor, 5)
        self.assertEqual(node_4.cor, PRETO)
        self.assertEqual(node_1.cor, PRETO)
        self.assertEqual(node_5.cor, VERMELHO)

if __name__ == '__main__':
    unittest.main()