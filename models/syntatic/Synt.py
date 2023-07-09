import logging as logger

from models.lexic.Lexer import Lexer
from models.syntatic.Procedures import Procedures

from models.error.GenericError import Error
from models.error.LexicError import LexicError
from models.error.SyntaxError import SyntaxError

from utility.consts import SyntSymbols, Tokens, ErrorCode

class Synt():
     """
        Classe que implementa o analisador sintático no modelo Descendente Preditivo Sem Retrocesso Com Erro, utilizando um pilha (@symbols_stack) para simular a árvore.

        @lexer -> Analisador léxico
        @procs -> Classe que implementa as regras gramaticais
        @curr_token -> próximo token presente na cadeia de entrada.
        @symbols_stack -> pilha de símbolos não terminais (@utility.consts.SyntSymbols) e terminais (@utility.consts.Tokens)

    """
     def __init__(self):
          self.__lexer = Lexer()
          self.__procs = Procedures()
          self.__curr_token = None
          self.__curr_line_code = 1
          self.__errors_list = []
          self.__symbols_stack = [SyntSymbols.INITIAL]
          self.out_file_path = None
     
     def set_curr_token(self,val:Tokens) -> None:
          self.__curr_token = val
     
     def get_curr_token(self) -> Tokens:
          return self.__curr_token

     def pop_stack(self) -> SyntSymbols | Tokens:
          return self.__symbols_stack.pop()
     
     def push_stack(self,values:list) -> None:
          values.reverse()
          for v in values:
               self.__symbols_stack.append(v)

     def is_empty_stack(self):
          return len(self.__symbols_stack) == 0   
     
     def get_line(self) -> int:
          return self.__curr_line_code
    
     def next_line(self) -> None:
         self.__curr_line_code += 1
     
     def save_error(self,msg:str,is_sintax:bool):
          self.__errors_list.append(f"Erro {'sintático' if is_sintax else 'léxico'} na linha {self.get_line():}: {msg}\n")

     def get_errors(self):
          return self.__errors_list
     
     def has_errors(self):
          return len(self.__errors_list) != 0
     @staticmethod
     def is_non_terminal(var):
          return var in SyntSymbols.SYMB_LIST

     def execute_procedure(self,code):
          """Método que empilha os símbolos terminais e não terminais conforme a análise preditiva sem retrocesso, realizando os possíveis tratamentos para os erros léxicos e sintáticos encontrados. Existem tratamentos específicos para os erros mais previsíeis e, para um erro genérico de token imprevisto, realiza o processo de resincronização (modo pânico)"""
          
          # Detecção de Comentários mal formatados
          if(self.get_curr_token()[1] == Tokens.COMMENT_ERROR):
               self.error_treatment(LexicError(ErrorCode.BAD_COMMENT),code)
          
          
          next_symbol = self.pop_stack()

          while self.is_non_terminal(next_symbol): # processo de empilhamento de terminais e não terminais
               procedure_return = self.__procs.next_procedure(next_symbol,self.get_curr_token())
               if not isinstance(procedure_return,Error):
                    self.push_stack(procedure_return)
                    next_symbol = self.pop_stack()
               else: # Tratamento de erros durante o desempilhamento (símbolos imprevistos para a regra selecionada)
                    self.error_treatment(procedure_return,code)
                    next_symbol = self.pop_stack()

          
          if (next_symbol == self.get_curr_token()[1]):
               return True
          
          # Tratamento de erros previsiveis
          if(next_symbol == Tokens.ID):
               if(self.get_curr_token()[1] == Tokens.NUM_INT) | (self.get_curr_token()[1] == Tokens.NUM_REAL) | (self.get_curr_token()[1] == Tokens.NUM_ERROR) | (self.get_curr_token()[1] == Tokens.TOKEN_ERROR):
                    self.error_treatment(LexicError(ErrorCode.BAD_IDENT))
                    return False
          elif(next_symbol == Tokens.NUM_INT) | (next_symbol == Tokens.NUM_INT):
               if(self.get_curr_token()[1] == Tokens.NUM_ERROR):
                    self.error_treatment(LexicError(ErrorCode.BAD_NUMBER))
                    return False
          elif(self.get_curr_token()[1] == Tokens.TOKEN_ERROR):
                    self.error_treatment(LexicError(ErrorCode.BAD_TOKEN))
                    return False
          elif(next_symbol == Tokens.SEMICOL):
               self.error_treatment(SyntaxError(ErrorCode.EXPECTED_TOKEN,"';' esperado"))
               return False
          elif(next_symbol == Tokens.COLON):
               self.error_treatment(SyntaxError(ErrorCode.EXPECTED_TOKEN,"':' esperado"))
               return False
          elif(next_symbol == Tokens.COMMA):
               self.error_treatment(SyntaxError(ErrorCode.EXPECTED_TOKEN,"',' esperado"))
               return False
          elif(next_symbol == Tokens.OPEN_PAR):
               self.error_treatment(SyntaxError(ErrorCode.EXPECTED_TOKEN,"'(' esperado"))
               return False
          elif(next_symbol == Tokens.CLOSE_PAR):
               self.error_treatment(SyntaxError(ErrorCode.EXPECTED_TOKEN,"')' esperado"))
               return False
          elif(next_symbol == Tokens.SET):
               if(self.get_curr_token()[1] == Tokens.EQUALS):
                    return self.error_treatment(LexicError(ErrorCode.BAD_SET))
               else:
                    self.error_treatment(SyntaxError(ErrorCode.UNEXPECTED_TOKEN,f"'{self.get_curr_token()[0]}' inesperado."))
          


     def compile(self,file_path, out_file_path):
          """Método principal da classe. Recebe os caminhos dos arquivos de entrada e saída e gerencia a coleta de token pelo Lexer e criação da árvore descendente (vide função @execute_procedure)"""

          self.out_file_path = out_file_path

          logger.info("Iniciando análise semântica")

          with open(file_path,'r') as code:
               line = code.readline()

               while len(line) > 0:
               # Leitura do arquivo linha a linha
                    self.__lexer.set_buffer(line) # Seta o buffer do analisador léxico
                    get_next = True # Define se deve puxar o próximo token ou não (tratamento de erros pode puxar também)
                    
                    while not self.__lexer.empty_buffer():
                         if get_next: # Em caso de erro, o @error_treatment já posiciona o lexer em um token sincronizado, então não é necessário pegar o próximo.
                              token = self.__lexer.get_next_token()
                              self.set_curr_token(token)

                         if(self.get_curr_token()[1] == Tokens.COMMENT)| ((self.get_curr_token()[1] == None) and (self.__symbols_stack[-1] != Tokens.SEMICOL)):
                              continue 

                         get_next = self.execute_procedure(code) # Executa a árvore descendente
                    self.next_line()
                    line = code.readline()
               
               logger.info("Todos os tokens foram identificados.")
               logger.info("Realizando últimas verificações...")
                    
               if not self.is_empty_stack():
                    self.error_treatment(SyntaxError(ErrorCode.UNEXPECTED_EOF,'final de arquivo inesperado.'))
               
               self.show_compile_result()

     def show_compile_result(self):
          """Imprime/Escreve no arquivo o resultado da compílação do arquivo."""

          if self.out_file_path is None:
               if self.has_errors():
                    for error in self.get_errors():
                         logger.info(error)
               else:
                    logger.info('Nenhum erro de compilação encontrado.')
                    logger.info('Compilação bem sucedida.')
          else:
               with open(self.out_file_path,'w') as file:
                    if self.has_errors():
                         for error in self.get_errors():
                              file.write(error)
                    else:
                         file.write('Compilação bem sucedida.')

     def error_treatment(self,error:Error,code=None):
          """ Método de tratamento de erros. Sempre recebe o erro e, em alguns códigos, o ponteiro de leitura do arquivo de entrada (quando é necessário repocionar o Lexer no token correto).

          Os erros são reconhecidos pelo seu código (em utility.consts.ErrorCode) e separados em LexicError e SyntError ( vide models.error). Com base no código gerado, um tratamento específico é realizado

          O retorno esperado para esse função é booleano, sendo:
          True -> é necessário pegar o próximo token pelo @compile()
          False -> Lexer foi posicionado no token sincronizado, não é necessário pegar o próximo em compile
          
          """
          
          if(isinstance(error,LexicError)):
               self.save_error(error.get_msg(),False)
               # Detecção de Erros léxicos básicos
               if(error.get_code() == ErrorCode.BAD_COMMENT):
                    # Caso seja um comentário sem fechamento, registra o erro e puxa o próximo token
                    self.__lexer.set_buffer(code.readline())
                    self.set_curr_token(self.__lexer.get_next_token())
                    return False
               elif(error.get_code() == ErrorCode.BAD_IDENT):
                    # Caso seja um identificador mal formatado, trabalha tentando identificar os próximos
                    # Verifica se o próximo Token é a continuação do nome do identificador. Se for, puxa
                    # o próximo token, para pular o identificador e continuar a análise
                    self.set_curr_token(self.__lexer.get_next_token())
                    if(self.get_curr_token()[1] == Tokens.ID):
                         self.set_curr_token(self.__lexer.get_next_token())
                         return False
               elif(error.get_code() == ErrorCode.BAD_NUMBER):
                    # Caso seja um número mal formatado, resgata o próximo token.
                    # Se se tratar de um identificador, entende-se como o erro de digitação que acompanha o número e o pula
                    self.set_curr_token(self.__lexer.get_next_token())
                    if(self.get_curr_token() == Tokens.ID):
                         self.set_curr_token(self.__lexer.get_next_token())
                         return None
               elif(error.get_code() == ErrorCode.BAD_TOKEN):
                    # Se for unicamente um caractere não pertencente a linguagem, pega o próximo token.
                    self.set_curr_token(self.__lexer.get_next_token())
                    return None
               elif(error.get_code() == ErrorCode.BAD_SET):
                    return True
               
          elif(isinstance(error,SyntaxError)):
               #Detecção de Erros sintáticos
               self.save_error(error.get_msg(),True)
               #Erro de final de arquivo inesperado
               if(error.get_code() == ErrorCode.UNEXPECTED_EOF): # Fim do arquivo inesperado
                    return False
               
               elif(error.get_code() == ErrorCode.PROGRAM_EXPECTED):
                    # Programa começa sem 'program'
                    self.push_stack([Tokens.PROGRAM,Tokens.ID,Tokens.SEMICOL,SyntSymbols.BODY,Tokens.DOT])
                    return self.resync(code)
               
               elif(error.get_code() == ErrorCode.EXPECTED_TOKEN):
                    # Algum token esperado não foi detectado (como '(',')',';',':', entre outros).
                    return None
               
               elif(error.get_code() == ErrorCode.UNEXPECTED_TOKEN):
                    # Um token inesperado foi encontrado em  alguma regra gramatical
                    return self.resync(code)

              
     def resync(self,code):
          """Caso seja detectado um erro sintático, o código entra é modo pânico e tenta realizar a resincronização dos tokens.
          Tokens resincronizantes são  ')', ';' , 'begin', 'end', '.', ',' e ':' e estão declarados em utility.consts.Tokens.RESYNC
          
          Primeiramente tenta encontrar algum símbolo de ressincronização no próprio arquivo. Quando encontra o primeiro, desempilha a árvore até chegar em um símbolo igual e, nesse ponto, o código é considerado ressincronizado.

          Isso é possível em quase todos os eventos pelas formas em que as regras da gramática estão definidas, pois esses símbolos sempre estão presentes em pontos significativos do código: final de blocos de execução, comandos ou declarações, permitindo um "reset" na árvore para ler o próximo comando. 
          """

          while(self.get_curr_token()[1] not in Tokens.RESYNC):
               # Primeiramente tenta encontrar um token resincronizante no código
               if(self.__lexer.empty_buffer()):
                    line = code.readline()
                    self.next_line()
                    if len(line) == 0: # Se acabar as linhas do arquivo, retorna EOF
                         return self.error_treatment(SyntaxError(ErrorCode.UNEXPECTED_EOF,'final de arquivo inesperado.'))
                    self.__lexer.set_buffer(line)

               self.set_curr_token(self.__lexer.get_next_token())
          
          # Uma vez setado o próximo token de sincronização, percorre a pilha até encontrá-lo
          if((len(self.__symbols_stack) > 0)):
               while(self.__symbols_stack[-1] != self.get_curr_token()[1]):
                    self.pop_stack()
                    if(len(self.__symbols_stack) > 0):
                         break
          
          if((len(self.__symbols_stack) > 0) == 0):
               return self.error_treatment(SyntaxError(ErrorCode.FALIED_RESYNC,'não foi possível resincronizar a compilação'))
          
          return False

               
