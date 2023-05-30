import logging as logger
import sys

from models.GenericAutomate import Automate
from utility.consts import Tokens

class OperatorAutomate(Automate):
    """
    Reconhecimento dos possíveis operadores que apareçam no código. Segue
    os moldes do reconhecimento de SingleSymb, porém optsou-se por criar uma
    classe separada para isso por organização.
    """

    def __init__(self) -> None:
        super().__init__()
        self.op_dict = {
            '*': Tokens.OP_MUL,
            '+': Tokens.OP_SUM,
            '-': Tokens.OP_SUB,
            '/': Tokens.OP_DIV,
            '%': Tokens.OP_MOD,
        }
    
    def process_state(self,c:str) -> None | tuple[str,str]:
        if c not in self.op_dict:
            logger.critical(' De alguma forma, o automato de operador foi selecionado erroneamente.')
            sys.exit(1)
        
        return (c,self.op_dict[c])
        
        
