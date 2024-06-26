from pathlib import Path

BASE_DIR = Path(__file__).parent
print(BASE_DIR)


arquivo = open(
    'D:/Workspace/ws-dio/05-Manipulacao_de_arquivos/lorem.txt', 'r')
# print(arquivo.read())
for linha in arquivo.readlines():
    print(linha)
# tip
# while len(linha := arquivo.readline()):
#     print(linha)

arquivo.close()
