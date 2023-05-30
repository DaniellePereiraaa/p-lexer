import logging as logger
import sys

from models.GenericAutomate import Automate
from utility.consts import Tokens

class CommentAutomate(Automate):
    """
    descrição: realiza o reconhecimento de comentários de linha única no código.
    Executado assim que aparece um '{' e aguarda o fechamento '}'. Caso não encontre até o final
    da linha, identifica como erro.
    """

    class States:
        COMMENT_READING = 0
        COMMMENT_ENDED = 1

    def __init__(self) -> None:
        super().__init__()
        self.token_value = ''
    
    def process_state(self,c:str) -> None | tuple[str,str]:
        if self.get_state() == self.States.COMMENT_READING:
            if c == '\n':
                return (self.token_value,Tokens.COMMENT_ERROR)
            
            self.token_value += c

            if c == '}':
                self.set_state(self.States.COMMMENT_ENDED)
                self.process_state(c)
        
        elif self.get_state() == self.States.COMMMENT_ENDED:
            return (self.token_value,Tokens.COMMENT)
        
        
