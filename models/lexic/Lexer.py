import logging as logger

from models.lexic.GenericAutomate import Automate
from models.lexic.IdentAutomate import IdentAutomate
from models.lexic.SingleSymbAutomate import SingleSymbAutomate
from models.lexic.CommentAutomate import CommentAutomate
from models.lexic.ComparatorAutomate import ComparatorAutomate
from models.lexic.NumberAutomate import   NumberAutomate
from models.lexic.OperatorAutomate import OperatorAutomate
from models.lexic.StringAutomate import StringAutomate

from utility import consts 

class Lexer(Automate):
    """ 
    Descrição: Lexer é a classe principal do analisador léxico desenvolvido no projeto. Apresenta apenas dois estados:

    INITIAL -> corresponde a estado inicial do automato diagramado originalmente. Está nele apenas quando um novo token está
    prestes a ser gerado.

    PROCESSING -> pseudo-estado, o qual assume quando algum token já está sendo reconhecido. Isso ocorre pois os reais estados de 
    reconhecimento do código estão subdividos nos demais automatos ( @IdentAutomate, @SingleSymbAutomate, etc.)

    possui em si também um buffer que armazena a última linha de código lida e percorre seus caracteres como uma lista (vide método @get_next_char()), além
    de um outro atributo, chamado @curr_automate, o qual armazena o trecho de autômato correspondente ao token que está sendo identificado no momento.

    Seu principal método é @get_next_token(), o qual efetivamente realiza o reconhecimento do próximo token presente no código. Todo token apresenta o seguinte
    formato:

    (<TOKEN_CODE>, <token_val>)

    <TOKEN_CODE>:   definido em uma lista de constantes em utility.consts.
    <token_val>:    valor do token, para caso de números e identificadores.
    """

    class States:
        INITIAL = 0
        PROCESSING = 1

    def __init__(self) -> None:
        super().__init__()
        self.__buffer = None
        self.__curr_automate = None
    
    # LABEL: MÉTODOS DE CONTROLE DO BUFFER

    def set_buffer(self,line:str) -> None:
        """
        Recebe e memoriza a próxima linha do arquivo.

        Args:
            line (str): linha do arquivo
        """
        
        self.__buffer = line
    
    def empty_buffer(self) -> bool:
        """
        Identifica se o buffer de linha está vazio ou não.

        Returns:
            bool: True -> buffer vazio ; False -> buffer contem algo
        """
        return (self.__buffer == '') | (self.__buffer is None) | (len(self.__buffer) == 0)
    
    def regen_buffer(self,c:str) -> None:
        logger.debug(f' Regenerando Buffer com: {c}')
        self.__buffer = c + self.__buffer
        logger.debug(f' buffer atual: {self.__buffer}')

    def get_next_char(self) -> str:
        """
        Retorna o próximo caractere da linha atual do arquivo
        Returns:
            str: próximo caractere
        """
        if not self.empty_buffer():
            logger.debug(f' buffer atual: "{self.__buffer}"')
            next = self.__buffer[0]
            self.__buffer = self.__buffer[1:]
            logger.debug(f' valor coletado: {next}')
            return next.lower()
        
        return None
    
    # LABEL: MÉTODOS DE CONTROLE DO AUTOMATO ATUAL

    def set_automate(self,automate_id:str) -> None:
        """
         Define o novo @curr_automate com base no id enviado. Utilizado no método
         @get_next_token, sempre que um novo reconhecimento é iniciado.

        """
        logger.debug(f' Selecionando automato {automate_id}')

        if(automate_id == consts.Automates.NUMBER):
            self.__curr_automate = NumberAutomate()

        elif(automate_id == consts.Automates.IDENT):
            self.__curr_automate = IdentAutomate()

        elif(automate_id == consts.Automates.SINGLE_SYMB):
            self.__curr_automate = SingleSymbAutomate()
        
        elif(automate_id == consts.Automates.COMPARATOR):
            self.__curr_automate = ComparatorAutomate()

        elif(automate_id == consts.Automates.COMMENT):
            self.__curr_automate = CommentAutomate()

        elif(automate_id == consts.Automates.OPERATOR):
            self.__curr_automate = OperatorAutomate()
        
        elif(automate_id == consts.Automates.STRING):
            self.__curr_automate = StringAutomate()
    
    def free_automate(self) -> None:
        """
            Limpa o @curr_automate
        """
        self.__curr_automate = None

    def is_undef_automate(self) -> bool:
        """
            Identifica se há um @curr_automate definido. 
            Return: 
                True -> não está definido
                False -> está definido
        """
        return self.__curr_automate is None
    
    def process_state(self,c:str) -> None | tuple[str,str]:

        """
            Executa o process_state do @curr_automate atual
        """
        
        if self.is_undef_automate():
            logger.warn('Nao foi definido nenhum automato para processar.')
            return None
        
        return self.__curr_automate.process_state(c)
    
    def get_next_token(self) -> tuple[str,str]:

        """
            Principal método da classe. Realiza o reconhecimento do próximo token, fazendo a leitura
            dos caracteres sequencialmente dispostos através do @buffer do método. 

            Se está no estado INITIAL, busca identificar o primeiro caractere do token e determinar quais dos
            subautomatos realizará o reconhecimento do token, setando ele em @curr_automate.

            Caso esteja no estado PROCESSING, significa que um token já está sendo identificado por algum @curr_automate, 
            então apenas continua chamando @process_state() com o proximo caractere até que seja retornado algum token.

            Uma vez retornado, primeiramente é feita a verificação se não é necessário resgatar o último caractere lido, pois há
            casos em que ele correponda ao início de um próximo token, como em casos de identificadores e números. Caso necessário,
            o valor em questão volta ao inicio do buffer.

            Por fim, o automato volta para o estado INITIAL, seu @curr_automate é limpo e o token gerado é retornado.
        """



        token = None
        curr_char = None

        while (token is None) & (curr_char != '\n'):
            if self.empty_buffer():
                return
            
            curr_char = self.get_next_char()
            logger.debug(f' Caractere em leitura: {curr_char}')

            if self.get_state() == self.States.INITIAL:

                if curr_char == '\n':
                    break 
                if curr_char == ' ':
                    continue

                if curr_char in consts.CharGroup.LETTER:
                    self.set_automate(consts.Automates.IDENT)

                elif curr_char in consts.CharGroup.NUMBER: 
                    self.set_automate(consts.Automates.NUMBER)

                elif curr_char in consts.CharGroup.SINGLE_SYMB:
                    self.set_automate(consts.Automates.SINGLE_SYMB)

                elif curr_char in consts.CharGroup.COMPARATORS:
                    self.set_automate(consts.Automates.COMPARATOR)
                
                elif curr_char in consts.CharGroup.OPERATORS:
                    self.set_automate(consts.Automates.OPERATOR)
                
                elif (curr_char == '\'') | (curr_char == '"'):
                    self.set_automate(consts.Automates.STRING)

                elif curr_char == '{':
                    self.set_automate(consts.Automates.COMMENT)
                else:
                    token = (curr_char,f'erro(\'{curr_char}\' nao reconhecido)')

            if not self.is_undef_automate():
                self.set_state(self.States.PROCESSING)
                token = self.process_state(curr_char)
        
        if (self.__curr_automate is not None):

            if (self.__curr_automate.get_previous_char() is not None):
                logger.debug(f' caractere anterior detectado: {self.__curr_automate.get_previous_char()}')
                self.regen_buffer(self.__curr_automate.get_previous_char())
        
        self.free_automate()
        self.set_state(self.States.INITIAL)
        return token 