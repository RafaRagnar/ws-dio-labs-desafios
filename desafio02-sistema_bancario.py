# pip install colorama
import textwrap
from colorama import Fore, Style   # type: ignore


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
    [u]\tCriar Usuário
    [c]\tNova Conta
    [l]\tListar Contas
    [q]\tSair
    =====================================
    => Digite a opção desejada: """

    return input(textwrap.dedent(
        Fore.YELLOW + menu_opcao + Style.RESET_ALL)).lower()


def depositar(saldo, valor, extrato, /):
    """
    Realiza um depósito na conta informada e atualiza o extrato da operação.

    Args:
    saldo (float): Saldo atual da conta.
    valor (float): Valor a ser depositado.
    extrato (str): Histórico de operações (opcional, padrão vazio).

    Returns:
    tuple: (saldo, extrato)
    """

    if valor > 0:
        saldo += valor
        extrato += f"Depósito:\tR$ {valor:.2f}\n"
        print(Fore.GREEN +
              f"\nDepósito realizado com sucesso! Saldo atual: R$ {saldo:.2f}"
              + Style.RESET_ALL)
    else:
        print(Fore.RED +
              "\nOperação inválida! O valor do depósito deve ser positivo."
              + Style.RESET_ALL)

    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite=500, numero_saques=0,
          limite_saques=3):
    """
    Realiza um saque na conta informada, verificando os limites e atualizando
    o extrato.

    Args:
    saldo (float): Saldo atual da conta.
    valor (float): Valor a ser sacado.
    extrato (str): Histórico de operações (opcional, padrão vazio).
    limite (float): Limite individual de saque (opcional, padrão R$ 500).
    numero_saques (int): Número de saques realizados no dia (opcional,
    padrão 0).
    limite_saques (int): Limite de saques por dia (opcional,
    padrão 3).

    Returns:
    tuple: (saldo, extrato)
    """

    if valor <= 0:
        print(Fore.RED +
              "\nOperação inválida! O valor do saque deve ser positivo."
              + Style.RESET_ALL)
        return saldo, extrato

    excede_saldo = valor > saldo
    excede_limite = valor > limite
    excede_saques = numero_saques >= limite_saques

    if excede_saldo:
        print(Fore.RED + "\nOperação falhou! Saldo insuficiente."
              + Style.RESET_ALL)

    elif excede_limite:
        print(Fore.RED +
              f"\nOperação falhou! Limite de saque excedido (R$ {
                  limite:.2f})."
              + Style.RESET_ALL)

    elif excede_saques:
        print(Fore.RED +
              f"\nOperação falhou! Limite de saques por dia excedido"
              f"({limite_saques} saques)." + Style.RESET_ALL)
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque:\t\tR$ {valor:.2f}\n"
        numero_saques += 1
        print(Fore.GREEN +
              f"\nSaque realizado com sucesso! Saldo atual: R$ {saldo:.2f}"
              + Style.RESET_ALL)
    else:
        print(Fore.RED +
              "\nOperação inválida! O valor do saque deve ser positivo."
              + Style.RESET_ALL)

    return saldo, extrato


def exibir_extrato(saldo, /, *, extrato):
    """
    Exibe o extrato de operações bancárias da conta informada.

    Args:
    saldo (float): Saldo atual da conta.
    extrato (str): Histórico de operações.
    """
    print(Fore.LIGHTGREEN_EX +
          "\n================ EXTRATO ==============="
          + Style.RESET_ALL)
    print(Fore.LIGHTGREEN_EX +
          "Não foram realizadas movimentações." if not extrato else extrato
          + Style.RESET_ALL)
    print(Fore.LIGHTGREEN_EX +
          f"\nSaldo:\t\tR$ {saldo:.2f}"
          + Style.RESET_ALL)
    print(Fore.LIGHTGREEN_EX +
          "=========================================="
          + Style.RESET_ALL)


def filtrar_usuario(cpf, usuarios):
    """
    Searches for a user by CPF in the provided `usuarios` list.

    Args:
    cpf (str): CPF of the user to search for (numbers only).
    usuarios (list): List of user dictionaries.

    Returns:
    dict or None: User dictionary if found, otherwise None.
    """

    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario

    return None


def criar_usuario(usuarios):
    """
    Creates a new user and adds it to the `usuarios` list.

    Args:
    nome (str): User's name.
    data_nascimento (str): User's date of birth in dd/mm/yyyy format.
    endereco (str): User's address.
    cpf (str): User's CPF (numbers only).
    usuarios (list): List of user dictionaries.

    Raises:
    ValueError: If the CPF is already registered.
    """
    cpf = input(
        Fore.YELLOW + "Informe o CPF (somente números): " + Style.RESET_ALL)
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print(Fore.RED + "Já existe usuário com esse CPF!" + Style.RESET_ALL)
        return

    nome = input(Fore.YELLOW + "Informe o nome completo: " + Style.RESET_ALL)
    data_nascimento = input(Fore.YELLOW +
                            "Informe a data de nascimento (dd/mm/yyyy): "
                            + Style.RESET_ALL)
    endereco = input(Fore.YELLOW +
                     "Informe o endereço (logradouro, nro - bairro -"
                     "cidade/sigla estado): " + Style.RESET_ALL)
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento,
                     "cpf": cpf, "endereco": endereco})

    print(Fore.GREEN + f"Usuário {nome} criado com sucesso!" + Style.RESET_ALL)


def criar_conta(agencia, numero_conta, usuarios):
    """
    Creates a new account and associates it with the specified user.

    Args:
    agencia (str): Account agency number.
    numero_conta (str): Account number.
    usuarios (list): List of user dictionaries.
    conta_data_structure (dict): Default account data structure.

    Returns:
    dict: The newly created account dictionary.
    """

    # Find the user by CPF
    cpf = input(Fore.YELLOW + "Digite o CPF do titular da conta: "
                + Style.RESET_ALL)
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print(Fore.GREEN + "Conta criada com sucesso!" + Style.RESET_ALL)
        return {'agencia': agencia, 'numero_conta': numero_conta,
                'usuario': usuario}

    print(Fore.RED + "Usuário não encontrado, encerrado a criação da conta!"
          + Style.RESET_ALL)


def listar_contas(contas):
    """
    Displays information about all accounts in the provided list.

    Args:
    contas (list): List of account dictionaries.
    """

    if not contas:
        print(Fore.RED + "Não há contas cadastradas." + Style.RESET_ALL)
        return

    print(Fore.GREEN +
          "\n================ LISTA DE CONTAS ==============="
          + Style.RESET_ALL)
    for i, conta in enumerate(contas):
        print(Fore.GREEN + f"\nConta {i + 1}:" + Style.RESET_ALL)
        print(Fore.GREEN + f"Agência:\t{conta['agencia']}" + Style.RESET_ALL)
        print(Fore.GREEN +
              f"Número da Conta:\t{conta['numero_conta']}" + Style.RESET_ALL)
        print(Fore.GREEN +
              f"Titular:\t{conta['usuario']['nome']}" + Style.RESET_ALL)
        print(Fore.GREEN +
              "----------------------------------------" + Style.RESET_ALL)
        print(Fore.GREEN +
              "==========================================" + Style.RESET_ALL)


if __name__ == '__main__':
    LIMITE_SAQUES = 3
    AGENCIA = "0001"

    saldo: int = 0
    limite: int = 500
    extrato: str = ""
    numero_saques: int = 0
    usuarios: list = []
    contas: list = []

    while True:
        opcao = menu()

        if opcao == "d":
            valor = float(input(Fore.LIGHTYELLOW_EX +
                                "\nInforme o valor do depósito: R$ "
                                + Style.RESET_ALL))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("\nInforme o valor do saque: R$ "))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES
            )

        elif opcao == "e":
            exibir_extrato(saldo, extrato=extrato)

        elif opcao == "u":
            criar_usuario(usuarios)

        elif opcao == "c":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "l":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print(Fore.RED +
                  "Opção inválida, selecione novamente a operação desejada!"
                  + Style.RESET_ALL)
