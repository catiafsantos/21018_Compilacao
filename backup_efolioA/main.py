# main.py

import sys
import subprocess
from antlr4 import *
from MOCLexer import MOCLexer
from MOCParser import MOCParser
from MOCErrorListener import MOCErrorListener

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
        parser.programa()
    except Exception as e:
        print(f"\n[Parsing interrompido]: {e}")

if __name__ == '__main__':
    main()