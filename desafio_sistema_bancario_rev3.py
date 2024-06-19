"""
Importa bibliotecas necessárias
Instalar o colorama - pip install colorama
"""
import datetime
from decimal import Decimal
from colorama import Fore, Style  # type: ignore

# Variáveis globais
AGENCIA = "0001"
LIMITE_SAQUES = 3
SALDO_MINIMO = 0
LIMITE_SAQUE = 500
usuarios: list = []
contas: list = []


# Funções para gerenciamento de usuários
def filtrar_usuario(cpf, usuarios):
    """
    Encontra um usuário na lista de usuários com base no CPF fornecido.

    Args:
        cpf (str): CPF do usuário a ser encontrado.
        usuarios (list): Lista de usuários cadastrados.

    Returns:
        dict: Dicionário contendo as informações do usuário encontrado,
              se existir. None caso o usuário não seja encontrado.
    """
    if not cpf:
        return None

    cpf_sem_formatacao = cpf.replace(".", "").replace("-", "")
    for usuario in usuarios:
        if usuario["cpf"] == cpf_sem_formatacao:
            return usuario
    return None


def criar_usuario(usuarios):
    """
    Cria um novo usuário no sistema.

    Args:
        usuarios (list): Lista de usuários cadastrados.

    Returns:
        None: Se o usuário já existir.
        str: Mensagem de sucesso caso o usuário seja criado.
    """
    cpf = input(
        Fore.YELLOW + "Informe o CPF (somente números): " + Style.RESET_ALL)
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print(Fore.RED + "Já existe usuário com esse CPF!" + Style.RESET_ALL)
        return

    nome = input(Fore.YELLOW + "Informe o nome completo: " + Style.RESET_ALL)
    data_nascimento = input(
        Fore.YELLOW + "Informe a data de nascimento (dd/mm/yyyy): "
        + Style.RESET_ALL)
    endereco = input(
        Fore.YELLOW +
        "Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): "
        + Style.RESET_ALL)

    novo_usuario = {
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco,
        "contas": []
    }
    usuarios.append(novo_usuario)

    print(Fore.GREEN + f"Usuário {nome} criado com sucesso!" + Style.RESET_ALL)
    print(Fore.YELLOW +
          "Deseja realizar mais operações? (s/n): " + Style.RESET_ALL)

    opcao = input().lower()
    if opcao == "s":
        menu_principal()
    else:
        print(Fore.GREEN + "Obrigado por utilizar o sistema!"
              + Style.RESET_ALL)


def listar_usuarios(usuarios):
    """
    Exibe uma lista formatada de todos os usuários cadastrados.

    Args:
        usuarios (list): Lista de usuários cadastrados.
    """
    if not usuarios:
        print(Fore.YELLOW + "Não há usuários cadastrados." + Style.RESET_ALL)
        return

    print(Fore.LIGHTBLUE_EX +
          "\n============== LISTA DE USUÁRIOS ==============\n"
          + Style.RESET_ALL)

    for i, usuario in enumerate(usuarios):
        nome = usuario["nome"]
        cpf = usuario["cpf"]
        data_nascimento = usuario["data_nascimento"]
        endereco = usuario["endereco"]

        print(f"{i+1}. Titular: {nome}\n")
        print(f"CPF: {cpf}\n")
        print(f"Data de Nascimento: {data_nascimento}\n")
        print(f"Endereço: {endereco}\n")

    print(Fore.LIGHTBLUE_EX +
          "\n=============================================\n"
          + Style.RESET_ALL)


# Funções para gerenciamento de contas
def gerar_numero_conta(contas):
    """
    Gera um novo número de conta exclusivo com base na lista de contas
    existente.

    Args:
        contas (list): Lista de contas cadastradas.

    Returns:
        int: Novo número de conta gerado.
    """
    if not contas:
        return 1

    return max([conta["numero_conta"] for conta in contas]) + 1


