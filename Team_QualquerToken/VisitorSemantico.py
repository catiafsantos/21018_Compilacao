from MOCVisitor import MOCVisitor

# Classe responsável pela análise semântica do programa
class VisitorSemantico(MOCVisitor):
    def __init__(self):
        self.contexto = []             # Pilha de contexto de variáveis
        self.lista_erros = []               # Lista de mensagens de erro semântico
        self.funcoes_declaradas = set()  # Guarda os nomes de funções declaradas (prototipos + definidas)
        self.variaveis_com_erro = set()  # # Guarda os nomes de funções declaradas (prototipos + definidas)

    def erros(self, arvore):
        self.visit(arvore)
        if self.lista_erros:
            raise Exception("\n".join(self.lista_erros))

    # Visita o nó 'programa' (nó raiz da árvore)
    def visitPrograma(self, ctx):
        if ctx.prototipos():
            self.visit(ctx.prototipos())
        if ctx.corpo():
            self.visit(ctx.corpo())

    # Visita o corpo principal do programa (funções + função principal)
    def visitCorpo(self, ctx):
        for unidade in ctx.unidade():
            self.visit(unidade)
        self.visit(ctx.funcaoPrincipal())

    # Visita a função principal
    def visitFuncaoPrincipal(self, ctx):
        self.contexto.append(set())  # Cria um novo contexto para toda a função principal

        if ctx.parametros():
            for p in ctx.parametros().parametro():
                if p.IDENTIFICADOR():
                    nome = p.IDENTIFICADOR().getText()
                    if nome in self.contexto[-1]:
                        self.lista_erros.append(f"[Erro semântico] Parâmetro '{nome}' já foi declarado.")
                    self.contexto[-1].add(nome)  # Adiciona o parâmetro ao contexto

        self.visitBloco(ctx.bloco(), novo_contexto=False)  # NÃO cria novo contexto aqui

        self.contexto.pop()  # Sai do contexto após a função terminar

    # Visita uma função comum (não principal)
    def visitFuncao(self, ctx):
        self.contexto.append(set())  # Cria um novo contexto para corpo + parâmetros

        if ctx.parametros():
            for p in ctx.parametros().parametro():
                if p.IDENTIFICADOR():
                    nome = p.IDENTIFICADOR().getText()
                    if nome in self.contexto[-1]:
                        self.lista_erros.append(f"[Erro semântico] Parâmetro '{nome}' já foi declarado.")
                    self.contexto[-1].add(nome)

        self.visitBloco(ctx.bloco(), novo_contexto=False)  # NÃO cria novo contexto aqui

        self.contexto.pop()

    # Visita um bloco de código entre chavetas
    def visitBloco(self, ctx, novo_contexto=True):
       if novo_contexto:
           self.contexto.append(set())  # Novo contexto local (ex: dentro de if/while)

       if ctx.instrucoes():
           self.visit(ctx.instrucoes())

       if novo_contexto:
           self.contexto.pop()  # Fim do contexto local

    # Visita todas as instruções dentro de um bloco
    def visitInstrucoes(self, ctx):
        for instr in ctx.instrucao():
            self.visit(instr)

    # Encaminha a visita para o tipo de instrução correto
    def visitInstrucao(self, ctx):
        if ctx.instrucaoEmparelhada():
            self.visit(ctx.instrucaoEmparelhada())
        elif ctx.instrucaoPorEmparelhar():
            self.visit(ctx.instrucaoPorEmparelhar())
        elif ctx.outraInstrucao():
            self.visit(ctx.outraInstrucao())

    # Visita uma instrução 'if...else'
    def visitInstrucaoEmparelhada(self, ctx):
        if ctx.expressao():
            self.visit(ctx.expressao())               # Verifica a condição
            self.visit(ctx.instrucaoEmparelhada())    # Verifica os blocos if/else
        else:
            self.visit(ctx.bloco())                   # Apenas bloco else

    # Visita uma instrução 'if' sem 'else'
    def visitInstrucaoPorEmparelhar(self, ctx):
        self.visit(ctx.expressao())  # Verifica a condição
        self.visit(ctx.bloco())      # Verifica o bloco 'then'

    # Trata instruções genéricas
    def visitOutraInstrucao(self, ctx):
        if ctx.declaracao():
            self.visit(ctx.declaracao())
        elif ctx.instrucaoAtribuicao():
            self.visit(ctx.instrucaoAtribuicao())
        elif ctx.bloco():
            self.visit(ctx.bloco())
        elif ctx.instrucaoWhile():
            self.visit(ctx.instrucaoWhile())
        elif ctx.instrucaoFor():
            self.visit(ctx.instrucaoFor())
        elif ctx.instrucaoReturn():
            self.visit(ctx.instrucaoReturn())
        elif ctx.instrucaoEscrita():
            self.visit(ctx.instrucaoEscrita())

    # Visita uma declaração de variáveis
    def visitDeclaracao(self, ctx):
        for var in ctx.listaVariaveis().variavel():
            nome = var.IDENTIFICADOR().getText()
            if nome in self.contexto[-1]:
               self.lista_erros.append(f"[Erro semântico] Variável '{nome}' já foi declarada.")
            else:
                self.contexto[-1].add(nome)
            self.visit(var)  # Visita a possível inicialização

    # Visita uma Variável dentro de uma declaração (com ou sem inicialização)
    def visitVariavel(self, ctx):
        if ctx.expressao():
            self.visit(ctx.expressao())
        elif ctx.blocoArray():
            self.visit(ctx.blocoArray())
        elif ctx.chamadaReads():
            self.visit(ctx.chamadaReads())

    # Visita um bloco de inicialização de Vetor (ex: {1,2,3})
    def visitBlocoArray(self, ctx):
        if ctx.listaValores():
            for expr in ctx.listaValores().expressao():
                self.visit(expr)

    # Verifica se a Variável usada numa atribuição foi declarada
    def visitInstrucaoAtribuicao(self, ctx):
        nome = ctx.IDENTIFICADOR().getText()
        if not any(nome in contexto for contexto in reversed(self.contexto)):
           self.lista_erros.append(f"[Erro semântico] Variável '{nome}' usada antes de ser declarada.")
        self.visit(ctx.expressao(0))  # Valor atribuído
        if ctx.ABRECOLCH():
            self.visit(ctx.expressao(1))  # Índice, se for acesso a Vetor

    # Visita uma instrução 'while'
    def visitInstrucaoWhile(self, ctx):
        self.visit(ctx.expressao())  # Condição
        self.visit(ctx.bloco())      # Corpo do ciclo

    # Visita uma instrução 'for'
    def visitInstrucaoFor(self, ctx):
        if ctx.expressaoOuAtribuicao(0):
            self.visit(ctx.expressaoOuAtribuicao(0))  # Inicialização
        if ctx.expressao():
            self.visit(ctx.expressao())               # Condição
        if ctx.expressaoOuAtribuicao(1):
            self.visit(ctx.expressaoOuAtribuicao(1))  # Passo
        self.visit(ctx.bloco())                       # Corpo do ciclo

    # Visita uma instrução 'return'
    def visitInstrucaoReturn(self, ctx):
        self.visit(ctx.expressao())

    # Visita uma instrução de escrita (write, writec, etc.)
    def visitInstrucaoEscrita(self, ctx):
        if ctx.expressao():
            self.visit(ctx.expressao())
        elif ctx.WRITEV():
            nome = ctx.IDENTIFICADOR().getText()
            if not any(nome in contexto for contexto in reversed(self.contexto)):
               self.lista_erros.append(f"[Erro semântico] Vetor '{nome}' usado antes de ser declarado.")

    # Visita expressões usadas isoladamente ou em atribuições
    def visitExpressaoOuAtribuicao(self, ctx):
        if ctx.expressao():
            self.visit(ctx.expressao())

    # Encaminha a visita da expressão para os filhos
    def visitExpressao(self, ctx):
        self.visitChildren(ctx)

    def visitIdComPrefixo(self, ctx):
        nome = ctx.IDENTIFICADOR().getText()
        resto = ctx.primaryRest()
    
        # Tem sufixo? Pode ser chamada ou acesso a vetor
        if resto and resto.getChildCount() > 0:
            primeiro = resto.getChild(0).getText()

            if primeiro == "(":  # chamada a função
                if nome not in self.funcoes_declaradas and nome not in self.variaveis_com_erro:
                    self.lista_erros.append(f"[Erro semântico] Função '{nome}' chamada mas não foi declarada.")
                    self.variaveis_com_erro.add(nome)
                # Visitamos todos os argumentos (se houver)
                if resto.getChildCount() > 2:  # Há algo entre parênteses
                    argumentos = resto.getChild(1)
                    if hasattr(argumentos, "expressao"):
                        for expr in argumentos.expressao():
                            self.visit(expr)
                return

            elif primeiro == "[":  # acesso a vetor
                self.visit(resto.expressao())  # visitar o índice
                return

        # Caso contrário: é apenas uma variável isolada
        if nome not in self.funcoes_declaradas and not any(nome in contexto for contexto in reversed(self.contexto)):
            if nome not in self.variaveis_com_erro:
                self.lista_erros.append(f"[Erro semântico] Variável '{nome}' usada antes de ser declarada.")
                self.variaveis_com_erro.add(nome)


    def visitChamadaFuncao(self, ctx):
        pass  # Funções built-in como read(), readc(), reads() não precisam de validação aqui

    def visitChamadaReads(self, ctx):
        pass

    def visitAcessoVetor(self, ctx):
        nome = ctx.IDENTIFICADOR().getText()
        if not any(nome in contexto for contexto in reversed(self.contexto)):
           self.lista_erros.append(f"[Erro semântico] Vetor '{nome}' usado antes de ser declarado.")
        self.visit(ctx.expressao())  # Verifica o índice

    # Visita um protótipo de função e regista o nome
    def visitPrototipo(self, ctx):
        nome = ctx.IDENTIFICADOR().getText()
        self.funcoes_declaradas.add(nome)

    # Visita o protótipo da função principal (main)
    def visitPrototipoPrincipal(self, ctx):
        self.funcoes_declaradas.add("main")