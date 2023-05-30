import logging as logger
import sys

from models.GenericAutomate import Automate
from utility.consts import Tokens

class ComparatorAutomate(Automate):
    """
    Realiza o reconhecimento dos possíveis símbolos comparadores da linguagem. São eles:
    :=  ->      atribuição (SET)
    >   ->      maior
    >=  ->      maior igual
    <   ->      menor
    <=  ->      menor igual
    !   ->      negação
    !=  ->      diferente

    Também identifica os dois pontos, uma vez que ele faz parte de um dos símbolos anteriores.
    """

    class States:
        COMPARATOR_INITIAL = 0

        COLON = 1 #     Estado Final
        SET = 2 #       Estado final

        GREATER = 3 #   Estado final
        GREATER_EQ = 4# Estado final

        LOWER = 5 #     Estado final
        LOWER_EQ = 6 #  Estado final

        NOT = 7 #       Estado final
        NOT_EQ = 8 #    Estado final

        SINGLE_EQ = 9
        EQUALS = 10 #   Estado final


    def __init__(self) -> None:
        super().__init__()
        self.token_value = ''
    
    def process_state(self,c:str) -> None | tuple[str,str]:
        
        # LABEL: Processamento do pseudo-estado inicial
        if self.get_state() == self.States.COMPARATOR_INITIAL: 
            if (c == ':'):
                self.set_state(self.States.COLON)

            elif (c == '>'):
                self.set_state(self.States.GREATER)
            
            elif (c == '<'):
                self.set_state(self.States.LOWER)
            
            elif (c == '!'):
                self.set_state(self.States.NOT)
            
            elif (c == '='):
                self.set_state(self.States.SINGLE_EQ)
            
            else:
                logger.critical(' De alguma forma, o automato de comparadores foi selecionado erroneamente.')
                sys.exit(1)

        # LABEL: Processamento do estado de COLON (recebeu ':' no primeiro estado)
        elif self.get_state() == self.States.COLON:
            if c == '=':
                self.set_state(self.States.SET)
                return self.process_state(c)
            else:
                self.set_previous_char(c)
                return (':',Tokens.COLON)
        
        # LABEL: Processamento estado de SET (leu ':=')
        elif self.get_state() == self.States.SET:
            return (':=',Tokens.SET)
        
        # LABEL: Processamento do estado de GREATER (recebeu '>' no primeiro estado)
        elif self.get_state() == self.States.GREATER: 
            if c == '=':
                self.set_state(self.States.GREATER_EQ)
                return self.process_state(c)
            else:
                self.set_previous_char(c)
                return ('>',Tokens.GREATER)
        
        # LABEL: Processamento estado de GREATER_EQ (leu '>=')
        elif self.get_state() == self.States.GREATER_EQ:
            return ('>=',Tokens.GREATER_EQ)
        
        # LABEL: Processamento do estado de LOWER (recebeu '<' no primeiro estado)
        elif self.get_state() == self.States.LOWER: 
            if c == '=':
                self.set_state(self.States.LOWER_EQ)
                return self.process_state(c)
            else:
                self.set_previous_char(c)
                return ('<',Tokens.LOWER)
        
        # LABEL: Processamento estado de GREATER_EQ (leu '>=')
        elif self.get_state() == self.States.LOWER_EQ:
            return ('<=',Tokens.LOWER_EQ)
        
        # LABEL: Processamento do estado de NOT (recebeu '!' no primeiro estado)
        elif self.get_state() == self.States.NOT: 
            if c == '=':
                self.set_state(self.States.NOT_EQ)
                return self.process_state(c)
            else:
                self.set_previous_char(c)
                return ('!', Tokens.NOT)
        
        # LABEL: Processamento estado de GREATER_EQ (leu '!=')
        elif self.get_state() == self.States.NOT_EQ:
            return ('!=', Tokens.NOT_EQ)

        # LABEL: Processamento do estado de NOT (recebeu '=' no primeiro estado)
        elif self.get_state() == self.States.SINGLE_EQ:
            if c != '=': 
                self.set_previous_char(c)
                return ('=',Tokens.EQ_ERROR)

            self.set_state(self.States.EQUALS)
            self.process_state(c)
        
        # LABEL: Processamento estado de GREATER_EQ (leu '==')
        elif self.get_state() == self.States.EQUALS:
            return ('==',Tokens.EQUALS)

        
            
            
        
        


            
        
