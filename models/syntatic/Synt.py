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
     
     def register_new_error(self,msg:str,is_sintax:bool):
          self.__errors_list.append(f"Erro {'sintático' if is_sintax else 'léxico'} na linha {self.get_line():}: {msg}\n")

     def get_errors(self):
          return self.__errors_list
     
     def has_errors(self):
          return len(self.__errors_list) != 0
     @staticmethod
     def is_non_terminal(var):
          return var in SyntSymbols.SYMB_LIST

     def execute_procedure(self):
          if(self.is_empty_stack()):
               self.error_treatment(SyntaxError(ErrorCode.BAD_DOT,"ponto final bloqueando leitura do código."))
          if(self.get_curr_token()[1] == Tokens.COMMENT_ERROR):
               return LexicError(ErrorCode.BAD_COMMENT)
          elif(self.get_curr_token()[1] == Tokens.NUM_ERROR):
               return LexicError(ErrorCode.BAD_IDENT)
          elif(self.get_curr_token()[1] == Tokens.STRING_ERROR):
               return LexicError(ErrorCode.BAD_STRING)
          
          next_symbol = self.pop_stack()
          while ((self.is_non_terminal(next_symbol)) and not(isinstance(next_symbol,SyntaxError))):
               procedure_return = self.__procs.next_procedure(next_symbol,self.get_curr_token())

               if(isinstance(procedure_return,SyntaxError)):
                    next_symbol = procedure_return
               else:
                    self.push_stack(procedure_return)
                    next_symbol = self.pop_stack()


          if(not isinstance(next_symbol,SyntaxError)):
               if(next_symbol != self.get_curr_token()[1]):
                    if(next_symbol == Tokens.CLOSE_PAR):
                         next_symbol = SyntaxError(ErrorCode.EXPECTED_TOKEN," ')' esperado.")
                    elif(next_symbol == Tokens.SEMICOL):
                         next_symbol = SyntaxError(ErrorCode.EXPECTED_TOKEN,"';' esperado")
                    elif(next_symbol == Tokens.BEGIN):
                         next_symbol = SyntaxError(ErrorCode.EXPECTED_TOKEN,"'begin' esperado")
                    elif(next_symbol == Tokens.END):
                         next_symbol = SyntaxError(ErrorCode.EXPECTED_TOKEN,"'end' esperado")

                    else:
                         next_symbol = SyntaxError(ErrorCode.UNEXPECTED_TOKEN,f" '{self.get_curr_token()[0]}' inesperado.")
          
          return next_symbol if isinstance(next_symbol,SyntaxError) else True

     def compile(self,file_path, out_file_path):

          self.out_file_path = out_file_path

          logger.info("Iniciando análise semântica")

          with open(file_path,'r') as code:
               for line in code:
                    self.__lexer.set_buffer(line)
                    while not self.__lexer.empty_buffer():
                         token = self.__lexer.get_next_token()
                         logger.info("obtendo token...")
                         if (token is not None):
                                   if(token[1] is Tokens.COMMENT):
                                        continue

                                   self.set_curr_token(token)
                                   proc_return = self.execute_procedure()  
                                   if(isinstance(proc_return,Error)):
                                        logger.info("Erro encontrado, iniciando registro e tratamento.")
                                        self.error_treatment(proc_return)
                    self.next_line()

               logger.info("Todos os tokens foram identificados.")
               logger.info("Realizando últimas verificações...")
               
               if not self.is_empty_stack():
                    self.error_treatment(SyntaxError(ErrorCode.UNEXPECTED_EOF,'final de arquivo inesperado.'))
               
               self.show_compile_result()
               

     def show_compile_result(self):
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


     def error_treatment(self,error:Error):
          if(isinstance(error,LexicError)):
               if(error.get_code() == ErrorCode.BAD_IDENT):
                    next_expected  = self.pop_stack()
                    if(next_expected == SyntSymbols.NUMBER):
                         self.register_new_error('número mal formatado',False)
                    else:
                         self.register_new_error(error.get_msg(),False)
                    return next_expected
               else:
                    self.register_new_error(error.get_msg(),False)
          elif(isinstance(error,SyntaxError)):
               if(error.get_code() == ErrorCode.PROGRAM_EXPECTED):
                    self.register_new_error(error.get_msg(),True)
                    stack_correction = self.__procs.next_procedure(SyntSymbols.INITIAL,('program',Tokens.PROGRAM))
                    self.push_stack(stack_correction)
                    self.pop_stack() # Remove o 'program' do topo da pilha
                    # executa novamente o procedure com o token lido, para continuar validá-lo como ident
                    proc_return = self.execute_procedure()  
                    if(isinstance(proc_return,Error)):
                         self.error_treatment(proc_return)
               elif(error.get_code() == ErrorCode.BAD_IDENT):
                    self.register_new_error(error.get_msg(),False)
                    self.push_stack([SyntSymbols.VARIABLES])
               elif(error.get_code() == ErrorCode.EXPECTED_TOKEN):
                    self.register_new_error(error.get_msg(),True)
                    proc_return = self.execute_procedure()
                    if(isinstance(proc_return,Error)):
                         self.error_treatment(proc_return)
               elif(error.get_code() == ErrorCode.UNEXPECTED_TOKEN):
                     pass
               elif(error.get_code() == ErrorCode.UNEXPECTED_EOF):
                    self.register_new_error(error.get_msg(),True)
               elif(error.get_code() == ErrorCode.BAD_DOT):
                    self.register_new_error(error.get_msg(),True)
                    self.show_compile_result()

          else:
               logger.critical('Erro inesperado encontrado. Encerrado execução.') 
               exit(1)


