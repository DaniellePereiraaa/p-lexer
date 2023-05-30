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
    NUM_INT = 'TK_NUM_INT'
    NUM_REAL = 'TK_NUM_REAL'
    ID = 'TK_IDENT'
    DOT = 'TK_DOT'
    COMMA = 'TK_COMMA'
    COLON = 'TK_COLON'
    SEMICOL = 'TK_SEMICOL'
    OPEN_PAR = 'TK_OPEN_PAR'
    CLOSE_PAR = 'TK_CLOSE_PAR'
    OPEN_BRKT = 'TK_OPEN_BRKT'
    CLOSE_BRKT = 'TK_CLOSE_BRKT'




# IDENTIFICADORES DE AUTOMATOS
class Automates:
    NUMBER = 1
    IDENT = 2
    SINGLE_SYMB = 3



# AGRUPAMENTO DE TIPOS DE CARACTERES
class CharGroup:
    NUMBER = '1234567890'
    LETTER = 'abcdefghijklmnopqrstuvwxyz_'
    SINGLE_SYMB = '.,:;()[]'

# DICIONARIO DE PALAVRAS RESERVADAS
RESERVED_WORDS = {
    "program":"TK_PROGRAM",
    "for":"TK_FOR",
    "end":"TK_END"
}