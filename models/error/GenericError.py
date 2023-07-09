class Error:
    def __init__(self,err_code, msg) -> None:
        self.__err_code = err_code
        self.__msg = msg

    def get_code(self):
        return self.__err_code
    
    def get_msg(self):
        return self.__msg