class Pessoa:
    def __init__(self, nome=None, idade=None) -> None:
        self.nome = nome
        self.idade = idade

    @classmethod
    def criar_de_data_nascimento(cls, ano, mes, dia, nome):

        idade = 2022 - ano
        return cls(nome, idade)

    @staticmethod
    def e_maior_idade(idade):
        return idade >= 18


p = Pessoa("Rafael", 42)
print(p.nome, p.idade)

p2 = Pessoa.criar_de_data_nascimento(1982, 5, 26, "Rafael")
print(p2.nome, p2.idade)

p3 = Pessoa.e_maior_idade(18)
p4 = Pessoa.e_maior_idade(8)

print(p3)
print(p4)
