from antlr4 import ParseTreeVisitor

class MOCVisitor(ParseTreeVisitor):
    def __init__(self):
        # Memória para armazenar as variáveis e os seus valores
        self.memory = {}
        self.prototipos = {}

    # Visita o programa principal e comeca pela funcao main
    def visitPrograma(self, ctx):
        print("[DEBUG] Entrou em visitPrograma")
        for unidade in ctx.unidade():
            self.visit(unidade)  # Regista todas as funcoes
        return self.visit(ctx.funcaoPrincipal())

    # Visita o corpo da funcao main (bloco de instrucoes)
    def visitFuncaoPrincipal(self, ctx):
        print("[DEBUG] Entrou em visitFuncaoPrincipal")
        return self.visit(ctx.bloco())

    # Visita o bloco e entra nas instrucoes contidas
    def visitBloco(self, ctx):
        print("[DEBUG] Entrou em visitBloco")
        return self.visit(ctx.instrucoes())

    # Percorre todas as instrucoes dentro de um bloco
    def visitInstrucoes(self, ctx):
        print("[DEBUG] Entrou em visitInstrucoes")
        for instr in ctx.instrucao():
            resultado = self.visit(instr)
            # Só termina cedo se for um return explícito
            if hasattr(instr, "instrucaoReturn") and instr.instrucaoReturn():
                print("[DEBUG] Return encontrado nas instrucoes")
                return resultado
            
    # Determina o tipo de instrucao (emparelhada ou por emparelhar)
    def visitInstrucao(self, ctx):
        print("[DEBUG] Entrou em visitInstrucao")
        if ctx.instrucaoEmparelhada():
            return self.visit(ctx.instrucaoEmparelhada())
        elif ctx.instrucaoPorEmparelhar():
            return self.visit(ctx.instrucaoPorEmparelhar())

    # Trata instrucoes emparelhadas (como if-else com ambos os blocos)
    def visitInstrucaoEmparelhada(self, ctx):
        print("[DEBUG] Entrou em visitInstrucaoEmparelhada")
        if ctx.outraInstrucao():
            return self.visit(ctx.outraInstrucao())
        else:
            cond = self.visit(ctx.expressao())
            if cond:
                return self.visit(ctx.instrucaoEmparelhada(0))
            else:
                return self.visit(ctx.instrucaoEmparelhada(1))

    # Trata instrucoes por emparelhar (como if sozinho ou else pendente)
    def visitInstrucaoPorEmparelhar(self, ctx):
        print("[DEBUG] Entrou em visitInstrucaoPorEmparelhar")
        cond = self.visit(ctx.expressao())
        if cond:
            return self.visit(ctx.instrucao())
        elif ctx.instrucaoEmparelhada():
            return self.visit(ctx.instrucaoEmparelhada())
        else:
            return self.visit(ctx.instrucaoPorEmparelhar())

    # Trata instrucoes normais (declaracoes, atribuicoes, ciclos, etc.)
    def visitOutraInstrucao(self, ctx):
        print(f"[DEBUG] Entrou em visitOutraInstrucao: {ctx.getText()}")

        if ctx.instrucaoEscrita():
            print("[DEBUG] Detectada instrucao de escrita")
            return self.visit(ctx.instrucaoEscrita())

        elif ctx.instrucaoAtribuicao():
            print("[DEBUG] Detectada instrucao de atribuicao")
            return self.visit(ctx.instrucaoAtribuicao())

        elif ctx.declaracao():
            print("[DEBUG] Detectada instrucao de declaracao")
            return self.visit(ctx.declaracao())

        elif ctx.bloco():
            print("[DEBUG] Detectado bloco de instrucoes")
            return self.visit(ctx.bloco())

        elif ctx.instrucaoWhile():
            print("[DEBUG] Detectado ciclo while")
            return self.visit(ctx.instrucaoWhile())

        elif ctx.instrucaoFor():
            print("[DEBUG] Detectado ciclo for")
            return self.visit(ctx.instrucaoFor())

        elif ctx.instrucaoReturn():
            print("[DEBUG] Detectada instrucao de retorno")
            return self.visit(ctx.instrucaoReturn())  # <- importante para retorno
        
    # Trata diferentes tipos de instrucao de escrita: write, writec, writev, writes
    def visitInstrucaoEscrita(self, ctx):
        print(f"[DEBUG] Entrou em visitInstrucaoEscrita: {ctx.getText()}")

        if ctx.getChild(0).getText() == 'write':
            valor = self.visit(ctx.expressao())
            if valor is None:
                print("[DEBUG] Aviso: valor retornado pelo write é None!")
            else:
                print(f"[DEBUG] write: {valor}")
            print(valor)
            return valor

        elif ctx.getChild(0).getText() == 'writec':
            valor = self.visit(ctx.expressao())
            print(f"[DEBUG] writec: ASCII({valor}) -> {chr(valor)}")
            print(chr(valor))
            return valor

        elif ctx.getChild(0).getText() == 'writev':
            nome = ctx.IDENTIFICADOR().getText()
            print(f"[DEBUG] writev: nome do vetor = {nome}")
            if nome not in self.memory:
                raise Exception(f"[Erro de Execucao] Vetor '{nome}' nao declarado.")
            vetor = self.memory[nome]
            if not isinstance(vetor, list):
                raise Exception(f"[Erro de Execucao] '{nome}' nao é um vetor.")
            print(f"[DEBUG] Conteúdo de {nome}: {vetor}")
            print("{" + ",".join(map(str, vetor)) + "}")
            return vetor

        elif ctx.getChild(0).getText() == 'writes':
            arg = ctx.argumentoString()
            if arg.IDENTIFICADOR():
                nome = arg.IDENTIFICADOR().getText()
                print(f"[DEBUG] writes com variável string: {nome}")
                if nome not in self.memory:
                    raise Exception(f"[Erro de Execucao] String '{nome}' nao declarada.")
                vetor = self.memory[nome]
                if not isinstance(vetor, list):
                    raise Exception(f"[Erro de Execucao] '{nome}' nao é uma string.")
                string_final = "".join(chr(c) for c in vetor if c != 0)
                print(f"[DEBUG] Conteúdo convertido: {string_final}")
                print(string_final)
                return vetor
            elif arg.STRINGLITERAL():
                texto = arg.STRINGLITERAL().getText()[1:-1]
                print(f"[DEBUG] writes literal: {texto}")
                print(texto)
                return texto

    # Trata atribuicoes simples: x = expr;
    def visitInstrucaoAtribuicao(self, ctx):
        print("[DEBUG] Entrou em visitInstrucaoAtribuicao")

        val = self.visit(ctx.expressao(0))
        print(f"[DEBUG] Valor atribuído = {val}")

        if ctx.ABRECOLCH():
            nome = ctx.IDENTIFICADOR().getText()
            indice = self.visit(ctx.expressao(1))
            print(f"[DEBUG] Atribuicao ao vetor: {nome}[{indice}] = {val}")
            if nome not in self.memory or not isinstance(self.memory[nome], list):
                raise Exception(f"[Erro de Execucao] Vetor '{nome}' nao declarado ou inválido.")
            self.memory[nome][indice] = val
            return val
        else:
            nome = ctx.IDENTIFICADOR().getText()
            print(f"[DEBUG] Atribuicao à variável: {nome} = {val}")
            print(f"[DEBUG] Antes: {nome} = {self.memory.get(nome)}")
            self.memory[nome] = val
            print(f"[DEBUG] Depois: {nome} = {val}")
            return val

    # Trata o ciclo while: while (condicao) { bloco }
    def visitInstrucaoWhile(self, ctx):
        print("[DEBUG] Entrou em visitInstrucaoWhile")
        while True:
            cond = self.visit(ctx.expressao())
            print(f"[DEBUG] Avaliacao da condicao do while: {cond}")
            if not cond:
                print("[DEBUG] Condicao falsa — a sair do while")
                break
            print("[DEBUG] Executando corpo do while")
            self.visit(ctx.bloco())

    # Trata declaracoes de variáveis: int x = 3;
    def visitDeclaracao(self, ctx):
        tipo = ctx.tipo().getText()
        for var_ctx in ctx.listaVariaveis().variavel():
            var = var_ctx.IDENTIFICADOR().getText()

            if var in self.memory:
                raise Exception(f"[Erro de Execucao] Variável '{var}' já foi declarada.")

            # v[] = {1, 2, 3}
            if var_ctx.blocoArray():
                lista = self.visit(var_ctx.blocoArray())
                self.memory[var] = lista
                print(f"[DEBUG] Vetor '{var}' inicializado com: {lista}")  # <- DEBUG AQUI

            # v[] = reads();
            elif var_ctx.expressao():
                val = self.visit(var_ctx.expressao())
                self.memory[var] = val

            # v; (sem valor)
            else:
                self.memory[var] = 0 if tipo == 'int' else 0.0

    # Trata expressoes com adicao: expr + expr
    def visitAdicao(self, ctx):
        left = self.visit(ctx.expressao(0))
        right = self.visit(ctx.expressao(1))
        resultado = left + right
        print(f"[DEBUG] Adicao: {left} + {right} = {resultado}")
        return resultado
        # To do : Validar se os operandos sao de tipos compatíveis.

    # Trata expressoes com subtracao: expr - expr
    def visitSubtracao(self, ctx):
        left = self.visit(ctx.expressao(0))
        right = self.visit(ctx.expressao(1))
        resultado = left - right
        print(f"[DEBUG] Subtracao: {left} - {right} = {resultado}")
        return resultado
        # To do : Validar se os operandos sao de tipos compatíveis.
    
    # Trata expressoes com multiplicacao: expr * expr
    def visitMultiplicacao(self, ctx):
        left = self.visit(ctx.expressao(0))
        right = self.visit(ctx.expressao(1))
        resultado = left * right
        print(f"[DEBUG] Multiplicacao: {left} * {right} = {resultado}")
        return resultado
        # To do : Validar se os operandos sao de tipos compatíveis.

    # Trata expressoes com divisao: expr / expr
    def visitDivisao(self, ctx):
        left = self.visit(ctx.expressao(0))
        right = self.visit(ctx.expressao(1))
        resultado = left / right
        print(f"[DEBUG] Divisao: {left} / {right} = {resultado}")
        return resultado
        # To do : Validar se os operandos sao de tipos compatíveis + validar divisao por zero

    # Trata números literais: 123
    def visitNumero(self, ctx):
        valor = int(ctx.NUMERO().getText())
        print(f"[DEBUG] Número literal: {valor}")
        return valor

    # Trata variáveis usadas em expressoes: x, y, etc.
    def visitVariavelID(self, ctx):
        nome = ctx.IDENTIFICADOR().getText()
        if nome in self.memory:
            valor = self.memory[nome]
            print(f"[DEBUG] Variável lida: {nome} = {valor}")
            return valor
        else:
            raise Exception(f"[Erro de Execucao] Variável '{nome}' nao declarada")

    # Trata expressoes entre parênteses: (expr)
    def visitParnteses(self, ctx):
        print(f"[DEBUG] Parênteses: ({ctx.getText()})")
        return self.visit(ctx.expressao())

    # Trata operacoes de casting: (int) x ou (double) x
    def visitCasting(self, ctx):
        tipo = ctx.tipo().getText()
        valor = self.visit(ctx.expressao())
        print(f"[DEBUG] Casting: ({tipo}) {valor}")

        if tipo == 'int':
            return int(valor)
        elif tipo == 'double':
            return float(valor)
        else:
            raise Exception(f"[Erro de Execucao] Tipo de cast desconhecido: {tipo}")

    # Trata números reais: 1.23
    def visitNumeroReal(self, ctx):
        valor = float(ctx.NUM_REAL().getText())
        print(f"[DEBUG] Número real: {valor}")
        return valor

    # Trata a instrucao de retorno: return expr;
    def visitInstrucaoReturn(self, ctx):
        valor = self.visit(ctx.expressao())
        print(f"[DEBUG] Return: {valor}")
        return valor

    # Trata chamadas de leitura: read(), readc(), reads()
    def visitChamadaLeitura(self, ctx):
        func = ctx.getText()
        print(f"[DEBUG] Entrou em visitChamadaLeitura: {func}")
        entrada = input("Introduz valor: ")

        if func == "read()":
            try:
                valor = int(entrada) if '.' not in entrada else float(entrada)
                print(f"[DEBUG] Leitura com read(): {valor}")
                return valor
            except ValueError:
                raise Exception("[Erro de Execucao] Valor inválido para read()")

        elif func == "readc()":
            if len(entrada) == 1:
                valor = ord(entrada[0])
                print(f"[DEBUG] Leitura com readc(): '{entrada[0]}' -> {valor}")
                return valor
            else:
                raise Exception("[Erro de Execucao] readc() espera apenas um único caráter.")

        elif func == "reads()":
            ascii_codes = [ord(char) for char in entrada] + [0]  # termina com 0
            print(f"[DEBUG] Leitura com reads(): {entrada} -> {ascii_codes}")
            return ascii_codes


    # Trata blocos de inicializacao de vetores: {1, 2, 3}
    def visitBlocoArray(self, ctx):
        if ctx.listaValores():
            lista = [self.visit(expr) for expr in ctx.listaValores().expressao()]
            print(f"[DEBUG] Bloco array inicializado com: {lista}")
            return lista
        else:
            print("[DEBUG] Bloco array vazio")
            return []

    # Acesso a elementos de vetores: v[i]
    def visitAcessoVetor(self, ctx):
        nome = ctx.IDENTIFICADOR().getText()
        indice = self.visit(ctx.expressao())
        print(f"[DEBUG] A tentar aceder a {nome}[{indice}]")

        if nome not in self.memory:
            raise Exception(f"[Erro de Execucao] Vetor '{nome}' nao declarado.")

        vetor = self.memory[nome]
        if not isinstance(vetor, list):
            raise Exception(f"[Erro de Execucao] '{nome}' nao é um vetor.")

        if indice < 0 or indice >= len(vetor):
            raise Exception(f"[Erro de Execucao] Índice fora dos limites do vetor '{nome}'.")

        print(f"[DEBUG] Acesso a {nome}[{indice}] = {vetor[indice]}")
        return vetor[indice]

    # Trata o ciclo for: for (...) { bloco }
    def visitInstrucaoFor(self, ctx):
        print("[DEBUG] A entrar no ciclo for")

        # Inicializacao
        if ctx.expressaoOuAtribuicao(0):
            print("[DEBUG] Inicializacao do for")
            self.visit(ctx.expressaoOuAtribuicao(0))

        # Condicao e incremento
        while True:
            cond = True
            if ctx.expressao():
                cond = self.visit(ctx.expressao())
                print(f"[DEBUG] Condicao do for: {cond}")
            if not cond:
                print("[DEBUG] Condicao do for falhou, sair do ciclo")
                break

            print("[DEBUG] Execucao do corpo do for")
            self.visit(ctx.bloco())

            if ctx.expressaoOuAtribuicao(1):
                print("[DEBUG] Incremento do for")
                self.visit(ctx.expressaoOuAtribuicao(1))

    # Trata a unidade de compilacao (declaracoes de funcoes e protótipos)
    def visitUnidade(self, ctx):
        print("[DEBUG] Entrou em visitUnidade")
        return self.visitChildren(ctx)

    # Trata protótipos de funcoes normais: int f(int x);
    def visitPrototipo(self, ctx):
        print("[DEBUG] Entrou em visitPrototipo")
        return self.visitChildren(ctx)

    # Trata protótipo da funcao principal: void main(void);
    def visitPrototipoPrincipal(self, ctx):
        print("[DEBUG] Entrou em visitPrototipoPrincipal")
        return self.visitChildren(ctx)

    # Guarda a definicao de uma funcao para posterior chamada
    def visitFuncao(self, ctx):
        nome = ctx.IDENTIFICADOR().getText()
        print(f"[DEBUG] Guardou funcao: {nome}")
        self.prototipos[nome] = ctx  # Guarda o nó da funcao para posterior execucao
        return None  # Nao executa a funcao agora

    # Trata a lista de parâmetros de uma funcao
    def visitParametros(self, ctx):
        print("[DEBUG] Entrou em visitParametros")
        return self.visitChildren(ctx)

    # Trata um parâmetro individual de uma funcao
    def visitParametro(self, ctx):
        print("[DEBUG] Entrou em visitParametro")
        return self.visitChildren(ctx)

    # Trata o tipo de dados: int ou double
    def visitTipo(self, ctx):
        print("[DEBUG] Entrou em visitTipo")
        return self.visitChildren(ctx)

    # Trata uma lista de variáveis numa declaracao
    def visitListaVariaveis(self, ctx):
        print("[DEBUG] Entrou em visitListaVariaveis")
        return self.visitChildren(ctx)

    # Trata uma variável individual numa declaracao
    def visitVariavel(self, ctx):
        print("[DEBUG] Entrou em visitVariavel")
        return self.visitChildren(ctx)

    # Trata uma lista de valores dentro de uma declaracao de vetor
    def visitListaValores(self, ctx):
        print("[DEBUG] Entrou em visitListaValores")
        return self.visitChildren(ctx)

    # Trata expressao lógica OU: expr || expr
    def visitOuLogico(self, ctx):
        print("[DEBUG] Entrou em visitOuLogico")
        left = self.visit(ctx.expressao(0))
        right = self.visit(ctx.expressao(1))
        resultado = left or right
        print(f"[DEBUG] Ou Lógico: {left} || {right} = {resultado}")
        return resultado

    # Trata operacao de módulo: expr % expr
    def visitModulo(self, ctx):
        print("[DEBUG] Entrou em visitModulo")
        left = self.visit(ctx.expressao(0))
        right = self.visit(ctx.expressao(1))
        resultado = left % right
        print(f"[DEBUG] Módulo: {left} % {right} = {resultado}")
        return resultado

    # Trata comparacoes relacionais: ==, !=, <, <=, >, >=
    def visitComparacao(self, ctx):
        print("[DEBUG] Entrou em visitComparacao")
        left = self.visit(ctx.expressao(0))
        right = self.visit(ctx.expressao(1))
        op = ctx.opRelacional().getText()

        resultado = {
            '==': left == right,
            '!=': left != right,
            '<': left < right,
            '<=': left <= right,
            '>': left > right,
            '>=': left >= right
        }.get(op)

        if resultado is None:
            raise Exception(f"[Erro de Execucao] Operador relacional desconhecido: {op}")

        print(f"[DEBUG] Comparacao: {left} {op} {right} = {resultado}")
        return resultado

    # Trata chamadas a funcoes definidas pelo utilizador
    def visitChamadaGenerica(self, ctx):
        nome_funcao = ctx.IDENTIFICADOR().getText()
        argumentos_ctx = ctx.argumentos()

        print(f"[DEBUG] Chamada à funcao: {nome_funcao}")

        if nome_funcao not in self.prototipos:
            raise Exception(f"[Erro de Execucao] Funcao '{nome_funcao}' nao encontrada.")

        funcao_ctx = self.prototipos[nome_funcao]

        # Preparar lista de argumentos
        argumentos = []
        if argumentos_ctx:
            for expr in argumentos_ctx.expressao():
                argumentos.append(self.visit(expr))

        # Validar número de parâmetros
        parametros_ctx = funcao_ctx.parametros().parametro()
        if len(argumentos) != len(parametros_ctx):
            raise Exception(f"[Erro de Execucao] Número incorreto de argumentos na chamada '{nome_funcao}'")

        # Guardar estado anterior da memória
        memoria_anterior = self.memory.copy()

        # Criar novo ambiente local para execucao da funcao
        self.memory = {}

        for i in range(len(argumentos)):
            nome_param = parametros_ctx[i].IDENTIFICADOR().getText()
            self.memory[nome_param] = argumentos[i]
            print(f"[DEBUG] Parâmetro: {nome_param} = {argumentos[i]}")

        # Executar corpo da funcao
        resultado = self.visit(funcao_ctx.bloco())

        # Restaurar memória original
        self.memory = memoria_anterior

        return resultado

    # Trata a negacao lógica: !expr
    def visitNegacao(self, ctx):
        print("[DEBUG] Entrou em visitNegacao")
        valor = self.visit(ctx.expressao())
        resultado = not valor
        print(f"[DEBUG] Negacao: !{valor} = {resultado}")
        return resultado

    # Trata o operador lógico E: expr && expr
    def visitELogico(self, ctx):
        print("[DEBUG] Entrou em visitELogico")
        left = self.visit(ctx.expressao(0))
        right = self.visit(ctx.expressao(1))
        resultado = left and right
        print(f"[DEBUG] E Lógico: {left} && {right} = {resultado}")
        return resultado

    # Visita os argumentos passados a uma funcao (delegado para os filhos)
    def visitArgumentos(self, ctx):
        print("[DEBUG] Entrou em visitArgumentos")
        return self.visitChildren(ctx)

    # Visita operadores relacionais auxiliares (geralmente usados na gramática)
    def visitOpRelacional(self, ctx):
        print("[DEBUG] Entrou em visitOpRelacional")
        return self.visitChildren(ctx)

    # Encaminha chamadas de funcao para a implementacao genérica
    def visitChamadaFuncao(self, ctx):
        print("[DEBUG] Entrou em visitChamadaFuncao")
        return self.visitChamadaGenerica(ctx.chamadaGenerica())

    # Trata expressoes que podem ser também atribuicoes
    def visitExpressaoOuAtribuicao(self, ctx):
        print("[DEBUG] Entrou em visitExpressaoOuAtribuicao")
        if ctx.ATRIBUICAO():
            nome = ctx.IDENTIFICADOR().getText()
            valor = self.visit(ctx.expressao())
            print(f"[DEBUG] Atribuicao (em for): {nome} = {valor}")
            self.memory[nome] = valor
            return valor
        else:
            return self.visit(ctx.expressao())
    
    # Visita argumentos de string (IDENTIFICADOR ou STRINGLITERAL)
    def visitArgumentoString(self, ctx):
        print("[DEBUG] Entrou em visitArgumentoString")
        return self.visitChildren(ctx)