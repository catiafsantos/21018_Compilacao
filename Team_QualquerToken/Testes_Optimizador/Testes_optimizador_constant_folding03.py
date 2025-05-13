import unittest
from antlr4 import *
from io import StringIO

from MOCErrorListener import MOCErrorListener
from OtimizadorTAC import otimizar_completo
from TabelaSimbolos import TabelaDeSimbolos
from VisitorSemantico import VisitorSemantico

# Supondo que TabelaDeSimbolos é usada internamente pelo VisitorTAC ou não é necessária aqui
# from TabelaSimbolos import TabelaDeSimbolos

# Certifique-se que os imports funcionam a partir da localização do seu teste
# Pode precisar de ajustar o sys.path se estiver numa estrutura de pastas diferente
try:
    from MOCLexer import MOCLexer
    from MOCParser import MOCParser
    # Importa a classe VisitorTAC a ser testada
    from VisitorTAC import VisitorTAC, gerar_texto_tac
    # VisitorSemantico pode ser necessário se o TAC depender de informações coletadas por ele
    # from VisitorSemantico import VisitorSemantico
except ImportError as e:
    print(f"Erro de Importação: {e}")
    print("Certifique-se que MOCLexer, MOCParser e VisitorTAC estão acessíveis.")
    # Exemplo:
    # import sys
    # sys.path.append('../src') # Ajuste o caminho conforme necessário

# Classe de Testes para o VisitorTAC
class TestVisitorTAC(unittest.TestCase):

    def _parse_e_gera_tac(self, codigo_moc):

        input_stream = InputStream(codigo_moc)

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
            return

        # 1. Criação da Tabela de Símbolos
        tabela_de_simbolos_principal = TabelaDeSimbolos()

        try:
            semantico = VisitorSemantico(tabela_de_simbolos_principal)
            semantico.erros(tree)
        except Exception as e:
            print(e)
            print("\nErros semânticos encontrados. A abortar o processo de geração de código intermédio.")
            exit(1)

        visitor = VisitorTAC(tabela_de_simbolos_principal)
        visitor.variaveis_declaradas = set().union(*semantico.contexto) if semantico.contexto else set()
        try:
            visitor.visit(tree)
            tac_original = gerar_texto_tac(visitor.tac_quadruplos)
            tac_otimizado = otimizar_completo(visitor.tac_quadruplos)
            tac_otimizado_txt = gerar_texto_tac(tac_otimizado)
            print("TAC original:\n")
            for linha in tac_original:
                print(linha)

            print("TAC optimizado:\n")
            for linha in tac_otimizado_txt:
                print(linha)
            print("\n")
            # print(tabela_de_simbolos_principal)
            return tac_otimizado_txt
        except Exception as e:
            print(f"\nErro durante a geração do TAC: {e}")
            return



    def assertTACEqual(self, tac_resultante, tac_esperado, msg=None):
        """
        Helper para comparar duas listas de quádruplos TAC.
        """
        # Converte tudo para lista de listas para comparação mais fácil (opcional)
        tac_resultante_list = [list(q) for q in tac_resultante]
        tac_esperado_list = [list(q) for q in tac_esperado]

        self.assertListEqual(tac_resultante_list, tac_esperado_list, msg)

    # --- Testes para Geração de TAC ---

    def test_operacoes_combinadas_inteiros(self):
        codigo = """
        /* teste de optimização em operações combinadas */
        void main(void);
        void main(void) {
            int c;
            int a = 5;
            int b = 10;
            c = a + b * 2; 
            int d = b + 1;
        }
        """

        print(codigo)
        resultado_tac = self._parse_e_gera_tac(codigo)
        print ("Testa a optimização em expressões combinadas")
        print("      Ver as conversoes de tipos int->double e double->int")
        print("       O processo está a ser feito.... pode ser mais ou menos agressivo...")



# Para executar os testes a partir da linha de comando:
# python -m unittest test_semantico.py
if __name__ == '__main__':
    unittest.main()