from models.error.GenericError import Error
from utility.consts import Tokens, ErrorCode

class LexicError(Error):
    def __init__(self, err_code) -> None:
        
        if(err_code == ErrorCode.BAD_NUMBER):
            msg = 'Número mal formatado'
        elif(err_code == ErrorCode.BAD_COMMENT):
            msg = 'Comentário mal formatado'
        elif(err_code == ErrorCode.BAD_IDENT):
            msg = 'Identificador mal formatado'
        elif(err_code == ErrorCode.BAD_TOKEN):
            msg = 'caractere não pertence a linguagem'
        elif(err_code == ErrorCode.BAD_SET):
            msg = "':=' esperado. Comparação inesperada."
        else:
            msg = 'Erro léxico mal gerado'

        super().__init__(err_code, msg)
