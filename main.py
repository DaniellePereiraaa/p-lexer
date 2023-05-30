import sys, os
import logging as logger
from models.Lexer import Lexer

# Configuração de logger
logger.basicConfig(encoding='utf-8', level=logger.ERROR)

if __name__ == '__main__':

    # INFO: Verificação das diretivas de execução
    args = sys.argv

    if len(args) < 2:
        logger.critical(" Quantidade de argumentos indesejada. Tente algo como: python main.py <caminho_do_arquivo>")
        sys.exit(1)

    # INFO: Verificação da existência do arquivo a ser lido
    file_path = args[1]

    if not os.path.exists(file_path):
        logger.critical(f" O arquivo informado ({file_path}) não foi encontrado.")
        sys.exit(1)

    # INFO: Análise Léxica do código
    lexer = Lexer()

    with open(file_path,'r') as code:
        line = code.readline()
        lexer.set_buffer(line)
        while not lexer.empty_buffer():
            print(lexer.get_next_token())
                
        