def criar_conta(agencia, usuarios):
    """
    Cria uma nova conta bancária para um usuário existente.

    Args:
        agencia (str): Agência da conta (deve ser "0001").
        usuarios (list): Lista de usuários cadastrados.

    Returns:
        dict: Dicionário contendo as informações da conta criada.
              None caso a agência seja inválida ou o usuário não seja
              encontrado.
    """
    if agencia != AGENCIA:
        print(Fore.RED + "Agência inválida! A agência precisa ser 0001."
              + Style.RESET_ALL)
        return None

    cpf = input(
        Fore.YELLOW + "Digite o CPF do titular da conta: " + Style.RESET_ALL)
    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print(Fore.RED +
              "Usuário não encontrado! Retornando ao menu principal!"
              + Style.RESET_ALL)
        menu_principal()
        return None

    numero_conta = gerar_numero_conta(contas)
    conta = {
        "agencia": agencia,
        "numero_conta": numero_conta,
        "titular": usuario,
        "saldo": Decimal(0.0),
        "limite_saque": Decimal(500.0),
        "numero_saques": 0,
        "extrato": "",
        "limite_saques_por_dia": 3
    }

    usuario["contas"].append(conta)
    contas.append(conta)

    print(Fore.GREEN + "Conta criada com sucesso!" + Style.RESET_ALL)
    return conta


def listar_contas(contas):
    """
    Exibe uma lista formatada de todas as contas cadastradas.

    Args:
        contas (list): Lista de contas cadastradas.
    """
    if not contas:
        print(Fore.YELLOW + "Não há contas cadastradas." + Style.RESET_ALL)
        menu_principal()
        return

    print(Fore.LIGHTBLUE_EX +
          "\n============== LISTA DE CONTAS ==============\n"
          + Style.RESET_ALL)

    for i, conta in enumerate(contas):
        titular = conta["titular"]
        agencia = conta["agencia"]
        numero_conta = conta["numero_conta"]
        saldo = conta["saldo"]

        print(f"{i+1}. Titular: {titular['nome']}\n")
        print(f"Agência: {agencia} - Conta: {numero_conta}")
        print(f"Saldo: R$ {saldo:.2f}\n")

    while True:
        opcao_continuar = input(
            Fore.YELLOW + "Deseja continuar operando? (s/n): "
            + Style.RESET_ALL)
        if opcao_continuar.lower() == "s":
            menu_principal()
            break
        elif opcao_continuar.lower() == "n":
            menu_principal()
            break
        else:
            print(Fore.RED +
                  "Opção inválida. Digite 's' para continuar ou 'n' para "
                  "voltar ao menu." + Style.RESET_ALL)


def selecionar_conta(contas):
    """
    Permite ao usuário escolher uma conta da lista de contas para realizar
    operações.

    Args:
        contas (list): Lista de contas cadastradas.

    Returns:
        dict: Dicionário contendo as informações da conta selecionada.
              None caso nenhuma conta seja selecionada ou a opção seja
              inválida.
    """
    if not contas:
        print(Fore.YELLOW + "Não há contas cadastradas." + Style.RESET_ALL)
        return None

    print(Fore.LIGHTBLUE_EX +
          "\n============== SELECIONAR CONTA ==============\n"
          + Style.RESET_ALL)

    for i, conta in enumerate(contas):
        titular = conta["titular"]
        agencia = conta["agencia"]
        numero_conta = conta["numero_conta"]
        print(
            f"{i+1}. Titular: {titular['nome']}\n   Agência: {agencia} - "
            "Conta: {numero_conta}\n")

    opcao = input(
        Fore.YELLOW + "Escolha a conta (digite o número ou 0 para sair): "
        + Style.RESET_ALL)

    try:
        opcao = int(opcao)
        if opcao <= 0 or opcao > len(contas):
            print(Fore.RED + "Opção inválida." + Style.RESET_ALL)
            return None
        return contas[opcao - 1]
    except ValueError:
        print(Fore.RED + "Opção inválida. Digite um número inteiro."
              + Style.RESET_ALL)
        return None


