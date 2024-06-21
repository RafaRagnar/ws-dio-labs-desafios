class Veiculo:
    def __init__(self, cor, placa, nru_rodas) -> None:
        self.cor = cor
        self.placa = placa
        self.nru_rodas = nru_rodas

    def ligar_motor(self):
        print("Ligando o motor!")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {
            ', '.join([f'{chave}={valor}' for chave, valor in
                       self.__dict__.items()])}"


class Motocicleta(Veiculo):
    ...


class Carro(Veiculo):
    ...


class Caminhao(Veiculo):
    def __init__(self, cor, placa, nru_rodas, carregado):
        super().__init__(cor, placa, nru_rodas)
        self.carregado = carregado

    def esta_carregado(self):
        print(f"{'Sim' if self.carregado else 'Não'} estou carregado")


moto = Motocicleta("preta", "abc-1234", 2)
moto.ligar_motor()

carro = Carro("branco", "def-5467", 4)
carro.ligar_motor()

caminhao = Caminhao("roxo", "ghi-8901", 8, True)
caminhao.ligar_motor()
caminhao.esta_carregado()
print()
print(moto)
print(carro)
print(caminhao)
