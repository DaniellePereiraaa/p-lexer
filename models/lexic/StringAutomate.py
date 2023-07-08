import logging as logger
import sys

from models.lexic.GenericAutomate import Automate
from utility.consts import Tokens

class StringAutomate(Automate):
    """
    Faz o reconhecimento de strings e chars. Ambos são identificados como strings pelo
    reconhecedor léxico. Uma string é sempre iniciada por aspas simples ou duplas, e
    seu final é identificado pelo mesmo que iniciou o automato. Isto é: sempre que uma string é
    iniciada por aspas simples, será encerrada por aspas simples, equivalentemente para aspas duplas.
    """

    class States:
        STRING_READING = 0
        STRING_COMPLETE = 1

    def __init__(self) -> None:
        super().__init__()
        self.token_value = ''
      
    def process_state(self,c:str) -> None | tuple[str,str]:
        if self.get_state() == self.States.STRING_READING:
            if self.token_value == '':
                self.token_value += c
            elif (c != self.token_value[0]): 
                self.token_value += c
            else:
                self.token_value += c
                self.set_state(self.States.STRING_COMPLETE)
                return self.process_state(c)

        elif self.get_state() == self.States.STRING_COMPLETE:
            return (self.token_value,Tokens.STRING)