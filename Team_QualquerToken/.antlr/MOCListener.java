// Generated from /Users/catiasantos/Documents/Code/CP/21018_Compilacao/Team_QualquerToken/MOC.g4 by ANTLR 4.13.1
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link MOCParser}.
 */
public interface MOCListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link MOCParser#programa}.
	 * @param ctx the parse tree
	 */
	void enterPrograma(MOCParser.ProgramaContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCParser#programa}.
	 * @param ctx the parse tree
	 */
	void exitPrograma(MOCParser.ProgramaContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCParser#prototipos}.
	 * @param ctx the parse tree
	 */
	void enterPrototipos(MOCParser.PrototiposContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCParser#prototipos}.
	 * @param ctx the parse tree
	 */
	void exitPrototipos(MOCParser.PrototiposContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCParser#corpo}.
	 * @param ctx the parse tree
	 */
	void enterCorpo(MOCParser.CorpoContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCParser#corpo}.
	 * @param ctx the parse tree
	 */
	void exitCorpo(MOCParser.CorpoContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCParser#unidade}.
	 * @param ctx the parse tree
	 */
	void enterUnidade(MOCParser.UnidadeContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCParser#unidade}.
	 * @param ctx the parse tree
	 */
	void exitUnidade(MOCParser.UnidadeContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCParser#prototipo}.
	 * @param ctx the parse tree
	 */
	void enterPrototipo(MOCParser.PrototipoContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCParser#prototipo}.
	 * @param ctx the parse tree
	 */
	void exitPrototipo(MOCParser.PrototipoContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCParser#prototipoPrincipal}.
	 * @param ctx the parse tree
	 */
	void enterPrototipoPrincipal(MOCParser.PrototipoPrincipalContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCParser#prototipoPrincipal}.
	 * @param ctx the parse tree
	 */
	void exitPrototipoPrincipal(MOCParser.PrototipoPrincipalContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCParser#funcaoPrincipal}.
	 * @param ctx the parse tree
	 */
	void enterFuncaoPrincipal(MOCParser.FuncaoPrincipalContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCParser#funcaoPrincipal}.
	 * @param ctx the parse tree
	 */
	void exitFuncaoPrincipal(MOCParser.FuncaoPrincipalContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCParser#funcao}.
	 * @param ctx the parse tree
	 */
	void enterFuncao(MOCParser.FuncaoContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCParser#funcao}.
	 * @param ctx the parse tree
	 */
	void exitFuncao(MOCParser.FuncaoContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCParser#parametros}.
	 * @param ctx the parse tree
	 */
	void enterParametros(MOCParser.ParametrosContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCParser#parametros}.
	 * @param ctx the parse tree
	 */
	void exitParametros(MOCParser.ParametrosContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCParser#parametro}.
	 * @param ctx the parse tree
	 */
	void enterParametro(MOCParser.ParametroContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCParser#parametro}.
	 * @param ctx the parse tree
	 */
	void exitParametro(MOCParser.ParametroContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCParser#tipo}.
	 * @param ctx the parse tree
	 */
	void enterTipo(MOCParser.TipoContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCParser#tipo}.
	 * @param ctx the parse tree
	 */
	void exitTipo(MOCParser.TipoContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCParser#declaracao}.
	 * @param ctx the parse tree
	 */
	void enterDeclaracao(MOCParser.DeclaracaoContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCParser#declaracao}.
	 * @param ctx the parse tree
	 */
	void exitDeclaracao(MOCParser.DeclaracaoContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCParser#listaVariaveis}.
	 * @param ctx the parse tree
	 */
	void enterListaVariaveis(MOCParser.ListaVariaveisContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCParser#listaVariaveis}.
	 * @param ctx the parse tree
	 */
	void exitListaVariaveis(MOCParser.ListaVariaveisContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCParser#variavel}.
	 * @param ctx the parse tree
	 */
	void enterVariavel(MOCParser.VariavelContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCParser#variavel}.
	 * @param ctx the parse tree
	 */
	void exitVariavel(MOCParser.VariavelContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCParser#blocoArray}.
	 * @param ctx the parse tree
	 */
	void enterBlocoArray(MOCParser.BlocoArrayContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCParser#blocoArray}.
	 * @param ctx the parse tree
	 */
	void exitBlocoArray(MOCParser.BlocoArrayContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCParser#listaValores}.
	 * @param ctx the parse tree
	 */
	void enterListaValores(MOCParser.ListaValoresContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCParser#listaValores}.
	 * @param ctx the parse tree
	 */
	void exitListaValores(MOCParser.ListaValoresContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCParser#expressao}.
	 * @param ctx the parse tree
	 */
	void enterExpressao(MOCParser.ExpressaoContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCParser#expressao}.
	 * @param ctx the parse tree
	 */
	void exitExpressao(MOCParser.ExpressaoContext ctx);
	/**
	 * Enter a parse tree produced by the {@code ouSimples}
	 * labeled alternative in {@link MOCParser#expressaoOr}.
	 * @param ctx the parse tree
	 */
	void enterOuSimples(MOCParser.OuSimplesContext ctx);
	/**
	 * Exit a parse tree produced by the {@code ouSimples}
	 * labeled alternative in {@link MOCParser#expressaoOr}.
	 * @param ctx the parse tree
	 */
	void exitOuSimples(MOCParser.OuSimplesContext ctx);
	/**
	 * Enter a parse tree produced by the {@code ouLogico}
	 * labeled alternative in {@link MOCParser#expressaoOr}.
	 * @param ctx the parse tree
	 */
	void enterOuLogico(MOCParser.OuLogicoContext ctx);
	/**
	 * Exit a parse tree produced by the {@code ouLogico}
	 * labeled alternative in {@link MOCParser#expressaoOr}.
	 * @param ctx the parse tree
	 */
	void exitOuLogico(MOCParser.OuLogicoContext ctx);
	/**
	 * Enter a parse tree produced by the {@code eLogico}
	 * labeled alternative in {@link MOCParser#expressaoAnd}.
	 * @param ctx the parse tree
	 */
	void enterELogico(MOCParser.ELogicoContext ctx);
	/**
	 * Exit a parse tree produced by the {@code eLogico}
	 * labeled alternative in {@link MOCParser#expressaoAnd}.
	 * @param ctx the parse tree
	 */
	void exitELogico(MOCParser.ELogicoContext ctx);
	/**
	 * Enter a parse tree produced by the {@code andSimples}
	 * labeled alternative in {@link MOCParser#expressaoAnd}.
	 * @param ctx the parse tree
	 */
	void enterAndSimples(MOCParser.AndSimplesContext ctx);
	/**
	 * Exit a parse tree produced by the {@code andSimples}
	 * labeled alternative in {@link MOCParser#expressaoAnd}.
	 * @param ctx the parse tree
	 */
	void exitAndSimples(MOCParser.AndSimplesContext ctx);
	/**
	 * Enter a parse tree produced by the {@code comparacaoSimples}
	 * labeled alternative in {@link MOCParser#expressaoEquality}.
	 * @param ctx the parse tree
	 */
	void enterComparacaoSimples(MOCParser.ComparacaoSimplesContext ctx);
	/**
	 * Exit a parse tree produced by the {@code comparacaoSimples}
	 * labeled alternative in {@link MOCParser#expressaoEquality}.
	 * @param ctx the parse tree
	 */
	void exitComparacaoSimples(MOCParser.ComparacaoSimplesContext ctx);
	/**
	 * Enter a parse tree produced by the {@code adicao}
	 * labeled alternative in {@link MOCParser#expressaoAdd}.
	 * @param ctx the parse tree
	 */
	void enterAdicao(MOCParser.AdicaoContext ctx);
	/**
	 * Exit a parse tree produced by the {@code adicao}
	 * labeled alternative in {@link MOCParser#expressaoAdd}.
	 * @param ctx the parse tree
	 */
	void exitAdicao(MOCParser.AdicaoContext ctx);
	/**
	 * Enter a parse tree produced by the {@code addSimples}
	 * labeled alternative in {@link MOCParser#expressaoAdd}.
	 * @param ctx the parse tree
	 */
	void enterAddSimples(MOCParser.AddSimplesContext ctx);
	/**
	 * Exit a parse tree produced by the {@code addSimples}
	 * labeled alternative in {@link MOCParser#expressaoAdd}.
	 * @param ctx the parse tree
	 */
	void exitAddSimples(MOCParser.AddSimplesContext ctx);
	/**
	 * Enter a parse tree produced by the {@code subtracao}
	 * labeled alternative in {@link MOCParser#expressaoAdd}.
	 * @param ctx the parse tree
	 */
	void enterSubtracao(MOCParser.SubtracaoContext ctx);
	/**
	 * Exit a parse tree produced by the {@code subtracao}
	 * labeled alternative in {@link MOCParser#expressaoAdd}.
	 * @param ctx the parse tree
	 */
	void exitSubtracao(MOCParser.SubtracaoContext ctx);
	/**
	 * Enter a parse tree produced by the {@code divisao}
	 * labeled alternative in {@link MOCParser#expressaoMul}.
	 * @param ctx the parse tree
	 */
	void enterDivisao(MOCParser.DivisaoContext ctx);
	/**
	 * Exit a parse tree produced by the {@code divisao}
	 * labeled alternative in {@link MOCParser#expressaoMul}.
	 * @param ctx the parse tree
	 */
	void exitDivisao(MOCParser.DivisaoContext ctx);
	/**
	 * Enter a parse tree produced by the {@code mulSimples}
	 * labeled alternative in {@link MOCParser#expressaoMul}.
	 * @param ctx the parse tree
	 */
	void enterMulSimples(MOCParser.MulSimplesContext ctx);
	/**
	 * Exit a parse tree produced by the {@code mulSimples}
	 * labeled alternative in {@link MOCParser#expressaoMul}.
	 * @param ctx the parse tree
	 */
	void exitMulSimples(MOCParser.MulSimplesContext ctx);
	/**
	 * Enter a parse tree produced by the {@code modulo}
	 * labeled alternative in {@link MOCParser#expressaoMul}.
	 * @param ctx the parse tree
	 */
	void enterModulo(MOCParser.ModuloContext ctx);
	/**
	 * Exit a parse tree produced by the {@code modulo}
	 * labeled alternative in {@link MOCParser#expressaoMul}.
	 * @param ctx the parse tree
	 */
	void exitModulo(MOCParser.ModuloContext ctx);
	/**
	 * Enter a parse tree produced by the {@code multiplicacao}
	 * labeled alternative in {@link MOCParser#expressaoMul}.
	 * @param ctx the parse tree
	 */
	void enterMultiplicacao(MOCParser.MultiplicacaoContext ctx);
	/**
	 * Exit a parse tree produced by the {@code multiplicacao}
	 * labeled alternative in {@link MOCParser#expressaoMul}.
	 * @param ctx the parse tree
	 */
	void exitMultiplicacao(MOCParser.MultiplicacaoContext ctx);
	/**
	 * Enter a parse tree produced by the {@code negacao}
	 * labeled alternative in {@link MOCParser#expressaoUnaria}.
	 * @param ctx the parse tree
	 */
	void enterNegacao(MOCParser.NegacaoContext ctx);
	/**
	 * Exit a parse tree produced by the {@code negacao}
	 * labeled alternative in {@link MOCParser#expressaoUnaria}.
	 * @param ctx the parse tree
	 */
	void exitNegacao(MOCParser.NegacaoContext ctx);
	/**
	 * Enter a parse tree produced by the {@code unarioNegativo}
	 * labeled alternative in {@link MOCParser#expressaoUnaria}.
	 * @param ctx the parse tree
	 */
	void enterUnarioNegativo(MOCParser.UnarioNegativoContext ctx);
	/**
	 * Exit a parse tree produced by the {@code unarioNegativo}
	 * labeled alternative in {@link MOCParser#expressaoUnaria}.
	 * @param ctx the parse tree
	 */
	void exitUnarioNegativo(MOCParser.UnarioNegativoContext ctx);
	/**
	 * Enter a parse tree produced by the {@code unariaSimples}
	 * labeled alternative in {@link MOCParser#expressaoUnaria}.
	 * @param ctx the parse tree
	 */
	void enterUnariaSimples(MOCParser.UnariaSimplesContext ctx);
	/**
	 * Exit a parse tree produced by the {@code unariaSimples}
	 * labeled alternative in {@link MOCParser#expressaoUnaria}.
	 * @param ctx the parse tree
	 */
	void exitUnariaSimples(MOCParser.UnariaSimplesContext ctx);
	/**
	 * Enter a parse tree produced by the {@code casting}
	 * labeled alternative in {@link MOCParser#castExpr}.
	 * @param ctx the parse tree
	 */
	void enterCasting(MOCParser.CastingContext ctx);
	/**
	 * Exit a parse tree produced by the {@code casting}
	 * labeled alternative in {@link MOCParser#castExpr}.
	 * @param ctx the parse tree
	 */
	void exitCasting(MOCParser.CastingContext ctx);
	/**
	 * Enter a parse tree produced by the {@code castSimples}
	 * labeled alternative in {@link MOCParser#castExpr}.
	 * @param ctx the parse tree
	 */
	void enterCastSimples(MOCParser.CastSimplesContext ctx);
	/**
	 * Exit a parse tree produced by the {@code castSimples}
	 * labeled alternative in {@link MOCParser#castExpr}.
	 * @param ctx the parse tree
	 */
	void exitCastSimples(MOCParser.CastSimplesContext ctx);
	/**
	 * Enter a parse tree produced by the {@code parenteses}
	 * labeled alternative in {@link MOCParser#primary}.
	 * @param ctx the parse tree
	 */
	void enterParenteses(MOCParser.ParentesesContext ctx);
	/**
	 * Exit a parse tree produced by the {@code parenteses}
	 * labeled alternative in {@link MOCParser#primary}.
	 * @param ctx the parse tree
	 */
	void exitParenteses(MOCParser.ParentesesContext ctx);
	/**
	 * Enter a parse tree produced by the {@code chamadaLeitura}
	 * labeled alternative in {@link MOCParser#primary}.
	 * @param ctx the parse tree
	 */
	void enterChamadaLeitura(MOCParser.ChamadaLeituraContext ctx);
	/**
	 * Exit a parse tree produced by the {@code chamadaLeitura}
	 * labeled alternative in {@link MOCParser#primary}.
	 * @param ctx the parse tree
	 */
	void exitChamadaLeitura(MOCParser.ChamadaLeituraContext ctx);
	/**
	 * Enter a parse tree produced by the {@code numero}
	 * labeled alternative in {@link MOCParser#primary}.
	 * @param ctx the parse tree
	 */
	void enterNumero(MOCParser.NumeroContext ctx);
	/**
	 * Exit a parse tree produced by the {@code numero}
	 * labeled alternative in {@link MOCParser#primary}.
	 * @param ctx the parse tree
	 */
	void exitNumero(MOCParser.NumeroContext ctx);
	/**
	 * Enter a parse tree produced by the {@code numeroReal}
	 * labeled alternative in {@link MOCParser#primary}.
	 * @param ctx the parse tree
	 */
	void enterNumeroReal(MOCParser.NumeroRealContext ctx);
	/**
	 * Exit a parse tree produced by the {@code numeroReal}
	 * labeled alternative in {@link MOCParser#primary}.
	 * @param ctx the parse tree
	 */
	void exitNumeroReal(MOCParser.NumeroRealContext ctx);
	/**
	 * Enter a parse tree produced by the {@code idComPrefixo}
	 * labeled alternative in {@link MOCParser#primary}.
	 * @param ctx the parse tree
	 */
	void enterIdComPrefixo(MOCParser.IdComPrefixoContext ctx);
	/**
	 * Exit a parse tree produced by the {@code idComPrefixo}
	 * labeled alternative in {@link MOCParser#primary}.
	 * @param ctx the parse tree
	 */
	void exitIdComPrefixo(MOCParser.IdComPrefixoContext ctx);
	/**
	 * Enter a parse tree produced by the {@code chamadaGenerica}
	 * labeled alternative in {@link MOCParser#primaryRest}.
	 * @param ctx the parse tree
	 */
	void enterChamadaGenerica(MOCParser.ChamadaGenericaContext ctx);
	/**
	 * Exit a parse tree produced by the {@code chamadaGenerica}
	 * labeled alternative in {@link MOCParser#primaryRest}.
	 * @param ctx the parse tree
	 */
	void exitChamadaGenerica(MOCParser.ChamadaGenericaContext ctx);
	/**
	 * Enter a parse tree produced by the {@code acessoVetor}
	 * labeled alternative in {@link MOCParser#primaryRest}.
	 * @param ctx the parse tree
	 */
	void enterAcessoVetor(MOCParser.AcessoVetorContext ctx);
	/**
	 * Exit a parse tree produced by the {@code acessoVetor}
	 * labeled alternative in {@link MOCParser#primaryRest}.
	 * @param ctx the parse tree
	 */
	void exitAcessoVetor(MOCParser.AcessoVetorContext ctx);
	/**
	 * Enter a parse tree produced by the {@code semSufixo}
	 * labeled alternative in {@link MOCParser#primaryRest}.
	 * @param ctx the parse tree
	 */
	void enterSemSufixo(MOCParser.SemSufixoContext ctx);
	/**
	 * Exit a parse tree produced by the {@code semSufixo}
	 * labeled alternative in {@link MOCParser#primaryRest}.
	 * @param ctx the parse tree
	 */
	void exitSemSufixo(MOCParser.SemSufixoContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCParser#argumentos}.
	 * @param ctx the parse tree
	 */
	void enterArgumentos(MOCParser.ArgumentosContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCParser#argumentos}.
	 * @param ctx the parse tree
	 */
	void exitArgumentos(MOCParser.ArgumentosContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCParser#opRelacional}.
	 * @param ctx the parse tree
	 */
	void enterOpRelacional(MOCParser.OpRelacionalContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCParser#opRelacional}.
	 * @param ctx the parse tree
	 */
	void exitOpRelacional(MOCParser.OpRelacionalContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCParser#chamadaFuncao}.
	 * @param ctx the parse tree
	 */
	void enterChamadaFuncao(MOCParser.ChamadaFuncaoContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCParser#chamadaFuncao}.
	 * @param ctx the parse tree
	 */
	void exitChamadaFuncao(MOCParser.ChamadaFuncaoContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCParser#chamadaReads}.
	 * @param ctx the parse tree
	 */
	void enterChamadaReads(MOCParser.ChamadaReadsContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCParser#chamadaReads}.
	 * @param ctx the parse tree
	 */
	void exitChamadaReads(MOCParser.ChamadaReadsContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCParser#bloco}.
	 * @param ctx the parse tree
	 */
	void enterBloco(MOCParser.BlocoContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCParser#bloco}.
	 * @param ctx the parse tree
	 */
	void exitBloco(MOCParser.BlocoContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCParser#instrucoes}.
	 * @param ctx the parse tree
	 */
	void enterInstrucoes(MOCParser.InstrucoesContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCParser#instrucoes}.
	 * @param ctx the parse tree
	 */
	void exitInstrucoes(MOCParser.InstrucoesContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCParser#instrucao}.
	 * @param ctx the parse tree
	 */
	void enterInstrucao(MOCParser.InstrucaoContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCParser#instrucao}.
	 * @param ctx the parse tree
	 */
	void exitInstrucao(MOCParser.InstrucaoContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCParser#instrucaoExpressao}.
	 * @param ctx the parse tree
	 */
	void enterInstrucaoExpressao(MOCParser.InstrucaoExpressaoContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCParser#instrucaoExpressao}.
	 * @param ctx the parse tree
	 */
	void exitInstrucaoExpressao(MOCParser.InstrucaoExpressaoContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCParser#instrucaoEmparelhada}.
	 * @param ctx the parse tree
	 */
	void enterInstrucaoEmparelhada(MOCParser.InstrucaoEmparelhadaContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCParser#instrucaoEmparelhada}.
	 * @param ctx the parse tree
	 */
	void exitInstrucaoEmparelhada(MOCParser.InstrucaoEmparelhadaContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCParser#instrucaoPorEmparelhar}.
	 * @param ctx the parse tree
	 */
	void enterInstrucaoPorEmparelhar(MOCParser.InstrucaoPorEmparelharContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCParser#instrucaoPorEmparelhar}.
	 * @param ctx the parse tree
	 */
	void exitInstrucaoPorEmparelhar(MOCParser.InstrucaoPorEmparelharContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCParser#outraInstrucao}.
	 * @param ctx the parse tree
	 */
	void enterOutraInstrucao(MOCParser.OutraInstrucaoContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCParser#outraInstrucao}.
	 * @param ctx the parse tree
	 */
	void exitOutraInstrucao(MOCParser.OutraInstrucaoContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCParser#instrucaoWhile}.
	 * @param ctx the parse tree
	 */
	void enterInstrucaoWhile(MOCParser.InstrucaoWhileContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCParser#instrucaoWhile}.
	 * @param ctx the parse tree
	 */
	void exitInstrucaoWhile(MOCParser.InstrucaoWhileContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCParser#instrucaoFor}.
	 * @param ctx the parse tree
	 */
	void enterInstrucaoFor(MOCParser.InstrucaoForContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCParser#instrucaoFor}.
	 * @param ctx the parse tree
	 */
	void exitInstrucaoFor(MOCParser.InstrucaoForContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCParser#expressaoOuAtribuicao}.
	 * @param ctx the parse tree
	 */
	void enterExpressaoOuAtribuicao(MOCParser.ExpressaoOuAtribuicaoContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCParser#expressaoOuAtribuicao}.
	 * @param ctx the parse tree
	 */
	void exitExpressaoOuAtribuicao(MOCParser.ExpressaoOuAtribuicaoContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCParser#instrucaoEscrita}.
	 * @param ctx the parse tree
	 */
	void enterInstrucaoEscrita(MOCParser.InstrucaoEscritaContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCParser#instrucaoEscrita}.
	 * @param ctx the parse tree
	 */
	void exitInstrucaoEscrita(MOCParser.InstrucaoEscritaContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCParser#instrucaoReturn}.
	 * @param ctx the parse tree
	 */
	void enterInstrucaoReturn(MOCParser.InstrucaoReturnContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCParser#instrucaoReturn}.
	 * @param ctx the parse tree
	 */
	void exitInstrucaoReturn(MOCParser.InstrucaoReturnContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCParser#instrucaoAtribuicao}.
	 * @param ctx the parse tree
	 */
	void enterInstrucaoAtribuicao(MOCParser.InstrucaoAtribuicaoContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCParser#instrucaoAtribuicao}.
	 * @param ctx the parse tree
	 */
	void exitInstrucaoAtribuicao(MOCParser.InstrucaoAtribuicaoContext ctx);
	/**
	 * Enter a parse tree produced by {@link MOCParser#argumentoString}.
	 * @param ctx the parse tree
	 */
	void enterArgumentoString(MOCParser.ArgumentoStringContext ctx);
	/**
	 * Exit a parse tree produced by {@link MOCParser#argumentoString}.
	 * @param ctx the parse tree
	 */
	void exitArgumentoString(MOCParser.ArgumentoStringContext ctx);
}