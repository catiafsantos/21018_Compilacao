# main.py

import os
import sys
import copy
import subprocess
from antlr4 import *
from antrl.MOCLexer import MOCLexer
from antrl.MOCParser import MOCParser
from parser.MOCErrorListener import MOCErrorListener
from utils.TabelaSimbolos import TabelaDeSimbolos
from VisitorSemantico import VisitorSemantico
from VisitorTAC import VisitorTAC, gerar_texto_tac
from OtimizadorTAC import otimizar_completo

def run_antlr4_parse(file_path, option):
    cmd = f"cat {file_path} | antlr4-parse MOC.g4 programa {option}"
    subprocess.run(cmd, shell=True)

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 main.py <ficheiro> [-tree | -gui]")
        return

    input_file = sys.argv[1]

    # Check if the file exists
    if not os.path.exists(input_file):
        print("O ficheiro " + input_file + " não existe.")
        return

    if "-tree" in sys.argv:
        run_antlr4_parse(input_file, "-tree")
        return

    if "-gui" in sys.argv:
        run_antlr4_parse(input_file, "-gui")
        return

    # --- Fase de Análise Sintática ---
    print("\n--- A iniciar Análise Sintática ---")

    input_stream = FileStream(input_file, encoding='utf-8')
    lexer = MOCLexer(input_stream)
    token_stream = CommonTokenStream(lexer)

    lexer.removeErrorListeners()
    lexer.addErrorListener(MOCErrorListener())

    parser = MOCParser(token_stream)
    parser.removeErrorListeners()
    parser.addErrorListener(MOCErrorListener())

    try:
        tree = parser.programa()
    except Exception as e:
        print(f"\n[Parsing interrompido]: {e}")
        return

    print("\n--- Análise Sintática concluída ---")

    if parser.getNumberOfSyntaxErrors() > 0:
        print("\nErros de sintaxe encontrados. A abortar o processo de geração de código intermédio.")
        sys.exit(1)

    # 1. Criação da Tabela de Símbolos
    tabela_de_simbolos_principal = TabelaDeSimbolos()

    # --- Análise Semântica ---
    print("\n--- A iniciar Análise Semântica ---")

    try:
        semantico = VisitorSemantico(tabela_de_simbolos_principal)
        semantico.erros(tree)
        print("\n--- Análise Semântica concluída ---")
    except Exception as e:
        print(e)
        print("\nErros semânticos encontrados. A abortar o processo de geração de código intermédio.")
        exit(1)


    # --- GERAÇÃO DE CÓDIGO INTERMÉDIO ---
    print("\n--- A iniciar Geração de Código Intermédio ---")
    visitor = VisitorTAC(tabela_de_simbolos_principal)
    visitor.variaveis_declaradas = set().union(*semantico.contexto) if semantico.contexto else set()
    try:
        visitor.visit(tree)
    except Exception as e:
        print(f"\nErro semântico durante geração de TAC: {e}")
        return
    print("\n--- Geração de Código Intermédio concluída ---")

    # --- Exibir TAC Gerado ---
    print("\n==== CÓDIGO TAC GERADO ====")
    tac_original = gerar_texto_tac(visitor.tac_quadruplos)
    for linha in tac_original:
        print(linha)

    # --- Otimização ---
    print("\n==== CÓDIGO TAC OTIMIZADO ====")
    # Melhoria para evitar modificar o tac gerado inicialmente
    tac_otimizado = otimizar_completo(copy.deepcopy(visitor.tac_quadruplos))
    tac_otimizado_txt = gerar_texto_tac(tac_otimizado)
    for linha in tac_otimizado_txt:
        print(linha)

    #--- Preparação codigo máquina ---
    #print(tabela_de_simbolos_principal)

if __name__ == '__main__':
    main()