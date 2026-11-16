# p-lexer — Analisador Léxico e Sintático para Linguagem P--

Implementação completa de um **compilador** para a linguagem fictícia **P--**, desenvolvido como projeto da disciplina de **Teoria da Computação e Compiladores**.

O projeto inclui:
- **Analisador Léxico** baseado em autômatos finitos determinísticos (AFD)
- **Analisador Sintático** descendente preditivo sem retrocesso com tratamento de erros
- **Tratamento de erros léxicos e sintáticos** com resincronização (modo pânico)

---

## Visão Geral da Arquitetura

```
p-lexer/
├── main.py                           # Ponto de entrada
├── models/
│   ├── lexic/                        # Analisador Léxico (AFD)
│   │   ├── Lexer.py                  # Orquestrador principal
│   │   ├── GenericAutomate.py        # Classe base dos autômatos
│   │   ├── IdentAutomate.py          # Identificadores e palavras reservadas
│   │   ├── NumberAutomate.py         # Números inteiros e reais
│   │   ├── SingleSymbAutomate.py     # Símbolos simples (.,;()[])
│   │   ├── ComparatorAutomate.py     # Operadores relacionais (:=, >, <, >=, <=, <>)
│   │   ├── OperatorAutomate.py       # Operadores aritméticos (+, -, *, /, %)
│   │   ├── CommentAutomate.py        # Comentários { ... }
│   │   └── StringAutomate.py         # Literais de string
│   ├── syntatic/                     # Analisador Sintático
│   │   ├── Synt.py                   # Parser descendente preditivo
│   │   └── Procedures.py             # Regras gramaticais (produções)
│   └── error/                        # Hierarquia de erros
│       ├── GenericError.py           # Classe base de erro
│       ├── LexicError.py             # Erros léxicos
│       └── SyntaxError.py            # Erros sintáticos
├── utility/
│   ├── consts.py                     # Tokens, autômatos, grupos de chars, palavras reservadas
│   └── args.py                       # Parsing de argumentos CLI
└── test/
    ├── code1.in                      # Exemplo: fatorial
    ├── code2.in
    └── code3.in
```

---

## Linguagem P--

A linguagem suporta:

| Categoria | Elementos |
|-----------|-----------|
| **Palavras reservadas** | `program`, `var`, `const`, `procedure`, `begin`, `end`, `if`, `then`, `else`, `while`, `do`, `for`, `to`, `read`, `write`, `integer`, `real` |
| **Tipos de dados** | `integer`, `real` |
| **Operadores aritméticos** | `+`, `-`, `*`, `/`, `%` |
| **Operadores relacionais** | `=`, `<>`, `<`, `>`, `<=`, `>=` |
| **Atribuição** | `:=` |
| **Delimitadores** | `;`, `:`, `,`, `.`, `(`, `)`, `[`, `]` |
| **Comentários** | `{ ... }` (podem ser multilinha) |
| **Strings** | `'...'` (com escape de aspas `""`) |
| **Identificadores** | Letras, dígitos e `_`, iniciando com letra |

### Exemplo de Código P--

```pascal
program fatorial;
{exemplo 1}
var x, aux, fat: integer;
begin
    read(x);
    fat:=1.;
    ligma='caminho de "Paca"';
    for aux:=1 to x do
        begin
            fat:=fat*aux+lignina;
        end;
    write(fat);
end.
```

---

## Analisador Léxico (Lexer)

Baseado em **Autômatos Finitos Determinísticos (AFD)** com arquitetura modular:

### Estados do Lexer Principal
- **INITIAL**: Aguarda início de novo token
- **PROCESSING**: Delegando reconhecimento a subautômato

### Subautômatos Especializados

| Autômato | Responsabilidade | Tokens Gerados |
|----------|------------------|----------------|
| `IdentAutomate` | Identificadores + palavras reservadas | `ID`, `PROGRAM`, `VAR`, `BEGIN`, etc. |
| `NumberAutomate` | Inteiros, reais, notação com ponto | `NUM_INT`, `NUM_REAL`, `NUM_ERR` |
| `SingleSymbAutomate` | Símbolos de 1 char | `DOT`, `COMMA`, `SEMICOL`, `OPEN_PAR`, etc. |
| `ComparatorAutomate` | Operadores relacionais de 1-2 chars | `SET`, `GREATER`, `LOWER_EQ`, `NOT_EQ`, etc. |
| `OperatorAutomate` | Operadores aritméticos | `OP_SUM`, `OP_SUB`, `OP_MUL`, `OP_DIV`, `OP_MOD` |
| `CommentAutomate` | Comentários `{...}` | `COMMENT`, `COMMENT_ERROR` |
| `StringAutomate` | Literais `'...'` | `STRING` (implícito) |

### Fluxo de Reconhecimento
1. Lexer lê char a char do buffer da linha
2. Em `INITIAL`: classifica primeiro char → seleciona subautômato
3. Em `PROCESSING`: delega ao subautômato até token completo
3. Retorna tupla `(lexema, token_code)`
4. Lookahead de 1 char (reinsere char no buffer se necessário)

---

## Analisador Sintático (Parser)

**Descendente Preditivo Sem Retrocesso** (LL(1)) com pilha explícita.

### Características
- **Pilha de símbolos**: Não-terminais (`SyntSymbols`) + Terminais (`Tokens`)
- **Tabela de produções**: Implementada em `Procedures.py`
- **Tratamento de erros**: Específico por tipo + resincronização genérica
- **Modo pânico**: Resincronização via tokens de sincronia (`BEGIN`, `END`, `;`, `)`, `,`, `:`, `.`)

