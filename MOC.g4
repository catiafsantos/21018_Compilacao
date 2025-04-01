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

// Símbolos e pontuação
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
NUMERO        : [0-9]+ ;
IDENTIFICADOR : [a-zA-Z_][a-zA-Z0-9_]* ;

// Espaços em branco (ignorados)
ESPACO : [ \t\r\n]+ -> skip ;

/*
 * ----------------------------
 * PARSER RULES (estrutura sintática)
 * ----------------------------
 */

// Programa = protótipos + (opcional) main + outras funções/declarações + EOF
programa
    : prototipo* prototipoPrincipal? unidade* funcaoPrincipal EOF
    ;

unidade
    : funcao
    | declaracao
    ;

// Protótipos de função
prototipo
    : tipo IDENTIFICADOR ABREPAR parametros? FECHAPAR PONTOVIRG
    ;

// Protótipo específico da função main
prototipoPrincipal
    : tipo 'main' ABREPAR parametros? FECHAPAR PONTOVIRG
    ;

// Função principal (main)
funcaoPrincipal
    : tipo 'main' ABREPAR parametros? FECHAPAR bloco
    ;

// Funções com corpo
funcao
    : tipo IDENTIFICADOR ABREPAR parametros? FECHAPAR bloco
    ;

// Parâmetros da função
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

// Declaração de variáveis
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

// Inicialização de vetores
blocoArray
    : ABRECHAVES listaValores? FECHACHAVES
    ;

listaValores
    : expressao (VIRGULA expressao)*
    ;

// Expressões com operadores, lógica, casting
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

// Funções de leitura (tratadas como literais no parser)
chamadaFuncao
    : 'read' ABREPAR FECHAPAR
    | 'readc' ABREPAR FECHAPAR
    | 'reads' ABREPAR FECHAPAR
    ;

// Bloco de instruções
bloco
    : ABRECHAVES instrucoes FECHACHAVES
    ;

instrucoes
    : instrução*
    ;

// Instrução geral (if com ou sem else, ciclos, escrita, etc.)
instrução
    : instruçãoEmparelhada
    | instruçãoPorEmparelhar
    ;

instruçãoEmparelhada
    : IF ABREPAR expressao FECHAPAR instruçãoEmparelhada ELSE instruçãoEmparelhada
    | outraInstrucao
    ;

instruçãoPorEmparelhar
    : IF ABREPAR expressao FECHAPAR instrução
    | IF ABREPAR expressao FECHAPAR instruçãoEmparelhada ELSE instruçãoPorEmparelhar
    ;

// Instruções normais (sem if): blocos, ciclos, escrita, etc.
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

// Ciclo for com 3 expressões
instrucaoFor
    : FOR ABREPAR expressaoOuAtribuicao? PONTOVIRG expressao? PONTOVIRG expressaoOuAtribuicao? FECHAPAR bloco
    ;

// Permite que expressões tipo "x = 2" apareçam em locais como o for(...)
expressaoOuAtribuicao
    : IDENTIFICADOR ATRIBUICAO expressao
    | expressao
    ;

// Funções de escrita no ecrã (usadas como literais para antlr4-parse funcionar)
instrucaoEscrita
    : 'write' ABREPAR expressao FECHAPAR PONTOVIRG
    | 'writec' ABREPAR expressao FECHAPAR PONTOVIRG
    | 'writev' ABREPAR IDENTIFICADOR FECHAPAR PONTOVIRG
    | 'writes' ABREPAR argumentoString FECHAPAR PONTOVIRG
    ;

// Instrução de retorno: return expressao;
instrucaoReturn
    : RETURN expressao PONTOVIRG
    ;

// Atribuição simples: x = 2;
instrucaoAtribuicao
    : (IDENTIFICADOR | IDENTIFICADOR ABRECOLCH expressao FECHACOLCH) ATRIBUICAO expressao PONTOVIRG
    ;

// Aceita identificadores ou strings literais como argumento de writes()
argumentoString
    : IDENTIFICADOR
    | STRINGLITERAL
    ;
