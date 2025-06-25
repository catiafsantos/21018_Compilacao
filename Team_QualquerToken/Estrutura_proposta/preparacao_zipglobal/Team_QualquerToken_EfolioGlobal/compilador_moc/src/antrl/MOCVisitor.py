# Generated from MOC.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .MOCParser import MOCParser
else:
    from MOCParser import MOCParser

# This class defines a complete generic visitor for a parse tree produced by MOCParser.

class MOCVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by MOCParser#programa.
    def visitPrograma(self, ctx:MOCParser.ProgramaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#prototipos.
    def visitPrototipos(self, ctx:MOCParser.PrototiposContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#corpo.
    def visitCorpo(self, ctx:MOCParser.CorpoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#unidade.
    def visitUnidade(self, ctx:MOCParser.UnidadeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#prototipo.
    def visitPrototipo(self, ctx:MOCParser.PrototipoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#prototipoPrincipal.
    def visitPrototipoPrincipal(self, ctx:MOCParser.PrototipoPrincipalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#funcaoPrincipal.
    def visitFuncaoPrincipal(self, ctx:MOCParser.FuncaoPrincipalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#funcao.
    def visitFuncao(self, ctx:MOCParser.FuncaoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#parametros.
    def visitParametros(self, ctx:MOCParser.ParametrosContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#parametro.
    def visitParametro(self, ctx:MOCParser.ParametroContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#tipo.
    def visitTipo(self, ctx:MOCParser.TipoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#declaracao.
    def visitDeclaracao(self, ctx:MOCParser.DeclaracaoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#listaVariaveis.
    def visitListaVariaveis(self, ctx:MOCParser.ListaVariaveisContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#variavel.
    def visitVariavel(self, ctx:MOCParser.VariavelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#blocoArray.
    def visitBlocoArray(self, ctx:MOCParser.BlocoArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#listaValores.
    def visitListaValores(self, ctx:MOCParser.ListaValoresContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#expressao.
    def visitExpressao(self, ctx:MOCParser.ExpressaoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#ouSimples.
    def visitOuSimples(self, ctx:MOCParser.OuSimplesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#ouLogico.
    def visitOuLogico(self, ctx:MOCParser.OuLogicoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#eLogico.
    def visitELogico(self, ctx:MOCParser.ELogicoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#andSimples.
    def visitAndSimples(self, ctx:MOCParser.AndSimplesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#comparacaoSimples.
    def visitComparacaoSimples(self, ctx:MOCParser.ComparacaoSimplesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#adicao.
    def visitAdicao(self, ctx:MOCParser.AdicaoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#addSimples.
    def visitAddSimples(self, ctx:MOCParser.AddSimplesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#subtracao.
    def visitSubtracao(self, ctx:MOCParser.SubtracaoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#divisao.
    def visitDivisao(self, ctx:MOCParser.DivisaoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#mulSimples.
    def visitMulSimples(self, ctx:MOCParser.MulSimplesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#modulo.
    def visitModulo(self, ctx:MOCParser.ModuloContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#multiplicacao.
    def visitMultiplicacao(self, ctx:MOCParser.MultiplicacaoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#negacao.
    def visitNegacao(self, ctx:MOCParser.NegacaoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#unarioNegativo.
    def visitUnarioNegativo(self, ctx:MOCParser.UnarioNegativoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#unariaSimples.
    def visitUnariaSimples(self, ctx:MOCParser.UnariaSimplesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#casting.
    def visitCasting(self, ctx:MOCParser.CastingContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#castSimples.
    def visitCastSimples(self, ctx:MOCParser.CastSimplesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#parenteses.
    def visitParenteses(self, ctx:MOCParser.ParentesesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#chamadaLeitura.
    def visitChamadaLeitura(self, ctx:MOCParser.ChamadaLeituraContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#numero.
    def visitNumero(self, ctx:MOCParser.NumeroContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#numeroReal.
    def visitNumeroReal(self, ctx:MOCParser.NumeroRealContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#idComPrefixo.
    def visitIdComPrefixo(self, ctx:MOCParser.IdComPrefixoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#chamadaGenerica.
    def visitChamadaGenerica(self, ctx:MOCParser.ChamadaGenericaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#acessoVetor.
    def visitAcessoVetor(self, ctx:MOCParser.AcessoVetorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#semSufixo.
    def visitSemSufixo(self, ctx:MOCParser.SemSufixoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#argumentos.
    def visitArgumentos(self, ctx:MOCParser.ArgumentosContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#opRelacional.
    def visitOpRelacional(self, ctx:MOCParser.OpRelacionalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#chamadaFuncao.
    def visitChamadaFuncao(self, ctx:MOCParser.ChamadaFuncaoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#chamadaReads.
    def visitChamadaReads(self, ctx:MOCParser.ChamadaReadsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#bloco.
    def visitBloco(self, ctx:MOCParser.BlocoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#instrucoes.
    def visitInstrucoes(self, ctx:MOCParser.InstrucoesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#instrucao.
    def visitInstrucao(self, ctx:MOCParser.InstrucaoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#instrucaoExpressao.
    def visitInstrucaoExpressao(self, ctx:MOCParser.InstrucaoExpressaoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#instrucaoEmparelhada.
    def visitInstrucaoEmparelhada(self, ctx:MOCParser.InstrucaoEmparelhadaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#instrucaoPorEmparelhar.
    def visitInstrucaoPorEmparelhar(self, ctx:MOCParser.InstrucaoPorEmparelharContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#outraInstrucao.
    def visitOutraInstrucao(self, ctx:MOCParser.OutraInstrucaoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#instrucaoWhile.
    def visitInstrucaoWhile(self, ctx:MOCParser.InstrucaoWhileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#instrucaoFor.
    def visitInstrucaoFor(self, ctx:MOCParser.InstrucaoForContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#expressaoOuAtribuicao.
    def visitExpressaoOuAtribuicao(self, ctx:MOCParser.ExpressaoOuAtribuicaoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#instrucaoEscrita.
    def visitInstrucaoEscrita(self, ctx:MOCParser.InstrucaoEscritaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#instrucaoReturn.
    def visitInstrucaoReturn(self, ctx:MOCParser.InstrucaoReturnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#instrucaoAtribuicao.
    def visitInstrucaoAtribuicao(self, ctx:MOCParser.InstrucaoAtribuicaoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MOCParser#argumentoString.
    def visitArgumentoString(self, ctx:MOCParser.ArgumentoStringContext):
        return self.visitChildren(ctx)



del MOCParser