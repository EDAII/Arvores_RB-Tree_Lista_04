import numpy as np
import time
from No import No, PRETO, VERMELHO, NIL


class RedBlackTree:
    
    # Folha Referenciada por todo novo no inserido
    NIL_LEAF = No(valor=None, cor=NIL, pai=None)

    def __init__(self):
        self.count = 0
        self.raiz = None
        self.ROTACOES = {
            'L': self._rotacao_direita,
            'R': self._rotacao_esquerda
        }

    def __iter__(self):
        
        if not self.raiz:
            return list()
        yield from self.raiz.__iter__()

    def insere(self, valor):
        
        if not self.raiz:
            self.raiz = No(valor, cor=PRETO, pai=None, esquerda=self.NIL_LEAF, direita=self.NIL_LEAF)
            self.count += 1
            return
        pai, No_dir = self._busca_pai(valor)
        if No_dir is None:
            return
        novo_No = No(valor=valor, cor=VERMELHO, pai=pai, esquerda=self.NIL_LEAF, direita=self.NIL_LEAF)
        if No_dir == 'L':
            pai.esquerda = novo_No
        else:
            pai.direita = novo_No

        self._testa_balanceamento(novo_No)
        self.count += 1


    def __caso_1(self, No):

        if self.raiz == No:
            No.cor = PRETO
            return
        self.__caso_2(No)

    def __caso_2(self, No):

        pai = No.pai
        irmao, direcao = self._busca_irmao(No)
        if irmao.cor == VERMELHO and pai.cor == PRETO and irmao.esquerda.cor != VERMELHO and irmao.direita.cor != VERMELHO:
            self.ROTACOES[direcao](No=None, pai=irmao, avo=pai)
            pai.cor = VERMELHO
            irmao.cor = PRETO
            return self.__caso_1(No)
        self.__caso_3(No)

    def __caso_3(self, No):

        pai = No.pai
        irmao, _ = self._busca_irmao(No)
        if (irmao.cor == PRETO and pai.cor == PRETO
           and irmao.esquerda.cor != VERMELHO and irmao.direita.cor != VERMELHO):
            irmao.cor = VERMELHO
            return self.__caso_1(pai)

        self.__caso_4(No)

    def __caso_4(self, No):

        pai = No.pai
        if pai.cor == VERMELHO:
            irmao, direcao = self._busca_irmao(No)
            if irmao.cor == PRETO and irmao.esquerda.cor != VERMELHO and irmao.direita.cor != VERMELHO:
                pai.cor, irmao.cor = irmao.cor, pai.cor
                return
        self.__caso_5(No)

    def __caso_5(self, No):

        irmao, direcao = self._busca_irmao(No)
        closer_No = irmao.direita if direcao == 'L' else irmao.esquerda
        outer_No = irmao.esquerda if direcao == 'L' else irmao.direita
        if closer_No.cor == VERMELHO and outer_No.cor != VERMELHO and irmao.cor == PRETO:
            if direcao == 'L':
                self._rotacao_esquerda(No=None, pai=closer_No, avo=irmao)
            else:
                self._rotacao_direita(No=None, pai=closer_No, avo=irmao)
            closer_No.cor = PRETO
            irmao.cor = VERMELHO

        self.__caso_6(No)

    def __caso_6(self, No):

        irmao, direcao = self._busca_irmao(No)
        outer_No = irmao.esquerda if direcao == 'L' else irmao.direita

        def __caso_6_rotation(direcao):
            pai_cor = irmao.pai.cor
            self.ROTACOES[direcao](No=None, pai=irmao, avo=irmao.pai)

            irmao.cor = pai_cor
            irmao.direita.cor = PRETO
            irmao.esquerda.cor = PRETO

        if irmao.cor == PRETO and outer_No.cor == VERMELHO:
            return __caso_6_rotation(direcao)

    def _testa_balanceamento(self, No):
 
        pai = No.pai
        valor = No.valor
        if (pai is None 
           or pai.pai is None
           or (No.cor != VERMELHO or pai.cor != VERMELHO)):
            return
        avo = pai.pai
        No_dir = 'L' if pai.valor > valor else 'R'
        pai_dir = 'L' if avo.valor > pai.valor else 'R'
        tio = avo.direita if pai_dir == 'L' else avo.esquerda
        geral_direcao = No_dir + pai_dir

        if tio == self.NIL_LEAF or tio.cor == PRETO:

            if geral_direcao == 'LL':
                self._rotacao_direita(No, pai, avo, to_troca_cor=True)
            elif geral_direcao == 'RR':
                self._rotacao_esquerda(No, pai, avo, to_troca_cor=True)
            elif geral_direcao == 'LR':
                self._rotacao_direita(No=None, pai=No, avo=pai)

                self._rotacao_esquerda(No=pai, pai=No, avo=avo, to_troca_cor=True)
            elif geral_direcao == 'RL':
                self._rotacao_esquerda(No=None, pai=No, avo=pai)

                self._rotacao_direita(No=pai, pai=No, avo=avo, to_troca_cor=True)
            else:
                raise Exception("{} is not a valid direcao!".format(geral_direcao))
        else:
            self._troca_cor(avo)

    # Troca pai e filho, se novo novo pai for nulo entao esta na raiz 
    def __atualiza_pai(self, No, pai_antigo_filho, novo_pai):
        
        No.pai = novo_pai
        if novo_pai:
            if novo_pai.valor > pai_antigo_filho.valor:
                novo_pai.esquerda = No
            else:
                novo_pai.direita = No
        else:
            self.raiz = No

    def _rotacao_direita(self, No, pai, avo, to_troca_cor=False):
       
        grand_avo = avo.pai
        self.__atualiza_pai(No=pai, pai_antigo_filho=avo, novo_pai=grand_avo)

        antigo_direita = pai.direita
        pai.direita = avo
        avo.pai = pai

        avo.esquerda = antigo_direita
        antigo_direita.pai = avo

        if to_troca_cor:
            pai.cor = PRETO
            No.cor = VERMELHO
            avo.cor = VERMELHO

    def _rotacao_esquerda(self, No, pai, avo, to_troca_cor=False):
       
        grand_avo = avo.pai
        self.__atualiza_pai(No=pai, pai_antigo_filho=avo, novo_pai=grand_avo)

        antigo_esquerda = pai.esquerda
        pai.esquerda = avo
        avo.pai = pai

        avo.direita = antigo_esquerda
        antigo_esquerda.pai = avo

        if to_troca_cor:
            pai.cor = PRETO
            No.cor = VERMELHO
            avo.cor = VERMELHO

    def _troca_cor(self, avo):
        
        avo.direita.cor = PRETO
        avo.esquerda.cor = PRETO
        if avo != self.raiz:
            avo.cor = VERMELHO
        self._testa_balanceamento(avo)

    def _busca_pai(self, valor):

        def busca(pai):

            if valor == pai.valor:
                return None, None
            elif pai.valor < valor:
                if pai.direita.cor == NIL:
                    return pai, 'R'
                return busca(pai.direita)
            elif valor < pai.valor:
                if pai.esquerda.cor == NIL:
                    return pai, 'L'
                return busca(pai.esquerda)

        return busca(self.raiz)

    def busca_No(self, valor):
       
        def busca(raiz):
            if raiz is None or raiz == self.NIL_LEAF:
                return None
            if valor > raiz.valor:
                return busca(raiz.direita)
            elif valor < raiz.valor:
                return busca(raiz.esquerda)
            else:
                return raiz

        No_encontrado = busca(self.raiz)
        return No_encontrado

    def _busca_sucessor_em_ordem(self, No):
        
        direita_No = No.direita
        esquerda_No = direita_No.esquerda
        if esquerda_No == self.NIL_LEAF:
            return direita_No
        while esquerda_No.esquerda != self.NIL_LEAF:
            esquerda_No = esquerda_No.esquerda
        return esquerda_No

    def _busca_irmao(self, No):

        pai = No.pai
        if No.valor >= pai.valor:
            irmao = pai.esquerda
            direcao = 'L'
        else:
            irmao = pai.direita
            direcao = 'R'
        return irmao, direcao
    
# Gera valores inteiros aleatorios de 1 ate 100000
def gera_valor_aleatorio():
    valor = np.random.randint(0, 100000)
    return valor


# Gera o vetor de valores randomicos
def gera_lista(limite_superior):
    lista = []
    for i in range(limite_superior):
        numero = gera_valor_aleatorio()
        lista.append(numero)
    return lista

def main():
    tamanho = input('Digite a quantidade de valores a serem inseridos\n')
    
    vetor = []
    vetor = gera_lista(int(tamanho))
    arvore = RedBlackTree()

    inicio = time.time()
    for valor in vetor:
        arvore.insere(valor)
    fim = time.time()

    print('Tempo para insercao: ', fim - inicio)

if __name__ == '__main__':
    main()