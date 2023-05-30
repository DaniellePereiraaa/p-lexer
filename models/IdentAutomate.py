from models.GenericAutomate import Automate
from utility.consts import CharGroup, Tokens, RESERVED_WORDS

class IdentAutomate(Automate):

    """
    Descrição: Automato responsável pelo reconhecimento de identificadores e palavras
    reservadas. Definido pelos seguintes estados:

    IDENT_READING -> caracteres e letras estão sendo reconhecidos como identificador
    IDENT_COMPLETE -> foi encontrado algum caracter que indique que o identificador está completo.
    
    Ao atingir o estado IDENT_COMPLETE, é feita a confirmação de que o identificador gerado corresponde
    ou não a alguma palavra reservada pertencente a linguagem. Existem os seguintes templates de token gerados por
    esse autômato:

    * (TK_IDENT,<valor>) - TOKEN DE IDENTIFICADOR
    * (<TK_RESERVED_WORD_CODE>,None) - TOKEN DE PALAVRA RESERVADA
    
    """

    class States:
        IDENT_READING = 0
        IDENT_COMPLETE = 1

    def __init__(self) -> None:
        super().__init__()
        self.token_value = ''
    
    def process_state(self,c:str) -> None | tuple[str,str]:
        
        # INFO :Estado de reconhecimento do identificador
        if self.get_state() == self.States.IDENT_READING:

            if c not in CharGroup.LETTER and c not in CharGroup.NUMBER:
                self.set_state(self.States.IDENT_COMPLETE)
                self.set_previous_char(c)
                self.process_state(c)
            
            else:
                self.token_value += c
                return None
        
        # INFO: Estado de identificador reconhecido e verificação de palavra reservada
        elif self.get_state() == self.States.IDENT_COMPLETE:

            if self.token_value in RESERVED_WORDS:
                return (RESERVED_WORDS[self.token_value],None)
            
            return (Tokens.ID,self.token_value)
        
