import sys, os
import logging as logger

from utility.args import get_args

from models.syntatic.Synt import Synt

# Configuração de logger
logger.basicConfig(encoding='utf-8', level=logger.INFO)

if __name__ == '__main__':

    # file_path, out_file_path = get_args() # Obtem os arquivos de origem e destino

    file_path = './test/code1.in'
    out_file_path = None
    if not os.path.exists(file_path):
        logger.critical(f" O arquivo informado ({file_path}) não foi encontrado.")
        sys.exit(1)

    # INFO: Análise Sintática
    synt = Synt()
    synt.compile(file_path,out_file_path)
    