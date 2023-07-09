from utility.consts import SyntSymbols, Tokens, ErrorCode
from models.error.SyntaxError import SyntaxError
from models.error.LexicError import LexicError
import logging as logger

class Procedures:
    """
    Classe que define e executa todas as regras gramaticais da linguagem. Para cada regra foi gerado um procedimento (método dessa classe) e um código número, correspondente a cada não-terminal da gramática, organizado em constantes presentes em utility.consts.SyntSymbols.

    Todo procedimento retorna uma lista de Tokens e SyntSymbols que serão empilhados na @symbol_stack da models.syntatic.Synt. Sistema baseado na Análise Sintática Descendente Preditiva sem Retrocesso com Erro.

    Algumas regras estão com tokens a mais que o descrito no arquivo de referência como forma de prever e tratar corretamente alguns possíveis erros. Também foi criada algumas regras auxiliares para converter a linguagem em LL(1).
    """

    @classmethod
    def next_procedure(cls,proc_code:SyntSymbols,token:Tokens) -> list| SyntaxError:
        """
        Método que seleciona o procedimento com base no código desempilhado de @symbol_stack
        """
        if(proc_code == SyntSymbols.INITIAL):
            return cls.programProcedure(token)
        elif(proc_code == SyntSymbols.BODY):
            return cls.bodyProcedure(token)
        elif(proc_code == SyntSymbols.PROC_BODY):
            return cls.procBodyProdecure(token)
        elif(proc_code == SyntSymbols.COMMANDS):
            return cls.commandsProcedure(token)
        elif(proc_code == SyntSymbols.CMD):
            return cls.cmdProcedure(token)
        elif(proc_code == SyntSymbols.CMD_IDENT):
            return cls.cmdIdentProcedure(token)
        
        elif(proc_code == SyntSymbols.DECLARE):
            return cls.declareProcedure(token)
        elif(proc_code == SyntSymbols.DECL_CONST):
            return cls.declareConstsProcedure(token)
        elif(proc_code == SyntSymbols.DECL_VAR):
            return cls.declareVarProcedure(token)
        elif(proc_code == SyntSymbols.DECL_PROC):
            return cls.declareProcProcedure(token)
        
        elif(proc_code == SyntSymbols.VARTYPE):
            return cls.varTypeProcedure(token)
        elif(proc_code == SyntSymbols.PARAMS):
            return cls.paramsProcedure(token)
        elif(proc_code == SyntSymbols.PARAMS_LIST):
            return cls.listParamsProcedure(token)
        elif(proc_code == SyntSymbols.MORE_PARAMS):
            return cls.moreParamsProcedure(token)
        elif(proc_code == SyntSymbols.ARGS):
            return cls.argumentsProcedure(token)
        elif(proc_code == SyntSymbols.ARGS_LIST):
            return cls.argsListProcedure(token)
        elif(proc_code == SyntSymbols.MORE_ARGS):
            return cls.moreArgsProcedure(token)
        
        elif(proc_code == SyntSymbols.VARIABLES):
            return cls.variablesProcedure(token)
        elif(proc_code == SyntSymbols.MORE_VARIABLES):
            return cls.moreVariablesProcedure(token)
        elif(proc_code == SyntSymbols.NUMBER):
            return cls.numberProcedure(token)
        
        elif(proc_code == SyntSymbols.CONDITION):
            return cls.conditionProcedure(token)
        elif(proc_code == SyntSymbols.ELSE):
            return cls.elseProcedure(token)
        elif(proc_code == SyntSymbols.EXPRESSION):
            return cls.expressionProcedure(token)
        elif(proc_code == SyntSymbols.RELATION):
            return cls.relationProcedure(token)
        elif(proc_code == SyntSymbols.TERM):
            return cls.termProcedure(token)
        elif(proc_code == SyntSymbols.MORE_TERMS):
            return cls.moreTermsProcedure(token)
        elif(proc_code == SyntSymbols.FACTOR):
            return cls.factorProcedure(token)
        elif(proc_code == SyntSymbols.MORE_FACTORS):
            return cls.moreFactorProcedure(token)
        
        elif(proc_code == SyntSymbols.OP_UN):
            return cls.opUnProcedure(token)
        elif(proc_code == SyntSymbols.OP_AD):
            return cls.opAdProcedure(token)
        elif(proc_code == SyntSymbols.OP_MUL):
            return cls.opMulProcedure(token)
        
        else:
            logger.critical('Código inválido na pilha. Encerrado processo.')
            exit(1)
        

    @staticmethod
    def programProcedure(token) -> list| SyntaxError:
        """<programa> ::= program ident ; <corpo>."""
        if(token[1] == Tokens.PROGRAM):
            return [Tokens.PROGRAM,Tokens.ID,Tokens.SEMICOL,SyntSymbols.BODY,Tokens.DOT]

        return SyntaxError(ErrorCode.PROGRAM_EXPECTED,"'program' esperado")
    
    @staticmethod
    def bodyProcedure(token) -> list| SyntaxError:
        """<corpo> ::= <dc> begin <comandos> end"""
        if((token[1] == Tokens.CONST) |  (token[1] == Tokens.VAR) | (token[1] == Tokens.PROCEDURE) | (token[1] == Tokens.BEGIN)):
            return [SyntSymbols.DECLARE,Tokens.BEGIN,SyntSymbols.COMMANDS,Tokens.END]
        
        return SyntaxError(ErrorCode.UNEXPECTED_TOKEN,f"Esperado declarações de constantes e variáveis, ou inicio do código. '{token[0]}' inesperado.")

    @staticmethod
    def declareProcedure(token) -> list| SyntaxError:
        """<dc> ::= <dc_c> <dc_v> <dc_p>"""
        if((token[1] == Tokens.CONST) |  (token[1] == Tokens.VAR) | (token[1] == Tokens.PROCEDURE) | (token[1] == Tokens.BEGIN)):
            return [SyntSymbols.DECL_CONST,SyntSymbols.DECL_VAR,SyntSymbols.DECL_PROC]
        
        return SyntaxError(ErrorCode.UNEXPECTED_TOKEN,f"Esperado declarações de constantes, variáveis, procedimentos, ou inicio do código. '{token[0]}' inesperado.")
    
    @staticmethod
    def declareConstsProcedure(token) -> list| SyntaxError:
        """<dc_c> ::= const ident = <numero> ; <dc_c> | λ"""
        if (token[1] == Tokens.CONST):
            return [Tokens.CONST,Tokens.ID,Tokens.SET,SyntSymbols.NUMBER,Tokens.SEMICOL,SyntSymbols.DECL_CONST]
        elif((token[1] == Tokens.VAR) | (token[1] == Tokens.PROCEDURE) | (token[1] == Tokens.BEGIN)):
            return []
        
        return SyntaxError(ErrorCode.UNEXPECTED_TOKEN,f"Esperado declarações de constantes, variáveis, procedimentos, ou inicio do código. '{token[0]}' inesperado.")

    @staticmethod
    def declareVarProcedure(token) -> list| SyntaxError: 
        """<dc_v> ::= var <variaveis> : <tipo_var> ; <dc_v> | λ"""
        if (token[1] == Tokens.VAR):
            return [Tokens.VAR,SyntSymbols.VARIABLES,Tokens.COLON,SyntSymbols.VARTYPE,Tokens.SEMICOL,SyntSymbols.DECL_VAR]
        elif((token[1] == Tokens.PROCEDURE) | (token[1] == Tokens.BEGIN)):
            return []
        
        return SyntaxError(ErrorCode.UNEXPECTED_TOKEN,f"Esperado declarações de variáveis, procedimentos, ou inicio do código. '{token[0]}' inesperado.")

    @staticmethod
    def declareProcProcedure(token) -> list | SyntaxError:
        """<dc_p> ::= procedure ident <parametros> ; <corpo_p> <dc_p> | λ"""
        if(token[1] == Tokens.PROCEDURE):
            return [Tokens.PROCEDURE,Tokens.ID,SyntSymbols.PARAMS,Tokens.SEMICOL,SyntSymbols.PROC_BODY,SyntSymbols.DECL_PROC]
        
        elif((token[1] == Tokens.BEGIN)):
            return []
        
        return SyntaxError(ErrorCode.UNEXPECTED_TOKEN,f"Esperado declarações de procedimentos, ou inicio do código. '{token[0]}' inesperado.")

    @staticmethod
    def variablesProcedure(token)->list| SyntaxError:
        """<variaveis> ::= ident <mais_var>"""
        if(token[1] == Tokens.ID) | (token[1] == Tokens.NUM_ERROR) | (token[1] == Tokens.TOKEN_ERROR) | (token[1] == Tokens.NUM_INT) | (token[1] == Tokens.NUM_REAL):
            return [Tokens.ID,SyntSymbols.MORE_VARIABLES]
        
        return SyntaxError(ErrorCode.UNEXPECTED_TOKEN,f"'{token[0]}' inesperado.")
    
    @staticmethod
    def moreVariablesProcedure(token) -> list | SyntaxError:
        """<mais_var> ::= , <variaveis> |<variaveis>|λ"""
        if(token[1]==Tokens.COMMA) | (token[1]==Tokens.ID):
            return [Tokens.COMMA,SyntSymbols.VARIABLES]
        elif((token[1] == Tokens.COLON) | (token[1] == Tokens.CLOSE_PAR) | (token[1] == Tokens.INTEGER) | (token[1] == Tokens.REAL)):
            return []
        
        return SyntaxError(ErrorCode.UNEXPECTED_TOKEN,f"'{token[0]}' inesperado.")
    
    @staticmethod
    def varTypeProcedure(token) -> list | SyntaxError:
        """<tipo_var> ::= real | integer | boolean"""
        if(token[1] == Tokens.INTEGER):
            return [Tokens.INTEGER]
        elif(token[1] == Tokens.REAL):
            return [Tokens.REAL]
        
        return SyntaxError(ErrorCode.EXPECTED_VARTYPE,f"Esperado tipo de variável. '{token[0]}' não é um tipo válido.")
    
    @staticmethod
    def paramsProcedure(token) -> list | SyntaxError:
        """<parametros> ::= ( <lista_par> ) | λ"""
        if(token[1] == Tokens.OPEN_PAR):
            return [Tokens.OPEN_PAR,SyntSymbols.PARAMS_LIST,Tokens.CLOSE_PAR]
        elif(token[1] == Tokens.COMMA):
            return []
        
        return SyntaxError(ErrorCode.UNEXPECTED_TOKEN,f"'{token[0]}' inesperado.")
        
    @staticmethod
    def procBodyProdecure(token) -> list | SyntaxError:
        """<corpo_p> ::= <dc_loc> begin <comandos> end ;"""
        if ((token[1]==Tokens.VAR) | (token[1] == Tokens.BEGIN)):
            return [SyntSymbols.DECL_VAR,Tokens.BEGIN,SyntSymbols.COMMANDS,Tokens.END,Tokens.SEMICOL]
        
        return SyntaxError(ErrorCode.UNEXPECTED_TOKEN,f"'{token[0]}' inesperado.")
    
    @staticmethod
    def listParamsProcedure(token) -> list | SyntaxError:
        """<lista_par> ::= <variaveis> : <tipo_var> <mais_par>"""
        if(token[1] == Tokens.ID) | (token[1] == Tokens.NUM_ERROR) | (token[1] == Tokens.TOKEN_ERROR) | (token[1] == Tokens.NUM_INT) | (token[1] == Tokens.NUM_REAL):
            return [SyntSymbols.VARIABLES,Tokens.COLON,SyntSymbols.VARTYPE,SyntSymbols.MORE_PARAMS]
        
        return SyntaxError(ErrorCode.UNEXPECTED_TOKEN,f"'{token[0]}' inesperado.")
    
    @staticmethod
    def moreParamsProcedure(token) -> list | SyntaxError:
        """<mais_par> ::= ; <lista_par> | λ"""
        if(token[1] == Tokens.COMMA):
            return [Tokens.COMMA,SyntSymbols.PARAMS_LIST]
        elif(token[1] == Tokens.CLOSE_PAR):
            return []
        
        return SyntaxError(ErrorCode.UNEXPECTED_TOKEN,f"'{token[0]}' inesperado.")
    
    @staticmethod
    def argsListProcedure(token) -> list | SyntaxError:
        """<lista_arg> ::= ( <argumentos> ) | λ"""
        if(token[1]==Tokens.OPEN_PAR):
            return [Tokens.OPEN_PAR,SyntSymbols.ARGS,Tokens.CLOSE_PAR]
        elif(token[1]==Tokens.SEMICOL):
            return []
        
        return SyntaxError(ErrorCode.UNEXPECTED_TOKEN,f"'{token[0]}' inesperado.")
    
    @staticmethod
    def argumentsProcedure(token) -> list | SyntaxError:
        """<argumentos> ::= ident <mais_ident>"""
        if(token[1] == Tokens.ID) | (token[1] == Tokens.NUM_ERROR) | (token[1] == Tokens.TOKEN_ERROR) | (token[1] == Tokens.NUM_INT) | (token[1] == Tokens.NUM_REAL):
            return [Tokens.ID,SyntSymbols.MORE_ARGS]
        
        return SyntaxError(ErrorCode.UNEXPECTED_TOKEN,f"'{token[0]}' inesperado.")
    
    @staticmethod
    def moreArgsProcedure(token) -> list | SyntaxError:
        """<mais_ident> ::= ; <argumentos> | λ"""
        if(token[1] == Tokens.SEMICOL):
            return [Tokens.SEMICOL,SyntSymbols.ARGS]
        elif(token[1] == Tokens.CLOSE_PAR):
            return []
        
        return SyntaxError(ErrorCode.UNEXPECTED_TOKEN,f"'{token[0]}' inesperado.")
    
    @staticmethod
    def commandsProcedure(token)-> list | SyntaxError:
        """<comandos> ::= <cmd> ; <comandos> | λ"""
        if((token[1]==Tokens.READ) | (token[1]==Tokens.WRITE) | (token[1]==Tokens.WHILE) | (token[1]==Tokens.IF) | (token[1]==Tokens.ID) | (token[1]==Tokens.BEGIN) | (token[1]== Tokens.FOR) | (token[1] == Tokens.NUM_ERROR) | (token[1] == Tokens.TOKEN_ERROR) | (token[1] == Tokens.NUM_INT) | (token[1] == Tokens.NUM_REAL)):
            return [SyntSymbols.CMD,Tokens.SEMICOL,SyntSymbols.COMMANDS]
        elif(token[1] == Tokens.END) | (token[1] == Tokens.DOT):
            return []
        
        return SyntaxError(ErrorCode.UNEXPECTED_TOKEN,f"'{token[0]}' inesperado.")
    
    @staticmethod
    def cmdProcedure(token)-> list | SyntaxError:
        """<cmd> ::= read ( <variaveis> ) |
            write ( <variaveis> ) |
            while ( <condicao> ) do <cmd> |
            if <condicao> then <cmd> <pfalsa> |
            ident <cmd_ident> |
            begin <comandos> end"""
        if(token[1] == Tokens.READ):
            return[Tokens.READ,Tokens.OPEN_PAR,SyntSymbols.VARIABLES,Tokens.CLOSE_PAR]
        elif(token[1] == Tokens.WRITE):
             return[Tokens.WRITE,Tokens.OPEN_PAR,SyntSymbols.VARIABLES,Tokens.CLOSE_PAR]
        elif(token[1] == Tokens.WHILE):
             return[Tokens.WHILE,Tokens.OPEN_PAR,SyntSymbols.CONDITION,Tokens.CLOSE_PAR,Tokens.DO,SyntSymbols.CMD]
        elif(token[1] == Tokens.IF):
            return [Tokens.IF,SyntSymbols.CONDITION,Tokens.THEN,SyntSymbols.ELSE]
        elif(token[1] == Tokens.ID) | (token[1] == Tokens.NUM_ERROR) | (token[1] == Tokens.TOKEN_ERROR) | (token[1] == Tokens.NUM_INT) | (token[1] == Tokens.NUM_REAL):
            return [Tokens.ID,SyntSymbols.CMD_IDENT]
        elif(token[1] == Tokens.BEGIN):
            return [Tokens.BEGIN,SyntSymbols.COMMANDS,Tokens.END]
        elif(token[1] == Tokens.FOR):
            return[Tokens.FOR,Tokens.ID,Tokens.SET,SyntSymbols.EXPRESSION,Tokens.TO,SyntSymbols.EXPRESSION,Tokens.DO,SyntSymbols.CMD]
        
        return SyntaxError(ErrorCode.UNEXPECTED_TOKEN,f"'{token[0]}' inesperado.")
    
    @staticmethod
    def cmdIdentProcedure(token)-> list | SyntaxError:
        """(Regra nova criada, para converter a linguagem em LL(1): <cmd_ident> ::= := <expressão> | <lista_args>"""
        if(token[1] == Tokens.SET):
            return [Tokens.SET,SyntSymbols.EXPRESSION]
        elif(token[1]==Tokens.OPEN_PAR) | (token[1] == Tokens.SEMICOL):
            return [SyntSymbols.PARAMS_LIST]
        
        return SyntaxError(ErrorCode.UNEXPECTED_TOKEN,f"'{token[0]}' inesperado.")
    
    @staticmethod
    def elseProcedure(token)-> list | SyntaxError:
        """<pfalsa> ::= else <cmd> | λ"""
        if(token[1] == Tokens.ELSE):
            return[Tokens.ELSE,SyntSymbols.CMD]
        elif(token[1]== Tokens.SEMICOL):
            return[]
        
        return SyntaxError(ErrorCode.UNEXPECTED_TOKEN,f"'{token[0]}' inesperado.")
    
    @staticmethod
    def conditionProcedure(token)-> list | SyntaxError:
        """<condicao> ::= <expressao> <relacao> <expressao>"""
        if((token[1] == Tokens.OP_SUM) | (token[1] == Tokens.OP_SUB) | (token[1] == Tokens.ID) | (token[1] == Tokens.NUM_INT) | (token[1] == Tokens.NUM_REAL) | (token[1] == Tokens.OPEN_PAR) | (token[1] == Tokens.NUM_ERROR) | (token[1] == Tokens.TOKEN_ERROR)):
            return[SyntSymbols.EXPRESSION,SyntSymbols.RELATION,SyntSymbols.EXPRESSION]
        
        return SyntaxError(ErrorCode.UNEXPECTED_TOKEN,f"'{token[0]}' inesperado.")
    
    @staticmethod
    def expressionProcedure(token)-> list | SyntaxError:
       """<expressao> ::= <termo> <outros_termos>"""
       if((token[1] == Tokens.OP_SUM) | (token[1] == Tokens.OP_SUB) | (token[1] == Tokens.ID) | (token[1] == Tokens.NUM_INT) | (token[1] == Tokens.NUM_REAL) | (token[1] == Tokens.OPEN_PAR) | (token[1] == Tokens.NUM_ERROR) | (token[1] == Tokens.TOKEN_ERROR)):
           return[SyntSymbols.TERM,SyntSymbols.MORE_TERMS]
       
       return SyntaxError(ErrorCode.UNEXPECTED_TOKEN,f"'{token[0]}' inesperado.") 

    @staticmethod
    def relationProcedure(token)-> list | SyntaxError:
        """<relacao> ::= = | <> | >= | <= | > | <"""
        if(token[1]==Tokens.LOWER):
            return [Tokens.LOWER]
        elif(token[1]==Tokens.LOWER_EQ):
            return [Tokens.LOWER_EQ]
        elif(token[1]==Tokens.GREATER):
            return [Tokens.GREATER]
        elif(token[1]==Tokens.GREATER_EQ):
            return [Tokens.GREATER_EQ] 
        elif(token[1]==Tokens.EQUALS):
            return [Tokens.EQUALS]
        elif(token[1]==Tokens.NOT_EQ):
            return [Tokens.NOT_EQ]
        
        return SyntaxError(ErrorCode.UNEXPECTED_TOKEN,f"'{token[0]}' inesperado.") 
    
    @staticmethod
    def termProcedure(token)-> list | SyntaxError:
        """<termo> ::= <op_un> <fator> <mais_fatores>"""
        if((token[1] == Tokens.OP_SUM) | (token[1] == Tokens.OP_SUB) | (token[1] == Tokens.ID) | (token[1] == Tokens.NUM_INT) | (token[1] == Tokens.NUM_REAL) | (token[1] == Tokens.OPEN_PAR) | (token[1] == Tokens.NUM_ERROR) | (token[1] == Tokens.TOKEN_ERROR)):
            return [SyntSymbols.OP_UN,SyntSymbols.FACTOR,SyntSymbols.MORE_FACTORS]
        
        return SyntaxError(ErrorCode.UNEXPECTED_TOKEN,f"'{token[0]}' inesperado.") 
    
    @staticmethod
    def moreTermsProcedure(token)-> list | SyntaxError:
        """<outros_termos> ::= <op_ad> <termo> <outros_termos> | λ"""
        if((token[1] == Tokens.OP_SUM) | (token[1] == Tokens.OP_SUB)):
            return [SyntSymbols.OP_AD,SyntSymbols.TERM,SyntSymbols.MORE_TERMS]
        elif((token[1] == Tokens.CLOSE_PAR) | (token[1] == Tokens.SEMICOL) | (token[1] == Tokens.LOWER) | (token[1] == Tokens.LOWER_EQ) | (token[1] == Tokens.GREATER) | (token[1] == Tokens.GREATER_EQ) | (token[1] == Tokens.EQUALS) | (token[1] == Tokens.NOT_EQ) | (token[1] == Tokens.TO) | (token[1] == Tokens.DO)):
            return []
        
        return SyntaxError(ErrorCode.UNEXPECTED_TOKEN,f"'{token[0]}' inesperado.") 
    
    @staticmethod
    def factorProcedure(token)-> list | SyntaxError:
        """<fator> ::= ident | <numero> | ( <expressao> )"""
        if(token[1] == Tokens.ID) | (token[1] == Tokens.NUM_ERROR) | (token[1] == Tokens.TOKEN_ERROR):
            return [Tokens.ID]
        elif((token[1] == Tokens.NUM_INT ) | (token[1] == Tokens.NUM_REAL) |  (token[1] == Tokens.NUM_ERROR)):
            return [SyntSymbols.NUMBER]
        elif(token[1] == Tokens.OPEN_PAR):
            return [ Tokens.OPEN_PAR,SyntSymbols.EXPRESSION, Tokens.CLOSE_PAR]

        return SyntaxError(ErrorCode.UNEXPECTED_TOKEN,f"'{token[0]}' inesperado.")
    
    @staticmethod
    def moreFactorProcedure(token) -> list | SyntaxError:
        """<mais_fatores> ::= <op_mul> <fator> <mais_fatores> | λ"""
        if((token[1] == Tokens.OP_MUL) | (token[1] == Tokens.OP_DIV) | (token[1] == Tokens.OP_MOD)):
            return [SyntSymbols.OP_MUL,SyntSymbols.FACTOR,SyntSymbols.MORE_FACTORS]
        elif((token[1] == Tokens.OP_SUB) | (token[1] == Tokens.OP_SUM) | (token[1] == Tokens.CLOSE_PAR) | (token[1] == Tokens.SEMICOL) | (token[1] == Tokens.LOWER) | (token[1] == Tokens.LOWER_EQ) | (token[1] == Tokens.GREATER) | (token[1] == Tokens.GREATER_EQ) | (token[1] == Tokens.EQUALS) | (token[1] == Tokens.NOT_EQ) | (token[1] == Tokens.TO) | (token[1] == Tokens.DO)):
            return []
        
        return SyntaxError(ErrorCode.UNEXPECTED_TOKEN,f"'{token[0]}' inesperado.")
        
    @staticmethod
    def opUnProcedure(token) -> list | SyntaxError:
        """<op_un> ::= + | - | λ"""
        if((token[1] == Tokens.OP_SUM)):
            return [Tokens.OP_SUM]
        elif(token[1] == Tokens.OP_SUB):
            return [Tokens.OP_SUB]
        elif((token[1] == Tokens.ID) | (token[1] == Tokens.NUM_INT) | (token[1] == Tokens.NUM_REAL) | (token[1] == Tokens.OPEN_PAR) | (token[1] == Tokens.NUM_ERROR) | (token[1] == Tokens.TOKEN_ERROR)) :
            return []
        
        return SyntaxError(ErrorCode.UNEXPECTED_TOKEN,f"'{token[0]}' inesperado.")
    
    @staticmethod
    def opAdProcedure(token) -> list | SyntaxError:
        """<op_ad> ::= + | -"""
        if((token[1] == Tokens.OP_SUM)):
            return [Tokens.OP_SUM]
        elif(token[1] == Tokens.OP_SUB):
            return [Tokens.OP_SUB]
        
        return SyntaxError(ErrorCode.UNEXPECTED_TOKEN,f"'{token[0]}' inesperado.")
    
    @staticmethod
    def opMulProcedure(token) -> list | SyntaxError:
        """<op_mul> ::= * | /"""
        if((token[1] == Tokens.OP_MUL)):
            return [Tokens.OP_MUL]
        elif(token[1] == Tokens.OP_DIV):
            return [Tokens.OP_DIV]
        elif(token[1] == Tokens.OP_MOD):
            return [Tokens.OP_MOD]
        
        return SyntaxError(ErrorCode.UNEXPECTED_TOKEN,f"'{token[0]}' inesperado.")
    
    @staticmethod
    def numberProcedure(token) -> list | SyntaxError:
        """<numero> ::= numero_int | numero_real"""
        if((token[1] == Tokens.NUM_INT)):
            return [Tokens.NUM_INT]
        elif(token[1] == Tokens.NUM_REAL) | (token[1] == Tokens.NUM_ERROR):
            return [Tokens.NUM_REAL]
        
        return SyntaxError(ErrorCode.UNEXPECTED_TOKEN,f"'{token[0]}' inesperado.")
