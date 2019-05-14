class OrgaoRN:
    def __init__(self, name, id, bruto, total, patronal):
        self.name = name
        self.id = id
        self.bruto = bruto
        self.patronal = patronal
        self.total = total
        self.servidores = []

    def __repr__(self):
        return '{}({})'.format(self.name, self.id)
