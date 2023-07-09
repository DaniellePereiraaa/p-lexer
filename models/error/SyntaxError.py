from models.error.GenericError import Error

class SyntaxError(Error):
    def __init__(self, err_code, msg) -> None:
        super().__init__(err_code, msg)


