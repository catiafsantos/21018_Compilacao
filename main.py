from antlr4 import *
from MOCLexer import MOCLexer
from MOCParser import MOCParser
from MOCVisitor import MOCVisitor
from MOCErrorListener import MOCErrorListener

def main():
    # Lê o input do utilizador (programa escrito)
    input_text = input("Digite o programa: ")
    input_stream = InputStream(input_text)

    # Cria o analisador léxico (Lexer)
    lexer = MOCLexer(input_stream)
    stream = CommonTokenStream(lexer)

    # Cria o parser e associa o fluxo de tokens
    parser = MOCParser(stream)

    # Remove os listeners de erro padrão e adiciona o personalizado
    parser.removeErrorListeners()
    parser.addErrorListener(MOCErrorListener())

    # Gera a árvore de parsing a partir da regra 'programa'
    tree = parser.programa()

    # Aplica o Visitor personalizado para interpretar
    visitor = MOCVisitor()
    try:
        visitor.visit(tree)
    except Exception as e:
        print(e)  # Mostra apenas a mensagem do erro

if __name__ == '__main__':
    main()
