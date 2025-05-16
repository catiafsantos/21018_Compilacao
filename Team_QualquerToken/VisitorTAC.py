from MOCVisitor import MOCVisitor
from TabelaSimbolos import TabelaDeSimbolos


# Classe que herda do MOCVisitor gerado pelo ANTLR e é responsável por gerar código intermédio (TAC)
class VisitorTAC(MOCVisitor):
    def __init__(self, tabela_simbolos: TabelaDeSimbolos):

        # inicializa tabela_simbolos, erros, etc.
        super().__init__()

        # Tabela de simbolos
        self.tabela_simbolos = tabela_simbolos

        # Lista onde se armazenam os quadruplos (código de três endereços) gerados
        self.tac_quadruplos = []

        # Contador de variáveis temporárias (t1, t2, ...)
        self.temp_count = 0

        # Contador de labels (L1, L2, ...) para usar em saltos e controlo de fluxo
        self.label_count = 0

        # Tabela de variáveis declaradas (para verificação semântica)
        self.variaveis_declaradas = set()

        # Conjunto de funções declaradas (para evitar redefinições)
        self.funcoes_declaradas = set()

    # Gera um novo nome de variável temporária e incrementa o contador
    def novo_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    # Gera um novo label e incrementa o contador
    def nova_label(self):
        self.label_count += 1
        return f"L{self.label_count}"

    # Adiciona um quadruplo (operação TAC) à lista
    # Se não for especificado um resultado ('res') e a operação exigir um, gera um temporário
    def adicionar_quadruplo(self, op, arg1=None, arg2=None, res=None):
        # Estas operações não precisam de campo 'res', por isso são tratadas à parte
        if res is None and op not in {
            "label", "goto", "ifgoto", "ifFalse",
            "return", "param", "call",
            "write", "writes", "writec", "writev", "alloc"
        }:
            # Gera um novo temporário para guardar o resultado da operação
            res = self.novo_temp()

        # Adiciona o quadruplo como dicionário à lista de instruções TAC
        self.tac_quadruplos.append({"op": op, "arg1": arg1, "arg2": arg2, "res": res})

        # Devolve o resultado (útil para encadear operações e continuar a gerar TAC)
        return res

    # Visita o nó 'programa' da árvore de parsing, que representa o programa inteiro
    def visitPrograma(self, ctx):
        # Guarda os nomes das funções declaradas nos protótipos
        for prot in ctx.prototipos().prototipo():
            nome = prot.IDENTIFICADOR().getText()
            self.funcoes_declaradas.add(nome)

        # Visita os protótipos de funções (declarações sem corpo)
        self.visit(ctx.prototipos())

        # Visita o corpo principal do programa (funções e função principal)
        self.visit(ctx.corpo())

    # Visita o 'corpo', que contém várias 'unidades' (funções normais) e a função principal
    def visitCorpo(self, ctx):
        # Gera TAC para cada função ou bloco de código encontrado
        for unidade in ctx.unidade():
            self.visit(unidade)

        # Por fim, gera TAC para a função principal
        self.visit(ctx.funcaoPrincipal())

    # Geração de TAC para a função principal do programa
    def visitFuncaoPrincipal(self, ctx):
        # Adiciona "main" à lista de funções declaradas (mesmo que seja redundante)
        self.funcoes_declaradas.add("main")

        # Marca o início da função principal com um label "main"
        self.adicionar_quadruplo("label", res="main")

        # Se a função principal tiver parâmetros definidos, associa cada um aos seus nomes
        if ctx.parametros():
            for i, p in enumerate(ctx.parametros().parametro()):
                if p.IDENTIFICADOR():
                    self.variaveis_declaradas.add(p.IDENTIFICADOR().getText())  # NOVO: regista como variável
                    self.adicionar_quadruplo("=", f"param{i+1}", res=p.IDENTIFICADOR().getText())

        # Visita o bloco principal da função (instruções)
        self.visit(ctx.bloco())

        # Gera o quadruplo "halt" para indicar o fim da execução do programa
        self.adicionar_quadruplo("halt")

        # Marca o fim da função principal com um label "end_main"
        self.adicionar_quadruplo("label", res="end_main")

    # Geração de TAC para uma função normal (não principal)
    def visitFuncao(self, ctx):
        # Obtém o nome da função a partir do identificador
        nome = ctx.IDENTIFICADOR().getText()
        self.funcoes_declaradas.add(nome)

        # Marca o início da função com um label com o nome da função
        self.adicionar_quadruplo("label", res=nome)

        # Associa cada parâmetro formal ao nome definido no corpo da função
        if ctx.parametros():
            for i, p in enumerate(ctx.parametros().parametro()):
                if p.IDENTIFICADOR():
                    nome_param = p.IDENTIFICADOR().getText()
                    # Atribui param1, param2, etc. aos nomes dos parâmetros declarados
                    self.adicionar_quadruplo("=", f"param{i+1}", res=p.IDENTIFICADOR().getText())
                    self.variaveis_declaradas.add(nome_param)

        # Visita o corpo da função
        self.visit(ctx.bloco())

        # Marca o fim da função com um label "end_<nome>"
        self.adicionar_quadruplo("label", res=f"end_{nome}")

    # Visita um bloco de instruções (abre e fecha chavetas)
    def visitBloco(self, ctx):
        # Visita as instruções dentro do bloco
        self.visit(ctx.instrucoes())

    # Visita todas as instruções de um bloco
    def visitInstrucoes(self, ctx):
        # Para cada instrução, aplica o visitor correspondente
        for instrucao in ctx.instrucao():
            self.visit(instrucao)

    # Encaminha a visita para o tipo concreto de instrução (if, while, atribuição, etc.)
    def visitInstrucao(self, ctx):
        return self.visitChildren(ctx)

    # Geração de TAC para instruções de atribuição (com ou sem acesso a vetor)
    def visitInstrucaoAtribuicao(self, ctx):
        # Obtém o nome da variável a ser atribuída
        nome = ctx.IDENTIFICADOR().getText()

        # Caso especial: atribuição a uma posição de vetor (ex: v[i] = ...)
        if ctx.ABRECOLCH():
            # Primeiro avalia a expressão do índice do vetor
            indice = self.visit(ctx.expressao(0))

            # Multiplica o índice por 4 (supondo 4 bytes por elemento) para obter o offset em bytes
            offset = self.adicionar_quadruplo("*", arg1=indice, arg2="4")

            # Avalia a expressão que será atribuída à posição do vetor
            valor = self.visit(ctx.expressao(1))

            # Gera um quadruplo do tipo "[]=" para representar v[offset] = valor
            self.adicionar_quadruplo("[]=", arg1=nome, arg2=offset, res=valor)
        else:
            # Atribuição simples: nome = valor
            valor = self.visit(ctx.expressao(0))

            # Gera o quadruplo de atribuição
            self.adicionar_quadruplo("=", valor, res=nome)


    # Geração de TAC para instrução 'return'
    def visitInstrucaoReturn(self, ctx):
        # Avalia a expressão de retorno e guarda o resultado
        valor = self.visit(ctx.expressao())

        # Cria o quadruplo 'return' com o valor a retornar
        self.adicionar_quadruplo("return", arg1=valor)

    # Geração de TAC para instruções de escrita (writes, write, writec, writev)
    def visitInstrucaoEscrita(self, ctx):
        if ctx.WRITES():
            # Caso seja writes("texto"), extrai o conteúdo da string
            texto = ctx.argumentoString().getText()

            # Gera o quadruplo para escrever uma string
            self.adicionar_quadruplo("writes", arg1=texto)

        elif ctx.WRITE():
            # Caso seja write(expr), avalia a expressão
            valor = self.visit(ctx.expressao())

            # Gera o quadruplo para escrever o valor numérico
            self.adicionar_quadruplo("write", arg1=valor)

        elif ctx.WRITEC():
            # Caso seja writec(expr), avalia a expressão
            valor = self.visit(ctx.expressao())

            # Gera o quadruplo para escrever o caractere correspondente
            self.adicionar_quadruplo("writec", arg1=valor)

        elif ctx.WRITEV():
            # Caso seja writev(vetor), obtém o nome do vetor
            nome = ctx.IDENTIFICADOR().getText()

            # Gera o quadruplo para imprimir todos os valores do vetor
            self.adicionar_quadruplo("writev", arg1=nome)

    # Geração de TAC para instruções que apenas avaliam expressões (por efeitos colaterais)
    def visitInstrucaoExpressao(self, ctx):
        # Avalia a expressão e guarda o resultado
        resultado = self.visit(ctx.expressao())

        # Se for uma chamada de função (resultado num temporário), gera uma atribuição "inútil"
        # para garantir que o TAC preserve a chamada mesmo que o resultado não seja usado
        if resultado and resultado.startswith("t"):
            self.adicionar_quadruplo("=", resultado)

    # Geração de TAC para estrutura de controlo 'while'
    def visitInstrucaoWhile(self, ctx):
        # Cria 3 labels: condição, corpo e fim
        L_cond = self.nova_label()
        L_body = self.nova_label()
        L_end = self.nova_label()

        # Marca o início da verificação da condição
        self.adicionar_quadruplo("label", res=L_cond)

        # Avalia a expressão condicional
        cond = self.visit(ctx.expressao())

        # Se for falsa, salta para o fim
        self.adicionar_quadruplo("ifFalse", arg1=cond, res=L_end)

        # Label para o início do corpo do loop
        self.adicionar_quadruplo("label", res=L_body)

        # Gera TAC para o corpo do loop
        self.visit(ctx.bloco())

        # No fim do corpo, volta a verificar a condição
        self.adicionar_quadruplo("goto", res=L_cond)

        # Marca o fim do ciclo
        self.adicionar_quadruplo("label", res=L_end)

    # Geração de TAC para estrutura 'if ... else' (instrução emparelhada)
    def visitInstrucaoEmparelhada(self, ctx):
        if ctx.expressao():
            # Criação dos labels para then, else e fim
            L_then = self.nova_label()
            L_else = self.nova_label()
            L_end = self.nova_label()

            # Avalia a condição
            cond = self.visit(ctx.expressao())

            # Se for falsa, vai diretamente para o ramo else
            self.adicionar_quadruplo("ifFalse", arg1=cond, res=L_else)

            # Label do bloco then
            self.adicionar_quadruplo("label", res=L_then)

            # Gera TAC para o bloco then
            self.visit(ctx.bloco())

            # Salta para o fim, ignorando o else
            self.adicionar_quadruplo("goto", res=L_end)

            # Label do bloco else
            self.adicionar_quadruplo("label", res=L_else)

            # Visita o ramo else (outra instrução emparelhada)
            self.visit(ctx.instrucaoEmparelhada())

            # Marca o fim do if-else
            self.adicionar_quadruplo("label", res=L_end)
        else:
            # Se não houver expressão condicional, trata-se de um else isolado
            self.visit(ctx.bloco())

    # Geração de TAC para 'if' sem else (instrução por emparelhar)
    def visitInstrucaoPorEmparelhar(self, ctx):
        # Criação dos labels para o bloco e para o fim
        L_then = self.nova_label()
        L_end = self.nova_label()

        # Avalia a condição
        cond = self.visit(ctx.expressao())

        # Se for falsa, salta o bloco
        self.adicionar_quadruplo("ifFalse", arg1=cond, res=L_end)

        # Label do bloco 'then'
        self.adicionar_quadruplo("label", res=L_then)

        # Gera TAC para o bloco
        self.visit(ctx.bloco())

        # Marca o fim do if
        self.adicionar_quadruplo("label", res=L_end)


     # Geração de TAC para instrução 'for'
    def visitInstrucaoFor(self, ctx):
        # Se existir uma expressão ou atribuição inicial (ex: i = 0), visita-a primeiro
        if ctx.expressaoOuAtribuicao(0):
            self.visit(ctx.expressaoOuAtribuicao(0))

        # Cria três labels: condição (inicio do loop), corpo e fim
        L_cond = self.nova_label()
        L_body = self.nova_label()
        L_end = self.nova_label()

        # Marca o início da verificação da condição
        self.adicionar_quadruplo("label", res=L_cond)

        # Se existir condição (ex: i < 10), avalia-a e gera salto condicional
        if ctx.expressao():
            cond = self.visit(ctx.expressao())
            self.adicionar_quadruplo("ifFalse", arg1=cond, res=L_end)

        # Label para o corpo do for
        self.adicionar_quadruplo("label", res=L_body)

        # Gera TAC para o corpo do loop
        self.visit(ctx.bloco())

        # Se existir passo (ex: i++ ou i = i + 1), avalia-o agora
        if ctx.expressaoOuAtribuicao(1):
            self.visit(ctx.expressaoOuAtribuicao(1))

        # Volta a verificar a condição
        self.adicionar_quadruplo("goto", res=L_cond)

        # Marca o fim do loop
        self.adicionar_quadruplo("label", res=L_end)

    # Geração de TAC para operação de adição (e1 + e2)
    def visitAdicao(self, ctx):
        # Avalia os operandos
        e1 = self.visit(ctx.expressaoAdd())
        e2 = self.visit(ctx.expressaoMul())

        # Gera quadruplo da adição e devolve o resultado (num temporário)
        return self.adicionar_quadruplo("+", e1, e2)

    # Geração de TAC para operação de subtração (e1 - e2)
    def visitSubtracao(self, ctx):
        e1 = self.visit(ctx.expressaoAdd())
        e2 = self.visit(ctx.expressaoMul())
        return self.adicionar_quadruplo("-", e1, e2)

    # Geração de TAC para operação de multiplicação (e1 * e2)
    def visitMultiplicacao(self, ctx):
        e1 = self.visit(ctx.expressaoMul())
        e2 = self.visit(ctx.expressaoUnaria())
        return self.adicionar_quadruplo("*", e1, e2)

    # Geração de TAC para operação de divisão (e1 / e2)
    def visitDivisao(self, ctx):
        e1 = self.visit(ctx.expressaoMul())
        e2 = self.visit(ctx.expressaoUnaria())
        return self.adicionar_quadruplo("/", e1, e2)

    # Geração de TAC para operação de módulo (e1 % e2)
    def visitModulo(self, ctx):
        e1 = self.visit(ctx.expressaoMul())
        e2 = self.visit(ctx.expressaoUnaria())
        return self.adicionar_quadruplo("%", e1, e2)

    # Geração de TAC para expressões relacionais (ex: a < b, a == b, etc.)
    def visitComparacaoSimples(self, ctx):
        if ctx.opRelacional():
            # Se houver operador relacional, avalia os dois lados
            e1 = self.visit(ctx.expressaoAdd(0))
            e2 = self.visit(ctx.expressaoAdd(1))

            # Extrai o operador relacional (<, <=, ==, etc.)
            op = ctx.opRelacional().getText()

            # Gera o quadruplo correspondente à operação relacional
            return self.adicionar_quadruplo(op, e1, e2)
        else:
            # Se não houver operador (ex: apenas uma expressão), devolve o valor dessa expressão
            return self.visit(ctx.expressaoAdd(0))
    # Geração de TAC para negação unária (ex: -x)
    def visitUnarioNegativo(self, ctx):
        expr = self.visit(ctx.expressaoUnaria())
        # Gera '0 - expr' para simular o sinal negativo
        return self.adicionar_quadruplo("-", "0", arg1=expr)

    # Geração de TAC para negação lógica (ex: !x)
    def visitNegacao(self, ctx):
        expr = self.visit(ctx.expressaoUnaria())
        # Gera quadruplo de negação lógica
        return self.adicionar_quadruplo("!", arg1=expr)

    # Apenas devolve o valor da expressão entre parênteses (sem TAC adicional)
    def visitParenteses(self, ctx):
        return self.visit(ctx.expressao())

    # Trata instruções que podem ser expressão ou atribuição (como parte do for)
    def visitExpressaoOuAtribuicao(self, ctx):
        if ctx.ATRIBUICAO():
            # É uma atribuição do tipo 'a = ...'
            nome = ctx.IDENTIFICADOR().getText()
            valor = self.visit(ctx.expressao())
            self.adicionar_quadruplo("=", valor, res=nome)
        else:
            # Apenas uma expressão normal (sem efeito visível)
            self.visit(ctx.expressao())

    # Converte um número inteiro literal para string e devolve (sem gerar TAC)
    def visitNumero(self, ctx):
        return ctx.NUMERO().getText()

    # Converte um número real literal para string e devolve (sem gerar TAC)
    def visitNumeroReal(self, ctx):
        return ctx.NUM_REAL().getText()

    # Visita um identificador com possível chamada ou acesso a vetor
    def visitIdComPrefixo(self, ctx):
        # Se for um identificador simples, verifica se foi declarado
        nome = ctx.IDENTIFICADOR().getText()

        if ctx.primaryRest():
            # Se houver um sufixo (ex: chamada ou acesso), processa-o
            resultado = self.visit(ctx.primaryRest())
            if resultado is not None:
                return resultado
        # Caso contrário, devolve o identificador diretamente
        return nome

    # Geração de TAC para chamadas especiais (read, reads, readc)
    def visitChamadaFuncao(self, ctx):
        temp = self.novo_temp()
        if ctx.READ():
            self.adicionar_quadruplo("call", "read", res=temp)
        elif ctx.READC():
            self.adicionar_quadruplo("call", "readc", res=temp)
        elif ctx.READS():
            self.adicionar_quadruplo("call", "reads", res=temp)
        return temp

    # Geração de TAC para chamada genérica de função (ex: f(x, y))
    def visitChamadaGenerica(self, ctx):
        nome_func = ctx.parentCtx.IDENTIFICADOR().getText()
        args = []

        # Visita cada argumento e guarda numa lista
        if ctx.argumentos():
            for expr in ctx.argumentos().expressao():
                valor = self.visit(expr)
                args.append(valor)

        # Para cada argumento, gera um quadruplo 'param'
        for a in args:
            self.adicionar_quadruplo("param", arg1=a)

        # Gera quadruplo de chamada e guarda o resultado num temporário
        resultado = self.novo_temp()
        self.adicionar_quadruplo("call", nome_func, res=resultado)
        return resultado

    # Geração de TAC para operador lógico 'ou' (||)
    def visitOuLogico(self, ctx):
        L_true = self.nova_label()
        L_end = self.nova_label()

        # Avalia a primeira parte da expressão
        op1 = self.visit(ctx.expressaoOr())
        self.adicionar_quadruplo("ifgoto", op1, res=L_true)

        # Avalia a segunda parte apenas se a primeira for falsa
        op2 = self.visit(ctx.expressaoAnd())
        self.adicionar_quadruplo("ifgoto", op2, res=L_true)

        # Se ambas forem falsas, o resultado é 0
        resultado = self.novo_temp()
        self.adicionar_quadruplo("=", "0", res=resultado)
        self.adicionar_quadruplo("goto", res=L_end)

        # Se alguma for verdadeira, o resultado é 1
        self.adicionar_quadruplo("label", res=L_true)
        self.adicionar_quadruplo("=", "1", res=resultado)
        self.adicionar_quadruplo("label", res=L_end)
        return resultado

    # Geração de TAC para operador lógico 'e' (&&)
    def visitELogico(self, ctx):
        L_false = self.nova_label()
        L_end = self.nova_label()

        # Avalia a primeira parte da expressão
        op1 = self.visit(ctx.expressaoAnd())
        self.adicionar_quadruplo("ifFalse", arg1=op1, res=L_false)

        # Avalia a segunda parte só se a primeira for verdadeira
        op2 = self.visit(ctx.expressaoEquality())
        self.adicionar_quadruplo("ifFalse", arg1=op2, res=L_false)

        # Se ambas forem verdadeiras, o resultado é 1
        resultado = self.novo_temp()
        self.adicionar_quadruplo("=", "1", res=resultado)
        self.adicionar_quadruplo("goto", res=L_end)

        # Se alguma falhar, o resultado é 0
        self.adicionar_quadruplo("label", res=L_false)
        self.adicionar_quadruplo("=", "0", res=resultado)
        self.adicionar_quadruplo("label", res=L_end)
        return resultado

    # Geração de TAC para conversão de tipos (cast)
    def visitCasting(self, ctx):
        tipo_destino = ctx.tipo().getText()
        valor_original = self.visit(ctx.castExpr())
        resultado = self.novo_temp()

        # Aplica o cast de tipo no TAC
        if tipo_destino == "int":
            self.adicionar_quadruplo("(int)", valor_original, res=resultado)
        elif tipo_destino == "double":
            self.adicionar_quadruplo("(double)", valor_original, res=resultado)
        else:
            # Se o tipo for inválido ou não precisar de cast, devolve o original
            resultado = valor_original

        return resultado


     # Trata sufixos de identificadores: chamada de função ou acesso a vetor
    def visitPrimaryRest(self, ctx):
        if ctx.chamadaGenerica():
            return self.visit(ctx.chamadaGenerica())
        elif ctx.acessoVetor():
            return self.visit(ctx.acessoVetor())
        return None  # Nenhum sufixo

    # Expressão aditiva simples (caso base sem + ou -)
    def visitAddSimples(self, ctx):
        return self.visit(ctx.expressaoMul())

    # Expressão multiplicativa simples (caso base sem * ou /)
    def visitMulSimples(self, ctx):
        return self.visit(ctx.expressaoUnaria())

    # Expressão unária simples (sem -, ! ou cast)
    def visitUnariaSimples(self, ctx):
        return self.visit(ctx.castExpr())

    # Expressão lógica OU simples (sem ||)
    def visitOuSimples(self, ctx):
        return self.visit(ctx.expressaoAnd())

    # Expressão lógica E simples (sem &&)
    def visitAndSimples(self, ctx):
        return self.visit(ctx.expressaoEquality())

    # Geração de TAC para acesso a vetor: v[i]
    def visitAcessoVetor(self, ctx):
        nome_vetor = ctx.parentCtx.IDENTIFICADOR().getText()
        indice = self.visit(ctx.expressao())

        # Calcula o offset: i * 4 (assumindo 4 bytes por elemento)
        temp_offset = self.adicionar_quadruplo("*", arg1=indice, arg2="4")

        # Lê valor de v[i] usando operador '[]'
        temp_valor = self.adicionar_quadruplo("[]", arg1=nome_vetor, arg2=temp_offset)
        return temp_valor

    # Visita uma declaração do tipo int x = ..., int v[] = ..., etc.
    def visitDeclaracao(self, ctx):
        for var in ctx.listaVariaveis().variavel():
            nome = var.IDENTIFICADOR().getText()
            self.variaveis_declaradas.add(nome)  # Regista a variável como declarada
            self.visit(var)

    # Geração de TAC para declaração individual de variável ou vetor
    def visitVariavel(self, ctx):
        nome = ctx.IDENTIFICADOR().getText()

        # Caso: int x = 2;
        if ctx.expressao():
            valor = self.visit(ctx.expressao())
            self.adicionar_quadruplo("=", valor, res=nome)

        # Caso: int v[] = {1,2,3}; ou int v[5] = {1,2};
        elif ctx.blocoArray():
            valores = self.visit(ctx.blocoArray())

            if ctx.NUMERO():  # Com tamanho explícito
                tamanho = int(ctx.NUMERO().getText())
                self.adicionar_quadruplo("alloc", arg1=nome, arg2=str(tamanho))

                for i in range(tamanho):
                    valor = valores[i] if i < len(valores) else "0"
                    offset = self.adicionar_quadruplo("*", arg1=str(i), arg2="4")
                    self.adicionar_quadruplo("[]=", arg1=nome, arg2=offset, res=valor)
            else:  # Sem tamanho explícito
                for i, valor in enumerate(valores):
                    offset = self.adicionar_quadruplo("*", arg1=str(i), arg2="4")
                    self.adicionar_quadruplo("[]=", arg1=nome, arg2=offset, res=valor)

        # Caso: int s[] = reads();
        elif ctx.chamadaReads():
            valor = self.visit(ctx.chamadaReads())
            self.adicionar_quadruplo("=", valor, res=nome)

        # Caso: int v[10];
        elif ctx.NUMERO() and not ctx.blocoArray():
            tamanho = ctx.NUMERO().getText()
            self.adicionar_quadruplo("alloc", arg1=nome, arg2=tamanho)

    # Constrói lista de valores num array (ex: {1,2,3})
    def visitBlocoArray(self, ctx):
        if ctx.listaValores():
            return [self.visit(expr) for expr in ctx.listaValores().expressao()]
        return []  # Array vazio

    # Geração de TAC para chamada a reads() que devolve um vetor
    def visitChamadaReads(self, ctx):
        temp = self.novo_temp()
        self.adicionar_quadruplo("call", "reads", res=temp)
        return temp

