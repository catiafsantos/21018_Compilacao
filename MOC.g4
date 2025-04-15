grammar MOC;

/*
 * ----------------------------
 * LEXER RULES (tokens básicos)
 * ----------------------------
 */

// Tipos de dados
INT     : 'int' ;           // Palavra-chave para declaração de inteiros
DOUBLE  : 'double' ;        // Palavra-chave para declaração de números reais
VOID    : 'void' ;          // Palavra-chave para funções que não retornam valor

// Função principal (main)
MAIN    : 'main' ;          // Palavra-chave que identifica a função principal

// Funções de leitura (tokens para ler valores do utilizador)
READ       : 'read' ;      // Lê um inteiro
READC      : 'readc' ;     // Lê um carácter (valor ASCII)
READS      : 'reads' ;     // Lê uma string

// Funções de escrita (tokens para escrever no ecrã)
WRITE      : 'write' ;     // Escreve um inteiro/double
WRITEC     : 'writec' ;    // Escreve um carácter
WRITEV     : 'writev' ;    // Escreve um vetor (exibe todos os valores)
WRITES     : 'writes' ;    // Escreve uma string ou vetor de caracteres

// Estruturas de controlo
IF      : 'if' ;            // Estrutura condicional
ELSE    : 'else' ;          // Bloco alternativo no condicional
WHILE   : 'while' ;         // Ciclo enquanto
FOR     : 'for' ;           // Ciclo for

// Operadores aritméticos
MAIS    : '+' ;             // Adição
MENOS   : '-' ;             // Subtração
MULT    : '*' ;             // Multiplicação
DIV     : '/' ;             // Divisão
MODULO  : '%' ;             // Módulo (resto da divisão)

// Operadores relacionais
MENOR       : '<' ;         // Menor que
MENORIGUAL  : '<=' ;        // Menor ou igual
MAIOR       : '>' ;         // Maior que
MAIORIGUAL  : '>=' ;        // Maior ou igual
IGUAL       : '==' ;        // Igualdade
DIFERENTE   : '!=' ;        // Diferença

// Operadores lógicos
E_LOGICO    : '&&' ;        // Operador lógico E
OU_LOGICO   : '||' ;        // Operador lógico OU
NAO         : '!' ;         // Operador lógico de negação

// Símbolos e pontuação
ATRIBUICAO   : '=' ;        // Operador de atribuição
VIRGULA      : ',' ;        // Separador de elementos (ex.: parâmetros, variáveis)
PONTOVIRG    : ';' ;        // Termina instruções
ABRECOLCH    : '[' ;        // Abre colchete (para arrays)
FECHACOLCH   : ']' ;        // Fecha colchete (para arrays)
ABRECHAVES   : '{' ;        // Abre chavetas (início de bloco)
FECHACHAVES  : '}' ;        // Fecha chavetas (fim de bloco)
ABREPAR      : '(' ;        // Abre parênteses
FECHAPAR     : ')' ;        // Fecha parênteses

// Palavra-chave de retorno
RETURN  : 'return' ;        // Retorna um valor numa função

