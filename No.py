# No e Cores
PRETO = 'PRETO'
VERMELHO = 'VERMELHO'
NIL = 'NIL'


class No:
    def __init__(self, valor, cor, pai, esquerda=None, direita=None):
        self.valor = valor
        self.cor = cor
        self.pai = pai
        self.esquerda = esquerda
        self.direita = direita

    def __repr__(self):
        return '{cor} {val} No'.format(cor=self.cor, val=self.valor)

    def __iter__(self):
        if self.esquerda.cor != NIL:
            yield from self.esquerda.__iter__()

        yield self.valor

        if self.direita.cor != NIL:
            yield from self.direita.__iter__()

    def __igual__(self, other):
        if self.cor == NIL and self.cor == other.cor:
            return True

        if self.pai is None or other.pai is None:
            pais_iguais = self.pai is None and other.pai is None
        else:
            pais_iguais = self.pai.valor == other.pai.valor and self.pai.cor == other.pai.cor
        return self.valor == other.valor and self.cor == other.cor and pais_iguais

    def tem_filho(self) -> bool:
        return bool(self.total_nos_filhos())

    def total_nos_filhos(self) -> int:
        if self.cor == NIL:
            return 0
        return sum([int(self.esquerda.cor != NIL), int(self.direita.cor != NIL)])