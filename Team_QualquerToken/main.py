# main.py

import sys
import subprocess
from antlr4 import *
from MOCLexer import MOCLexer
from MOCParser import MOCParser
from MOCErrorListener import MOCErrorListener
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

    if "-tree" in sys.argv:
        run_antlr4_parse(input_file, "-tree")
        return

    if "-gui" in sys.argv:
        run_antlr4_parse(input_file, "-gui")
        return

    # --- Fase de Análise Sintática ---
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

    print("--- Análise sintática concluída ---")

    if parser.getNumberOfSyntaxErrors() > 0:
        print("\nErros de sintaxe encontrados. A abortar o processo de geração de código intermédio.")
        sys.exit(1)

    # --- Análise Semântica ---
    print("\n--- A iniciar Análise Semântica ---")
    
    try:
        semantico = VisitorSemantico()
        semantico.visit(tree)

        # Verifica se foram acumulados erros semânticos
        if semantico.erros:
            for erro in semantico.erros:
                print(erro)
            print("\nErros semânticos encontrados. A abortar o processo de geração de código intermédio.")
            exit(1)

        print("\n--- Análise Semântica concluída ---")
    except Exception as e:
        print(e)
        exit(1)

    # --- GERAÇÃO DE CÓDIGO INTERMÉDIO ---
    print("\n--- A iniciar Geração de Código Intermédio ---")
    visitor = VisitorTAC()
    visitor.variaveis_declaradas = set().union(*semantico.contexto) if semantico.contexto else set()
    try:
        visitor.visit(tree)
    except Exception as e:
        print(f"\nErro semântico durante geração de TAC: {e}")
        return
    print("--- Geração de Código Intermédio Concluída ---")

    # --- Exibir TAC Gerado ---
    print("\n==== CÓDIGO TAC GERADO ====")
    tac_original = gerar_texto_tac(visitor.tac_quadruplos)
    for linha in tac_original:
        print(linha)

    # --- Otimização ---
    print("\n==== CÓDIGO TAC OTIMIZADO ====")
    tac_otimizado = otimizar_completo(visitor.tac_quadruplos)
    tac_otimizado_txt = gerar_texto_tac(tac_otimizado)
    for linha in tac_otimizado_txt:
        print(linha)

if __name__ == '__main__':
    main()