"""
Objetivo Geral
Iniciar a modelagem do sistema bancário em POO. Adicionar classes para
cliente e as operações bancárias: depósito e saque.

Desafio:
Atualizar a implementação do sistema bancário, para armazenar os dados de
clientes e contas bancárias em objetos ao invés de dicionários. O código deve
seguir o modelo de classes UML a seguir:
"""
import textwrap
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path

from colorama import Fore, Style  # type: ignore

ROOT_PATH = Path(__file__).parent


class ContaIterador:
    """
    Esta classe fornece um iterador para percorrer uma lista de contas.

    Atributos:
        contas (list): A lista de contas a serem iteradas.

    Métodos:
        __iter__(self): Retorna o próprio objeto ContaIterador (self) para
        permitir o uso em loops 'for'.
        __next__(self): Retorna a próxima conta formatada como string,
        incluindo agência, número, titular e saldo com duas casas decimais.
            - Levanta a exceção StopIteration quando não houver mais contas a
            serem iteradas.
    """

    def __init__(self, contas):
        self.contas = contas
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        try:
            conta = self.contas[self._index]
            return f"""\
            Agência:\t{conta.agencia}
            Número:\t\t{conta.numero}
            Titular:\t{conta.cliente.nome}
            Saldo:\t\tR$ {conta.saldo:.2f}
        """
        except IndexError:
            raise StopIteration
        finally:
            self._index += 1


class Cliente:
    """
    Classe que representa um cliente do banco.

    Atributos:
        endereco (str): Endereço do cliente.
        contas (list): Lista de contas bancárias do cliente.
    """

    def __init__(self, endereco: str):
        self.endereco = endereco
        self.contas: list = []
        self.indice_conta = 0

    def realizar_transacao(self, conta, transacao):
        """
        Realiza uma transação na conta especificada.

        Args:
            conta (Conta): Conta na qual a transação será realizada.
            transacao (Transacao): Transação a ser realizada.
        """
        if len(conta.historico.transacoes_do_dia()) >= 2:
            print(Fore.RED + "Você excedeu o número de transações permitidos "
                  "para hoje!" + Style.RESET_ALL)
            return

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

    def __init__(self, nome: str, data_nascimento: int,
                 cpf: str, endereco: str):
        super().__init__(endereco)
        self.nome: str = nome
        self.data_nascimento: int = data_nascimento
        self.cpf: str = cpf

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: ('{self.nome}', '{self.cpf}')>"


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

    def __init__(self, numero: int, cliente: str):
        self._saldo: float | int = 0
        self._numero: int = numero
        self._agencia: str = "0001"
        self._cliente: str = cliente
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
        else:
            print(Fore.RED +
                  "Valor de depósito inválido. Tente novamente."
                  + Style.RESET_ALL)
            return False

        return True


