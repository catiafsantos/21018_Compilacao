# MOCC - My Own C Compiler
**UAb 2024/2025 – Unidade Curricular de Compilação**

Este projeto consiste no desenvolvimento de um compilador para a linguagem **MOC (My Own C)**, uma linguagem fictícia inspirada em C, com uma gramática simplificada adaptada para o ensino e análise de compiladores.


## Introdução

A linguagem MOC tem como objetivo permitir a exploração dos conceitos de análise léxica e sintática com ferramentas modernas como **ANTLR4**. Este repositório contém a gramática completa em ANTLR, bem como os scripts necessários para compilar, analisar e validar código-fonte nesta linguagem.

> **Requisitos recomendados:**  
> - Python 3.10 ou superior  
> - ANTLR versão 4.13.2  
> - Sistema com Java instalado (necessário para o ANTLR)

Para mais contexto sobre a linguagem, consulta o enunciado oficial fornecido na UC:  
**[Enunciado do e-fólio A](https://elearning.uab.pt/pluginfile.php/3918150/mod_assign/introattachment/0/MOCC.pdf?forcedownload=1)**

---

## Estrutura do Projeto

Este projeto insere-se no eFolio B, continuação do eFolio A com a fusão de dois grupos para a continuação do projeto.

- [Grupo: Qualquer] - [Andreia Romão - 1702430 / Cátia Santos - 1702194]
- [Grupo: Token] - [Rui Menino - 1103425 / Luís Tavares - 1803237 / José Augusto Azevedo - 2200655]


| Ficheiro              | Descrição                                                           |
|-----------------------|---------------------------------------------------------------------|
| `main.py`             | Script principal com menu e execução automática do ANTLR            |
| `MOC.g4`              | Ficheiro de gramática (regras léxicas e sintáticas)                 |
| `MOCErrorListener.py` | Tratamento de erros com mensagens legíveis para o utilizador        |
| `MOCVisitorDEBUG.py`  | Visitor alternativo com debug passo-a-passo (não usado por defeito) |
| `reset_antlr.sh`      | Script utilitário para limpar e regenerar ficheiros do ANTLR        |
| `README.md`           | Instruções de utilização e documentação técnica do projeto          |
| `Exemplos_Teste/`     | Pasta com 6 ficheiros de testes:exemplo1 a exemplo3 -> enunciado    |
|                       | :exemplo 4 e exemplo 4 -> testes extremos, sucesso e falha          |
|                       | :Possiveis_testes_Sucesso-Erro -> todos os testes criados           |

---

## Como executar

### Instalar o Python

Este projeto requer **Python 3.10** ou superior.

### Windows

1. Vá a [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)
2. Clique em “Download Python 3.X”
3. Durante a instalação, **ative a opção** `Add Python to PATH`
4. Verificar a instalação:

```bash
python --version
```
### Terminal recomendado: Git Bash

Para que o comando `main.py -tree` funcione corretamente no Windows, é necessário usar um terminal compatível com comandos Unix, como `cat`. O terminal **Git Bash** é a forma mais simples de garantir essa compatibilidade.

#### Como instalar o Git Bash:

1. Vá a: [https://git-scm.com/download/win](https://git-scm.com/download/win)
2. Faça o download do executável para Windows mais recente
3. Durante a instalação, pode aceitar todas as opções por defeito
4. Após a instalação, abra o **Git Bash** (procure "Git Bash" no menu Iniciar, ou altere o tipo de terminal no IDE que está a usar)

#### Como utilizar:

No Git Bash, pode executar os comandos do projeto normalmente. Exemplo:

```
python3 main.py Exemplos_Teste/exemplo1.txt -tree
```
---

### Linux (Debian/Ubuntu)

```bash
sudo apt update
sudo apt install python3 python3-pip
python3 --version
```
---
### macOS

```bash
brew install python
```

> Em todos os sistemas, certifique que está a usar `python3` e `pip3`, especialmente se tiver o Python 2 instalado por defeito.

---

### Preparar ambiente

1. Instale o ANTLR4 e adicione ao PATH (ver instruções em: https://github.com/antlr/antlr4)
2. Instale dependências:
```bash
pip install antlr4-python3-runtime
```
---
### Compilar
```bash
antlr4 -Dlanguage=Python3 -visitor MOC.g4
```

### Executar exemplos com ErrorListener personalizado 
> Assume-se que o ficheiro `exemplo1.txt` contém um exemplo de código na linguagem definida.

> Valida o ficheiro `exemplo1.txt` de acordo com a gramática.
```bash
python3 main.py Exemplos_Teste/exemplo1.txt 
```
> Gera e imprime a árvore sintática textual (parse tree).

```bash
python3 main.py Exemplos_Teste/exemplo1.txt -tree
```
> Abre a árvore sintática numa interface gráfica (requer Java com GUI).

```bash
python3 main.py Exemplos_Teste/exemplo1.txt -gui
```
#### Executar exemplos com ErrorListener default do ANTLR
> Assume-se que o ficheiro `exemplo1.txt` contém um exemplo de código na linguagem definida.

> Valida o ficheiro `exemplo1.txt` de acordo com a gramática.
```bash
cat Exemplos_Teste/exemplo1.txt  | antlr4-parse MOC.g4 programa
```
> Gera e imprime a árvore sintática textual (parse tree).

```bash
cat Exemplos_Teste/exemplo1.txt  | antlr4-parse MOC.g4 programa -tree
```
> Abre a árvore sintática numa interface gráfica (requer Java com GUI).

```bash
cat Exemplos_Teste/exemplo1.txt  | antlr4-parse MOC.g4 programa -gui
```

---

## Exemplos de código válidos (retirados do enunciado)

```c
int fact(int);
void main(void);

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
```

> Não são permitidas diretivas `#include` nem operadores como `++`, `--`, `+=`, etc.

---

## Erros comuns e mensagens

- `Token inválido '#'` → A linguagem MOC não suporta diretivas como `#include`.
- `mismatched input '=' expecting ';'` → Erro comum em inicializações incorretas de vetores com tamanho explícito.
- `Função 'x' não definida.` → Chamada de função sem definição correspondente.

---

## Regenerar ficheiros do ANTLR (opcional)

Sempre que for alterada a gramática:

```bash
./reset_antlr.sh
```

Este script remove os ficheiros antigos e regenera todos os `.py` a partir do `MOC.g4`.

---

## Autores

- [Grupo: Qualquer Token] - [Andreia Romão - 1702430 / Cátia Santos - 1702194 / Rui Menino - 1103425 / Luís Tavares - 1803237 / José Augusto Azevedo - 2200655]


- UC de Compilação – Universidade Aberta, 2024/2025
