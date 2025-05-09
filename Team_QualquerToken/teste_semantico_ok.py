"""

    AQUI VAMOS COLOCAR OS TESTES QUE ESTÃO OK .... ASSIM MANTEMOS NO teste_semantico.py só os que falham


    """
import unittest
from antlr4 import *
from io import StringIO

# Certifique-se que os imports funcionam a partir da localização do seu teste
# Pode precisar de ajustar o sys.path se estiver numa estrutura de pastas diferente
try:
    from MOCLexer import MOCLexer
    from MOCParser import MOCParser
    from VisitorSemantico import VisitorSemantico # Importa a classe a ser testada
except ImportError:
    print("Erro: Certifique-se que MOCLexer, MOCParser e VisitorSemantico estão acessíveis.")
    import sys
    # Exemplo: sys.path.append('../src') # Ajustar o caminho

# Classe de Testes -
class TestVisitorSemantico(unittest.TestCase):

    def _parse_e_visita(self, codigo_moc):
        """
        Função auxiliar para fazer o parse do código MOC e executar o VisitorSemantico.
        Retorna True se passar sem erros, ou a Exceção se ocorrer um erro semântico.
        """
        input_stream = InputStream(codigo_moc)
        lexer = MOCLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = MOCParser(stream)
        tree = parser.programa() # Assume 'programa' como regra inicial

        # Verifica erros sintáticos primeiro
        if parser.getNumberOfSyntaxErrors() > 0:
            # Retorna um erro específico para indicar falha no parse, não no semântico
            # Ou pode levantar uma exceção diferente
            return SyntaxError("Erro sintático detectado no código de teste.")

        visitor = VisitorSemantico()
        try:
            visitor.erros(tree)
            return True # Passou sem erros semânticos
        except Exception as e:
            return e # Retorna a exceção para análise no teste

    # --- Testes para Código Válido ---

    def test_declaracao_simples_valida(self):
        codigo = """
        void main(void);
        void main(void) {
            int x;
            double y;
        }
        """
        resultado = self._parse_e_visita(codigo)
        self.assertTrue(resultado, f"Código válido levantou erro: {resultado}")

    def test_atribuicao_valida(self):
        codigo = """
        void main(void);
        void main(void) {
            int x;
            x = 5;
        }
        """
        resultado = self._parse_e_visita(codigo)
        self.assertTrue(resultado, f"Código válido levantou erro: {resultado}")

    def test_uso_parametro_valido(self):
        codigo = """
        int func(int p);
        void main(void);

        int func(int p) {
           int y;
           y = p + 1; // Usa o parâmetro 'p'
           return y;
        }

        void main(void) {
           int z;
           z = func(10);
        }
        """
        resultado = self._parse_e_visita(codigo)
        self.assertTrue(resultado, f"Código válido levantou erro: {resultado}")

    def test_escopo_local_valido(self):
        codigo = """
        void main(void);
        void func(void);

        void func(void) {
            int x; // x local a func
            x = 1;
        }

        void main(void) {
            int x; // x local a main, diferente do de func
            x = 2;
            func();
        }
        """
        resultado = self._parse_e_visita(codigo)
        self.assertTrue(resultado, f"Código válido levantou erro: {resultado}")


    # --- Testes para Erros Semânticos ---

    def test_erro_variavel_nao_declarada_atribuicao(self):
        codigo = """
        void main(void);
        void main(void) {
            x = 5; // Erro: x não declarada
        }
        """
        resultado = self._parse_e_visita(codigo)
        self.assertIsInstance(resultado, Exception)
        self.assertIn("Variável 'x' usada antes de ser declarada", str(resultado))

    def test_erro_variavel_nao_declarada_expressao(self):
        codigo = """
        void main(void);
        void main(void) {
            int y;
            y = x + 1; // Erro: x não declarada
        }
        """
        resultado = self._parse_e_visita(codigo)
        self.assertIsInstance(resultado, Exception)
        # A mensagem pode variar dependendo de onde exatamente o erro é pego
        # (visitIdComPrefixo ou outro)
        self.assertIn("usada antes de ser declarada", str(resultado))
        self.assertIn("'x'", str(resultado))


    def test_erro_declaracao_duplicada_mesmo_escopo(self):
        codigo = """
        void main(void);
        void main(void) {
            int x;
            double x; // Erro: x já declarada neste escopo
        }
        """
        resultado = self._parse_e_visita(codigo)
        self.assertIsInstance(resultado, Exception)
        self.assertIn("Variável 'x' já foi declarada", str(resultado))



    def test_erro_funcao_nao_declarada_chamada(self):
         # Nota: A implementação atual do VisitorSemantico pode não pegar este erro
         # especificamente em visitIdComPrefixo se não distinguir bem função de var.
         # Pode precisar refinar a lógica ou a tabela de símbolos.
         codigo = """
         void main(void);
         void main(void) {
             int res;
             res = funcaoInexistente(5); // Erro: funcaoInexistente não declarada
         }
         """
         resultado = self._parse_e_visita(codigo)
         # Ajuste a asserção conforme a mensagem de erro que o seu visitor REALMENTE gera
         self.assertIsInstance(resultado, Exception)
         self.assertIn("Função 'funcaoInexistente' chamada mas não foi declarada.", str(resultado)) # Mensagem genérica atual
         self.assertIn("'funcaoInexistente'", str(resultado))


# Para executar os testes a partir da linha de comando:
# python -m unittest test_semantico.py
if __name__ == '__main__':
    unittest.main()