# Funções para transações em contas
def depositar(conta, valor):
    """
    Realiza um depósito na conta especificada.

    Args:
        conta (dict): Dicionário contendo as informações da conta.
        valor (float): Valor a ser depositado.
    """
    if valor <= 0:
        print(Fore.RED + "Valor de depósito inválido." + Style.RESET_ALL)
        menu_conta(conta)
        return

    conta["saldo"] += Decimal(valor)
    print(Fore.GREEN +
          f"Depósito de R$ {valor:.2f} realizado com sucesso!"
          + Style.RESET_ALL)
    atualizar_extrato(conta, f"Depósito: R$ {valor:.2f}")
    menu_conta(conta)


def sacar(conta, valor):
    """
    Realiza um saque na conta especificada, verificando o saldo, limites e
    atualizando as informações da conta e extrato.

    Args:
        conta (dict): Dicionário contendo as informações da conta.
        valor (float): Valor a ser sacado.
    """
    if valor <= 0:
        print(Fore.RED + "Valor de saque inválido." + Style.RESET_ALL)
        menu_conta(conta)

    if conta["saldo"] - Decimal(valor) < Decimal(SALDO_MINIMO):
        print(Fore.RED +
              f"Saldo insuficiente. O saldo mínimo é de R$ {SALDO_MINIMO:.2f}."
              + Style.RESET_ALL)
        menu_conta(conta)

    if conta["numero_saques"] >= conta["limite_saques_por_dia"]:
        print(Fore.RED +
              f"Limite de saques diários atingido. Você só pode realizar "
              f"{LIMITE_SAQUES} saques por dia." + Style.RESET_ALL)
        menu_conta(conta)

    try:
        limite_saque_decimal = Decimal(conta["limite_saque"])

        if valor > limite_saque_decimal:
            print(Fore.RED +
                  f"Valor de saque excede o limite de R$ "
                  f"{limite_saque_decimal:.2f} por saque." + Style.RESET_ALL)
            menu_conta(conta)

    except TypeError:
        print(Fore.RED +
              "Erro de conversão de limite de saque. Tente novamente."
              + Style.RESET_ALL)
        menu_conta(conta)

    conta["saldo"] -= Decimal(valor)
    conta["numero_saques"] += 1

    print(Fore.GREEN +
          f"Saque de R$ {valor:.2f} realizado com sucesso!\n"
          + Style.RESET_ALL)
    atualizar_extrato(conta, f"Saque: R$ {-valor:.2f}")

    while True:
        opcao_continuar = input(
            Fore.YELLOW + "Deseja continuar operando na conta? (s/n): "
            + Style.RESET_ALL)
        if opcao_continuar.lower() == "s":
            menu_conta(conta)
            break
        elif opcao_continuar.lower() == "n":
            menu_principal()
            break

        else:
            print(Fore.RED +
                  "Opção inválida. Digite 's' para continuar ou 'n' para "
                  "voltar ao menu." + Style.RESET_ALL)
            menu_conta(conta)


def atualizar_extrato(conta, transacao):
    """
    Adiciona uma nova transação ao extrato da conta, formatando a data e hora
    e o valor da operação.

    Args:
        conta (dict): Dicionário contendo as informações da conta.
        transacao (str): Descrição da transação a ser adicionada.
    """
    data_hora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    conta["extrato"] = f"{data_hora} - {transacao}\n" + conta["extrato"]


def exibir_extrato(conta):
    """
    Mostra o extrato da conta formatado, incluindo histórico de transações e
    saldo atual.

    Args:
        conta (dict): Dicionário contendo as informações da conta.
    """
    if not conta["extrato"]:
        print(Fore.YELLOW + "Não há movimentações no extrato."
              + Style.RESET_ALL)
        menu_conta(conta)
        return

    print(Fore.BLUE + "\n============== EXTRATO BANCÁRIO ==============\n"
          + Style.RESET_ALL)
    print(f"Titular: {conta['titular']['nome']}")
    print(f"Agência: {conta['agencia']} - Conta: {conta['numero_conta']}")
    print("-" * 50)
    print(conta["extrato"])
    print("-" * 50)
    print(Fore.BLUE +
          f"Saldo atual: R$ {conta['saldo']:.2f}\n" + Style.RESET_ALL)
    menu_conta(conta)


