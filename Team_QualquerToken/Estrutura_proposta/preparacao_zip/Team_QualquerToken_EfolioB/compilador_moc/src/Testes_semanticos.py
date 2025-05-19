import unittest
from antlr4 import *
from io import StringIO

from utils.TabelaSimbolos import TabelaDeSimbolos

# Certifique-se que os imports funcionam a partir da localização do seu teste
# Pode precisar de ajustar o sys.path se estiver numa estrutura de pastas diferente
try:
    from antrl.MOCLexer import MOCLexer
    from antrl.MOCParser import MOCParser
    from VisitorSemantico import VisitorSemantico # Importa a classe a ser testada
except ImportError:
    print("Erro: Certifique-se que MOCLexer, MOCParser e VisitorSemantico estão acessíveis.")
    # Pode adicionar lógica para ajustar sys.path aqui se necessário
    import sys
    # Exemplo: sys.path.append('../src') # Ajuste o caminho

# Classe de Testes
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

        # 1. Criação da Tabela de Símbolos
        tabela_de_simbolos_principal = TabelaDeSimbolos()

        visitor = VisitorSemantico(tabela_de_simbolos_principal)
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

    def test_contexto_local_valido(self):
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


    def test_erro_vetor_nao_declarado_acesso(self):
        codigo = """
        void main(void);
        void main(void) {
            int i;
            i = meuVetor[0]; // Erro: meuVetor não declarado
        }
        """
        resultado = self._parse_e_visita(codigo)
        self.assertIsInstance(resultado, Exception)
        self.assertIn("Erro semântico", str(resultado))


    def test_erro_variavel_nao_declarada_atribuicao(self):
        codigo = """
        void main(void);
        void main(void) {
            x = 5; // Erro: x não declarada
        }
        """
        resultado = self._parse_e_visita(codigo)
        self.assertIsInstance(resultado, Exception)
        self.assertIn("Erro semântico", str(resultado))

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
        self.assertIn("Erro semântico", str(resultado))


    def test_erro_declaracao_duplicada_mesmo_contexto(self):
        codigo = """
        void main(void);
        void main(void) {
            int x;
            double x; // Erro: x já declarada neste contexto
        }
        """
        resultado = self._parse_e_visita(codigo)
        self.assertIsInstance(resultado, Exception)
        self.assertIn("Erro semântico", str(resultado))



    def test_erro_funcao_nao_declarada_chamada(self):
         codigo = """
         void main(void);
         void main(void) {
             int res;
             res = funcaoInexistente(5); // Erro: funcaoInexistente não declarada
         }
         """
         resultado = self._parse_e_visita(codigo)

         self.assertIsInstance(resultado, Exception)
         self.assertIn("Erro semântico", str(resultado))




    def test_acesso_variavel_fora_contexto(self):
        codigo = """
        void func1(void);
        void main(void);
        void func1(void) {
            int x;
            x = 10;
        }
        void main(void) {
            int y;
            y = x; // Erro: x não está no contexto de main
        }
        """
        resultado = self._parse_e_visita(codigo)

        self.assertIsInstance(resultado, Exception)
        self.assertIn("Erro semântico", str(resultado))


    def test_erro_loop_for_variavel_controle_nao_declarada(self):
        codigo = """
        void main(void);
        void main(void) {
            int soma;
            soma = 0;
            for (i = 0; i < 10; i = i + 1) { // Erro: i não declarado
                soma = soma + i;
            }
        }
        """
        resultado = self._parse_e_visita(codigo)

        self.assertIsInstance(resultado, Exception)
        self.assertIn("Erro semântico", str(resultado))

    def test_erro_loop_while_condicao_nao_declarada(self):
        codigo = """
        void main(void);
        void main(void) {
            int contador;
            contador = 0;
            while (condicao) { // Erro: condicao não declarada
                contador = contador + 1; 
            }
        }
        """
        resultado = self._parse_e_visita(codigo)
        self.assertIsInstance(resultado, Exception)
        self.assertIn("Erro semântico", str(resultado))


    def test_erro_if_condicao_nao_declarada(self):
        codigo = """
        void main(void);
        void main(void) {
            int valor;
            valor = 10;
            if (flagAtivada) { // Erro: flagAtivada não declarada
                valor = 20;
            }
        }
        """
        resultado = self._parse_e_visita(codigo)
        self.assertIsInstance(resultado, Exception)
        self.assertIn("Erro semântico", str(resultado))



    def test_codigo_sem_erros_semanticos_esperados(self):
        codigo_correto = """
        void main(void);
        void main(void) {
            int a;
            int b;
            int c;
            a = 10;
            b = 20;
            c = a + b;
            if (c > 10) {
                b = 0;
            }
        }
        """
        resultado = self._parse_e_visita(codigo_correto)
        self.assertTrue(resultado, "Esperava um resultado de sucesso (True).")




# Para executar os testes a partir da linha de comando:
# python -m unittest test_semantico.py
if __name__ == '__main__':
    unittest.main()