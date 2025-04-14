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

| Ficheiro              | Descrição                                                           |
|-----------------------|---------------------------------------------------------------------|
| `main.py`             | Script principal com menu e execução automática do ANTLR            |
| `MOC.g4`              | Ficheiro de gramática (regras léxicas e sintáticas)                 |
| `MOCErrorListener.py` | Tratamento de erros com mensagens legíveis para o utilizador        |
| `MOCVisitorDEBUG.py`  | Visitor alternativo com debug passo-a-passo (não usado por defeito) |
| `reset_antlr.sh`      | Script utilitário para limpar e regenerar ficheiros do ANTLR        |
| `README.md`           | Instruções de utilização e documentação técnica do projeto          |

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

### Linux (Debian/Ubuntu)

```bash
sudo apt update
sudo apt install python3 python3-pip
```

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

### Executar exemplos

```bash
python3 main.py exemplo.txt
```
Valida o ficheiro `exemplo.txt` de acordo com a gramática.

```bash
python3 main.py exemplo.txt -tree
```
Gera e imprime a árvore sintática textual (parse tree).

```bash
python3 main.py exemplo.txt -gui
```
Abre a árvore sintática numa interface gráfica (requer Java com GUI).

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

- [Grupo: Qualquer] - [Andreia Romão - 1702430 / Cátia Santos - 1702194]
- UC de Compilação – Universidade Aberta, 2024/2025
