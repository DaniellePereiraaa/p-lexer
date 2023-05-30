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
    NUM_ERROR = 'erro(declaracao de numero invalida)'

    STRING = 'STRING'

    ID = 'ID'

    DOT = 'SIMB_PNT'
    COMMA = 'SIMB_VGL'
    
    SEMICOL = 'SIMB_PV'
    OPEN_PAR = 'SIMB_OPN_PAR'
    CLOSE_PAR = 'SIMB_CLS_PAR'
    OPEN_BRKT = 'SIMB_OPN_COLC'
    CLOSE_BRKT = 'SIMB_CLS_COLC'

    COMMENT = 'SIMB_COMENTARIO'
    COMMENT_ERROR = 'erro(fim do comentario nao encontrado)'

    COLON = 'SIMB_DP'
    SET = 'SIMB_ATRIB'
    GREATER = 'SIMB_MAIOR'
    GREATER_EQ = 'SIMB_MAIOR_IGUAL'
    LOWER = 'SIMB_MENOR'
    LOWER_EQ = 'SIMB_MENOR_IGUAL'
    NOT = 'SIMB_NEGACAO'
    NOT_EQ = 'SIMB_DIFERENTE'
    EQUALS = 'SIMB_IGUAL'

    EQ_ERROR = "erro(simbolo '=' nao reconhecido)"

    OP_SUM = 'SIMB_SOMA'
    OP_SUB = 'SIMB_SUB'
    OP_DIV = 'SIMB_DIV'
    OP_MUL = 'SIMB_MULT'
    OP_MOD = 'SIMB_RESTO'
    

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
    COMPARATORS = ':=><!'
    OPERATORS = '*+-/%'

# DICIONARIO DE PALAVRAS RESERVADAS
RESERVED_WORDS = {
    "program":"SIMB_PROGRAM",
    "for":"SIMB_FOR",
    "var":"SIMB_VAR",
    "end":"SIMB_END",
    "begin":"SIMB_BEGIN",
    "boolean":"SIMB_TIPO",
    "integer":"SIMB_TIPO",
    "real":"SIMB_TIPO",
    "string":"SIMB_TIPO",
    "while":"SIMB_WHILE",
    "if":"SIMB_IF",
    "else":"SIMB_ELSE",
    "const":"SIMB_CONST",
    "do":"SIMB_DO",
    "procedure":"SIMB_PROCEDURE",
    "then":"SIMB_THEN"
}