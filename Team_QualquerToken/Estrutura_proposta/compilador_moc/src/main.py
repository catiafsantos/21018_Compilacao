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
from Gerador_P3Assembly import GeradorP3Assembly

def run_antlr4_parselinux(file_path, option):
    cmd = f"cat {file_path} | antlr4-parse MOC.g4 programa {option}"
    subprocess.run(cmd, shell=True)

def resource_path(relative_path):
    """
    Obtém o caminho absoluto para um recurso, funcionando tanto em
    ambiente de desenvolvimento como num executável PyInstaller.
    """
    try:
        # O PyInstaller cria uma pasta temporária e guarda o seu caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Se _MEIPASS não estiver definido, não estamos num executável
        # e o caminho base é o diretório do nosso script.
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def run_antlr4_parse(file_path, option):
    """
    Executa o antlr4-parse de forma multiplataforma, passando o conteúdo
    de um ficheiro para o seu standard input.
    """
    # 1. Verificar se o ficheiro de entrada existe antes de continuar.
    if not os.path.exists(file_path):
        print(f"Erro: O ficheiro de entrada '{file_path}' não foi encontrado.")
        return

    # IMPORTANTE: Obtenha o caminho para o ficheiro de gramática usando a nova função.
    # O argumento "MOC.g4" deve corresponder à estrutura que você usou no --add-data.
    # Veja a nota abaixo.
    grammar_file_path = resource_path("gramatica/MOC.g4")

    # O comando agora usa o caminho absoluto correto para a gramática.
    cmd_list = ["antlr4-parse", grammar_file_path, "programa", option]

    # 2. O comando a ser executado, dividido numa lista.
    #    Isto é mais seguro do que usar shell=True.
    #cmd_list = ["antlr4-parse", "MOC.g4", "programa", option]

    try:
        # 3. Ler o conteúdo do ficheiro de código-fonte.
        #    Esta parte substitui o 'cat'.
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()

        # 4. Executar o comando e passar o conteúdo para o stdin.
        print(f"A executar o ANTLR para '{file_path}' com a opção '{option}'...")
        subprocess.run(
            cmd_list,
            input=file_content,  # Passa o conteúdo do ficheiro para o stdin do comando
            text=True,  # Trata o input como texto (codificação automática)
            check=True  # Lança uma exceção se o comando falhar (retornar um código de erro)
        )

    except FileNotFoundError:
        # Este erro pode ocorrer se o comando 'antlr4-parse' não for encontrado no PATH do sistema.
        print("\nERRO: O comando 'antlr4-parse' não foi encontrado.")
        print("Verifique se o ANTLR foi instalado corretamente e se o seu PATH está configurado.")

    except subprocess.CalledProcessError as e:
        # Este erro ocorre se o antlr4-parse for executado mas falhar (ex: erro de sintaxe no ficheiro)
        print(f"\nERRO: A análise do ANTLR falhou. Código de retorno: {e.returncode}")
        # A saída de erro do antlr4-parse já terá sido impressa no terminal.

    except Exception as e:
        # Para outros erros inesperados.
        print(f"Ocorreu um erro inesperado: {e}")
def main():
    # Determina se o script está a ser executado como um ficheiro .py ou como um executável "congelado".
    # A função getattr() é usada para aceder ao atributo de forma segura, retornando False se ele não existir.
    if getattr(sys, 'frozen', False):
        # Se estiver "congelado", estamos a executar o .exe.
        # O nome do programa é o nome base do ficheiro executável.
        program_name = os.path.basename(sys.executable)
    else:
        # Se não, estamos a executar o script .py.
        # O nome do programa é o interpretador Python seguido do nome do script.
        # __file__ contém o caminho para o script atual.
        program_name = f"python3 {os.path.basename(__file__)}"

    if len(sys.argv) < 2:
        print(f"Uso: {program_name} <ficheiro> [-tree | -gui]")
        sys.exit(1)  # É uma boa prática usar sys.exit() para terminar o programa aqui.


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

    #--- Gerar código final em P3 Assembly ---
    print("\n==== CÓDIGO ASSEMBLY P3 GERADO ====")

    # 1. Instanciar o gerador P3
    p3_generator = GeradorP3Assembly(tac_otimizado)

    # 2. Chamar o método para gerar o código Assembly P3 a partir do TAC otimizado
    #    Este método deve receber a lista de quádruplas TAC *otimizadas* (objetos, não texto).
    #    No exemplo anterior, chamei este método de `generate_from_tac_list`.
    try:
        # 'tac_otimizado' deve ser a lista de objetos/quádruplas TAC
        codigo_assembly_p3 = p3_generator.generate_from_tac_list(tac_otimizado)

        # 3. Imprimir ou salvar o código Assembly P3
        print(codigo_assembly_p3)

        # Gravar o código final num arquivo .as para o assembler P3, na mesma pasta do .moc
        output_file = input_file.replace(".moc", ".as")
#        with open(output_file, "w", encoding="cp1252") as f:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(codigo_assembly_p3)
        print("\nCódigo Assembly P3 gravado em '{}'.".format(output_file))

    except Exception as e:
        print(f"\nErro ao gerar código Assembly P3: {e}")
        # Pode ser útil imprimir mais detalhes do erro ou rastreamento da pilha aqui
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()