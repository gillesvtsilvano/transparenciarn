class ServidorRN:
    def __init__(self, nome, orgao, cargo, ch, remuneracao_base, remuneracao_outras,
    previdencia, ir, redutor, descontos_outros, liquido):
        self.nome = nome
        self.orgao = orgao
        self.cargo = cargo
        self.ch = ch
        self.remuneracao_base = remuneracao_base
        self.remuneracao_outras = remuneracao_outras
        self.previdencia = previdencia
        self.ir = ir
        self.redutor = redutor
        self.descontos_outros = descontos_outros
        self.liquido = liquido

    def __repr__(self):
        return "{} ({})".format(self.nome, self.orgao)