# Menu principal
def menu_principal():
    """
    Exibe o menu principal do sistema bancário e permite ao usuário escolher
    a opção desejada para gerenciar usuários e contas.

    Esta função exibe um banner inicial, apresenta as opções disponíveis
    (criar usuário, nova conta, listar contas, sair) e direciona o usuário
    para a função correspondente de acordo com a escolha.

    Retorna:
        None
    """
    print(Fore.MAGENTA +
          "\n==================== BANCO XYZ ====================\n"
          + Style.RESET_ALL)
    print(Fore.MAGENTA + "[u]\tCriar Usuário" + Style.RESET_ALL)
    print(Fore.MAGENTA + "[c]\tNova Conta" + Style.RESET_ALL)
    print(Fore.MAGENTA + "[l]\tListar Contas" + Style.RESET_ALL)
    print(Fore.MAGENTA + "[q]\tSair" + Style.RESET_ALL)

    opcao = input(Fore.YELLOW + "Escolha uma opção: " + Style.RESET_ALL)

    if opcao.lower() == 'u':
        criar_usuario(usuarios)
    elif opcao.lower() == 'c':
        conta_criada = criar_conta(AGENCIA, usuarios)
        if conta_criada:
            menu_conta(conta_criada)
    elif opcao.lower() == 'l':
        listar_contas(contas)
    elif opcao.lower() == 'q':
        print(Fore.GREEN + "Saindo do sistema..." + Style.RESET_ALL)
    else:
        print(Fore.RED + "Opção inválida." + Style.RESET_ALL)
        menu_principal()


# Conta Menu
def menu_conta(conta):
    """
    Exibe o menu de operações bancárias para uma conta específica.

    Esta função exibe informações da conta selecionada (titular, agência,
    conta, saldo) e apresenta as opções disponíveis (depositar, sacar,
    extrato, voltar ao menu anterior). O usuário escolhe a opção desejada,
    e a função direciona para a função correspondente para realizar a
    operação na conta selecionada ou retornar ao menu principal.

    Args:
        conta (dict): Dicionário contendo as informações da conta selecionada.

    Retorna:
        None
    """
    print(Fore.CYAN + "\n============== CONTA BANCÁRIA ==============\n"
          + Style.RESET_ALL)
    print(f"Titular: {conta['titular']['nome']}")
    print(f"Agência: {conta['agencia']} - Conta: {conta['numero_conta']}")
    print(f"Saldo: R$ {conta['saldo']:.2f}")
    print(Fore.CYAN + "[d]\tDepositar" + Style.RESET_ALL)
    print(Fore.CYAN + "[s]\tSacar" + Style.RESET_ALL)
    print(Fore.CYAN + "[e]\tExtrato" + Style.RESET_ALL)
    print(Fore.CYAN + "[q]\tVoltar ao menu anterior" + Style.RESET_ALL)

    opcao = input(Fore.YELLOW + "Escolha uma opção: " + Style.RESET_ALL)

    try:
        if opcao.lower() == 'd':
            valor = float(
                input(Fore.YELLOW + "Informe o valor do depósito: R$ "
                      + Style.RESET_ALL))
            depositar(conta, valor)
        elif opcao.lower() == 's':
            valor = float(
                input(Fore.YELLOW + "Informe o valor do saque: R$ "
                      + Style.RESET_ALL))
            sacar(conta, valor)
        elif opcao.lower() == 'e':
            exibir_extrato(conta)
        elif opcao.lower() == 'q':
            menu_principal()
        else:
            print(Fore.RED + "Opção inválida." + Style.RESET_ALL)
            menu_conta(conta)
    except ValueError:
        print(Fore.RED +
              "Opção inválida. Digite um número inteiro ou letra minúscula."
              + Style.RESET_ALL)
        menu_conta(conta)


# Inicia o programa
if __name__ == "__main__":
    menu_principal()