// String literal, utilizada em WRITES para textos
STRINGLITERAL : '"' (~["\r\n])* '"' ;

// Comentários ao estilo C (são ignorados)
COMENTARIO_BLOCK : '/*' .*? '*/' -> skip ; // Comentários em bloco (/* ... */)
COMENTARIO_LINE  : '//' ~[\r\n]* -> skip ; // Comentários de linha (// ... até o fim da linha)

// Tokens para números e identificadores
NUM_REAL : [0-9]+ '.' [0-9]+ ;          // Número real (ex.: 3.14)
NUMERO   : [0-9]+ ;                     // Número inteiro
IDENTIFICADOR : [a-zA-Z_][a-zA-Z0-9_]* ; // Nome de variável, função, etc.

// Espaços em branco (tab, espaço, nova linha) são ignorados
ESPACO : [ \t\r\n]+ -> skip ;

/*
 * ----------------------------
 * PARSER RULES (estrutura sintática)
 * ----------------------------
 */

// programa:
// Um programa é composto por duas seções:
//   1. A seção de protótipos, que deve conter pelo menos um protótipo da função main.
//      A ordem dos protótipos é arbitrária, mas todos devem vir antes das definições.
//   2. O corpo, que contém as unidades (declarações/definições) e a definição completa
//      da função main (ponto de entrada).
programa
    : prototipos corpo EOF
    ;

// prototipos:
// Esta regra exige uma sequência de protótipos, na qual deve existir pelo menos
// um 'prototipoPrincipal' (o protótipo da main). Para isso, definimos a regra de forma
// que a sequência termine com pelo menos um 'prototipoPrincipal' em algum lugar.
prototipos
    : (prototipo | prototipoPrincipal)* prototipoPrincipal (prototipo | prototipoPrincipal)*
    ;

// corpo: 
// O corpo do programa contém todas as unidades (declarações e definições) seguidas
// da definição da função main.
corpo
    : unidade* funcaoPrincipal
    ;

// Unidade: pode ser uma função ou uma declaração de variáveis.
unidade
    : funcao
    | declaracao
    ;

// Protótipos de função (declaração de função sem corpo)
prototipo
    : tipo IDENTIFICADOR ABREPAR parametros? FECHAPAR PONTOVIRG
    ;

// Protótipo principal (main) – declaração sem corpo.
prototipoPrincipal
    : tipo MAIN ABREPAR parametros? FECHAPAR PONTOVIRG
    ;

// Função principal (main) – contém o bloco de instruções.
funcaoPrincipal
    : tipo MAIN ABREPAR parametros? FECHAPAR bloco
    ;

// Funções com corpo (demais funções)
funcao
    : tipo IDENTIFICADOR ABREPAR parametros? FECHAPAR bloco
    ;

// parametros:
// Define os parâmetros de uma função, podendo ser:
//   - VOID (sem parâmetros)
//   - Um único parâmetro (apenas o tipo)
//   - Vários parâmetros separados por vírgula.
parametros
    : VOID                         // permite o uso de 'void'
    | tipo                         // apenas o tipo (ex.: int)
    | parametro (VIRGULA parametro)* // lista de parâmetros completos (ex.: int x, double y)
    ;

// parametro:
// Define a forma de um único parâmetro: pode ser só o tipo, ou tipo com identificador,
// ou um vetor (tipo seguido de identificador entre colchetes).
parametro
    : tipo
    | tipo IDENTIFICADOR
    | tipo ABRECOLCH FECHACOLCH  // apenas para prototipos de vectores
    | tipo IDENTIFICADOR ABRECOLCH FECHACOLCH  // vetor como parâmetro
    ;

// tipo:
// Define os tipos permitidos na linguagem.
tipo
    : INT
    | DOUBLE
    | VOID
    ;

// Declaração de variáveis: o tipo seguido por uma lista de variáveis.
declaracao
    : tipo listaVariaveis PONTOVIRG
    ;

// Lista de variáveis, separadas por vírgulas.
listaVariaveis
    : variavel (VIRGULA variavel)*
    ;

// variavel:
// Define uma variável que pode ser declarada de diferentes formas:
//   - Apenas um identificador
//   - Com atribuição a expressões comuns (ex: int x = 2;)
//   - Vetor com tamanho fixo, com ou sem inicialização por bloco
//   - Vetor com atribuição direta à função reads() (ex: s[] = reads();)    
variavel
    : IDENTIFICADOR                                      // ex: int x;
    | IDENTIFICADOR ATRIBUICAO expressao                 // ex: int x = 2;
    | IDENTIFICADOR ABRECOLCH NUMERO FECHACOLCH          // ex: int v[10];
    | IDENTIFICADOR ABRECOLCH FECHACOLCH ATRIBUICAO chamadaReads  // ex: s[] = reads();
    | IDENTIFICADOR ABRECOLCH FECHACOLCH ATRIBUICAO blocoArray    // ex: v[] = {1, 2, 3};
    | IDENTIFICADOR ABRECOLCH NUMERO FECHACOLCH ATRIBUICAO blocoArray // ex: v[3] = {1, 2, 3};
    ;

// Bloco de inicialização para arrays:
// Conjunto de expressões entre chaves.
blocoArray
    : ABRECHAVES listaValores? FECHACHAVES
    ;

// Lista de valores para inicialização de arrays, separados por vírgula.
listaValores
    : expressao (VIRGULA expressao)*
    ;


// Expressões: Operadores, Lógica, Comparações e Casting
// A análise das expressões segue a precedência dos operadores:
//  1. Lógicos: OU (||), E (&&) e negação (!)
//  2. Comparações: operadores relacionais (<, <=, >, >=, ==, !=)
//  3. Aritméticos: adição/subtração e multiplicação/divisão/módulo
//   4. Casting: conversão de tipos (ex.: (int) expr)
//   5. Elementos básicos: literais, variáveis, chamadas de função, acessos a vetor

expressao
    : expressaoOr
    ;

// Operador lógico OU (||) – tem menor precedência entre os lógicos.
expressaoOr
    : expressaoOr OU_LOGICO expressaoAnd     # ouLogico
    | expressaoAnd                           # ouSimples
    ;

// Operador lógico E (&&)
expressaoAnd
    : expressaoAnd E_LOGICO expressaoEquality  # eLogico
    | expressaoEquality                        # andSimples
    ;

// Comparações (ex.: <, <=, ==, etc.)
expressaoEquality
    : expressaoAdd (opRelacional expressaoAdd)?  # comparacaoSimples
    ;

// Operadores de adição e subtração
expressaoAdd
    : expressaoAdd MAIS expressaoMul          # adicao
    | expressaoAdd MENOS expressaoMul         # subtracao
    | expressaoMul                            # addSimples
    ;

// Operadores de multiplicação, divisão e módulo
expressaoMul
    : expressaoMul MULT expressaoUnaria       # multiplicacao
    | expressaoMul DIV expressaoUnaria        # divisao
    | expressaoMul MODULO expressaoUnaria     # modulo
    | expressaoUnaria                         # mulSimples
    ;

// Operadores unários (ex.: negação !)
expressaoUnaria
    : NAO expressaoUnaria                     # negacao
    | MENOS expressaoUnaria                   # unarioNegativo
    | castExpr                                # unariaSimples
    ;

// Casting: permite converter um valor para um outro tipo (ex.: (int) x)
castExpr
    : ABREPAR tipo FECHAPAR castExpr            # casting
    | primary                                  # castSimples
    ;

// Elementos básicos (primary):
// Pode ser uma expressão entre parênteses, uma chamada de função, um literal (número),
// ou um identificador que pode ser seguido de elementos adicionais (chamada genérica ou acesso a vetor).
primary
    : ABREPAR expressao FECHAPAR                # parenteses
    | chamadaFuncao                            # chamadaLeitura
    | NUMERO                                   # numero
    | NUM_REAL                                 # numeroReal
    | IDENTIFICADOR primaryRest                # idComPrefixo
    ;

// Sufixos para um identificador: podem indicar uma chamada de função ou um acesso a vetor.
// Se não houver nada, é apenas a variável.
primaryRest
    : ABREPAR argumentos? FECHAPAR              # chamadaGenerica
    | ABRECOLCH expressao FECHACOLCH            # acessoVetor
    |                                          # semSufixo
    ;

// Lista de argumentos para funções, separados por vírgulas.
argumentos
    : expressao (VIRGULA expressao)*
    ;

// Operadores relacionais para comparações
opRelacional
    : MENOR
    | MENORIGUAL
    | MAIOR
    | MAIORIGUAL
    | IGUAL
    | DIFERENTE
    ;

//---------------------------------------------------------
// Regras para Funções de Leitura e Escrita
//---------------------------------------------------------

// Regras para funções de leitura (usando os tokens READ, READC, READS)
chamadaFuncao
    : READ ABREPAR FECHAPAR
    | READC ABREPAR FECHAPAR
    | READS ABREPAR FECHAPAR
    ;

// chamadaReads:
// Permite unicamente a chamada à função reads(), usada para vetores de inteiros (como strings)
chamadaReads
    : READS ABREPAR FECHAPAR
    ;

//---------------------------------------------------------
// Bloco de Instruções
//---------------------------------------------------------

/*
 * Um bloco é um conjunto de instruções delimitado por chavetas.
 */
bloco
    : ABRECHAVES instrucoes FECHACHAVES
    ;

// Lista (possivelmente vazia) de instruções.
instrucoes
    : instrucao*
    ;

// Regra 'instrucao' – define as diferentes formas de instrução.
// Pode ser um if (com ou sem else), um bloco, uma declaração, ciclo, escrita, retorno ou atribuição.
instrucao
    : instrucaoEmparelhada
    | instrucaoPorEmparelhar
    | outraInstrucao
    ;

instrucaoExpressao
    : expressao PONTOVIRG
    ;

// Instrução emparelhada: usada para o if com else; também pode ser apenas um bloco.
instrucaoEmparelhada
    : IF ABREPAR expressao FECHAPAR bloco ELSE instrucaoEmparelhada
    | bloco
    ;

// Instrução por emparelhar: usada para o if sem else.
instrucaoPorEmparelhar
    : IF ABREPAR expressao FECHAPAR bloco
    | IF ABREPAR expressao FECHAPAR bloco ELSE instrucaoPorEmparelhar
    ;

// Outras instruções: declarações, ciclos, escrita, retorno, atribuições, etc.
outraInstrucao
    : bloco
    | declaracao
    | instrucaoWhile
    | instrucaoFor
    | instrucaoEscrita
    | instrucaoReturn             
    | instrucaoAtribuicao
    | instrucaoExpressao
    ;

// Instrução de ciclo while.
instrucaoWhile
    : WHILE ABREPAR expressao FECHAPAR bloco
    ;

// Instrução de ciclo for, podendo ter expressões de inicialização, condição e atualização.
instrucaoFor
    : FOR ABREPAR expressaoOuAtribuicao? PONTOVIRG expressao? PONTOVIRG expressaoOuAtribuicao? FECHAPAR bloco
    ;

// Regra para expressões ou atribuições (usada principalmente no for, ex.: i = 2)
expressaoOuAtribuicao
    : IDENTIFICADOR ATRIBUICAO expressao
    | expressao
    ;

// Instrução de escrita no ecrã: utiliza os tokens de escrita.
instrucaoEscrita
    : WRITE ABREPAR expressao FECHAPAR PONTOVIRG
    | WRITEC ABREPAR expressao FECHAPAR PONTOVIRG
    | WRITEV ABREPAR IDENTIFICADOR FECHAPAR PONTOVIRG
    | WRITES ABREPAR argumentoString FECHAPAR PONTOVIRG
    ;

// Instrução de retorno (return) – termina uma função devolvendo um valor.
instrucaoReturn
    : RETURN expressao PONTOVIRG
    ;

// Instrução de atribuição: atribuição simples de um valor a uma variável ou posição de vetor.
instrucaoAtribuicao
    : (IDENTIFICADOR | IDENTIFICADOR ABRECOLCH expressao FECHACOLCH) ATRIBUICAO expressao PONTOVIRG
    ;

// Argumento para a escrita de strings: pode ser um identificador ou um literal de string.
argumentoString
    : IDENTIFICADOR
    | STRINGLITERAL
    ;