class ContaCorrente(Conta):
    """
    Classe que representa uma conta corrente.

    Atributos:
        limite (float): Limite de crédito da conta.
        limite_saque (int): Limite diário de saques.
    """

    def __init__(self, numero, cliente, limite=500, limite_saque=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saque = limite_saque

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.
             transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saque

        if excedeu_limite:
            print(Fore.RED +
                  "Limite de saque diário excedido. Limite: "
                  f"R$ {self.limite:.2f}" + Style.RESET_ALL)

        elif excedeu_saques:
            print(Fore.RED +
                  "Número de saques diários excedido. Limite: "
                  f"{self.limite_saque} saques" + Style.RESET_ALL)
        else:
            return super().sacar(valor)

        return False

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: ('{
            self.agencia}', '{self.numero}', '{self.cliente.nome}' )>"

    def __str__(self) -> str:
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t{self.numero}
            Titular:\t{self.cliente.nome}
            """


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

    def gerar_relatorio(self, tipo_transacao=None):
        """
        Gera um iterador para percorrer as transações filtradas por tipo.

        Args:
            tipo_transacao (str, optional): O tipo de transação a ser filtrado
            (por exemplo, 'saque' ou 'deposito').
                    Se None, retorna todas as transações.

        Yields:
            dict: Dicionário representando a transação, contendo os atributos
            'conta', 'valor' e 'tipo'.
        """
        for transacao in self._transacoes:
            if (
                tipo_transacao is None
                or transacao["tipo"].lower() == tipo_transacao.lower()
            ):
                yield transacao

    def transacoes_do_dia(self):
        """
        Retorna uma lista com todas as transações realizadas no dia atual.

        Returns:
            list: Uma lista contendo dicionários que representam as transações
            do dia atual.
                Cada dicionário possui atributos como 'conta', 'valor' e
                'tipo'.
        """
        data_atual = datetime.now().date()
        transacoes = []
        for transacao in self._transacoes:
            data_transacao = datetime.strptime(
                transacao["data"], "%d/%m/%Y %H:%M:%S"
            ).date()
            if data_atual == data_transacao:
                transacoes.append(transacao)
        return transacoes


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


def log_transacao(func):
    """
    Decorator que registra a execução de uma função em um arquivo de log.

    Args:
        func (function): A função a ser decorada.

    Returns:
        function: A função decorada envolvida em um wrapper que registra a
        execução.

    Exemplos:

    @log_transacao
    def realizar_transacao(conta, valor, tipo):
        # Fazer a transação

    # A função 'realizar_transacao' agora será registrada no arquivo 'log.txt'
    # sempre que for executada.
    """
    def envelope(*args, **kwargs):
        resultado = func(*args, **kwargs)
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(ROOT_PATH / "log.txt", "a", encoding="utf-8") as arquivo:
            arquivo.write(
                f"[{data_hora}] Função '{func.__name__}' executada com "
                f"argumentos {args} e {kwargs}. Retornou {resultado}\n"
            )
        return resultado

    return envelope


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
    """
    Obtém a primeira conta bancária do cliente (se existir).

    Args:
        cliente: Objeto do cliente.

    Returns:
        Conta do cliente ou None.
    """
    if not cliente.contas:
        print("\nCliente não possui conta!")
        return

    # Não permite cliente escolher a conta
    return cliente.contas[0]


@log_transacao
def depositar(clientes):
    """
    Realiza um depósito na conta bancária de um cliente.

    Args:
        clientes (lista de Cliente): Lista de objetos Cliente.

    Retorna:
        None

    Observações:
        * A função solicita ao usuário o CPF do cliente e o valor do depósito.
        * Utiliza as funções `filtrar_cliente`, `recuperar_conta_cliente` e
        `realizar_transacao` para realizar o depósito.
        * Imprime mensagens na tela para informar o usuário sobre o andamento
        da operação.
    """
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


@log_transacao
def sacar(clientes):
    """
    Realiza um saque na conta bancária de um cliente.

    Args:
        clientes (lista de Cliente): Lista de objetos Cliente.

    Retorna:
        None

    Observações:
        * A função solicita ao usuário o CPF do cliente e o valor do saque.
        * Utiliza as funções `filtrar_cliente`, `recuperar_conta_cliente` e
        `realizar_transacao` para realizar o saque.
        * Imprime mensagens na tela para informar o usuário sobre o andamento
        da operação.
    """
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


@log_transacao
def exibir_extrato(clientes):
    """
    Exibe o extrato bancário de um cliente.

    Args:
        clientes (lista de Cliente): Lista de objetos Cliente.

    Retorna:
        None

    Observações:
        * A função solicita ao usuário o CPF do cliente.
        * Utiliza as funções `filtrar_cliente` e `recuperar_conta_cliente`
        para obter a conta do cliente.
        * Se a conta for encontrada, imprime o extrato com informações sobre
        as transações realizadas e o saldo atual da conta.
        * Se a conta não for encontrada ou se não houver transações, imprime
        mensagens informativas.
    """
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
    extrato = ""
    tem_transacao = False
    for transacao in conta.historico.gerar_relatorio():
        tem_transacao = True
        extrato += (Fore.YELLOW +
                    f"\n{transacao['data']}\n{transacao['tipo']}:\n\tR$ "
                    f"{transacao['valor']:.2f}" + Style.RESET_ALL)

    if not tem_transacao:
        extrato = (Fore.YELLOW +
                   "Não foram realizadas movimentações." + Style.RESET_ALL)
    print(extrato)
    print(Fore.YELLOW + f"\nSaldo:\n\tR$ {conta.saldo:.2f}" + Style.RESET_ALL)
    print(Fore.YELLOW + " ======================================== "
          + Style.RESET_ALL)


@log_transacao
def criar_cliente(clientes):
    """
    Cria um novo cliente e o adiciona à lista de clientes.

    Args:
        clientes (lista de Cliente): Lista de objetos Cliente.

    Retorna:
        None

    Observações:
        * A função solicita ao usuário os dados do cliente: CPF, nome, data
        de nascimento e endereço.
        * Verifica se já existe um cliente com o CPF informado. Se existir,
        retorna uma mensagem de erro.
        * Cria um novo objeto `ClienteFisica` com os dados informados.
        * Adiciona o novo cliente à lista de clientes.
        * Imprime uma mensagem de sucesso após a criação do cliente.
    """
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


@log_transacao
def criar_conta(numero_conta, clientes, contas):
    """
    Cria uma nova conta corrente para um cliente e a adiciona à lista de
    contas.

    Args:
        numero_conta (str): Número da conta corrente.
        clientes (lista de Cliente): Lista de objetos Cliente.
        contas (lista de ContaCorrente): Lista de objetos ContaCorrente.

    Retorna:
        None

    Observações:
        * A função solicita ao usuário o CPF do cliente.
        * Utiliza a função `filtrar_cliente` para obter o objeto `Cliente`
        correspondente ao CPF informado.
        * Se o cliente não for encontrado, retorna uma mensagem de erro.
        * Cria um novo objeto `ContaCorrente` usando o método `nova_conta` da
        classe `ContaCorrente`, passando o cliente e o número da conta como
        argumentos.
        * Adiciona a nova conta à lista de contas e à lista de contas do
        cliente.
        * Imprime uma mensagem de sucesso após a criação da conta.
    """
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
    """
    Exibe uma lista detalhada de todas as contas bancárias.

    Args:
        contas (lista de Conta): Lista de objetos Conta.

    Retorna:
        None

    Observações:
        * A função percorre a lista de contas e imprime cada conta em um
        formato detalhado.
        * O formato inclui informações como número da conta, nome do cliente,
        saldo, tipo de conta e histórico de transações.
        * Utiliza a função `textwrap.dedent` para formatar a saída de forma
        legível.
    """
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
