grammar MOC;

/*
 * ----------------------------
 * LEXER RULES (tokens básicos)
 * ----------------------------
 */

// Tipos de dados
INT     : 'int' ;
DOUBLE  : 'double' ;
VOID    : 'void' ;

// Estruturas de controlo
IF      : 'if' ;
ELSE    : 'else' ;
WHILE   : 'while' ;
FOR     : 'for' ;

// Operadores aritméticos
MAIS    : '+' ;
MENOS   : '-' ;
MULT    : '*' ;
DIV     : '/' ;
MODULO  : '%' ;

// Operadores relacionais
MENOR       : '<' ;
MENORIGUAL  : '<=' ;
MAIOR       : '>' ;
MAIORIGUAL  : '>=' ;
IGUAL       : '==' ;
DIFERENTE   : '!=' ;

// Operadores lógicos
E_LOGICO    : '&&' ;
OU_LOGICO   : '||' ;
NAO         : '!' ;

// Símbolos e pontuacao
ATRIBUICAO   : '=' ;
VIRGULA      : ',' ;
PONTOVIRG    : ';' ;
ABRECOLCH    : '[' ;
FECHACOLCH   : ']' ;
ABRECHAVES   : '{' ;
FECHACHAVES  : '}' ;
ABREPAR      : '(' ;
FECHAPAR     : ')' ;

// return
RETURN  : 'return' ;

