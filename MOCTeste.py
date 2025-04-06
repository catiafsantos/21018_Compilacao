from antlr4 import *
from MOCLexer import MOCLexer
from MOCParser import MOCParser
from MOCVisitor import MOCVisitor
from MOCErrorListener import MOCErrorListener
import sys

def main():
    if len(sys.argv) < 2:
        print("Uso: python MOCTeste.py <ficheiro.txt>")
        return

    # Lê o ficheiro fornecido por argumento
    filename = sys.argv[1]
    with open(filename, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # Substitui espaços especiais (caso existam)
    clean_text = raw_text.replace('\u00A0', ' ')

    # Cria input stream
    input_stream = InputStream(clean_text)

    # Lexer e token stream
    lexer = MOCLexer(input_stream)
    token_stream = CommonTokenStream(lexer)

    # Cria o parser diretamente antes de consumir os tokens
    parser = MOCParser(token_stream)
    parser.removeErrorListeners()
    parser.addErrorListener(MOCErrorListener())

    # Mostra os tokens já via CommonTokenStream (sem esgotar o lexer)
    print("#################### TOKENS RECONHECIDOS ####################")
    token_stream.fill()
    symbolic_names = MOCLexer.symbolicNames
    for token in token_stream.tokens:
        if 0 <= token.type < len(symbolic_names):
            nome = symbolic_names[token.type]
        else:
            nome = f"<desconhecido:{token.type}>"
        print(f"{token.text!r} -> {nome}")

    # Faz parsing e mostra árvore
    print("\n#################### ÁRVORE SINTÁTICA ####################")
    tree = parser.programa()
    print(tree.toStringTree(recog=parser))

    # Visita a árvore com o interpretador
    print("\n#################### EXECUÇÃO ####################")
    visitor = MOCVisitor()
    try:
        resultado_final = visitor.visit(tree)
        if resultado_final is not None:
            print(f"[Resultado Final]: {resultado_final}")
    except Exception as e:
        print(f"[Erro de Execução] {e}")

if __name__ == "__main__":
    main()