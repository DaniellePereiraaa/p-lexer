"""
Descrição: Arquivo que agrupa em classes um conjunto de constantes utilizadas ao longo do código.
Assim, tem-se de forma mais organizada e maleável valores repetidamente utilizados no decorrer
do algoritmo.

Tokens:         registra todos os valores de tokens para cada simbolo possível (exceto palavras reservadas).
Automates:      códigos numéricos para os possíveis "subautomatos" que o analisador léxico pode utilizar.
CharGroup:      agrupamento de caracteres com uma mesma característica e/ou natureza em strings.
RESERVED_WORDS: dicionário de palavras reservadas da linguagem, com seus respectivos tokens.
"""


# CONSTANTES DE TOKEN
class Tokens:
    NUM_INT = 'NUM_INT'
    NUM_REAL = 'NUM_REAL'
    NUM_ERROR = 'NUM_ERR'

    ID = 'ID'

    DOT = 'SIMB_PNT'
    COMMA = 'SIMB_VGL'
    
    SEMICOL = 'SIMB_PV'
    OPEN_PAR = 'SIMB_OPN_PAR'
    CLOSE_PAR = 'SIMB_CLS_PAR'
    OPEN_BRKT = 'SIMB_OPN_COLC'
    CLOSE_BRKT = 'SIMB_CLS_COLC'

    COMMENT = 'SIMB_COMENTARIO'
    COMMENT_ERROR = 'COMMENT_ERR'

    COLON = 'SIMB_DP'
    SET = 'SIMB_ATRIB'
    GREATER = 'SIMB_MAIOR'
    GREATER_EQ = 'SIMB_MAIOR_IGUAL'
    LOWER = 'SIMB_MENOR'
    LOWER_EQ = 'SIMB_MENOR_IGUAL'
    NOT = 'SIMB_NEGACAO'
    NOT_EQ = 'SIMB_DIFERENTE'
    EQUALS = 'SIMB_IGUAL'

    OP_SUM = 'SIMB_SOMA'
    OP_SUB = 'SIMB_SUB'
    OP_DIV = 'SIMB_DIV'
    OP_MUL = 'SIMB_MULT'
    OP_MOD = 'SIMB_RESTO'

    PROGRAM = "SIMB_PROGRAM"
    FOR = "SIMB_FOR"
    VAR = "SIMB_VAR"
    END = "SIMB_END"
    BEGIN = "SIMB_BEGIN"
    INTEGER = "SIMB_INT"
    REAL = "SIMB_REAL"
    WHILE = "SIMB_WHILE"
    IF = "SIMB_IF"
    ELSE = "SIMB_ELSE"
    CONST = "SIMB_CONST"
    DO = "SIMB_DO"
    PROCEDURE = "SIMB_PROC"
    THEN = "SIMB_THEN"
    READ = "SIMB_READ"
    WRITE = "SIMB_WRITE"
    TO = 'SIMB_TO'

    TOKEN_ERROR = 'TOKEN_ERR'
    RESYNC = (BEGIN,END,DOT,CLOSE_PAR,COMMA,COLON,SEMICOL)

# IDENTIFICADORES DE AUTOMATOS
class Automates:
    NUMBER = 1
    IDENT = 2
    SINGLE_SYMB = 3
    COMMENT = 4
    COMPARATOR = 5
    OPERATOR = 6
    STRING =7


# AGRUPAMENTO DE TIPOS DE CARACTERES
class CharGroup:
    NUMBER = '1234567890'
    LETTER = 'abcdefghijklmnopqrstuvwxyz_'
    SINGLE_SYMB = '.,;()[]'
    COMPARATORS = ':=><'
    OPERATORS = '*+-/%'

# DICIONARIO DE PALAVRAS RESERVADAS
RESERVED_WORDS = {
    "program":Tokens.PROGRAM,
    "for":Tokens.FOR,
    "var":Tokens.VAR,
    "end":Tokens.END,
    "begin":Tokens.BEGIN,
    "integer":Tokens.INTEGER,
    "real":Tokens.REAL,
    "while":Tokens.WHILE,
    "if":Tokens.IF,
    "else":Tokens.ELSE,
    "const":Tokens.CONST,
    "do":Tokens.DO,
    "procedure":Tokens.PROCEDURE,
    "then":Tokens.THEN,
    "read":Tokens.READ,
    "write":Tokens.WRITE,
    "to" : Tokens.TO
}

# CONSTANTES PARA ANÁLISE SINTÁTICA
class SyntSymbols:
        INITIAL = 100
        BODY = 101
        PROC_BODY = 102
        COMMANDS = 103
        CMD = 104
        CMD_IDENT = 105
        

        DECLARE = 110
        DECL_CONST = 111
        DECL_VAR = 112
        DECL_PROC = 113

        VARTYPE = 120
        PARAMS = 121
        PARAMS_LIST = 122
        MORE_PARAMS = 123
        ARGS = 124
        ARGS_LIST=125
        MORE_ARGS = 126

        VARIABLES = 130
        MORE_VARIABLES = 131
        NUMBER = 132
        IDENT = 134

        CONDITION = 140
        ELSE = 141
        EXPRESSION = 142
        RELATION = 143
        TERM = 144
        MORE_TERMS = 145
        FACTOR = 146
        MORE_FACTORS = 147

        OP_UN = 150
        OP_AD = 151
        OP_MUL = 152

        SYMB_LIST = (INITIAL,BODY,PROC_BODY,COMMANDS,CMD,CMD_IDENT,DECLARE,DECL_CONST,DECL_PROC,DECL_VAR,VARTYPE,PARAMS,PARAMS_LIST,MORE_PARAMS,ARGS,ARGS_LIST,MORE_ARGS,VARIABLES,MORE_VARIABLES,NUMBER, IDENT, CONDITION,ELSE,EXPRESSION,RELATION,TERM,MORE_TERMS,FACTOR,MORE_FACTORS,OP_UN,OP_AD,OP_MUL)

class ErrorCode:
        PROGRAM_EXPECTED = 901
        UNEXPECTED_TOKEN = 902
        EXPECTED_TOKEN = 903
        UNEXPECTED_EOF = 905
        FALIED_RESYNC = 906
        
        BAD_IDENT = 1001
        BAD_NUMBER = 1002
        BAD_TOKEN = 1003
        BAD_COMMENT = 1004
        BAD_SET = 1005
