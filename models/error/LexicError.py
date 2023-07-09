from models.error.GenericError import Error
from utility.consts import Tokens, ErrorCode

class LexicError(Error):
    def __init__(self, token_err) -> None:

        if(token_err == Tokens.NUM_ERROR):
            err_code = ErrorCode.BAD_IDENT
            msg = 'identificador mal formado.'
        elif(token_err == Tokens.STRING_ERROR):
            err_code = ErrorCode.BAD_STRING
            msg = 'string precisa ser fechada.'
            
        else:
            err_code = ErrorCode.BAD_COMMENT
            msg = "Comentário sem fechamento. Esperao '}'"


        super().__init__(err_code, msg)
    pass