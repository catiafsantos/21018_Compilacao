# main.py

import sys
import subprocess
from antlr4 import *
from MOCLexer import MOCLexer
from MOCParser import MOCParser
from MOCErrorListener import MOCErrorListener
from MOCVisitorDEBUG import MOCVisitor


def run_antlr4_parse(file_path, option):
    cmd = f"cat {file_path} | antlr4-parse MOC.g4 programa {option}"
    subprocess.run(cmd, shell=True)

def main():
    global tree
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

    # Execução com listener de erro personalizado
    input_stream = FileStream(input_file, encoding='utf-8')
    lexer = MOCLexer(input_stream)
    token_stream = CommonTokenStream(lexer)

    lexer.removeErrorListeners()
    lexer.addErrorListener(MOCErrorListener())  # Para erros léxicos

    parser = MOCParser(token_stream)
    parser.removeErrorListeners()  # Remove os listeners padrão
    parser.addErrorListener(MOCErrorListener())  # Para erros sintaxicos

    try:
        tree = parser.programa() # Obtém a Parse Tree
    except Exception as e:
        print(f"\n[Parsing interrompido]: {e}")
    print("--- Análise sintática concluída ---")

    # Verifica se houve erros de sintaxe ANTES de tentar visitar
    if parser.getNumberOfSyntaxErrors() > 0:
        print("\n!!! Erros de sintaxe encontrados. Abortando geração de código intermédio. !!!")
        sys.exit(1)

    # --- GERAÇÃO DO CÓDIGO INTERMÉDIO ---
    print("\n--- A iniciar Geração de Código Intermédio ---")
    # 1. Criar uma instância do seu Visitor customizado
    visitor = MOCVisitor()

    # 2. Chamar o método visit na raiz da árvore
    codigo_intermedio_final = visitor.visit(tree) # O método visitPrograma retorna a lista

    print("--- Geração de Código Intermédio Concluída ---")

    # 3. Imprimir ou processar o código intermédio gerado
    print("\n--- Código Intermédio Resultante ---")
    if codigo_intermedio_final: # Verifica se algo foi retornado/gerado
        for instrucao in codigo_intermedio_final:
            print(instrucao)
    else:
        print("(Nenhuma instrução gerada ou retornada pelo visitor principal)")
if __name__ == '__main__':
    main()