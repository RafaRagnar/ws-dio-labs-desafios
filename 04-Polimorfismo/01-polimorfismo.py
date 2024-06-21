class Passaro:
    def voar(self):
        print("Voando...")


class Pardal(Passaro):
    def voar(self):
        print("Pardal pode voar")


class Avestruz(Passaro):
    def voar(self):
        print("Avestruz não pode voar...")

# Exemplo ruim do uso de herança para "ganhar" o método voar


class Aviao(Passaro):
    def voar(self):
        print("Avião está decolando...")


def plano_de_voo(obj):
    obj.voar()


p1 = Pardal()
p2 = Avestruz()

plano_de_voo(p1)
plano_de_voo(p2)
plano_de_voo(Aviao())
