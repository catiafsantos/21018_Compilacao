# Generated from MOC.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .MOCParser import MOCParser
else:
    from MOCParser import MOCParser

# This class defines a complete listener for a parse tree produced by MOCParser.
class MOCListener(ParseTreeListener):

    # Enter a parse tree produced by MOCParser#programa.
    def enterPrograma(self, ctx:MOCParser.ProgramaContext):
        pass

    # Exit a parse tree produced by MOCParser#programa.
    def exitPrograma(self, ctx:MOCParser.ProgramaContext):
        pass


    # Enter a parse tree produced by MOCParser#prototipos.
    def enterPrototipos(self, ctx:MOCParser.PrototiposContext):
        pass

    # Exit a parse tree produced by MOCParser#prototipos.
    def exitPrototipos(self, ctx:MOCParser.PrototiposContext):
        pass


    # Enter a parse tree produced by MOCParser#corpo.
    def enterCorpo(self, ctx:MOCParser.CorpoContext):
        pass

    # Exit a parse tree produced by MOCParser#corpo.
    def exitCorpo(self, ctx:MOCParser.CorpoContext):
        pass


    # Enter a parse tree produced by MOCParser#unidade.
    def enterUnidade(self, ctx:MOCParser.UnidadeContext):
        pass

    # Exit a parse tree produced by MOCParser#unidade.
    def exitUnidade(self, ctx:MOCParser.UnidadeContext):
        pass


    # Enter a parse tree produced by MOCParser#prototipo.
    def enterPrototipo(self, ctx:MOCParser.PrototipoContext):
        pass

    # Exit a parse tree produced by MOCParser#prototipo.
    def exitPrototipo(self, ctx:MOCParser.PrototipoContext):
        pass


    # Enter a parse tree produced by MOCParser#prototipoPrincipal.
    def enterPrototipoPrincipal(self, ctx:MOCParser.PrototipoPrincipalContext):
        pass

    # Exit a parse tree produced by MOCParser#prototipoPrincipal.
    def exitPrototipoPrincipal(self, ctx:MOCParser.PrototipoPrincipalContext):
        pass


    # Enter a parse tree produced by MOCParser#funcaoPrincipal.
    def enterFuncaoPrincipal(self, ctx:MOCParser.FuncaoPrincipalContext):
        pass

    # Exit a parse tree produced by MOCParser#funcaoPrincipal.
    def exitFuncaoPrincipal(self, ctx:MOCParser.FuncaoPrincipalContext):
        pass


    # Enter a parse tree produced by MOCParser#funcao.
    def enterFuncao(self, ctx:MOCParser.FuncaoContext):
        pass

    # Exit a parse tree produced by MOCParser#funcao.
    def exitFuncao(self, ctx:MOCParser.FuncaoContext):
        pass


    # Enter a parse tree produced by MOCParser#parametros.
    def enterParametros(self, ctx:MOCParser.ParametrosContext):
        pass

    # Exit a parse tree produced by MOCParser#parametros.
    def exitParametros(self, ctx:MOCParser.ParametrosContext):
        pass


    # Enter a parse tree produced by MOCParser#parametro.
    def enterParametro(self, ctx:MOCParser.ParametroContext):
        pass

    # Exit a parse tree produced by MOCParser#parametro.
    def exitParametro(self, ctx:MOCParser.ParametroContext):
        pass


    # Enter a parse tree produced by MOCParser#tipo.
    def enterTipo(self, ctx:MOCParser.TipoContext):
        pass

    # Exit a parse tree produced by MOCParser#tipo.
    def exitTipo(self, ctx:MOCParser.TipoContext):
        pass


    # Enter a parse tree produced by MOCParser#declaracao.
    def enterDeclaracao(self, ctx:MOCParser.DeclaracaoContext):
        pass

    # Exit a parse tree produced by MOCParser#declaracao.
    def exitDeclaracao(self, ctx:MOCParser.DeclaracaoContext):
        pass


    # Enter a parse tree produced by MOCParser#listaVariaveis.
    def enterListaVariaveis(self, ctx:MOCParser.ListaVariaveisContext):
        pass

    # Exit a parse tree produced by MOCParser#listaVariaveis.
    def exitListaVariaveis(self, ctx:MOCParser.ListaVariaveisContext):
        pass


    # Enter a parse tree produced by MOCParser#variavel.
    def enterVariavel(self, ctx:MOCParser.VariavelContext):
        pass

    # Exit a parse tree produced by MOCParser#variavel.
    def exitVariavel(self, ctx:MOCParser.VariavelContext):
        pass


    # Enter a parse tree produced by MOCParser#blocoArray.
    def enterBlocoArray(self, ctx:MOCParser.BlocoArrayContext):
        pass

    # Exit a parse tree produced by MOCParser#blocoArray.
    def exitBlocoArray(self, ctx:MOCParser.BlocoArrayContext):
        pass


    # Enter a parse tree produced by MOCParser#listaValores.
    def enterListaValores(self, ctx:MOCParser.ListaValoresContext):
        pass

    # Exit a parse tree produced by MOCParser#listaValores.
    def exitListaValores(self, ctx:MOCParser.ListaValoresContext):
        pass


    # Enter a parse tree produced by MOCParser#expressao.
    def enterExpressao(self, ctx:MOCParser.ExpressaoContext):
        pass

    # Exit a parse tree produced by MOCParser#expressao.
    def exitExpressao(self, ctx:MOCParser.ExpressaoContext):
        pass


    # Enter a parse tree produced by MOCParser#ouSimples.
    def enterOuSimples(self, ctx:MOCParser.OuSimplesContext):
        pass

    # Exit a parse tree produced by MOCParser#ouSimples.
    def exitOuSimples(self, ctx:MOCParser.OuSimplesContext):
        pass


    # Enter a parse tree produced by MOCParser#ouLogico.
    def enterOuLogico(self, ctx:MOCParser.OuLogicoContext):
        pass

    # Exit a parse tree produced by MOCParser#ouLogico.
    def exitOuLogico(self, ctx:MOCParser.OuLogicoContext):
        pass


    # Enter a parse tree produced by MOCParser#eLogico.
    def enterELogico(self, ctx:MOCParser.ELogicoContext):
        pass

    # Exit a parse tree produced by MOCParser#eLogico.
    def exitELogico(self, ctx:MOCParser.ELogicoContext):
        pass


    # Enter a parse tree produced by MOCParser#andSimples.
    def enterAndSimples(self, ctx:MOCParser.AndSimplesContext):
        pass

    # Exit a parse tree produced by MOCParser#andSimples.
    def exitAndSimples(self, ctx:MOCParser.AndSimplesContext):
        pass


    # Enter a parse tree produced by MOCParser#comparacaoSimples.
    def enterComparacaoSimples(self, ctx:MOCParser.ComparacaoSimplesContext):
        pass

    # Exit a parse tree produced by MOCParser#comparacaoSimples.
    def exitComparacaoSimples(self, ctx:MOCParser.ComparacaoSimplesContext):
        pass


    # Enter a parse tree produced by MOCParser#adicao.
    def enterAdicao(self, ctx:MOCParser.AdicaoContext):
        pass

    # Exit a parse tree produced by MOCParser#adicao.
    def exitAdicao(self, ctx:MOCParser.AdicaoContext):
        pass


    # Enter a parse tree produced by MOCParser#addSimples.
    def enterAddSimples(self, ctx:MOCParser.AddSimplesContext):
        pass

    # Exit a parse tree produced by MOCParser#addSimples.
    def exitAddSimples(self, ctx:MOCParser.AddSimplesContext):
        pass


    # Enter a parse tree produced by MOCParser#subtracao.
    def enterSubtracao(self, ctx:MOCParser.SubtracaoContext):
        pass

    # Exit a parse tree produced by MOCParser#subtracao.
    def exitSubtracao(self, ctx:MOCParser.SubtracaoContext):
        pass


    # Enter a parse tree produced by MOCParser#divisao.
    def enterDivisao(self, ctx:MOCParser.DivisaoContext):
        pass

    # Exit a parse tree produced by MOCParser#divisao.
    def exitDivisao(self, ctx:MOCParser.DivisaoContext):
        pass


    # Enter a parse tree produced by MOCParser#mulSimples.
    def enterMulSimples(self, ctx:MOCParser.MulSimplesContext):
        pass

    # Exit a parse tree produced by MOCParser#mulSimples.
    def exitMulSimples(self, ctx:MOCParser.MulSimplesContext):
        pass


    # Enter a parse tree produced by MOCParser#modulo.
    def enterModulo(self, ctx:MOCParser.ModuloContext):
        pass

    # Exit a parse tree produced by MOCParser#modulo.
    def exitModulo(self, ctx:MOCParser.ModuloContext):
        pass


    # Enter a parse tree produced by MOCParser#multiplicacao.
    def enterMultiplicacao(self, ctx:MOCParser.MultiplicacaoContext):
        pass

    # Exit a parse tree produced by MOCParser#multiplicacao.
    def exitMultiplicacao(self, ctx:MOCParser.MultiplicacaoContext):
        pass


    # Enter a parse tree produced by MOCParser#negacao.
    def enterNegacao(self, ctx:MOCParser.NegacaoContext):
        pass

    # Exit a parse tree produced by MOCParser#negacao.
    def exitNegacao(self, ctx:MOCParser.NegacaoContext):
        pass


    # Enter a parse tree produced by MOCParser#unarioNegativo.
    def enterUnarioNegativo(self, ctx:MOCParser.UnarioNegativoContext):
        pass

    # Exit a parse tree produced by MOCParser#unarioNegativo.
    def exitUnarioNegativo(self, ctx:MOCParser.UnarioNegativoContext):
        pass


    # Enter a parse tree produced by MOCParser#unariaSimples.
    def enterUnariaSimples(self, ctx:MOCParser.UnariaSimplesContext):
        pass

    # Exit a parse tree produced by MOCParser#unariaSimples.
    def exitUnariaSimples(self, ctx:MOCParser.UnariaSimplesContext):
        pass


    # Enter a parse tree produced by MOCParser#casting.
    def enterCasting(self, ctx:MOCParser.CastingContext):
        pass

    # Exit a parse tree produced by MOCParser#casting.
    def exitCasting(self, ctx:MOCParser.CastingContext):
        pass


    # Enter a parse tree produced by MOCParser#castSimples.
    def enterCastSimples(self, ctx:MOCParser.CastSimplesContext):
        pass

    # Exit a parse tree produced by MOCParser#castSimples.
    def exitCastSimples(self, ctx:MOCParser.CastSimplesContext):
        pass


    # Enter a parse tree produced by MOCParser#parenteses.
    def enterParenteses(self, ctx:MOCParser.ParentesesContext):
        pass

    # Exit a parse tree produced by MOCParser#parenteses.
    def exitParenteses(self, ctx:MOCParser.ParentesesContext):
        pass


    # Enter a parse tree produced by MOCParser#chamadaLeitura.
    def enterChamadaLeitura(self, ctx:MOCParser.ChamadaLeituraContext):
        pass

    # Exit a parse tree produced by MOCParser#chamadaLeitura.
    def exitChamadaLeitura(self, ctx:MOCParser.ChamadaLeituraContext):
        pass


    # Enter a parse tree produced by MOCParser#numero.
    def enterNumero(self, ctx:MOCParser.NumeroContext):
        pass

    # Exit a parse tree produced by MOCParser#numero.
    def exitNumero(self, ctx:MOCParser.NumeroContext):
        pass


    # Enter a parse tree produced by MOCParser#numeroReal.
    def enterNumeroReal(self, ctx:MOCParser.NumeroRealContext):
        pass

    # Exit a parse tree produced by MOCParser#numeroReal.
    def exitNumeroReal(self, ctx:MOCParser.NumeroRealContext):
        pass


    # Enter a parse tree produced by MOCParser#idComPrefixo.
    def enterIdComPrefixo(self, ctx:MOCParser.IdComPrefixoContext):
        pass

    # Exit a parse tree produced by MOCParser#idComPrefixo.
    def exitIdComPrefixo(self, ctx:MOCParser.IdComPrefixoContext):
        pass


    # Enter a parse tree produced by MOCParser#chamadaGenerica.
    def enterChamadaGenerica(self, ctx:MOCParser.ChamadaGenericaContext):
        pass

    # Exit a parse tree produced by MOCParser#chamadaGenerica.
    def exitChamadaGenerica(self, ctx:MOCParser.ChamadaGenericaContext):
        pass


    # Enter a parse tree produced by MOCParser#acessoVetor.
    def enterAcessoVetor(self, ctx:MOCParser.AcessoVetorContext):
        pass

    # Exit a parse tree produced by MOCParser#acessoVetor.
    def exitAcessoVetor(self, ctx:MOCParser.AcessoVetorContext):
        pass


    # Enter a parse tree produced by MOCParser#semSufixo.
    def enterSemSufixo(self, ctx:MOCParser.SemSufixoContext):
        pass

    # Exit a parse tree produced by MOCParser#semSufixo.
    def exitSemSufixo(self, ctx:MOCParser.SemSufixoContext):
        pass


    # Enter a parse tree produced by MOCParser#argumentos.
    def enterArgumentos(self, ctx:MOCParser.ArgumentosContext):
        pass

    # Exit a parse tree produced by MOCParser#argumentos.
    def exitArgumentos(self, ctx:MOCParser.ArgumentosContext):
        pass


    # Enter a parse tree produced by MOCParser#opRelacional.
    def enterOpRelacional(self, ctx:MOCParser.OpRelacionalContext):
        pass

    # Exit a parse tree produced by MOCParser#opRelacional.
    def exitOpRelacional(self, ctx:MOCParser.OpRelacionalContext):
        pass


    # Enter a parse tree produced by MOCParser#chamadaFuncao.
    def enterChamadaFuncao(self, ctx:MOCParser.ChamadaFuncaoContext):
        pass

    # Exit a parse tree produced by MOCParser#chamadaFuncao.
    def exitChamadaFuncao(self, ctx:MOCParser.ChamadaFuncaoContext):
        pass


    # Enter a parse tree produced by MOCParser#chamadaReads.
    def enterChamadaReads(self, ctx:MOCParser.ChamadaReadsContext):
        pass

    # Exit a parse tree produced by MOCParser#chamadaReads.
    def exitChamadaReads(self, ctx:MOCParser.ChamadaReadsContext):
        pass


    # Enter a parse tree produced by MOCParser#bloco.
    def enterBloco(self, ctx:MOCParser.BlocoContext):
        pass

    # Exit a parse tree produced by MOCParser#bloco.
    def exitBloco(self, ctx:MOCParser.BlocoContext):
        pass


    # Enter a parse tree produced by MOCParser#instrucoes.
    def enterInstrucoes(self, ctx:MOCParser.InstrucoesContext):
        pass

    # Exit a parse tree produced by MOCParser#instrucoes.
    def exitInstrucoes(self, ctx:MOCParser.InstrucoesContext):
        pass


    # Enter a parse tree produced by MOCParser#instrucao.
    def enterInstrucao(self, ctx:MOCParser.InstrucaoContext):
        pass

    # Exit a parse tree produced by MOCParser#instrucao.
    def exitInstrucao(self, ctx:MOCParser.InstrucaoContext):
        pass


    # Enter a parse tree produced by MOCParser#instrucaoExpressao.
    def enterInstrucaoExpressao(self, ctx:MOCParser.InstrucaoExpressaoContext):
        pass

    # Exit a parse tree produced by MOCParser#instrucaoExpressao.
    def exitInstrucaoExpressao(self, ctx:MOCParser.InstrucaoExpressaoContext):
        pass


    # Enter a parse tree produced by MOCParser#instrucaoEmparelhada.
    def enterInstrucaoEmparelhada(self, ctx:MOCParser.InstrucaoEmparelhadaContext):
        pass

    # Exit a parse tree produced by MOCParser#instrucaoEmparelhada.
    def exitInstrucaoEmparelhada(self, ctx:MOCParser.InstrucaoEmparelhadaContext):
        pass


    # Enter a parse tree produced by MOCParser#instrucaoPorEmparelhar.
    def enterInstrucaoPorEmparelhar(self, ctx:MOCParser.InstrucaoPorEmparelharContext):
        pass

    # Exit a parse tree produced by MOCParser#instrucaoPorEmparelhar.
    def exitInstrucaoPorEmparelhar(self, ctx:MOCParser.InstrucaoPorEmparelharContext):
        pass


    # Enter a parse tree produced by MOCParser#outraInstrucao.
    def enterOutraInstrucao(self, ctx:MOCParser.OutraInstrucaoContext):
        pass

    # Exit a parse tree produced by MOCParser#outraInstrucao.
    def exitOutraInstrucao(self, ctx:MOCParser.OutraInstrucaoContext):
        pass


    # Enter a parse tree produced by MOCParser#instrucaoWhile.
    def enterInstrucaoWhile(self, ctx:MOCParser.InstrucaoWhileContext):
        pass

    # Exit a parse tree produced by MOCParser#instrucaoWhile.
    def exitInstrucaoWhile(self, ctx:MOCParser.InstrucaoWhileContext):
        pass


    # Enter a parse tree produced by MOCParser#instrucaoFor.
    def enterInstrucaoFor(self, ctx:MOCParser.InstrucaoForContext):
        pass

    # Exit a parse tree produced by MOCParser#instrucaoFor.
    def exitInstrucaoFor(self, ctx:MOCParser.InstrucaoForContext):
        pass


    # Enter a parse tree produced by MOCParser#expressaoOuAtribuicao.
    def enterExpressaoOuAtribuicao(self, ctx:MOCParser.ExpressaoOuAtribuicaoContext):
        pass

    # Exit a parse tree produced by MOCParser#expressaoOuAtribuicao.
    def exitExpressaoOuAtribuicao(self, ctx:MOCParser.ExpressaoOuAtribuicaoContext):
        pass


    # Enter a parse tree produced by MOCParser#instrucaoEscrita.
    def enterInstrucaoEscrita(self, ctx:MOCParser.InstrucaoEscritaContext):
        pass

    # Exit a parse tree produced by MOCParser#instrucaoEscrita.
    def exitInstrucaoEscrita(self, ctx:MOCParser.InstrucaoEscritaContext):
        pass


    # Enter a parse tree produced by MOCParser#instrucaoReturn.
    def enterInstrucaoReturn(self, ctx:MOCParser.InstrucaoReturnContext):
        pass

    # Exit a parse tree produced by MOCParser#instrucaoReturn.
    def exitInstrucaoReturn(self, ctx:MOCParser.InstrucaoReturnContext):
        pass


    # Enter a parse tree produced by MOCParser#instrucaoAtribuicao.
    def enterInstrucaoAtribuicao(self, ctx:MOCParser.InstrucaoAtribuicaoContext):
        pass

    # Exit a parse tree produced by MOCParser#instrucaoAtribuicao.
    def exitInstrucaoAtribuicao(self, ctx:MOCParser.InstrucaoAtribuicaoContext):
        pass


    # Enter a parse tree produced by MOCParser#argumentoString.
    def enterArgumentoString(self, ctx:MOCParser.ArgumentoStringContext):
        pass

    # Exit a parse tree produced by MOCParser#argumentoString.
    def exitArgumentoString(self, ctx:MOCParser.ArgumentoStringContext):
        pass



del MOCParser