### Símbolos Não-Terminais Principais
| Símbolo | Descrição |
|---------|-----------|
| `INITIAL` | Início da análise (`program id ; body .`) |
| `BODY` / `PROC_BODY` | Corpo de programa/procedimento |
| `DECLARE` | Seção de declarações (`const`, `var`, `procedure`) |
| `COMMANDS` / `CMD` | Lista de comandos |
| `EXPRESSION` / `TERM` / `FACTOR` | Expressões aritméticas com precedência |
| `CONDITION` / `RELATION` | Condicionais e operadores relacionais |

---

## Tratamento de Erros

### Erros Léxicos (`LexicError`)
| Código | Descrição | Recuperação |
|--------|-----------|-------------|
| `BAD_COMMENT` | Comentário não fechado | Pula para próxima linha |
| `BAD_IDENT` | Identificador malformado | Pula token(s) até token válido |
| `BAD_NUMBER` | Número malformado (ex: `1..2`) | Pula token, ignora ID seguinte se houver |
| `BAD_TOKEN` | Caractere inválido na linguagem | Pula caractere |
| `BAD_SET` | `:` não seguido de `=` | Continua análise |

### Erros Sintáticos (`SyntaxError`)
| Código | Descrição | Recuperação |
|--------|-----------|-------------|
| `PROGRAM_EXPECTED` | Falta `program` no início | Insere produção esperada na pilha |
| `EXPECTED_TOKEN` | Token esperado não encontrado (`;`, `:`, `,`, `(`, `)`) | Modo pânico |
| `UNEXPECTED_TOKEN` | Token inesperado na regra | Modo pânico |
| `UNEXPECTED_EOF` | Fim de arquivo prematuro | Finaliza com erro |
| `FALIED_RESYNC` | Resincronização falhou | Aborta compilação |

### Resincronização (Modo Pânico)
1. Avança no código até encontrar token de sincronia (`RESYNC`)
2. Desempilha símbolos até topo da pilha == token de sincronia
3. Retoma análise a partir desse ponto

---

## Como Executar

### Requisitos
- Python 3.8+

### Uso Básico
```bash
# Compila arquivo P-- e mostra erros no console
python main.py entrada.p--

# Compila e salva resultado em arquivo
python main.py entrada.p-- saida.txt
```

### Exemplos de Teste
```bash
python main.py test/code1.in
python main.py test/code2.in
python main.py test/code3.in
```

### Saída
- **Sucesso**: `Compilação bem sucedida.`
- **Erros**: Lista de erros léxicos e sintáticos com número da linha
  ```
  Erro léxico na linha 5: Identificador mal formatado: '123abc'
  Erro sintático na linha 8: ';' esperado
  ```

---

## Design Patterns & Decisões Técnicas

| Padrão | Aplicação |
|--------|-----------|
| **State Pattern** | Lexer e subautômatos implementam máquina de estados |
| **Strategy** | Cada subautômato encapsula lógica de reconhecimento distinta |
| **Composite** | Pilha de símbolos mistura terminais e não-terminais |
| **Template Method** | `GenericAutomate` define fluxo, subclasses implementam `process_state` |
| **Error Recovery** | Tratamento específico + resincronização genérica (modo pânico) |

### Por que AFD para o Léxico?
- **Determinístico**: O(1) por caractere, sem backtracking
- **Modular**: Cada categoria de token tem autômato isolado
- **Extensível**: Novos tokens = novo subautômato + registro no `Lexer.set_automate()`

### Por que Descendente Preditivo para o Sintático?
- **Legível**: Estrutura espelha a gramática
- **Controle de erro**: Fácil inserir tratamentos em pontos específicos
- **Sem retrocesso**: Eficiente para gramáticas LL(1) como P--

---

## Estrutura de Tokens (utility/consts.py)

```python
# Tokens terminais
Tokens.NUM_INT, Tokens.NUM_REAL, Tokens.ID
Tokens.SET (:=), Tokens.COLON (:), Tokens.SEMICOL (;)
Tokens.GREATER, Tokens.LOWER_EQ, Tokens.NOT_EQ, ...
Tokens.OP_SUM, Tokens.OP_MUL, ...
Tokens.PROGRAM, Tokens.BEGIN, Tokens.END, ...

# Tokens de sincronização para resincronização
Tokens.RESYNC = (BEGIN, END, DOT, CLOSE_PAR, COMMA, COLON, SEMICOL)
```

---

## Exemplos de Erros Detectados

### Léxicos
```pascal
{ Comentario sem fechamento
123abc  { Identificador começando com número }
1.2.3   { Número malformado }
@simbolo_invalido
```

### Sintáticos
```pascal
program teste;       { Falta begin }
var x: integer       { Falta ; }
begin x := 1 end.    { Falta ; antes de end }
if x > 0 then        { Falta then/do/begin }
```

---

## Licença

Projeto acadêmico — livre para fins educacionais.

---

## Autor

Desenvolvido para a disciplina **Teoria da Computação e Compiladores**.

Demonstra:
- Construção de analisador léxico com AFD modular
- Parser descendente preditivo (LL(1)) com pilha explícita
- Tratamento robusto de erros com recuperação (modo pânico)
- Arquitetura limpa, extensível e bem documentada
- Linguagem Pascal-like completa com tipos, procedimentos, controle de fluxo