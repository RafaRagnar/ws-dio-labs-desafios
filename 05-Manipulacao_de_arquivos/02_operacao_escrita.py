arquivo = open(
    "D:/Workspace/ws-dio/05-Manipulacao_de_arquivos/teste.txt", "w"
)
arquivo.write("Escrevendo dados em um novo arquivo.")
arquivo.writelines(["\n", "escrevendo", "\n", "um",
                   "\n", "novo", "\n", "texto"])
arquivo.close()
