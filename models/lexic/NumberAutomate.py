import logging as logger
import sys

from models.lexic.GenericAutomate import Automate
from utility.consts import Tokens , CharGroup

class NumberAutomate(Automate):
    """
    Faz o reconhecimento de números inteiros e reais. Ativado sempre que um dígito aparece fora
    do contexto de um identificador. A princípio, reconhece como um inteiro, até que seja econtrado
    um '.', passando a identificar o número como real. 

    Quando encontra esse '.', é necessário que apareça um dígito imediatamente após. Caso contrário, 
    será considerado um erro.
    """

    class States:
        NUMBER_INT_READING = 0
        NUMBER_INT_COMPLETE = 1

        DOT_TRANSITION = 2

        NUMBER_FLOAT_READING = 3
        NUMBER_FLOAT_COMPLETE = 4


    def __init__(self) -> None:
        super().__init__()
        self.token_value = ''
    
    def process_state(self,c:str) -> None | tuple[str,str]:
      # LABEL: reconhecimento de número inteiro
        if (self.get_state() == self.States.NUMBER_INT_READING):
            if c in  CharGroup.NUMBER:
                self.token_value += c
            elif c == '.':
                self.token_value += c
                self.set_state(self.States.DOT_TRANSITION)
            else:
                self.set_previous_char(c)
                self.set_state(self.States.NUMBER_INT_COMPLETE)
                return self.process_state(c)
        # LABEL: número inteiro reconhecido
        elif (self.get_state() == self.States.NUMBER_INT_COMPLETE):
            return (self.token_value,Tokens.NUM_INT)
        
        # LABEL: processo de transição entre número inteiro e número real (leu um '.')
        elif (self.get_state() == self.States.DOT_TRANSITION):
            if c in CharGroup.NUMBER:
                self.token_value += c
                self.set_state(self.States.NUMBER_FLOAT_READING)
            else: 
                self.set_previous_char(c)
                return (self.token_value,Tokens.NUM_ERROR)
        
        # LABEL: reconhecimento de número real
        elif (self.get_state() == self.States.NUMBER_FLOAT_READING):
            if c in  CharGroup.NUMBER:
                self.token_value += c
            else:
                self.set_previous_char(c)
                self.set_state(self.States.NUMBER_FLOAT_COMPLETE)
                return self.process_state(c)

        # LABEL: número real reconhecido
        elif (self.get_state() == self.States.NUMBER_FLOAT_COMPLETE):
            return (self.token_value,Tokens.NUM_REAL)