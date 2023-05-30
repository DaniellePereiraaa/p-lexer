import sys, os
import logging as logger
from models.Lexer import Lexer

# Configuração de logger
logger.basicConfig(encoding='utf-8', level=logger.WARN)

if __name__ == '__main__':

    # INFO: Verificação das diretivas de execução
    args = sys.argv

    if len(args) < 2:
        logger.critical(" Quantidade de argumentos indesejada. Tente algo como:\n\t python main.py <caminho_do_arquivo> \n\t python main.py <caminho_do_arquivo> <caminho_de_destino>")
        sys.exit(1)

    # INFO: Verificação da existência do arquivo a ser lido
    file_path = args[1]
    out_file_path = None

    if len(args) > 2:
        out_file_path = args[2]

    if not os.path.exists(file_path):
        logger.critical(f" O arquivo informado ({file_path}) não foi encontrado.")
        sys.exit(1)

    # INFO: Análise Léxica do código
    lexer = Lexer()
    if out_file_path is None:
        with open(file_path,'r') as code:
                for line in code:
                    lexer.set_buffer(line)
                    while not lexer.empty_buffer():
                        token = lexer.get_next_token()
                        if token is not None:
                            print(token)
                        print("Pressione qualquer tecla para continuar...")
                        input()
    else:
          with open(file_path,'r') as code, open(out_file_path,'w') as out:
                for line in code:
                    lexer.set_buffer(line)
                    while not lexer.empty_buffer():
                        token = lexer.get_next_token()
                        if token is not None:
                            out.write(f'{token[0]}, {token[1]}\n')
                
        

