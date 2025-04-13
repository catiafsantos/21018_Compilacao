# 21018_Compilacao
UAb 2024/2025 - UC de Compilação

Instruções de utilizaçãp:


python3 main.py exemplo.txt            // Corre o programa para validar a gramática              
python3 main.py exemplo.txt -tree      // Corre o programa para validar a gramática e gerar a árvore sintática
python3 main.py exemplo.txt -gui       // Corre o programa para validar a gramática e gerar a árvore sintática com interface gráfica             


########### Enunciado do EfolioA ###########
```
/* e-fólio A
   Compilação 2024/25
   Linguagem: MOC (My Own C)
   Compilador da linguagem: MOCC
*/

/* Os comentários são o habitual do C */
/* A sintaxe é a habitual do C, com as restrições que se seguem:
   - Não há #include nem qualquer diretiva #
   - As variáveis podem ser int ou double, podendo ser simples ou vetores
   - O valor inteiro pode ser visto como um caráter
   - Um vetor de inteiros pode ser visto como uma string de carateres
*/

/* Declaração de variáveis */
int m, n, v[10];
double x, y, z;

/* Inicialização com expressões aritméticas */
int m = 1, n = 2 * m;
double x = 3.14, y = x / 2;

/* Inicialização com valores introduzidos pelo utilizador */
int m = read();       // lê um inteiro
double n = read();    // lê um double
int c = readc();      // lê um caráter (código ASCII)
int s[] = reads();    // lê uma string (códigos ASCII terminando em 0)

/* Mistura de inicializações */
int a, b = read(), c = 2 * b, v[] = {1, 2, 3}; // v fica com tamanho 3 automaticamente

/* Regras adicionais:
   - Se a variável ainda não tiver sido declarada anteriormente, deve dar erro
   - Não existem estruturas
   - Conversões entre int e double seguem as regras do C
   - Pode haver casting (double) e (int)
*/

/* Prototipagem de funções */
int fact(int);
void main(void);

/* Exemplos de blocos e condições */
if (x > y) {
    y = x;
} else {
    x = y;
}

if (x > y) {
    y = 0;
}

/* Ciclos */
while (x > 0) {
    x = x - 10;
}

for (i = 0; i < 10; i = i + 1) {
    x = x + i;
    y = y + x;
}

/* Regras adicionais:
   - Não é possível usar ++, --, +=, etc.
   - A função read() lê apenas um valor de cada vez
   - Para ler um vetor de int ou double, é necessário um ciclo for
   - Para ler uma string ou caráter, usa-se reads() ou readc()
*/

/* Escrita no ecrã */
c = readc();  // lê um caráter
s = reads();  // lê uma string

/* Exemplos de escrita */
write(v[0]);      // escreve: 97
writec(v[0]);     // escreve: a
writev(v);        // escreve: {97, 98, 99, 0}
writes(v);        // escreve: abc
writes("Hello, World!"); // escreve a string e muda de linha

/* Exemplo 1: Fatorial (versão recursiva) */
int fact(int k) {
    if (k <= 1) {
        return 1;
    } else {
        return k * fact(k - 1);
    }
}

void main(void) {
    int n;
    writes("Introduza inteiro: ");
    n = read();
    write(fact(n));
}

/* Exemplo 2: Fatorial (versão iterativa) */
int fact(int k) {
    int i, n = 1;
    for (i = 2; i <= k; i = i + 1) {
        n = n * i;
    }
    return n;
}

void main(void) {
    int n;
    writes("Introduza inteiro: ");
    n = read();
    write(fact(n));
}

/* Exemplo 3: Média de uma lista de valores positivos */
double avg(double v[], int size) {
    int i;
    double sum = 0;
    for (i = 0; i < size; i = i + 1) {
        sum = sum + v[i];
    }
    return sum / size;
}

void main(void) {
    int i, n;
    double v[100];
    writes("Introduza tamanho do vetor, seguido dos respetivos valores: ");
    n = read();
    for (i = 0; i < n; i = i + 1) {
        v[i] = read();
    }
    write(avg(v, n));
}
```
