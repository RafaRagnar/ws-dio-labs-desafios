import textwrap
from datetime import datetime
from abc import ABC, abstractmethod
from colorama import Fore, Style  # type: ignore


class Cliente:
    """
    Classe que representa um cliente do banco.

    Atributos:
        endereco (str): Endereço do cliente.
        contas (list): Lista de contas bancárias do cliente.
    """

    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        """
        Realiza uma transação na conta especificada.

        Args:
            conta (Conta): Conta na qual a transação será realizada.
            transacao (Transacao): Transação a ser realizada.
        """
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        """
        Adiciona uma conta bancária à lista de contas do cliente.

        Args:
            conta (Conta): Conta a ser adicionada.
        """
        self.contas.append(conta)


class PessoaFisica(Cliente):
    """
    Classe que representa um cliente pessoa física.

    Atributos:
        nome (str): Nome do cliente.
        data_nascimento (int): Data de nascimento do cliente (formato
        YYYYMMDD).
        cpf (str): CPF do cliente.
    """

    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    """
    Classe que representa uma conta bancária.

    Atributos:
        _saldo (float | int): Saldo da conta.
        _numero (int): Número da conta.
        _agencia (str): Agência da conta.
        _cliente (str): Nome do cliente titular da conta.
        _historico (Historico): Histórico de transações da conta.
    """

    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        """
        Cria uma nova instância de conta bancária.

        Args:
            cliente (str): Nome do cliente titular da conta.
            numero (int): Número da conta.

        Returns:
            Conta: Nova instância de conta bancária.
        """
        return cls(numero, cliente)

    @property
    def saldo(self):
        """
        Retorna o saldo da conta.

        Returns:
            float | int: Saldo da conta.
        """
        return self._saldo

    @property
    def numero(self):
        """
        Retorna o número da conta.

        Returns:
            int: Número da conta.
        """
        return self._numero

    @property
    def agencia(self):
        """
        Retorna a agência da conta.

        Returns:
            str: Agência da conta.
        """
        return self._agencia

    @property
    def cliente(self):
        """
        Retorna o nome do cliente titular da conta.

        Returns:
            str: Nome do cliente titular da conta.
        """
        return self._cliente

    @property
    def historico(self):
        """
        Retorna o histórico de transações da conta.

        Returns:
            Historico: Histórico de transações da conta.
        """
        return self._historico

    def sacar(self, valor):
        """
        Realiza um saque na conta.

        Args:
            valor (float | int): Valor a ser sacado.

        Returns:
            bool: True se o saque foi realizado com sucesso, False caso
            contrário.
        """
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print(Fore.RED +
                  f"Saldo insuficiente. O saldo é de R$ {saldo:.2f}."
                  + Style.RESET_ALL)
        elif valor > 0:
            self._saldo -= valor
            print(Fore.GREEN +
                  f"Saque de R$ {valor:.2f} realizado com sucesso!\n"
                  + Style.RESET_ALL)
            self._historico.adicionar_transacao(Saque(valor))
            return True
        else:
            print(Fore.RED +
                  "Valor de saque inválido. Tente novamente."
                  + Style.RESET_ALL)
        return False

    def depositar(self, valor):
        """
        Realiza um depósito na conta.

        Args:
            valor (float | int): Valor a ser depositado.

        Returns:
            bool: True se o depósito foi realizado com sucesso, False caso
            contrário.
        """
        if valor > 0:
            self._saldo += valor
            print(Fore.GREEN +
                  f"Depósito de R$ {valor:.2f} realizado com sucesso!\n"
                  + Style.RESET_ALL)
            self._historico.adicionar_transacao(Deposito(valor))
            return True
        else:
            print(Fore.RED +
                  "Valor de depósito inválido. Tente novamente."
                  + Style.RESET_ALL)
        return False


