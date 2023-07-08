import sys
import logging as logger

def get_args():
    """
    Função auxiliar para resgatar os valores de entrada nos argumentos de execução 
    do programa.

    Os argumentos são obitidos de duas maneiras:
        python main.py <caminho_do_arquivo>
        python main.py <caminho_do_arquivo> <caminho_de_destino>

    No primeiro, a saída é impressa no terminal. O segundo recebe um arquivo de destino e formata a execução para tal formato.
    """
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
    
    return file_path,out_file_path