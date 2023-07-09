import logging as logger
from abc import ABC,abstractclassmethod

class Automate:

    """
        descrição: Classe define genericamente o conceito de automato. Implementado por praticamente
        todas as outras classes do código.

        @curr_state -> registra o estado atual do automato, através de um valor numérico. O estado inicial 
        é sempre identificado por 0.

        @prv_char -> registra o caractere anterior ao que está sendo processado atualmente. Utilizado
        nas situações em que é necessário iniciar a geração do próximo token a partir do  ultimo caractere
        lido no token anterior
    """

    def __init__(self) -> None:
        self.__curr_state = 0
        self.__prv_char = None
        pass

    def set_state(self,state_code:int ) -> None:
        logger.debug(f' Alteração de estado de {self.__curr_state} para {state_code}')
        self.__curr_state = state_code
    
    def get_state(self) -> int: 
        return self.__curr_state
    
    def set_previous_char(self,c:str) -> None:
        self.__prv_char = c
    
    def get_previous_char(self) -> None:
        return self.__prv_char

    @abstractclassmethod
    def process_state(self,c)-> None | tuple[str,str]:
        """Faz o reconhecimento da cadeia com base no caractere lido e no estado atual.
        Implementado distintamente para cada automato do código, por isso é abstrato.
        Args:
            c(char): caractere lido

        Returns:
            any: retorna principalmente None ou o Token gerado.
        """
        pass