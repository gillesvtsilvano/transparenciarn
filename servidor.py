class ServidorRN:
    def __init__(self, nome, cargo, ch, remuneracao_base, remuneracao_outras,
    previdencia, ir, redutor, descontos_outros, liquido, orgao):
        self.nome = nome
        self.cargo = cargo
        self.ch = ch
        self.remuneracao_base = remuneracao_base
        self.remuneracao_outras = remuneracao_outras
        self.previdencia = previdencia
        self.ir = ir
        self.redutor = redutor
        self.descontos_outros = descontos_outros
        self.liquido = liquido
        self.orgao = orgao

    def __repr__(self):
        return "{} ({})".format(self.nome, self.orgao)