class Bicicleta:
    def __init__(self, cor, modelo, ano, valor):
        self.cor = cor
        self.modelo = modelo
        self.ano = ano
        self.valor = valor
        self.marcha = 1

    def buzinar(self):
        print("Plim plim...")

    def parar(self):
        print("Parando bicicleta...")
        print("Bicicleta parada!")

    def correr(self):
        print("Vrummmmm...")

    def trocar_marcha(self, nro_marcha):
        print("Trocando marcha!")

        def _trocar_marcha(nro_marcha):
            if nro_marcha > self.marcha:
                print("Marcha trocada ...")
            else:
                print("Não foi possível trocar de marcha ...")

    def __str__(self) -> str:
        # return (f"Bicicleta: cor={self.cor}, modelo={self.modelo}, "
        #         f"ano={self.ano}, valor={self.valor}")
        return f"{self.__class__.__name__}: {
            ', '.join([f'{chave}={valor}' for chave, valor in
                       self.__dict__.items()])}"


bic_01 = Bicicleta("vermelho", "caloi", 2022, 600)
bic_01.buzinar()
bic_01.correr()
bic_01.parar()
print(bic_01.cor, bic_01.modelo, bic_01.ano, bic_01.valor)

bic_02 = Bicicleta("verde", "monark", 2000, 189)
Bicicleta.buzinar(bic_02)
print(bic_02.cor)
print(bic_02)
