import logging as logger

from models.lexic.Lexer import Lexer

class Synt():

    def __init__(self):
        self.__lexer = Lexer()
    
    def compile(self,file_path, out_file_path):
        logger.info('Iniciando análise sintática.')
        logger.info(f'Arquivo de entrada:{file_path}')
        logger.info(f'Arquivo de entrada:{file_path}')
        logger.info(f'Arquivo de saída:{out_file_path}')

        if out_file_path is None:
            with open(file_path,'r') as code:
                    for line in code:
                        self.__lexer.set_buffer(line)
                        while not self.__lexer.empty_buffer():
                            token = self.__lexer.get_next_token()
                            if token is not None:
                                print(token)
                            # print("Pressione qualquer tecla para continuar...")
                                # input()
        else:
            with open(file_path,'r') as code, open(out_file_path,'w') as out:
                    for line in code:
                        self.__lexer.set_buffer(line)
                        while not self.__lexer.empty_buffer():
                            token = self.__lexer.get_next_token()
                            if token is not None:
                                out.write(f'{token[0]}, {token[1]}\n')


