class Animal:
    def __init__(self, nro_patas) -> None:
        self.nro_patas = nro_patas

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {
            ', '.join([f'{chave}={valor}' for chave, valor in
                       self.__dict__.items()])}"


class Mamifero(Animal):
    def __init__(self, cor_pelo, **kwargs) -> None:
        self.cor_pelo = cor_pelo
        super().__init__(**kwargs)

    def __str__(self) -> str:
        return "Mamifero"


class Ave(Animal):
    def __init__(self, cor_bico, **kwargs) -> None:
        self.cor_bico = cor_bico
        super().__init__(**kwargs)

    def __str__(self) -> str:
        return "Ave"


class Cachorro(Mamifero):
    ...


class Gato(Mamifero):
    ...


class Leao(Mamifero):
    ...


class FalarMixin:
    def falar(self):
        return ("oi estou falando")


class Ornitorrinco(Mamifero, Ave, FalarMixin):
    def __init__(self, cor_bico, cor_pelo, nro_patas):
        print(Ornitorrinco.__mro__)
        print(Ornitorrinco.mro())
        super().__init__(
            cor_bico=cor_bico, cor_pelo=cor_pelo, nro_patas=nro_patas)

    def __str__(self) -> str:
        return "Ornitorrinco"


gato = Gato(nro_patas=4, cor_pelo="preto")
print(gato)

ornitorrinco = Ornitorrinco(nro_patas=4, cor_pelo="marrom", cor_bico="laranja")
print(ornitorrinco)
print(ornitorrinco.falar())
