menu = """
\nSistema Bancário Simplificado
-------------------------------
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite_saque = 500
extrato = ""
numero_saques = 0
limite_saques_por_dia = 3

while True:
    opcao = input(menu).lower()

    if opcao == "d":
        valor_deposito = float(input("Informe o valor do depósito: R$ "))

        if valor_deposito > 0:
            saldo += valor_deposito
            extrato += f"Depósito: R$ {valor_deposito:.2f}\n"
            print(f"Depósito realizado com sucesso! Saldo atual: R$ {
                  saldo:.2f}")
        else:
            print("Valor inválido. O valor do depósito deve ser positivo.")

    elif opcao == "s":
        valor_saque = float(input("Informe o valor do saque: R$ "))

        excede_saldo = valor_saque > saldo
        excede_limite = valor_saque > limite_saque
        excede_saques = numero_saques >= limite_saques_por_dia

        if excede_saldo:
            print("Operação falhou! Saldo insuficiente.")
        elif excede_limite:
            print(
                f"Operação falhou! Limite de saque excedido (R$ {limite_saque:.2f}).")
        elif excede_saques:
            print(f"Operação falhou! Limite de saques por dia excedido ({
                  limite_saques_por_dia} saques).")
        elif valor_saque > 0:
            saldo -= valor_saque
            extrato += f"Saque: R$ {valor_saque:.2f}\n"
            numero_saques += 1
            print(f"Saque realizado com sucesso! Saldo atual: R$ {saldo:.2f}")
        else:
            print("Valor inválido. O valor do saque deve ser positivo.")

    elif opcao == "e":
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==========================================")

    elif opcao == "q":
        print("Obrigado por utilizar o Sistema Bancário Simplificado!")
        break

    else:
        print("Operação inválida. Tente novamente.")
