import re


def validar_numero_telefone(numero):
    """
    Função para validar se um número de telefone está no formato correto.

    Parâmetros:
      numero (str): O número de telefone a ser validado.

    Retorno:
      str: Mensagem indicando se o número é válido ou inválido.
    """

    # Expressão regular para validar o formato do número de telefone
    regex = r"^\(\d{2}\) \d{5}-\d{4}$"

    # Valida o número de telefone usando a expressão regular
    if re.search(regex, numero):
        return "Número de telefone válido."
    else:
        return "Número de telefone inválido."


# Exemplos de uso
numero1 = "(88) 98888-8888"
numero2 = "(11)91111-1111"
numero3 = "225555-555"

print(f"Número {numero1}: {validar_numero_telefone(numero1)}")
print(f"Número {numero2}: {validar_numero_telefone(numero2)}")
print(f"Número {numero3}: {validar_numero_telefone(numero3)}")
