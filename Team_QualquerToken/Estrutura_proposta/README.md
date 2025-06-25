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
**[Identificação da linguagem MOC](https://elearning.uab.pt/pluginfile.php/3918150/mod_assign/introattachment/0/MOCC.pdf?forcedownload=1)**

---

## Estrutura do Projeto

Este projeto insere-se no eFolio B, continuação do eFolio A com a fusão de dois grupos para a continuação do projeto.

- [Grupo: Qualquer] - [Andreia Romão - 1702430 / Cátia Santos - 1702194]
- [Grupo: Token]    - [Rui Menino - 1103425 / Luís Tavares - 1803237 / José Augusto Azevedo - 2200655]

```plaintext
compilador_moc/
│
├── relatorio/                      # Relatório do efolioB
│
├── src/
│   ├── antlr/                      # Ficheiros gerados automaticamente pelo ANTLR
│   │   ├── MOCLexer.py
│   │   ├── MOCVisitor.py
│   │   ├── MOCListener.py
│   │   ├── MOCParser.py
│   │   └── MOC.tokens, .interp (...)
│   │
│   ├── dist/
│   │   ├── compilador_moc.exe      # Ficheiro .exe para gerar o código assemblly P3
│   │   ├── criar_exe.txt           # Ficheiro com as instruções de geração do .exe
│   │   ├── exemplo1.as             # Ficheiro com o código assembly gerado pelo compilador (.exe)
│   │   └── exemplo1.moc            # Ficheiro com o programa a ser convertido para assembly
│   │
│   ├── parser/
│   │   ├── MOC.g4                 # Gramática da linguagem MOC
│   │   └── MOCErrorListener.py    # Listener com tratamento personalizado de erros
│   │
│   ├── test_examples/             # Programas de teste em MOC (.moc) [exemplos do enuciado, adicionais ou funcionalidade]
│   │   ├── exemplo1.moc, exemplo2.moc, exemplo3.moc       # Testes de exemplo do enunciado
│   │   ├── exemplo4.moc, exemplo5.moc, exemplo6.moc       # Exemplos de teste adicionais
│   │   ├── variavel_n_duplicada.moc
│   │   ├── compatibilidade_de_tipos.moc
│   │   ├── variavel_k_nao_declarada.moc
│   │   ├── compatibilidade_de_tipos.moc
│   │   └── Testes_optimizador01.moc (...)                 # Testes para validar cada uma das otimizações aplicadas
│   │
│   ├── utils/
│   │   ├── TabelaSimbolos.py      # Tabela de símbolos usada na análise semântica
│   │
│   ├── Gerador_P3Assembly.py      # Aplicação do gerador de código assemblyP3
│   ├── VisitorSemantico.py        # Visitor que faz verificação semântica (tipos, declarações)
│   ├── VisitorTAC.py              # Visitor responsável pela geração de TAC
│   ├── OtimizadorTAC.py           # Aplicação das otimizações ao TAC gerado
│   ├── Testes_semanticos.py       # Script para correr os testes semanticos
│   └── main.py                    # Script principal com menu de execução
|
└── README.md                      # Instruções de instalação, execução e descrição do projeto
```
---

## Pré-requesitos

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


## Instruções de execução

No terminal, a partir da pasta `src/`, execute:

```bash
python main.py test_examples/nome_do_ficheiro.moc
```
---
### Exemplos:

```bash
python main.py test_examples/Testes_optimizador12.moc
```

```bash
python main.py test_examples/compatibilidade_de_tipos.moc
```

#### Resultado esperado (exemplo com sucesso)

```text
--- A iniciar Análise Sintática ---

--- Análise Sintática concluída ---

--- A iniciar Análise Semântica ---

--- Análise Semântica concluída ---

--- A iniciar Geração de Código Intermédio ---

--- Geração de Código Intermédio concluída ---

==== CÓDIGO TAC GERADO ====
...

==== CÓDIGO TAC OTIMIZADO ====
...

==== CÓDIGO ASSEMBLY P3 GERADO ====
;============== Região de Dados (inicia no endereço 8000h)
                ORIG    8000h
...
Código Assembly P3 gravado em 'test_examples/as_exemplo_ciclo_for_inputs.as'
```
#### Resultado esperado (exemplo com erro)

```text
--- A iniciar Análise Sintática ---

--- Análise Sintática concluída ---

--- A iniciar Análise Semântica ---
[Erro semântico] Atribuição de tipo incompatível em 'c' (esperado: int, obtido: double)

Erros semânticos encontrados. A abortar o processo de geração de código intermédio.
```
---
## Testes
### Testes manuais

> Todos os testes de código-fonte da linguagem MOC estão na pasta:

```
src/test_examples/
```

Pode correr qualquer um destes ficheiros com o script principal `main.py`, que irá:

1. Fazer a análise sintática
2. Fazer a análise semântica
3. Gerar código intermediário (TAC), se não houver erros
4. Aplicar otimizações ao TAC
---
### Testes automatizados [Semânticos]

> Script de testes automáticos para verificar se a análise semântica está a detetar corretamente erros como:

- variáveis ou funções não declaradas
- declarações duplicadas
- erros em condições `if`, ciclos `for` ou `while`

O ficheiro de testes encontra-se em `src/Testes_semanticos.py`.

#### Instruções de execução

No terminal, entre na pasta `src/`:

```bash
cd src
python Testes_semanticos.py
```

Se tudo estiver correto, deve ver algo como:

```bash
..............
----------------------------------------------------------------------
Ran 14 tests in 0.063s

OK
```
---
### NOTA:
> Para mais informações sobre a análise sintática/léxica ou mais sobre informções do efolioA verificar o link: **https://github.com/catiafsantos/21018_Compilacao/blob/main/README.md**
---

## Autores

- [Grupo: Qualquer Token] - [Andreia Romão - 1702430 / Cátia Santos - 1702194 / Rui Menino - 1103425 / Luís Tavares - 1803237 / José Augusto Azevedo - 2200655]


- UC de Compilação – Universidade Aberta, 2024/2025