class ContaCorrente(Conta):
    """
    Classe que representa uma conta corrente.

    Atributos:
        limite (float): Limite de crédito da conta.
        limite_saque (int): Limite diário de saques.
    """

    def __init__(self, numero: int, cliente: str, limite=500, limite_saque=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saque = limite_saque

    def sacar(self, valor):
        """
        Realiza um saque na conta corrente, considerando o limite de crédito
        e o limite diário de saques.

        Args:
            valor (float | int): Valor a ser sacado.

        Returns:
            bool: True se o saque foi realizado com sucesso, False caso
            contrário.
        """
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes
             if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saque

        if excedeu_limite:
            print(Fore.RED +
                  f"Limite de saque diário excedido. Limite: R$ {
                      self.limite:.2f}"
                  + Style.RESET_ALL)
        elif excedeu_saques:
            print(Fore.RED +
                  f"Número de saques diários excedido. Limite: {
                      self.limite_saque} saques"
                  + Style.RESET_ALL)
        else:
            return super().sacar(valor)

        return False

    def __str__(self) -> str:
        """
        Retorna uma string representando a conta corrente.

        Returns:
            str: String representando a conta corrente.
        """
        return Fore.YELLOW + f"""
               Agência:\t{self.agencia}
               C/C:\t{self.numero}
               Titular:\t{self.cliente.nome}
            """ + Style.RESET_ALL


class Historico:
    """
    Classe que representa o histórico de transações de uma conta.

    Atributos:
        _transacoes (list): Lista de transações realizadas na conta.
    """

    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        """
        Retorna a lista de transações realizadas na conta.

        Returns:
            list: Lista de transações realizadas na conta.
        """
        return self._transacoes

    def adicionar_transacao(self, transacao):
        """
        Adiciona uma transação ao histórico da conta.

        Args:
            transacao (Transacao): Transação a ser adicionada.
        """
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })


class Transacao(ABC):
    """
    Classe abstrata que representa uma transação bancária.

    Atributos:
    valor (float | int): Valor da transação.
    """

    @property
    @abstractmethod
    def valor(self):
        """
        Retorna o valor da transação.

        Returns:
            float | int: Valor da transação.
        """

    @classmethod
    @abstractmethod
    def registrar(cls, conta):
        """
        Registra a transação na conta especificada.

        Args:
            conta (Conta): Conta na qual a transação será registrada.
        """


class Saque(Transacao):
    """
    Classe que representa uma transação de saque.

    Atributos:
        valor (float | int): Valor do saque.
    """

    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        """
        Retorna o valor do saque.

        Returns:
            float | int: Valor do saque.
        """
        return self._valor

    def registrar(self, conta):
        """
        Registra o saque na conta especificada.

        Args:
            conta (Conta): Conta na qual o saque será registrado.
        """
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    """
    Classe que representa uma transação de depósito.

    Atributos:
        valor (float | int): Valor do depósito.
    """

    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        """
        Retorna o valor do depósito.

        Returns:
            float | int: Valor do depósito.
        """
        return self._valor

    def registrar(self, conta):
        """
        Registra o depósito na conta especificada.

        Args:
            conta (Conta): Conta na qual o depósito será registrado.
        """
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def menu():
    """
    Apresenta o menu principal do sistema bancário e captura a opção do
    usuário.

    Returns:
    str: Opção escolhida pelo usuário.
    """
    menu_opcao = """\n
================ MENU ===============
[d]\tDepositar
[s]\tSacar
[e]\tExtrato
[nc]\tNova Conta
[lc]\tListar Contas
[nu]\tNovo Usuário
[q]\tSair
=====================================
=> Digite a opção desejada: """

    return input(textwrap.dedent(
        Fore.YELLOW + menu_opcao + Style.RESET_ALL)).lower()


