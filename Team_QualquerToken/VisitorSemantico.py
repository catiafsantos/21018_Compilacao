from MOCVisitor import MOCVisitor

class VisitorSemantico(MOCVisitor):
    def __init__(self):
        self.tabela_simbolos = set()  # Variáveis declaradas
        self.erros = []               # Lista de erros semânticos (opcional)

    def visitPrograma(self, ctx):
        if ctx.corpo():
            self.visit(ctx.corpo())

    def visitCorpo(self, ctx):
        for unidade in ctx.unidade():
            self.visit(unidade)
        self.visit(ctx.funcaoPrincipal())

    def visitFuncaoPrincipal(self, ctx):
        self.visit(ctx.bloco())

    def visitFuncao(self, ctx):
        self.visit(ctx.bloco())

    def visitBloco(self, ctx):
        if ctx.instrucoes():
            self.visit(ctx.instrucoes())

    def visitInstrucoes(self, ctx):
        for instr in ctx.instrucao():
            self.visit(instr)

    def visitInstrucao(self, ctx):
        if ctx.instrucaoEmparelhada():
            self.visit(ctx.instrucaoEmparelhada())
        elif ctx.instrucaoPorEmparelhar():
            self.visit(ctx.instrucaoPorEmparelhar())
        elif ctx.outraInstrucao():
            self.visit(ctx.outraInstrucao())

    def visitInstrucaoEmparelhada(self, ctx):
        if ctx.expressao():
            self.visit(ctx.expressao())
            self.visit(ctx.instrucaoEmparelhada())
        else:
            self.visit(ctx.bloco())

    def visitInstrucaoPorEmparelhar(self, ctx):
        self.visit(ctx.expressao())
        self.visit(ctx.bloco())

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

    def visitDeclaracao(self, ctx):
        for var in ctx.listaVariaveis().variavel():
            nome = var.IDENTIFICADOR().getText()
            if nome in self.tabela_simbolos:
                self.erros.append(f"Variável '{nome}' já foi declarada.")
            else:
                self.tabela_simbolos.add(nome)
            self.visit(var)

    def visitVariavel(self, ctx):
        if ctx.expressao():
            self.visit(ctx.expressao())
        elif ctx.blocoArray():
            self.visit(ctx.blocoArray())
        elif ctx.chamadaReads():
            self.visit(ctx.chamadaReads())

    def visitBlocoArray(self, ctx):
        if ctx.listaValores():
            for expr in ctx.listaValores().expressao():
                self.visit(expr)

    def visitInstrucaoAtribuicao(self, ctx):
        nome = ctx.IDENTIFICADOR().getText()
        if nome not in self.tabela_simbolos:
            self.erros.append(f"Variável '{nome}' usada antes de ser declarada.")
        self.visit(ctx.expressao(0))
        if ctx.ABRECOLCH():
            self.visit(ctx.expressao(1))

    def visitInstrucaoWhile(self, ctx):
        self.visit(ctx.expressao())
        self.visit(ctx.bloco())

    def visitInstrucaoFor(self, ctx):
        if ctx.expressaoOuAtribuicao(0):
            self.visit(ctx.expressaoOuAtribuicao(0))
        if ctx.expressao():
            self.visit(ctx.expressao())
        if ctx.expressaoOuAtribuicao(1):
            self.visit(ctx.expressaoOuAtribuicao(1))
        self.visit(ctx.bloco())

    def visitInstrucaoReturn(self, ctx):
        self.visit(ctx.expressao())

    def visitInstrucaoEscrita(self, ctx):
        if ctx.expressao():
            self.visit(ctx.expressao())

    def visitExpressaoOuAtribuicao(self, ctx):
        if ctx.expressao():
            self.visit(ctx.expressao())

    def visitExpressao(self, ctx):
        self.visitChildren(ctx)