# Função auxiliar para gerar código TAC como texto (em forma legível)
def gerar_texto_tac(quadruplos):
    linhas = []
    for q in quadruplos:
        op = q['op']
        a1 = q.get('arg1')
        a2 = q.get('arg2')
        r  = q.get('res')

        if op == "label":
            linhas.append(f"{r}:")
        elif op == "goto":
            linhas.append(f"goto {r}")
        elif op == "ifgoto":
            linhas.append(f"if {a1} goto {r}")
        elif op == "ifFalse":
            linhas.append(f"ifFalse {a1} goto {r}")
        elif op == "call":
            linhas.append(f"{r} = call {a1}")
        elif op == "param":
            linhas.append(f"param {a1}")
        elif op == "return":
            linhas.append(f"return {a1}")
        elif op == "write":
            linhas.append(f"write {a1}")
        elif op == "writes":
            linhas.append(f"writes {a1}")
        elif op == "writec":
            linhas.append(f"writec {a1}")
        elif op == "writev":
            linhas.append(f"writev {a1}")
        elif op == "readc":
            linhas.append(f"readc {a1}")
        elif op == "reads":
            linhas.append(f"reads {a1}")
        elif op == "=":
            linhas.append(f"{r} = {a1}")
        elif op in {"(int)", "(double)"}:
            linhas.append(f"{r} = {op} {a1}")
        elif op == "[]":
            linhas.append(f"{r} = {a1}[{a2}]")
        elif op == "[]=":
            linhas.append(f"{a1}[{a2}] = {r}")
        elif op == "alloc":
            linhas.append(f"alloc {a1}, {a2}")
        elif op == "halt":
            linhas.append("halt")
        else:
            linhas.append(f"{r} = {a1} {op} {a2}")
    return linhas