def filtrar_cliente(cpf, clientes):
    """
    Filtra o cliente com base no CPF.
    """
    clientes_filtrados = [cliente for cliente in
                          clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\nCliente não possui conta!")
        return

    # Não permite cliente escolher a conta
    return cliente.contas[0]


def depositar(clientes):
    cpf = input(
        Fore.YELLOW + "Informe o CPF do clientes: " + Style.RESET_ALL)
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(Fore.RED + "\nCliente não encontrado!" + Style.RESET_ALL)
        return

    valor = float(input(Fore.LIGHTYELLOW_EX +
                        "\nInforme o valor do depósito: R$ "
                        + Style.RESET_ALL))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input(
        Fore.YELLOW + "Informe o CPF do clientes: " + Style.RESET_ALL)
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(Fore.RED + "\nCliente não encontrado!" + Style.RESET_ALL)
        return

    valor = float(input(Fore.LIGHTYELLOW_EX +
                        "\nInforme o valor do saque: R$ "
                        + Style.RESET_ALL))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input(
        Fore.YELLOW + "Informe o CPF do clientes: " + Style.RESET_ALL)
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(Fore.RED + "\nCliente não encontrado!" + Style.RESET_ALL)
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print(Fore.YELLOW + "\n ================ EXTRATO =============== "
          + Style.RESET_ALL)
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = (Fore.YELLOW +
                   "Não foram realizadas movimentações." + Style.RESET_ALL)
    else:
        for transacao in transacoes:
            extrato += (Fore.YELLOW + f"\n{transacao['tipo']}:\n\tR$"
                        f"{transacao['valor']:.2f}" + Style.RESET_ALL)
    print(extrato)
    print(Fore.YELLOW + f"\nSaldo:\n\tR$ {conta.saldo:.2f}" + Style.RESET_ALL)
    print(Fore.YELLOW + " ======================================== "
          + Style.RESET_ALL)


def criar_cliente(clientes):
    cpf = input(
        Fore.YELLOW + "Informe o CPF do clientes: " + Style.RESET_ALL)
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print(Fore.RED + "\nJá existe cliente com esse CPF!" + Style.RESET_ALL)
        return

    nome = input(Fore.YELLOW + "Informe o nome completo: " + Style.RESET_ALL)
    data_nascimento = input(Fore.YELLOW +
                            "Informe a data de nascimento (dd-mm-aaaa): "
                            + Style.RESET_ALL)
    endereco = input(Fore.YELLOW +
                     "Informe o endereço (logradouro, nro - bairro - "
                     "cidade/sigla estado): "
                     + Style.RESET_ALL)

    cliente = PessoaFisica(
        nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print(Fore.GREEN + "\n Cliente criado com sucesso!" + Style.RESET_ALL)


def criar_conta(numero_conta, clientes, contas):
    cpf = input(
        Fore.YELLOW + "Informe o CPF do clientes: " + Style.RESET_ALL)
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print(Fore.RED + "\nCliente não encontrado!" + Style.RESET_ALL)
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print(Fore.GREEN + "\nConta criada com sucesso!" + Style.RESET_ALL)


def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


def main():
    """
    Função principal do sistema bancário.
    """
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            # Depositar
            depositar(clientes)

        elif opcao == "s":
            # Sacar
            sacar(clientes)

        elif opcao == "e":
            # Extrato
            exibir_extrato(clientes)

        elif opcao == "nu":
            # Criar Usuário
            criar_cliente(clientes)

        elif opcao == "nc":
            # Nova Conta
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            # Listar Contas
            listar_contas(contas)

        elif opcao == "q":
            # Sair
            print("Saindo do sistema...")
            break

        else:
            print(Fore.RED +
                  "Opção inválida, selecione novamente a operação desejada!"
                  + Style.RESET_ALL)


if __name__ == '__main__':
    # Exemplo de uso
    # cliente1 = PessoaFisica("João Silva", 19801231,
    #                         "12345678901", "Rua dos Girassóis, 123")
    # conta1 = ContaCorrente(12345, cliente1.nome, limite=1000)
    # cliente1.adicionar_conta(conta1)
    # print(conta1)

    # conta1.depositar(500)
    # conta1.sacar(200)
    # conta1.sacar(400)  # Limite excedido
    # conta1.depositar(-100)  # Valor inválido
    # conta1.sacar(100)

    # print(conta1.historico)

    main()
