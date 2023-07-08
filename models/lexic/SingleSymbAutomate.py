import logging as logger
import sys

from models.lexic.GenericAutomate import Automate
from utility.consts import Tokens

class SingleSymbAutomate(Automate):

    """
    Descrição: "Automato" responsável por um conjunto de estados que correspondem a caracteres únicos, 
    que por si só correspondêm a um token. São eles:

    '.' (ponto)
    ',' (virugla)
    ';' (ponto e vírgula)
    '(' (abre parentesis)
    ')' (fecha parentesis)


    Basicamente o process_state desse automato apenas identifica qual desses pontos corresponde o
    caractere lido e retorna o token correspondente.
    """

    def __init__(self) -> None:
        super().__init__()
        self.pcnt_dict = {
            '.': Tokens.DOT,
            ',': Tokens.COMMA,
            ';': Tokens.SEMICOL,
            '(': Tokens.OPEN_PAR,
            ')': Tokens.CLOSE_PAR,
            '[': Tokens.OPEN_BRKT,
            ']': Tokens.CLOSE_BRKT
        }
    
    def process_state(self,c:str) -> None | tuple[str,str]:
        if c not in self.pcnt_dict:
            logger.critical(' De alguma forma, o automato de pontuacao foi selecionado erroneamente.')
            sys.exit(1)
        
        return (c,self.pcnt_dict[c])