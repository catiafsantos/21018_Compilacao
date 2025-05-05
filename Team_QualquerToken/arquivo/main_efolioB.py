from antlr4 import FileStream, CommonTokenStream
from MOCLexer import MOCLexer
from MOCParser import MOCParser
from VisitorTAC import VisitorTAC, gerar_texto_tac
from OtimizadorTAC import * 

def compilar_tac(ficheiro_moc):
    # Lê o ficheiro de input
    input_stream = FileStream(ficheiro_moc, encoding='utf-8')
    lexer = MOCLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = MOCParser(stream)

    arvore = parser.programa()  # nó inicial

    # VisitorTAC atua diretamente sobre a árvore
    visitor_tac = VisitorTAC()
    # Agora está assim mas temos de pensar tratar deste erro em algum lado- trata-se de um erro semântico
    try:
        visitor_tac.visit(arvore)
    except Exception as e:
        print(f"\nErro semântico: {e}")
        return


    # Aplicar otimização
    tac_optimizado = otimizar_completo(visitor_tac.tac_quadruplos)

    # Mostrar resultado final
    print("==== CÓDIGO TAC GERADO ====")
    linhas = gerar_texto_tac(visitor_tac.tac_quadruplos)
    for linha in linhas:
        print(linha)

    # Mostrar TAC otimizado
    print("==== CÓDIGO TAC OTIMIZADO ====")
    linhas = gerar_texto_tac(tac_optimizado)
    for linha in linhas:
        print(linha)

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Uso: python3 nome_do_script.py <ficheiro.moc>")
    else:
        compilar_tac(sys.argv[1])