// String literal para writes("texto")
STRINGLITERAL : '"' (~["\r\n])* '"' ;

// Comentários do estilo C
COMENTARIO : '/*' .*? '*/' -> skip ;

// Tokens básicos
NUM_REAL : [0-9]+ '.' [0-9]+ ;
NUMERO   : [0-9]+ ;
IDENTIFICADOR : [a-zA-Z_][a-zA-Z0-9_]* ;

// Espacos em branco (ignorados)
ESPACO : [ \t\r\n]+ -> skip ;

/*
 * ----------------------------
 * PARSER RULES (estrutura sintática)
 * ----------------------------
 */

// Programa = protótipos + (opcional) main + outras funcoes/declaracoes + EOF
programa
    : prototipo* prototipoPrincipal? unidade* funcaoPrincipal EOF
    ;

unidade
    : funcao
    | declaracao
    ;

// Protótipos de funcao
prototipo
    : tipo IDENTIFICADOR ABREPAR parametros? FECHAPAR PONTOVIRG
    ;

// Protótipo específico da funcao main
prototipoPrincipal
    : tipo 'main' ABREPAR parametros? FECHAPAR PONTOVIRG
    ;

// Funcao principal (main)
funcaoPrincipal
    : tipo 'main' ABREPAR parametros? FECHAPAR bloco
    ;

// Funcoes com corpo
funcao
    : tipo IDENTIFICADOR ABREPAR parametros? FECHAPAR bloco
    ;

// Parâmetros da funcao
parametros
    : 'void'                         // permite void
    | tipo                           // permite apenas o tipo (ex: int)
    | parametro (VIRGULA parametro)* // permite vários parâmetros completos (ex: int x, double y)
    ;


parametro
    : tipo
    | tipo IDENTIFICADOR
    | tipo IDENTIFICADOR ABRECOLCH FECHACOLCH // para vetores como parâmetros
    ;

tipo
    : INT
    | DOUBLE
    | VOID
    ;

// Declaracao de variáveis
declaracao
    : tipo listaVariaveis PONTOVIRG
    ;

listaVariaveis
    : variavel (VIRGULA variavel)*
    ;

variavel
    : IDENTIFICADOR
    | IDENTIFICADOR ATRIBUICAO expressao
    | IDENTIFICADOR ABRECOLCH NUMERO FECHACOLCH
    | IDENTIFICADOR ABRECOLCH FECHACOLCH ATRIBUICAO expressao       // ex: s[] = reads();
    | IDENTIFICADOR ABRECOLCH FECHACOLCH ATRIBUICAO blocoArray      // ex: v[] = {1,2,3};
    ;

// Inicializacao de vetores
blocoArray
    : ABRECHAVES listaValores? FECHACHAVES
    ;

listaValores
    : expressao (VIRGULA expressao)*
    ;

// Expressoes com operadores, lógica, casting
expressao
    : NAO expressao                              # Negacao
    | expressao MULT expressao                   # Multiplicacao
    | expressao DIV expressao                    # Divisao
    | expressao MODULO expressao                 # Modulo
    | expressao MAIS expressao                   # Adicao
    | expressao MENOS expressao                  # Subtracao
    | expressao opRelacional expressao           # Comparacao
    | expressao E_LOGICO expressao               # ELogico
    | expressao OU_LOGICO expressao              # OuLogico
    | ABREPAR expressao FECHAPAR                 # Parnteses
    | IDENTIFICADOR                              # VariavelID
    | IDENTIFICADOR ABRECOLCH expressao FECHACOLCH # AcessoVetor
    | NUMERO                                     # Numero
    | NUM_REAL                                  # NumeroReal
    | chamadaFuncao                              # ChamadaLeitura
    | IDENTIFICADOR ABREPAR argumentos? FECHAPAR # ChamadaGenerica
    | ABREPAR tipo FECHAPAR expressao            # Casting
    ;

// Argumentos para chamadas genéricas
argumentos
    : expressao (VIRGULA expressao)*
    ;

opRelacional
    : MENOR
    | MENORIGUAL
    | MAIOR
    | MAIORIGUAL
    | IGUAL
    | DIFERENTE
    ;

// Funcoes de leitura (tratadas como literais no parser)
chamadaFuncao
    : 'read' ABREPAR FECHAPAR
    | 'readc' ABREPAR FECHAPAR
    | 'reads' ABREPAR FECHAPAR
    ;

// Bloco de instrucoes
bloco
    : ABRECHAVES instrucoes FECHACHAVES
    ;

instrucoes
    : instrucao*
    ;

// Instrucao geral (if com ou sem else, ciclos, escrita, etc.)
instrucao
    : instrucaoEmparelhada
    | instrucaoPorEmparelhar
    ;

instrucaoEmparelhada
    : IF ABREPAR expressao FECHAPAR instrucaoEmparelhada ELSE instrucaoEmparelhada
    | outraInstrucao
    ;

instrucaoPorEmparelhar
    : IF ABREPAR expressao FECHAPAR instrucao
    | IF ABREPAR expressao FECHAPAR instrucaoEmparelhada ELSE instrucaoPorEmparelhar
    ;

// Instrucoes normais (sem if): blocos, ciclos, escrita, etc.
outraInstrucao
    : bloco
    | declaracao
    | instrucaoWhile
    | instrucaoFor
    | instrucaoEscrita
    | instrucaoReturn             
    | instrucaoAtribuicao
    ;

// Ciclo while
instrucaoWhile
    : WHILE ABREPAR expressao FECHAPAR bloco
    ;

// Ciclo for com 3 expressoes
instrucaoFor
    : FOR ABREPAR expressaoOuAtribuicao? PONTOVIRG expressao? PONTOVIRG expressaoOuAtribuicao? FECHAPAR bloco
    ;

// Permite que expressoes tipo "x = 2" aparecam em locais como o for(...)
expressaoOuAtribuicao
    : IDENTIFICADOR ATRIBUICAO expressao
    | expressao
    ;

// Funcoes de escrita no ecra (usadas como literais para antlr4-parse funcionar)
instrucaoEscrita
    : 'write' ABREPAR expressao FECHAPAR PONTOVIRG
    | 'writec' ABREPAR expressao FECHAPAR PONTOVIRG
    | 'writev' ABREPAR IDENTIFICADOR FECHAPAR PONTOVIRG
    | 'writes' ABREPAR argumentoString FECHAPAR PONTOVIRG
    ;

// Instrucao de retorno: return expressao;
instrucaoReturn
    : RETURN expressao PONTOVIRG
    ;

// Atribuicao simples: x = 2;
instrucaoAtribuicao
    : (IDENTIFICADOR | IDENTIFICADOR ABRECOLCH expressao FECHACOLCH) ATRIBUICAO expressao PONTOVIRG
    ;

// Aceita identificadores ou strings literais como argumento de writes()
argumentoString
    : IDENTIFICADOR
    | STRINGLITERAL
    ;