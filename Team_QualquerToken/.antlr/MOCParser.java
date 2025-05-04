// Generated from /Users/catiasantos/Documents/Code/CP/21018_Compilacao/Team_QualquerToken/MOC.g4 by ANTLR 4.13.1
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast", "CheckReturnValue"})
public class MOCParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.13.1", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		INT=1, DOUBLE=2, VOID=3, MAIN=4, READ=5, READC=6, READS=7, WRITE=8, WRITEC=9, 
		WRITEV=10, WRITES=11, IF=12, ELSE=13, WHILE=14, FOR=15, MAIS=16, MENOS=17, 
		MULT=18, DIV=19, MODULO=20, MENOR=21, MENORIGUAL=22, MAIOR=23, MAIORIGUAL=24, 
		IGUAL=25, DIFERENTE=26, E_LOGICO=27, OU_LOGICO=28, NAO=29, ATRIBUICAO=30, 
		VIRGULA=31, PONTOVIRG=32, ABRECOLCH=33, FECHACOLCH=34, ABRECHAVES=35, 
		FECHACHAVES=36, ABREPAR=37, FECHAPAR=38, RETURN=39, STRINGLITERAL=40, 
		COMENTARIO_BLOCK=41, COMENTARIO_LINE=42, NUM_REAL=43, NUMERO=44, IDENTIFICADOR=45, 
		ESPACO=46;
	public static final int
		RULE_programa = 0, RULE_prototipos = 1, RULE_corpo = 2, RULE_unidade = 3, 
		RULE_prototipo = 4, RULE_prototipoPrincipal = 5, RULE_funcaoPrincipal = 6, 
		RULE_funcao = 7, RULE_parametros = 8, RULE_parametro = 9, RULE_tipo = 10, 
		RULE_declaracao = 11, RULE_listaVariaveis = 12, RULE_variavel = 13, RULE_blocoArray = 14, 
		RULE_listaValores = 15, RULE_expressao = 16, RULE_expressaoOr = 17, RULE_expressaoAnd = 18, 
		RULE_expressaoEquality = 19, RULE_expressaoAdd = 20, RULE_expressaoMul = 21, 
		RULE_expressaoUnaria = 22, RULE_castExpr = 23, RULE_primary = 24, RULE_primaryRest = 25, 
		RULE_argumentos = 26, RULE_opRelacional = 27, RULE_chamadaFuncao = 28, 
		RULE_chamadaReads = 29, RULE_bloco = 30, RULE_instrucoes = 31, RULE_instrucao = 32, 
		RULE_instrucaoExpressao = 33, RULE_instrucaoEmparelhada = 34, RULE_instrucaoPorEmparelhar = 35, 
		RULE_outraInstrucao = 36, RULE_instrucaoWhile = 37, RULE_instrucaoFor = 38, 
		RULE_expressaoOuAtribuicao = 39, RULE_instrucaoEscrita = 40, RULE_instrucaoReturn = 41, 
		RULE_instrucaoAtribuicao = 42, RULE_argumentoString = 43;
	private static String[] makeRuleNames() {
		return new String[] {
			"programa", "prototipos", "corpo", "unidade", "prototipo", "prototipoPrincipal", 
			"funcaoPrincipal", "funcao", "parametros", "parametro", "tipo", "declaracao", 
			"listaVariaveis", "variavel", "blocoArray", "listaValores", "expressao", 
			"expressaoOr", "expressaoAnd", "expressaoEquality", "expressaoAdd", "expressaoMul", 
			"expressaoUnaria", "castExpr", "primary", "primaryRest", "argumentos", 
			"opRelacional", "chamadaFuncao", "chamadaReads", "bloco", "instrucoes", 
			"instrucao", "instrucaoExpressao", "instrucaoEmparelhada", "instrucaoPorEmparelhar", 
			"outraInstrucao", "instrucaoWhile", "instrucaoFor", "expressaoOuAtribuicao", 
			"instrucaoEscrita", "instrucaoReturn", "instrucaoAtribuicao", "argumentoString"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'int'", "'double'", "'void'", "'main'", "'read'", "'readc'", "'reads'", 
			"'write'", "'writec'", "'writev'", "'writes'", "'if'", "'else'", "'while'", 
			"'for'", "'+'", "'-'", "'*'", "'/'", "'%'", "'<'", "'<='", "'>'", "'>='", 
			"'=='", "'!='", "'&&'", "'||'", "'!'", "'='", "','", "';'", "'['", "']'", 
			"'{'", "'}'", "'('", "')'", "'return'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, "INT", "DOUBLE", "VOID", "MAIN", "READ", "READC", "READS", "WRITE", 
			"WRITEC", "WRITEV", "WRITES", "IF", "ELSE", "WHILE", "FOR", "MAIS", "MENOS", 
			"MULT", "DIV", "MODULO", "MENOR", "MENORIGUAL", "MAIOR", "MAIORIGUAL", 
			"IGUAL", "DIFERENTE", "E_LOGICO", "OU_LOGICO", "NAO", "ATRIBUICAO", "VIRGULA", 
			"PONTOVIRG", "ABRECOLCH", "FECHACOLCH", "ABRECHAVES", "FECHACHAVES", 
			"ABREPAR", "FECHAPAR", "RETURN", "STRINGLITERAL", "COMENTARIO_BLOCK", 
			"COMENTARIO_LINE", "NUM_REAL", "NUMERO", "IDENTIFICADOR", "ESPACO"
		};
	}
	private static final String[] _SYMBOLIC_NAMES = makeSymbolicNames();
	public static final Vocabulary VOCABULARY = new VocabularyImpl(_LITERAL_NAMES, _SYMBOLIC_NAMES);

	/**
	 * @deprecated Use {@link #VOCABULARY} instead.
	 */
	@Deprecated
	public static final String[] tokenNames;
	static {
		tokenNames = new String[_SYMBOLIC_NAMES.length];
		for (int i = 0; i < tokenNames.length; i++) {
			tokenNames[i] = VOCABULARY.getLiteralName(i);
			if (tokenNames[i] == null) {
				tokenNames[i] = VOCABULARY.getSymbolicName(i);
			}

			if (tokenNames[i] == null) {
				tokenNames[i] = "<INVALID>";
			}
		}
	}

	@Override
	@Deprecated
	public String[] getTokenNames() {
		return tokenNames;
	}

	@Override

	public Vocabulary getVocabulary() {
		return VOCABULARY;
	}

	@Override
	public String getGrammarFileName() { return "MOC.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public MOCParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ProgramaContext extends ParserRuleContext {
		public PrototiposContext prototipos() {
			return getRuleContext(PrototiposContext.class,0);
		}
		public CorpoContext corpo() {
			return getRuleContext(CorpoContext.class,0);
		}
		public TerminalNode EOF() { return getToken(MOCParser.EOF, 0); }
		public ProgramaContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_programa; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterPrograma(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitPrograma(this);
		}
	}

	public final ProgramaContext programa() throws RecognitionException {
		ProgramaContext _localctx = new ProgramaContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_programa);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(88);
			prototipos();
			setState(89);
			corpo();
			setState(90);
			match(EOF);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class PrototiposContext extends ParserRuleContext {
		public List<PrototipoPrincipalContext> prototipoPrincipal() {
			return getRuleContexts(PrototipoPrincipalContext.class);
		}
		public PrototipoPrincipalContext prototipoPrincipal(int i) {
			return getRuleContext(PrototipoPrincipalContext.class,i);
		}
		public List<PrototipoContext> prototipo() {
			return getRuleContexts(PrototipoContext.class);
		}
		public PrototipoContext prototipo(int i) {
			return getRuleContext(PrototipoContext.class,i);
		}
		public PrototiposContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_prototipos; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterPrototipos(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitPrototipos(this);
		}
	}

	public final PrototiposContext prototipos() throws RecognitionException {
		PrototiposContext _localctx = new PrototiposContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_prototipos);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(96);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,1,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					{
					setState(94);
					_errHandler.sync(this);
					switch ( getInterpreter().adaptivePredict(_input,0,_ctx) ) {
					case 1:
						{
						setState(92);
						prototipo();
						}
						break;
					case 2:
						{
						setState(93);
						prototipoPrincipal();
						}
						break;
					}
					} 
				}
				setState(98);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,1,_ctx);
			}
			setState(99);
			prototipoPrincipal();
			setState(104);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,3,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					{
					setState(102);
					_errHandler.sync(this);
					switch ( getInterpreter().adaptivePredict(_input,2,_ctx) ) {
					case 1:
						{
						setState(100);
						prototipo();
						}
						break;
					case 2:
						{
						setState(101);
						prototipoPrincipal();
						}
						break;
					}
					} 
				}
				setState(106);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,3,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class CorpoContext extends ParserRuleContext {
		public FuncaoPrincipalContext funcaoPrincipal() {
			return getRuleContext(FuncaoPrincipalContext.class,0);
		}
		public List<UnidadeContext> unidade() {
			return getRuleContexts(UnidadeContext.class);
		}
		public UnidadeContext unidade(int i) {
			return getRuleContext(UnidadeContext.class,i);
		}
		public CorpoContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_corpo; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterCorpo(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitCorpo(this);
		}
	}

	public final CorpoContext corpo() throws RecognitionException {
		CorpoContext _localctx = new CorpoContext(_ctx, getState());
		enterRule(_localctx, 4, RULE_corpo);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(110);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,4,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					{
					{
					setState(107);
					unidade();
					}
					} 
				}
				setState(112);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,4,_ctx);
			}
			setState(113);
			funcaoPrincipal();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class UnidadeContext extends ParserRuleContext {
		public FuncaoContext funcao() {
			return getRuleContext(FuncaoContext.class,0);
		}
		public DeclaracaoContext declaracao() {
			return getRuleContext(DeclaracaoContext.class,0);
		}
		public UnidadeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_unidade; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterUnidade(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitUnidade(this);
		}
	}

	public final UnidadeContext unidade() throws RecognitionException {
		UnidadeContext _localctx = new UnidadeContext(_ctx, getState());
		enterRule(_localctx, 6, RULE_unidade);
		try {
			setState(117);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,5,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(115);
				funcao();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(116);
				declaracao();
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class PrototipoContext extends ParserRuleContext {
		public TipoContext tipo() {
			return getRuleContext(TipoContext.class,0);
		}
		public TerminalNode IDENTIFICADOR() { return getToken(MOCParser.IDENTIFICADOR, 0); }
		public TerminalNode ABREPAR() { return getToken(MOCParser.ABREPAR, 0); }
		public TerminalNode FECHAPAR() { return getToken(MOCParser.FECHAPAR, 0); }
		public TerminalNode PONTOVIRG() { return getToken(MOCParser.PONTOVIRG, 0); }
		public ParametrosContext parametros() {
			return getRuleContext(ParametrosContext.class,0);
		}
		public PrototipoContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_prototipo; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterPrototipo(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitPrototipo(this);
		}
	}

	public final PrototipoContext prototipo() throws RecognitionException {
		PrototipoContext _localctx = new PrototipoContext(_ctx, getState());
		enterRule(_localctx, 8, RULE_prototipo);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(119);
			tipo();
			setState(120);
			match(IDENTIFICADOR);
			setState(121);
			match(ABREPAR);
			setState(123);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if ((((_la) & ~0x3f) == 0 && ((1L << _la) & 14L) != 0)) {
				{
				setState(122);
				parametros();
				}
			}

			setState(125);
			match(FECHAPAR);
			setState(126);
			match(PONTOVIRG);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class PrototipoPrincipalContext extends ParserRuleContext {
		public TipoContext tipo() {
			return getRuleContext(TipoContext.class,0);
		}
		public TerminalNode MAIN() { return getToken(MOCParser.MAIN, 0); }
		public TerminalNode ABREPAR() { return getToken(MOCParser.ABREPAR, 0); }
		public TerminalNode FECHAPAR() { return getToken(MOCParser.FECHAPAR, 0); }
		public TerminalNode PONTOVIRG() { return getToken(MOCParser.PONTOVIRG, 0); }
		public ParametrosContext parametros() {
			return getRuleContext(ParametrosContext.class,0);
		}
		public PrototipoPrincipalContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_prototipoPrincipal; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterPrototipoPrincipal(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitPrototipoPrincipal(this);
		}
	}

	public final PrototipoPrincipalContext prototipoPrincipal() throws RecognitionException {
		PrototipoPrincipalContext _localctx = new PrototipoPrincipalContext(_ctx, getState());
		enterRule(_localctx, 10, RULE_prototipoPrincipal);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(128);
			tipo();
			setState(129);
			match(MAIN);
			setState(130);
			match(ABREPAR);
			setState(132);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if ((((_la) & ~0x3f) == 0 && ((1L << _la) & 14L) != 0)) {
				{
				setState(131);
				parametros();
				}
			}

			setState(134);
			match(FECHAPAR);
			setState(135);
			match(PONTOVIRG);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class FuncaoPrincipalContext extends ParserRuleContext {
		public TipoContext tipo() {
			return getRuleContext(TipoContext.class,0);
		}
		public TerminalNode MAIN() { return getToken(MOCParser.MAIN, 0); }
		public TerminalNode ABREPAR() { return getToken(MOCParser.ABREPAR, 0); }
		public TerminalNode FECHAPAR() { return getToken(MOCParser.FECHAPAR, 0); }
		public BlocoContext bloco() {
			return getRuleContext(BlocoContext.class,0);
		}
		public ParametrosContext parametros() {
			return getRuleContext(ParametrosContext.class,0);
		}
		public FuncaoPrincipalContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_funcaoPrincipal; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterFuncaoPrincipal(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitFuncaoPrincipal(this);
		}
	}

	public final FuncaoPrincipalContext funcaoPrincipal() throws RecognitionException {
		FuncaoPrincipalContext _localctx = new FuncaoPrincipalContext(_ctx, getState());
		enterRule(_localctx, 12, RULE_funcaoPrincipal);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(137);
			tipo();
			setState(138);
			match(MAIN);
			setState(139);
			match(ABREPAR);
			setState(141);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if ((((_la) & ~0x3f) == 0 && ((1L << _la) & 14L) != 0)) {
				{
				setState(140);
				parametros();
				}
			}

			setState(143);
			match(FECHAPAR);
			setState(144);
			bloco();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class FuncaoContext extends ParserRuleContext {
		public TipoContext tipo() {
			return getRuleContext(TipoContext.class,0);
		}
		public TerminalNode IDENTIFICADOR() { return getToken(MOCParser.IDENTIFICADOR, 0); }
		public TerminalNode ABREPAR() { return getToken(MOCParser.ABREPAR, 0); }
		public TerminalNode FECHAPAR() { return getToken(MOCParser.FECHAPAR, 0); }
		public BlocoContext bloco() {
			return getRuleContext(BlocoContext.class,0);
		}
		public ParametrosContext parametros() {
			return getRuleContext(ParametrosContext.class,0);
		}
		public FuncaoContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_funcao; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterFuncao(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitFuncao(this);
		}
	}

	public final FuncaoContext funcao() throws RecognitionException {
		FuncaoContext _localctx = new FuncaoContext(_ctx, getState());
		enterRule(_localctx, 14, RULE_funcao);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(146);
			tipo();
			setState(147);
			match(IDENTIFICADOR);
			setState(148);
			match(ABREPAR);
			setState(150);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if ((((_la) & ~0x3f) == 0 && ((1L << _la) & 14L) != 0)) {
				{
				setState(149);
				parametros();
				}
			}

			setState(152);
			match(FECHAPAR);
			setState(153);
			bloco();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ParametrosContext extends ParserRuleContext {
		public TerminalNode VOID() { return getToken(MOCParser.VOID, 0); }
		public TipoContext tipo() {
			return getRuleContext(TipoContext.class,0);
		}
		public List<ParametroContext> parametro() {
			return getRuleContexts(ParametroContext.class);
		}
		public ParametroContext parametro(int i) {
			return getRuleContext(ParametroContext.class,i);
		}
		public List<TerminalNode> VIRGULA() { return getTokens(MOCParser.VIRGULA); }
		public TerminalNode VIRGULA(int i) {
			return getToken(MOCParser.VIRGULA, i);
		}
		public ParametrosContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_parametros; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterParametros(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitParametros(this);
		}
	}

	public final ParametrosContext parametros() throws RecognitionException {
		ParametrosContext _localctx = new ParametrosContext(_ctx, getState());
		enterRule(_localctx, 16, RULE_parametros);
		int _la;
		try {
			setState(165);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,11,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(155);
				match(VOID);
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(156);
				tipo();
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(157);
				parametro();
				setState(162);
				_errHandler.sync(this);
				_la = _input.LA(1);
				while (_la==VIRGULA) {
					{
					{
					setState(158);
					match(VIRGULA);
					setState(159);
					parametro();
					}
					}
					setState(164);
					_errHandler.sync(this);
					_la = _input.LA(1);
				}
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ParametroContext extends ParserRuleContext {
		public TipoContext tipo() {
			return getRuleContext(TipoContext.class,0);
		}
		public TerminalNode IDENTIFICADOR() { return getToken(MOCParser.IDENTIFICADOR, 0); }
		public TerminalNode ABRECOLCH() { return getToken(MOCParser.ABRECOLCH, 0); }
		public TerminalNode FECHACOLCH() { return getToken(MOCParser.FECHACOLCH, 0); }
		public ParametroContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_parametro; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterParametro(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitParametro(this);
		}
	}

	public final ParametroContext parametro() throws RecognitionException {
		ParametroContext _localctx = new ParametroContext(_ctx, getState());
		enterRule(_localctx, 18, RULE_parametro);
		try {
			setState(180);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,12,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(167);
				tipo();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(168);
				tipo();
				setState(169);
				match(IDENTIFICADOR);
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(171);
				tipo();
				setState(172);
				match(ABRECOLCH);
				setState(173);
				match(FECHACOLCH);
				}
				break;
			case 4:
				enterOuterAlt(_localctx, 4);
				{
				setState(175);
				tipo();
				setState(176);
				match(IDENTIFICADOR);
				setState(177);
				match(ABRECOLCH);
				setState(178);
				match(FECHACOLCH);
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class TipoContext extends ParserRuleContext {
		public TerminalNode INT() { return getToken(MOCParser.INT, 0); }
		public TerminalNode DOUBLE() { return getToken(MOCParser.DOUBLE, 0); }
		public TerminalNode VOID() { return getToken(MOCParser.VOID, 0); }
		public TipoContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_tipo; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterTipo(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitTipo(this);
		}
	}

	public final TipoContext tipo() throws RecognitionException {
		TipoContext _localctx = new TipoContext(_ctx, getState());
		enterRule(_localctx, 20, RULE_tipo);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(182);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & 14L) != 0)) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class DeclaracaoContext extends ParserRuleContext {
		public TipoContext tipo() {
			return getRuleContext(TipoContext.class,0);
		}
		public ListaVariaveisContext listaVariaveis() {
			return getRuleContext(ListaVariaveisContext.class,0);
		}
		public TerminalNode PONTOVIRG() { return getToken(MOCParser.PONTOVIRG, 0); }
		public DeclaracaoContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_declaracao; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterDeclaracao(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitDeclaracao(this);
		}
	}

	public final DeclaracaoContext declaracao() throws RecognitionException {
		DeclaracaoContext _localctx = new DeclaracaoContext(_ctx, getState());
		enterRule(_localctx, 22, RULE_declaracao);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(184);
			tipo();
			setState(185);
			listaVariaveis();
			setState(186);
			match(PONTOVIRG);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ListaVariaveisContext extends ParserRuleContext {
		public List<VariavelContext> variavel() {
			return getRuleContexts(VariavelContext.class);
		}
		public VariavelContext variavel(int i) {
			return getRuleContext(VariavelContext.class,i);
		}
		public List<TerminalNode> VIRGULA() { return getTokens(MOCParser.VIRGULA); }
		public TerminalNode VIRGULA(int i) {
			return getToken(MOCParser.VIRGULA, i);
		}
		public ListaVariaveisContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_listaVariaveis; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterListaVariaveis(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitListaVariaveis(this);
		}
	}

	public final ListaVariaveisContext listaVariaveis() throws RecognitionException {
		ListaVariaveisContext _localctx = new ListaVariaveisContext(_ctx, getState());
		enterRule(_localctx, 24, RULE_listaVariaveis);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(188);
			variavel();
			setState(193);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==VIRGULA) {
				{
				{
				setState(189);
				match(VIRGULA);
				setState(190);
				variavel();
				}
				}
				setState(195);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class VariavelContext extends ParserRuleContext {
		public TerminalNode IDENTIFICADOR() { return getToken(MOCParser.IDENTIFICADOR, 0); }
		public TerminalNode ATRIBUICAO() { return getToken(MOCParser.ATRIBUICAO, 0); }
		public ExpressaoContext expressao() {
			return getRuleContext(ExpressaoContext.class,0);
		}
		public TerminalNode ABRECOLCH() { return getToken(MOCParser.ABRECOLCH, 0); }
		public TerminalNode NUMERO() { return getToken(MOCParser.NUMERO, 0); }
		public TerminalNode FECHACOLCH() { return getToken(MOCParser.FECHACOLCH, 0); }
		public ChamadaReadsContext chamadaReads() {
			return getRuleContext(ChamadaReadsContext.class,0);
		}
		public BlocoArrayContext blocoArray() {
			return getRuleContext(BlocoArrayContext.class,0);
		}
		public VariavelContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_variavel; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterVariavel(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitVariavel(this);
		}
	}

	public final VariavelContext variavel() throws RecognitionException {
		VariavelContext _localctx = new VariavelContext(_ctx, getState());
		enterRule(_localctx, 26, RULE_variavel);
		try {
			setState(220);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,14,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(196);
				match(IDENTIFICADOR);
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(197);
				match(IDENTIFICADOR);
				setState(198);
				match(ATRIBUICAO);
				setState(199);
				expressao();
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(200);
				match(IDENTIFICADOR);
				setState(201);
				match(ABRECOLCH);
				setState(202);
				match(NUMERO);
				setState(203);
				match(FECHACOLCH);
				}
				break;
			case 4:
				enterOuterAlt(_localctx, 4);
				{
				setState(204);
				match(IDENTIFICADOR);
				setState(205);
				match(ABRECOLCH);
				setState(206);
				match(FECHACOLCH);
				setState(207);
				match(ATRIBUICAO);
				setState(208);
				chamadaReads();
				}
				break;
			case 5:
				enterOuterAlt(_localctx, 5);
				{
				setState(209);
				match(IDENTIFICADOR);
				setState(210);
				match(ABRECOLCH);
				setState(211);
				match(FECHACOLCH);
				setState(212);
				match(ATRIBUICAO);
				setState(213);
				blocoArray();
				}
				break;
			case 6:
				enterOuterAlt(_localctx, 6);
				{
				setState(214);
				match(IDENTIFICADOR);
				setState(215);
				match(ABRECOLCH);
				setState(216);
				match(NUMERO);
				setState(217);
				match(FECHACOLCH);
				setState(218);
				match(ATRIBUICAO);
				setState(219);
				blocoArray();
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class BlocoArrayContext extends ParserRuleContext {
		public TerminalNode ABRECHAVES() { return getToken(MOCParser.ABRECHAVES, 0); }
		public TerminalNode FECHACHAVES() { return getToken(MOCParser.FECHACHAVES, 0); }
		public ListaValoresContext listaValores() {
			return getRuleContext(ListaValoresContext.class,0);
		}
		public BlocoArrayContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_blocoArray; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterBlocoArray(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitBlocoArray(this);
		}
	}

	public final BlocoArrayContext blocoArray() throws RecognitionException {
		BlocoArrayContext _localctx = new BlocoArrayContext(_ctx, getState());
		enterRule(_localctx, 28, RULE_blocoArray);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(222);
			match(ABRECHAVES);
			setState(224);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if ((((_la) & ~0x3f) == 0 && ((1L << _la) & 61710627111136L) != 0)) {
				{
				setState(223);
				listaValores();
				}
			}

			setState(226);
			match(FECHACHAVES);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ListaValoresContext extends ParserRuleContext {
		public List<ExpressaoContext> expressao() {
			return getRuleContexts(ExpressaoContext.class);
		}
		public ExpressaoContext expressao(int i) {
			return getRuleContext(ExpressaoContext.class,i);
		}
		public List<TerminalNode> VIRGULA() { return getTokens(MOCParser.VIRGULA); }
		public TerminalNode VIRGULA(int i) {
			return getToken(MOCParser.VIRGULA, i);
		}
		public ListaValoresContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_listaValores; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterListaValores(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitListaValores(this);
		}
	}

	public final ListaValoresContext listaValores() throws RecognitionException {
		ListaValoresContext _localctx = new ListaValoresContext(_ctx, getState());
		enterRule(_localctx, 30, RULE_listaValores);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(228);
			expressao();
			setState(233);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==VIRGULA) {
				{
				{
				setState(229);
				match(VIRGULA);
				setState(230);
				expressao();
				}
				}
				setState(235);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ExpressaoContext extends ParserRuleContext {
		public ExpressaoOrContext expressaoOr() {
			return getRuleContext(ExpressaoOrContext.class,0);
		}
		public ExpressaoContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_expressao; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterExpressao(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitExpressao(this);
		}
	}

	public final ExpressaoContext expressao() throws RecognitionException {
		ExpressaoContext _localctx = new ExpressaoContext(_ctx, getState());
		enterRule(_localctx, 32, RULE_expressao);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(236);
			expressaoOr(0);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ExpressaoOrContext extends ParserRuleContext {
		public ExpressaoOrContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_expressaoOr; }
	 
		public ExpressaoOrContext() { }
		public void copyFrom(ExpressaoOrContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class OuSimplesContext extends ExpressaoOrContext {
		public ExpressaoAndContext expressaoAnd() {
			return getRuleContext(ExpressaoAndContext.class,0);
		}
		public OuSimplesContext(ExpressaoOrContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterOuSimples(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitOuSimples(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class OuLogicoContext extends ExpressaoOrContext {
		public ExpressaoOrContext expressaoOr() {
			return getRuleContext(ExpressaoOrContext.class,0);
		}
		public TerminalNode OU_LOGICO() { return getToken(MOCParser.OU_LOGICO, 0); }
		public ExpressaoAndContext expressaoAnd() {
			return getRuleContext(ExpressaoAndContext.class,0);
		}
		public OuLogicoContext(ExpressaoOrContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterOuLogico(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitOuLogico(this);
		}
	}

	public final ExpressaoOrContext expressaoOr() throws RecognitionException {
		return expressaoOr(0);
	}

	private ExpressaoOrContext expressaoOr(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		ExpressaoOrContext _localctx = new ExpressaoOrContext(_ctx, _parentState);
		ExpressaoOrContext _prevctx = _localctx;
		int _startState = 34;
		enterRecursionRule(_localctx, 34, RULE_expressaoOr, _p);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			{
			_localctx = new OuSimplesContext(_localctx);
			_ctx = _localctx;
			_prevctx = _localctx;

			setState(239);
			expressaoAnd(0);
			}
			_ctx.stop = _input.LT(-1);
			setState(246);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,17,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					{
					_localctx = new OuLogicoContext(new ExpressaoOrContext(_parentctx, _parentState));
					pushNewRecursionContext(_localctx, _startState, RULE_expressaoOr);
					setState(241);
					if (!(precpred(_ctx, 2))) throw new FailedPredicateException(this, "precpred(_ctx, 2)");
					setState(242);
					match(OU_LOGICO);
					setState(243);
					expressaoAnd(0);
					}
					} 
				}
				setState(248);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,17,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ExpressaoAndContext extends ParserRuleContext {
		public ExpressaoAndContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_expressaoAnd; }
	 
		public ExpressaoAndContext() { }
		public void copyFrom(ExpressaoAndContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ELogicoContext extends ExpressaoAndContext {
		public ExpressaoAndContext expressaoAnd() {
			return getRuleContext(ExpressaoAndContext.class,0);
		}
		public TerminalNode E_LOGICO() { return getToken(MOCParser.E_LOGICO, 0); }
		public ExpressaoEqualityContext expressaoEquality() {
			return getRuleContext(ExpressaoEqualityContext.class,0);
		}
		public ELogicoContext(ExpressaoAndContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterELogico(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitELogico(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class AndSimplesContext extends ExpressaoAndContext {
		public ExpressaoEqualityContext expressaoEquality() {
			return getRuleContext(ExpressaoEqualityContext.class,0);
		}
		public AndSimplesContext(ExpressaoAndContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterAndSimples(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitAndSimples(this);
		}
	}

	public final ExpressaoAndContext expressaoAnd() throws RecognitionException {
		return expressaoAnd(0);
	}

	private ExpressaoAndContext expressaoAnd(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		ExpressaoAndContext _localctx = new ExpressaoAndContext(_ctx, _parentState);
		ExpressaoAndContext _prevctx = _localctx;
		int _startState = 36;
		enterRecursionRule(_localctx, 36, RULE_expressaoAnd, _p);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			{
			_localctx = new AndSimplesContext(_localctx);
			_ctx = _localctx;
			_prevctx = _localctx;

			setState(250);
			expressaoEquality();
			}
			_ctx.stop = _input.LT(-1);
			setState(257);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,18,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					{
					_localctx = new ELogicoContext(new ExpressaoAndContext(_parentctx, _parentState));
					pushNewRecursionContext(_localctx, _startState, RULE_expressaoAnd);
					setState(252);
					if (!(precpred(_ctx, 2))) throw new FailedPredicateException(this, "precpred(_ctx, 2)");
					setState(253);
					match(E_LOGICO);
					setState(254);
					expressaoEquality();
					}
					} 
				}
				setState(259);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,18,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ExpressaoEqualityContext extends ParserRuleContext {
		public ExpressaoEqualityContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_expressaoEquality; }
	 
		public ExpressaoEqualityContext() { }
		public void copyFrom(ExpressaoEqualityContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ComparacaoSimplesContext extends ExpressaoEqualityContext {
		public List<ExpressaoAddContext> expressaoAdd() {
			return getRuleContexts(ExpressaoAddContext.class);
		}
		public ExpressaoAddContext expressaoAdd(int i) {
			return getRuleContext(ExpressaoAddContext.class,i);
		}
		public OpRelacionalContext opRelacional() {
			return getRuleContext(OpRelacionalContext.class,0);
		}
		public ComparacaoSimplesContext(ExpressaoEqualityContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterComparacaoSimples(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitComparacaoSimples(this);
		}
	}

	public final ExpressaoEqualityContext expressaoEquality() throws RecognitionException {
		ExpressaoEqualityContext _localctx = new ExpressaoEqualityContext(_ctx, getState());
		enterRule(_localctx, 38, RULE_expressaoEquality);
		try {
			_localctx = new ComparacaoSimplesContext(_localctx);
			enterOuterAlt(_localctx, 1);
			{
			setState(260);
			expressaoAdd(0);
			setState(264);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,19,_ctx) ) {
			case 1:
				{
				setState(261);
				opRelacional();
				setState(262);
				expressaoAdd(0);
				}
				break;
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ExpressaoAddContext extends ParserRuleContext {
		public ExpressaoAddContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_expressaoAdd; }
	 
		public ExpressaoAddContext() { }
		public void copyFrom(ExpressaoAddContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class AdicaoContext extends ExpressaoAddContext {
		public ExpressaoAddContext expressaoAdd() {
			return getRuleContext(ExpressaoAddContext.class,0);
		}
		public TerminalNode MAIS() { return getToken(MOCParser.MAIS, 0); }
		public ExpressaoMulContext expressaoMul() {
			return getRuleContext(ExpressaoMulContext.class,0);
		}
		public AdicaoContext(ExpressaoAddContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterAdicao(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitAdicao(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class AddSimplesContext extends ExpressaoAddContext {
		public ExpressaoMulContext expressaoMul() {
			return getRuleContext(ExpressaoMulContext.class,0);
		}
		public AddSimplesContext(ExpressaoAddContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterAddSimples(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitAddSimples(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SubtracaoContext extends ExpressaoAddContext {
		public ExpressaoAddContext expressaoAdd() {
			return getRuleContext(ExpressaoAddContext.class,0);
		}
		public TerminalNode MENOS() { return getToken(MOCParser.MENOS, 0); }
		public ExpressaoMulContext expressaoMul() {
			return getRuleContext(ExpressaoMulContext.class,0);
		}
		public SubtracaoContext(ExpressaoAddContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterSubtracao(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitSubtracao(this);
		}
	}

	public final ExpressaoAddContext expressaoAdd() throws RecognitionException {
		return expressaoAdd(0);
	}

	private ExpressaoAddContext expressaoAdd(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		ExpressaoAddContext _localctx = new ExpressaoAddContext(_ctx, _parentState);
		ExpressaoAddContext _prevctx = _localctx;
		int _startState = 40;
		enterRecursionRule(_localctx, 40, RULE_expressaoAdd, _p);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			{
			_localctx = new AddSimplesContext(_localctx);
			_ctx = _localctx;
			_prevctx = _localctx;

			setState(267);
			expressaoMul(0);
			}
			_ctx.stop = _input.LT(-1);
			setState(277);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,21,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					setState(275);
					_errHandler.sync(this);
					switch ( getInterpreter().adaptivePredict(_input,20,_ctx) ) {
					case 1:
						{
						_localctx = new AdicaoContext(new ExpressaoAddContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_expressaoAdd);
						setState(269);
						if (!(precpred(_ctx, 3))) throw new FailedPredicateException(this, "precpred(_ctx, 3)");
						setState(270);
						match(MAIS);
						setState(271);
						expressaoMul(0);
						}
						break;
					case 2:
						{
						_localctx = new SubtracaoContext(new ExpressaoAddContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_expressaoAdd);
						setState(272);
						if (!(precpred(_ctx, 2))) throw new FailedPredicateException(this, "precpred(_ctx, 2)");
						setState(273);
						match(MENOS);
						setState(274);
						expressaoMul(0);
						}
						break;
					}
					} 
				}
				setState(279);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,21,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ExpressaoMulContext extends ParserRuleContext {
		public ExpressaoMulContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_expressaoMul; }
	 
		public ExpressaoMulContext() { }
		public void copyFrom(ExpressaoMulContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class DivisaoContext extends ExpressaoMulContext {
		public ExpressaoMulContext expressaoMul() {
			return getRuleContext(ExpressaoMulContext.class,0);
		}
		public TerminalNode DIV() { return getToken(MOCParser.DIV, 0); }
		public ExpressaoUnariaContext expressaoUnaria() {
			return getRuleContext(ExpressaoUnariaContext.class,0);
		}
		public DivisaoContext(ExpressaoMulContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterDivisao(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitDivisao(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class MulSimplesContext extends ExpressaoMulContext {
		public ExpressaoUnariaContext expressaoUnaria() {
			return getRuleContext(ExpressaoUnariaContext.class,0);
		}
		public MulSimplesContext(ExpressaoMulContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterMulSimples(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitMulSimples(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ModuloContext extends ExpressaoMulContext {
		public ExpressaoMulContext expressaoMul() {
			return getRuleContext(ExpressaoMulContext.class,0);
		}
		public TerminalNode MODULO() { return getToken(MOCParser.MODULO, 0); }
		public ExpressaoUnariaContext expressaoUnaria() {
			return getRuleContext(ExpressaoUnariaContext.class,0);
		}
		public ModuloContext(ExpressaoMulContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterModulo(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitModulo(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class MultiplicacaoContext extends ExpressaoMulContext {
		public ExpressaoMulContext expressaoMul() {
			return getRuleContext(ExpressaoMulContext.class,0);
		}
		public TerminalNode MULT() { return getToken(MOCParser.MULT, 0); }
		public ExpressaoUnariaContext expressaoUnaria() {
			return getRuleContext(ExpressaoUnariaContext.class,0);
		}
		public MultiplicacaoContext(ExpressaoMulContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterMultiplicacao(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitMultiplicacao(this);
		}
	}

	public final ExpressaoMulContext expressaoMul() throws RecognitionException {
		return expressaoMul(0);
	}

	private ExpressaoMulContext expressaoMul(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		ExpressaoMulContext _localctx = new ExpressaoMulContext(_ctx, _parentState);
		ExpressaoMulContext _prevctx = _localctx;
		int _startState = 42;
		enterRecursionRule(_localctx, 42, RULE_expressaoMul, _p);
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			{
			_localctx = new MulSimplesContext(_localctx);
			_ctx = _localctx;
			_prevctx = _localctx;

			setState(281);
			expressaoUnaria();
			}
			_ctx.stop = _input.LT(-1);
			setState(294);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,23,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					setState(292);
					_errHandler.sync(this);
					switch ( getInterpreter().adaptivePredict(_input,22,_ctx) ) {
					case 1:
						{
						_localctx = new MultiplicacaoContext(new ExpressaoMulContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_expressaoMul);
						setState(283);
						if (!(precpred(_ctx, 4))) throw new FailedPredicateException(this, "precpred(_ctx, 4)");
						setState(284);
						match(MULT);
						setState(285);
						expressaoUnaria();
						}
						break;
					case 2:
						{
						_localctx = new DivisaoContext(new ExpressaoMulContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_expressaoMul);
						setState(286);
						if (!(precpred(_ctx, 3))) throw new FailedPredicateException(this, "precpred(_ctx, 3)");
						setState(287);
						match(DIV);
						setState(288);
						expressaoUnaria();
						}
						break;
					case 3:
						{
						_localctx = new ModuloContext(new ExpressaoMulContext(_parentctx, _parentState));
						pushNewRecursionContext(_localctx, _startState, RULE_expressaoMul);
						setState(289);
						if (!(precpred(_ctx, 2))) throw new FailedPredicateException(this, "precpred(_ctx, 2)");
						setState(290);
						match(MODULO);
						setState(291);
						expressaoUnaria();
						}
						break;
					}
					} 
				}
				setState(296);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,23,_ctx);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			unrollRecursionContexts(_parentctx);
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ExpressaoUnariaContext extends ParserRuleContext {
		public ExpressaoUnariaContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_expressaoUnaria; }
	 
		public ExpressaoUnariaContext() { }
		public void copyFrom(ExpressaoUnariaContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class UnarioNegativoContext extends ExpressaoUnariaContext {
		public TerminalNode MENOS() { return getToken(MOCParser.MENOS, 0); }
		public ExpressaoUnariaContext expressaoUnaria() {
			return getRuleContext(ExpressaoUnariaContext.class,0);
		}
		public UnarioNegativoContext(ExpressaoUnariaContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterUnarioNegativo(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitUnarioNegativo(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class UnariaSimplesContext extends ExpressaoUnariaContext {
		public CastExprContext castExpr() {
			return getRuleContext(CastExprContext.class,0);
		}
		public UnariaSimplesContext(ExpressaoUnariaContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterUnariaSimples(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitUnariaSimples(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class NegacaoContext extends ExpressaoUnariaContext {
		public TerminalNode NAO() { return getToken(MOCParser.NAO, 0); }
		public ExpressaoUnariaContext expressaoUnaria() {
			return getRuleContext(ExpressaoUnariaContext.class,0);
		}
		public NegacaoContext(ExpressaoUnariaContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterNegacao(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitNegacao(this);
		}
	}

	public final ExpressaoUnariaContext expressaoUnaria() throws RecognitionException {
		ExpressaoUnariaContext _localctx = new ExpressaoUnariaContext(_ctx, getState());
		enterRule(_localctx, 44, RULE_expressaoUnaria);
		try {
			setState(302);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case NAO:
				_localctx = new NegacaoContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(297);
				match(NAO);
				setState(298);
				expressaoUnaria();
				}
				break;
			case MENOS:
				_localctx = new UnarioNegativoContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(299);
				match(MENOS);
				setState(300);
				expressaoUnaria();
				}
				break;
			case READ:
			case READC:
			case READS:
			case ABREPAR:
			case NUM_REAL:
			case NUMERO:
			case IDENTIFICADOR:
				_localctx = new UnariaSimplesContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(301);
				castExpr();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class CastExprContext extends ParserRuleContext {
		public CastExprContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_castExpr; }
	 
		public CastExprContext() { }
		public void copyFrom(CastExprContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class CastSimplesContext extends CastExprContext {
		public PrimaryContext primary() {
			return getRuleContext(PrimaryContext.class,0);
		}
		public CastSimplesContext(CastExprContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterCastSimples(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitCastSimples(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class CastingContext extends CastExprContext {
		public TerminalNode ABREPAR() { return getToken(MOCParser.ABREPAR, 0); }
		public TipoContext tipo() {
			return getRuleContext(TipoContext.class,0);
		}
		public TerminalNode FECHAPAR() { return getToken(MOCParser.FECHAPAR, 0); }
		public CastExprContext castExpr() {
			return getRuleContext(CastExprContext.class,0);
		}
		public CastingContext(CastExprContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterCasting(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitCasting(this);
		}
	}

	public final CastExprContext castExpr() throws RecognitionException {
		CastExprContext _localctx = new CastExprContext(_ctx, getState());
		enterRule(_localctx, 46, RULE_castExpr);
		try {
			setState(310);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,25,_ctx) ) {
			case 1:
				_localctx = new CastingContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(304);
				match(ABREPAR);
				setState(305);
				tipo();
				setState(306);
				match(FECHAPAR);
				setState(307);
				castExpr();
				}
				break;
			case 2:
				_localctx = new CastSimplesContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(309);
				primary();
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class PrimaryContext extends ParserRuleContext {
		public PrimaryContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_primary; }
	 
		public PrimaryContext() { }
		public void copyFrom(PrimaryContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ChamadaLeituraContext extends PrimaryContext {
		public ChamadaFuncaoContext chamadaFuncao() {
			return getRuleContext(ChamadaFuncaoContext.class,0);
		}
		public ChamadaLeituraContext(PrimaryContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterChamadaLeitura(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitChamadaLeitura(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ParentesesContext extends PrimaryContext {
		public TerminalNode ABREPAR() { return getToken(MOCParser.ABREPAR, 0); }
		public ExpressaoContext expressao() {
			return getRuleContext(ExpressaoContext.class,0);
		}
		public TerminalNode FECHAPAR() { return getToken(MOCParser.FECHAPAR, 0); }
		public ParentesesContext(PrimaryContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterParenteses(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitParenteses(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class NumeroContext extends PrimaryContext {
		public TerminalNode NUMERO() { return getToken(MOCParser.NUMERO, 0); }
		public NumeroContext(PrimaryContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterNumero(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitNumero(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class IdComPrefixoContext extends PrimaryContext {
		public TerminalNode IDENTIFICADOR() { return getToken(MOCParser.IDENTIFICADOR, 0); }
		public PrimaryRestContext primaryRest() {
			return getRuleContext(PrimaryRestContext.class,0);
		}
		public IdComPrefixoContext(PrimaryContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterIdComPrefixo(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitIdComPrefixo(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class NumeroRealContext extends PrimaryContext {
		public TerminalNode NUM_REAL() { return getToken(MOCParser.NUM_REAL, 0); }
		public NumeroRealContext(PrimaryContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterNumeroReal(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitNumeroReal(this);
		}
	}

	public final PrimaryContext primary() throws RecognitionException {
		PrimaryContext _localctx = new PrimaryContext(_ctx, getState());
		enterRule(_localctx, 48, RULE_primary);
		try {
			setState(321);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case ABREPAR:
				_localctx = new ParentesesContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(312);
				match(ABREPAR);
				setState(313);
				expressao();
				setState(314);
				match(FECHAPAR);
				}
				break;
			case READ:
			case READC:
			case READS:
				_localctx = new ChamadaLeituraContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(316);
				chamadaFuncao();
				}
				break;
			case NUMERO:
				_localctx = new NumeroContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				setState(317);
				match(NUMERO);
				}
				break;
			case NUM_REAL:
				_localctx = new NumeroRealContext(_localctx);
				enterOuterAlt(_localctx, 4);
				{
				setState(318);
				match(NUM_REAL);
				}
				break;
			case IDENTIFICADOR:
				_localctx = new IdComPrefixoContext(_localctx);
				enterOuterAlt(_localctx, 5);
				{
				setState(319);
				match(IDENTIFICADOR);
				setState(320);
				primaryRest();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class PrimaryRestContext extends ParserRuleContext {
		public PrimaryRestContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_primaryRest; }
	 
		public PrimaryRestContext() { }
		public void copyFrom(PrimaryRestContext ctx) {
			super.copyFrom(ctx);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class ChamadaGenericaContext extends PrimaryRestContext {
		public TerminalNode ABREPAR() { return getToken(MOCParser.ABREPAR, 0); }
		public TerminalNode FECHAPAR() { return getToken(MOCParser.FECHAPAR, 0); }
		public ArgumentosContext argumentos() {
			return getRuleContext(ArgumentosContext.class,0);
		}
		public ChamadaGenericaContext(PrimaryRestContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterChamadaGenerica(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitChamadaGenerica(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class SemSufixoContext extends PrimaryRestContext {
		public SemSufixoContext(PrimaryRestContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterSemSufixo(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitSemSufixo(this);
		}
	}
	@SuppressWarnings("CheckReturnValue")
	public static class AcessoVetorContext extends PrimaryRestContext {
		public TerminalNode ABRECOLCH() { return getToken(MOCParser.ABRECOLCH, 0); }
		public ExpressaoContext expressao() {
			return getRuleContext(ExpressaoContext.class,0);
		}
		public TerminalNode FECHACOLCH() { return getToken(MOCParser.FECHACOLCH, 0); }
		public AcessoVetorContext(PrimaryRestContext ctx) { copyFrom(ctx); }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterAcessoVetor(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitAcessoVetor(this);
		}
	}

	public final PrimaryRestContext primaryRest() throws RecognitionException {
		PrimaryRestContext _localctx = new PrimaryRestContext(_ctx, getState());
		enterRule(_localctx, 50, RULE_primaryRest);
		int _la;
		try {
			setState(333);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,28,_ctx) ) {
			case 1:
				_localctx = new ChamadaGenericaContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(323);
				match(ABREPAR);
				setState(325);
				_errHandler.sync(this);
				_la = _input.LA(1);
				if ((((_la) & ~0x3f) == 0 && ((1L << _la) & 61710627111136L) != 0)) {
					{
					setState(324);
					argumentos();
					}
				}

				setState(327);
				match(FECHAPAR);
				}
				break;
			case 2:
				_localctx = new AcessoVetorContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(328);
				match(ABRECOLCH);
				setState(329);
				expressao();
				setState(330);
				match(FECHACOLCH);
				}
				break;
			case 3:
				_localctx = new SemSufixoContext(_localctx);
				enterOuterAlt(_localctx, 3);
				{
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ArgumentosContext extends ParserRuleContext {
		public List<ExpressaoContext> expressao() {
			return getRuleContexts(ExpressaoContext.class);
		}
		public ExpressaoContext expressao(int i) {
			return getRuleContext(ExpressaoContext.class,i);
		}
		public List<TerminalNode> VIRGULA() { return getTokens(MOCParser.VIRGULA); }
		public TerminalNode VIRGULA(int i) {
			return getToken(MOCParser.VIRGULA, i);
		}
		public ArgumentosContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_argumentos; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterArgumentos(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitArgumentos(this);
		}
	}

	public final ArgumentosContext argumentos() throws RecognitionException {
		ArgumentosContext _localctx = new ArgumentosContext(_ctx, getState());
		enterRule(_localctx, 52, RULE_argumentos);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(335);
			expressao();
			setState(340);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while (_la==VIRGULA) {
				{
				{
				setState(336);
				match(VIRGULA);
				setState(337);
				expressao();
				}
				}
				setState(342);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class OpRelacionalContext extends ParserRuleContext {
		public TerminalNode MENOR() { return getToken(MOCParser.MENOR, 0); }
		public TerminalNode MENORIGUAL() { return getToken(MOCParser.MENORIGUAL, 0); }
		public TerminalNode MAIOR() { return getToken(MOCParser.MAIOR, 0); }
		public TerminalNode MAIORIGUAL() { return getToken(MOCParser.MAIORIGUAL, 0); }
		public TerminalNode IGUAL() { return getToken(MOCParser.IGUAL, 0); }
		public TerminalNode DIFERENTE() { return getToken(MOCParser.DIFERENTE, 0); }
		public OpRelacionalContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_opRelacional; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterOpRelacional(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitOpRelacional(this);
		}
	}

	public final OpRelacionalContext opRelacional() throws RecognitionException {
		OpRelacionalContext _localctx = new OpRelacionalContext(_ctx, getState());
		enterRule(_localctx, 54, RULE_opRelacional);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(343);
			_la = _input.LA(1);
			if ( !((((_la) & ~0x3f) == 0 && ((1L << _la) & 132120576L) != 0)) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ChamadaFuncaoContext extends ParserRuleContext {
		public TerminalNode READ() { return getToken(MOCParser.READ, 0); }
		public TerminalNode ABREPAR() { return getToken(MOCParser.ABREPAR, 0); }
		public TerminalNode FECHAPAR() { return getToken(MOCParser.FECHAPAR, 0); }
		public TerminalNode READC() { return getToken(MOCParser.READC, 0); }
		public TerminalNode READS() { return getToken(MOCParser.READS, 0); }
		public ChamadaFuncaoContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_chamadaFuncao; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterChamadaFuncao(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitChamadaFuncao(this);
		}
	}

	public final ChamadaFuncaoContext chamadaFuncao() throws RecognitionException {
		ChamadaFuncaoContext _localctx = new ChamadaFuncaoContext(_ctx, getState());
		enterRule(_localctx, 56, RULE_chamadaFuncao);
		try {
			setState(354);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case READ:
				enterOuterAlt(_localctx, 1);
				{
				setState(345);
				match(READ);
				setState(346);
				match(ABREPAR);
				setState(347);
				match(FECHAPAR);
				}
				break;
			case READC:
				enterOuterAlt(_localctx, 2);
				{
				setState(348);
				match(READC);
				setState(349);
				match(ABREPAR);
				setState(350);
				match(FECHAPAR);
				}
				break;
			case READS:
				enterOuterAlt(_localctx, 3);
				{
				setState(351);
				match(READS);
				setState(352);
				match(ABREPAR);
				setState(353);
				match(FECHAPAR);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ChamadaReadsContext extends ParserRuleContext {
		public TerminalNode READS() { return getToken(MOCParser.READS, 0); }
		public TerminalNode ABREPAR() { return getToken(MOCParser.ABREPAR, 0); }
		public TerminalNode FECHAPAR() { return getToken(MOCParser.FECHAPAR, 0); }
		public ChamadaReadsContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_chamadaReads; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterChamadaReads(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitChamadaReads(this);
		}
	}

	public final ChamadaReadsContext chamadaReads() throws RecognitionException {
		ChamadaReadsContext _localctx = new ChamadaReadsContext(_ctx, getState());
		enterRule(_localctx, 58, RULE_chamadaReads);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(356);
			match(READS);
			setState(357);
			match(ABREPAR);
			setState(358);
			match(FECHAPAR);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class BlocoContext extends ParserRuleContext {
		public TerminalNode ABRECHAVES() { return getToken(MOCParser.ABRECHAVES, 0); }
		public InstrucoesContext instrucoes() {
			return getRuleContext(InstrucoesContext.class,0);
		}
		public TerminalNode FECHACHAVES() { return getToken(MOCParser.FECHACHAVES, 0); }
		public BlocoContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_bloco; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterBloco(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitBloco(this);
		}
	}

	public final BlocoContext bloco() throws RecognitionException {
		BlocoContext _localctx = new BlocoContext(_ctx, getState());
		enterRule(_localctx, 60, RULE_bloco);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(360);
			match(ABRECHAVES);
			setState(361);
			instrucoes();
			setState(362);
			match(FECHACHAVES);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class InstrucoesContext extends ParserRuleContext {
		public List<InstrucaoContext> instrucao() {
			return getRuleContexts(InstrucaoContext.class);
		}
		public InstrucaoContext instrucao(int i) {
			return getRuleContext(InstrucaoContext.class,i);
		}
		public InstrucoesContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_instrucoes; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterInstrucoes(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitInstrucoes(this);
		}
	}

	public final InstrucoesContext instrucoes() throws RecognitionException {
		InstrucoesContext _localctx = new InstrucoesContext(_ctx, getState());
		enterRule(_localctx, 62, RULE_instrucoes);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(367);
			_errHandler.sync(this);
			_la = _input.LA(1);
			while ((((_la) & ~0x3f) == 0 && ((1L << _la) & 62294742720494L) != 0)) {
				{
				{
				setState(364);
				instrucao();
				}
				}
				setState(369);
				_errHandler.sync(this);
				_la = _input.LA(1);
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class InstrucaoContext extends ParserRuleContext {
		public InstrucaoEmparelhadaContext instrucaoEmparelhada() {
			return getRuleContext(InstrucaoEmparelhadaContext.class,0);
		}
		public InstrucaoPorEmparelharContext instrucaoPorEmparelhar() {
			return getRuleContext(InstrucaoPorEmparelharContext.class,0);
		}
		public OutraInstrucaoContext outraInstrucao() {
			return getRuleContext(OutraInstrucaoContext.class,0);
		}
		public InstrucaoContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_instrucao; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterInstrucao(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitInstrucao(this);
		}
	}

	public final InstrucaoContext instrucao() throws RecognitionException {
		InstrucaoContext _localctx = new InstrucaoContext(_ctx, getState());
		enterRule(_localctx, 64, RULE_instrucao);
		try {
			setState(373);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,32,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(370);
				instrucaoEmparelhada();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(371);
				instrucaoPorEmparelhar();
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(372);
				outraInstrucao();
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class InstrucaoExpressaoContext extends ParserRuleContext {
		public ExpressaoContext expressao() {
			return getRuleContext(ExpressaoContext.class,0);
		}
		public TerminalNode PONTOVIRG() { return getToken(MOCParser.PONTOVIRG, 0); }
		public InstrucaoExpressaoContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_instrucaoExpressao; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterInstrucaoExpressao(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitInstrucaoExpressao(this);
		}
	}

	public final InstrucaoExpressaoContext instrucaoExpressao() throws RecognitionException {
		InstrucaoExpressaoContext _localctx = new InstrucaoExpressaoContext(_ctx, getState());
		enterRule(_localctx, 66, RULE_instrucaoExpressao);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(375);
			expressao();
			setState(376);
			match(PONTOVIRG);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class InstrucaoEmparelhadaContext extends ParserRuleContext {
		public TerminalNode IF() { return getToken(MOCParser.IF, 0); }
		public TerminalNode ABREPAR() { return getToken(MOCParser.ABREPAR, 0); }
		public ExpressaoContext expressao() {
			return getRuleContext(ExpressaoContext.class,0);
		}
		public TerminalNode FECHAPAR() { return getToken(MOCParser.FECHAPAR, 0); }
		public BlocoContext bloco() {
			return getRuleContext(BlocoContext.class,0);
		}
		public TerminalNode ELSE() { return getToken(MOCParser.ELSE, 0); }
		public InstrucaoEmparelhadaContext instrucaoEmparelhada() {
			return getRuleContext(InstrucaoEmparelhadaContext.class,0);
		}
		public InstrucaoEmparelhadaContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_instrucaoEmparelhada; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterInstrucaoEmparelhada(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitInstrucaoEmparelhada(this);
		}
	}

	public final InstrucaoEmparelhadaContext instrucaoEmparelhada() throws RecognitionException {
		InstrucaoEmparelhadaContext _localctx = new InstrucaoEmparelhadaContext(_ctx, getState());
		enterRule(_localctx, 68, RULE_instrucaoEmparelhada);
		try {
			setState(387);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case IF:
				enterOuterAlt(_localctx, 1);
				{
				setState(378);
				match(IF);
				setState(379);
				match(ABREPAR);
				setState(380);
				expressao();
				setState(381);
				match(FECHAPAR);
				setState(382);
				bloco();
				setState(383);
				match(ELSE);
				setState(384);
				instrucaoEmparelhada();
				}
				break;
			case ABRECHAVES:
				enterOuterAlt(_localctx, 2);
				{
				setState(386);
				bloco();
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class InstrucaoPorEmparelharContext extends ParserRuleContext {
		public TerminalNode IF() { return getToken(MOCParser.IF, 0); }
		public TerminalNode ABREPAR() { return getToken(MOCParser.ABREPAR, 0); }
		public ExpressaoContext expressao() {
			return getRuleContext(ExpressaoContext.class,0);
		}
		public TerminalNode FECHAPAR() { return getToken(MOCParser.FECHAPAR, 0); }
		public BlocoContext bloco() {
			return getRuleContext(BlocoContext.class,0);
		}
		public TerminalNode ELSE() { return getToken(MOCParser.ELSE, 0); }
		public InstrucaoPorEmparelharContext instrucaoPorEmparelhar() {
			return getRuleContext(InstrucaoPorEmparelharContext.class,0);
		}
		public InstrucaoPorEmparelharContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_instrucaoPorEmparelhar; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterInstrucaoPorEmparelhar(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitInstrucaoPorEmparelhar(this);
		}
	}

	public final InstrucaoPorEmparelharContext instrucaoPorEmparelhar() throws RecognitionException {
		InstrucaoPorEmparelharContext _localctx = new InstrucaoPorEmparelharContext(_ctx, getState());
		enterRule(_localctx, 70, RULE_instrucaoPorEmparelhar);
		try {
			setState(403);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,34,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(389);
				match(IF);
				setState(390);
				match(ABREPAR);
				setState(391);
				expressao();
				setState(392);
				match(FECHAPAR);
				setState(393);
				bloco();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(395);
				match(IF);
				setState(396);
				match(ABREPAR);
				setState(397);
				expressao();
				setState(398);
				match(FECHAPAR);
				setState(399);
				bloco();
				setState(400);
				match(ELSE);
				setState(401);
				instrucaoPorEmparelhar();
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class OutraInstrucaoContext extends ParserRuleContext {
		public BlocoContext bloco() {
			return getRuleContext(BlocoContext.class,0);
		}
		public DeclaracaoContext declaracao() {
			return getRuleContext(DeclaracaoContext.class,0);
		}
		public InstrucaoWhileContext instrucaoWhile() {
			return getRuleContext(InstrucaoWhileContext.class,0);
		}
		public InstrucaoForContext instrucaoFor() {
			return getRuleContext(InstrucaoForContext.class,0);
		}
		public InstrucaoEscritaContext instrucaoEscrita() {
			return getRuleContext(InstrucaoEscritaContext.class,0);
		}
		public InstrucaoReturnContext instrucaoReturn() {
			return getRuleContext(InstrucaoReturnContext.class,0);
		}
		public InstrucaoAtribuicaoContext instrucaoAtribuicao() {
			return getRuleContext(InstrucaoAtribuicaoContext.class,0);
		}
		public InstrucaoExpressaoContext instrucaoExpressao() {
			return getRuleContext(InstrucaoExpressaoContext.class,0);
		}
		public OutraInstrucaoContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_outraInstrucao; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterOutraInstrucao(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitOutraInstrucao(this);
		}
	}

	public final OutraInstrucaoContext outraInstrucao() throws RecognitionException {
		OutraInstrucaoContext _localctx = new OutraInstrucaoContext(_ctx, getState());
		enterRule(_localctx, 72, RULE_outraInstrucao);
		try {
			setState(413);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,35,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(405);
				bloco();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(406);
				declaracao();
				}
				break;
			case 3:
				enterOuterAlt(_localctx, 3);
				{
				setState(407);
				instrucaoWhile();
				}
				break;
			case 4:
				enterOuterAlt(_localctx, 4);
				{
				setState(408);
				instrucaoFor();
				}
				break;
			case 5:
				enterOuterAlt(_localctx, 5);
				{
				setState(409);
				instrucaoEscrita();
				}
				break;
			case 6:
				enterOuterAlt(_localctx, 6);
				{
				setState(410);
				instrucaoReturn();
				}
				break;
			case 7:
				enterOuterAlt(_localctx, 7);
				{
				setState(411);
				instrucaoAtribuicao();
				}
				break;
			case 8:
				enterOuterAlt(_localctx, 8);
				{
				setState(412);
				instrucaoExpressao();
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class InstrucaoWhileContext extends ParserRuleContext {
		public TerminalNode WHILE() { return getToken(MOCParser.WHILE, 0); }
		public TerminalNode ABREPAR() { return getToken(MOCParser.ABREPAR, 0); }
		public ExpressaoContext expressao() {
			return getRuleContext(ExpressaoContext.class,0);
		}
		public TerminalNode FECHAPAR() { return getToken(MOCParser.FECHAPAR, 0); }
		public BlocoContext bloco() {
			return getRuleContext(BlocoContext.class,0);
		}
		public InstrucaoWhileContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_instrucaoWhile; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterInstrucaoWhile(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitInstrucaoWhile(this);
		}
	}

	public final InstrucaoWhileContext instrucaoWhile() throws RecognitionException {
		InstrucaoWhileContext _localctx = new InstrucaoWhileContext(_ctx, getState());
		enterRule(_localctx, 74, RULE_instrucaoWhile);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(415);
			match(WHILE);
			setState(416);
			match(ABREPAR);
			setState(417);
			expressao();
			setState(418);
			match(FECHAPAR);
			setState(419);
			bloco();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class InstrucaoForContext extends ParserRuleContext {
		public TerminalNode FOR() { return getToken(MOCParser.FOR, 0); }
		public TerminalNode ABREPAR() { return getToken(MOCParser.ABREPAR, 0); }
		public List<TerminalNode> PONTOVIRG() { return getTokens(MOCParser.PONTOVIRG); }
		public TerminalNode PONTOVIRG(int i) {
			return getToken(MOCParser.PONTOVIRG, i);
		}
		public TerminalNode FECHAPAR() { return getToken(MOCParser.FECHAPAR, 0); }
		public BlocoContext bloco() {
			return getRuleContext(BlocoContext.class,0);
		}
		public List<ExpressaoOuAtribuicaoContext> expressaoOuAtribuicao() {
			return getRuleContexts(ExpressaoOuAtribuicaoContext.class);
		}
		public ExpressaoOuAtribuicaoContext expressaoOuAtribuicao(int i) {
			return getRuleContext(ExpressaoOuAtribuicaoContext.class,i);
		}
		public ExpressaoContext expressao() {
			return getRuleContext(ExpressaoContext.class,0);
		}
		public InstrucaoForContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_instrucaoFor; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterInstrucaoFor(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitInstrucaoFor(this);
		}
	}

	public final InstrucaoForContext instrucaoFor() throws RecognitionException {
		InstrucaoForContext _localctx = new InstrucaoForContext(_ctx, getState());
		enterRule(_localctx, 76, RULE_instrucaoFor);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(421);
			match(FOR);
			setState(422);
			match(ABREPAR);
			setState(424);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if ((((_la) & ~0x3f) == 0 && ((1L << _la) & 61710627111136L) != 0)) {
				{
				setState(423);
				expressaoOuAtribuicao();
				}
			}

			setState(426);
			match(PONTOVIRG);
			setState(428);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if ((((_la) & ~0x3f) == 0 && ((1L << _la) & 61710627111136L) != 0)) {
				{
				setState(427);
				expressao();
				}
			}

			setState(430);
			match(PONTOVIRG);
			setState(432);
			_errHandler.sync(this);
			_la = _input.LA(1);
			if ((((_la) & ~0x3f) == 0 && ((1L << _la) & 61710627111136L) != 0)) {
				{
				setState(431);
				expressaoOuAtribuicao();
				}
			}

			setState(434);
			match(FECHAPAR);
			setState(435);
			bloco();
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ExpressaoOuAtribuicaoContext extends ParserRuleContext {
		public TerminalNode IDENTIFICADOR() { return getToken(MOCParser.IDENTIFICADOR, 0); }
		public TerminalNode ATRIBUICAO() { return getToken(MOCParser.ATRIBUICAO, 0); }
		public ExpressaoContext expressao() {
			return getRuleContext(ExpressaoContext.class,0);
		}
		public ExpressaoOuAtribuicaoContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_expressaoOuAtribuicao; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterExpressaoOuAtribuicao(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitExpressaoOuAtribuicao(this);
		}
	}

	public final ExpressaoOuAtribuicaoContext expressaoOuAtribuicao() throws RecognitionException {
		ExpressaoOuAtribuicaoContext _localctx = new ExpressaoOuAtribuicaoContext(_ctx, getState());
		enterRule(_localctx, 78, RULE_expressaoOuAtribuicao);
		try {
			setState(441);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,39,_ctx) ) {
			case 1:
				enterOuterAlt(_localctx, 1);
				{
				setState(437);
				match(IDENTIFICADOR);
				setState(438);
				match(ATRIBUICAO);
				setState(439);
				expressao();
				}
				break;
			case 2:
				enterOuterAlt(_localctx, 2);
				{
				setState(440);
				expressao();
				}
				break;
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class InstrucaoEscritaContext extends ParserRuleContext {
		public TerminalNode WRITE() { return getToken(MOCParser.WRITE, 0); }
		public TerminalNode ABREPAR() { return getToken(MOCParser.ABREPAR, 0); }
		public ExpressaoContext expressao() {
			return getRuleContext(ExpressaoContext.class,0);
		}
		public TerminalNode FECHAPAR() { return getToken(MOCParser.FECHAPAR, 0); }
		public TerminalNode PONTOVIRG() { return getToken(MOCParser.PONTOVIRG, 0); }
		public TerminalNode WRITEC() { return getToken(MOCParser.WRITEC, 0); }
		public TerminalNode WRITEV() { return getToken(MOCParser.WRITEV, 0); }
		public TerminalNode IDENTIFICADOR() { return getToken(MOCParser.IDENTIFICADOR, 0); }
		public TerminalNode WRITES() { return getToken(MOCParser.WRITES, 0); }
		public ArgumentoStringContext argumentoString() {
			return getRuleContext(ArgumentoStringContext.class,0);
		}
		public InstrucaoEscritaContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_instrucaoEscrita; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterInstrucaoEscrita(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitInstrucaoEscrita(this);
		}
	}

	public final InstrucaoEscritaContext instrucaoEscrita() throws RecognitionException {
		InstrucaoEscritaContext _localctx = new InstrucaoEscritaContext(_ctx, getState());
		enterRule(_localctx, 80, RULE_instrucaoEscrita);
		try {
			setState(466);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case WRITE:
				enterOuterAlt(_localctx, 1);
				{
				setState(443);
				match(WRITE);
				setState(444);
				match(ABREPAR);
				setState(445);
				expressao();
				setState(446);
				match(FECHAPAR);
				setState(447);
				match(PONTOVIRG);
				}
				break;
			case WRITEC:
				enterOuterAlt(_localctx, 2);
				{
				setState(449);
				match(WRITEC);
				setState(450);
				match(ABREPAR);
				setState(451);
				expressao();
				setState(452);
				match(FECHAPAR);
				setState(453);
				match(PONTOVIRG);
				}
				break;
			case WRITEV:
				enterOuterAlt(_localctx, 3);
				{
				setState(455);
				match(WRITEV);
				setState(456);
				match(ABREPAR);
				setState(457);
				match(IDENTIFICADOR);
				setState(458);
				match(FECHAPAR);
				setState(459);
				match(PONTOVIRG);
				}
				break;
			case WRITES:
				enterOuterAlt(_localctx, 4);
				{
				setState(460);
				match(WRITES);
				setState(461);
				match(ABREPAR);
				setState(462);
				argumentoString();
				setState(463);
				match(FECHAPAR);
				setState(464);
				match(PONTOVIRG);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class InstrucaoReturnContext extends ParserRuleContext {
		public TerminalNode RETURN() { return getToken(MOCParser.RETURN, 0); }
		public ExpressaoContext expressao() {
			return getRuleContext(ExpressaoContext.class,0);
		}
		public TerminalNode PONTOVIRG() { return getToken(MOCParser.PONTOVIRG, 0); }
		public InstrucaoReturnContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_instrucaoReturn; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterInstrucaoReturn(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitInstrucaoReturn(this);
		}
	}

	public final InstrucaoReturnContext instrucaoReturn() throws RecognitionException {
		InstrucaoReturnContext _localctx = new InstrucaoReturnContext(_ctx, getState());
		enterRule(_localctx, 82, RULE_instrucaoReturn);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(468);
			match(RETURN);
			setState(469);
			expressao();
			setState(470);
			match(PONTOVIRG);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class InstrucaoAtribuicaoContext extends ParserRuleContext {
		public TerminalNode ATRIBUICAO() { return getToken(MOCParser.ATRIBUICAO, 0); }
		public List<ExpressaoContext> expressao() {
			return getRuleContexts(ExpressaoContext.class);
		}
		public ExpressaoContext expressao(int i) {
			return getRuleContext(ExpressaoContext.class,i);
		}
		public TerminalNode PONTOVIRG() { return getToken(MOCParser.PONTOVIRG, 0); }
		public TerminalNode IDENTIFICADOR() { return getToken(MOCParser.IDENTIFICADOR, 0); }
		public TerminalNode ABRECOLCH() { return getToken(MOCParser.ABRECOLCH, 0); }
		public TerminalNode FECHACOLCH() { return getToken(MOCParser.FECHACOLCH, 0); }
		public InstrucaoAtribuicaoContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_instrucaoAtribuicao; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterInstrucaoAtribuicao(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitInstrucaoAtribuicao(this);
		}
	}

	public final InstrucaoAtribuicaoContext instrucaoAtribuicao() throws RecognitionException {
		InstrucaoAtribuicaoContext _localctx = new InstrucaoAtribuicaoContext(_ctx, getState());
		enterRule(_localctx, 84, RULE_instrucaoAtribuicao);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(478);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,41,_ctx) ) {
			case 1:
				{
				setState(472);
				match(IDENTIFICADOR);
				}
				break;
			case 2:
				{
				setState(473);
				match(IDENTIFICADOR);
				setState(474);
				match(ABRECOLCH);
				setState(475);
				expressao();
				setState(476);
				match(FECHACOLCH);
				}
				break;
			}
			setState(480);
			match(ATRIBUICAO);
			setState(481);
			expressao();
			setState(482);
			match(PONTOVIRG);
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	@SuppressWarnings("CheckReturnValue")
	public static class ArgumentoStringContext extends ParserRuleContext {
		public TerminalNode IDENTIFICADOR() { return getToken(MOCParser.IDENTIFICADOR, 0); }
		public TerminalNode STRINGLITERAL() { return getToken(MOCParser.STRINGLITERAL, 0); }
		public ArgumentoStringContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_argumentoString; }
		@Override
		public void enterRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).enterArgumentoString(this);
		}
		@Override
		public void exitRule(ParseTreeListener listener) {
			if ( listener instanceof MOCListener ) ((MOCListener)listener).exitArgumentoString(this);
		}
	}

	public final ArgumentoStringContext argumentoString() throws RecognitionException {
		ArgumentoStringContext _localctx = new ArgumentoStringContext(_ctx, getState());
		enterRule(_localctx, 86, RULE_argumentoString);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(484);
			_la = _input.LA(1);
			if ( !(_la==STRINGLITERAL || _la==IDENTIFICADOR) ) {
			_errHandler.recoverInline(this);
			}
			else {
				if ( _input.LA(1)==Token.EOF ) matchedEOF = true;
				_errHandler.reportMatch(this);
				consume();
			}
			}
		}
		catch (RecognitionException re) {
			_localctx.exception = re;
			_errHandler.reportError(this, re);
			_errHandler.recover(this, re);
		}
		finally {
			exitRule();
		}
		return _localctx;
	}

	public boolean sempred(RuleContext _localctx, int ruleIndex, int predIndex) {
		switch (ruleIndex) {
		case 17:
			return expressaoOr_sempred((ExpressaoOrContext)_localctx, predIndex);
		case 18:
			return expressaoAnd_sempred((ExpressaoAndContext)_localctx, predIndex);
		case 20:
			return expressaoAdd_sempred((ExpressaoAddContext)_localctx, predIndex);
		case 21:
			return expressaoMul_sempred((ExpressaoMulContext)_localctx, predIndex);
		}
		return true;
	}
	private boolean expressaoOr_sempred(ExpressaoOrContext _localctx, int predIndex) {
		switch (predIndex) {
		case 0:
			return precpred(_ctx, 2);
		}
		return true;
	}
	private boolean expressaoAnd_sempred(ExpressaoAndContext _localctx, int predIndex) {
		switch (predIndex) {
		case 1:
			return precpred(_ctx, 2);
		}
		return true;
	}
	private boolean expressaoAdd_sempred(ExpressaoAddContext _localctx, int predIndex) {
		switch (predIndex) {
		case 2:
			return precpred(_ctx, 3);
		case 3:
			return precpred(_ctx, 2);
		}
		return true;
	}
	private boolean expressaoMul_sempred(ExpressaoMulContext _localctx, int predIndex) {
		switch (predIndex) {
		case 4:
			return precpred(_ctx, 4);
		case 5:
			return precpred(_ctx, 3);
		case 6:
			return precpred(_ctx, 2);
		}
		return true;
	}

	public static final String _serializedATN =
		"\u0004\u0001.\u01e7\u0002\u0000\u0007\u0000\u0002\u0001\u0007\u0001\u0002"+
		"\u0002\u0007\u0002\u0002\u0003\u0007\u0003\u0002\u0004\u0007\u0004\u0002"+
		"\u0005\u0007\u0005\u0002\u0006\u0007\u0006\u0002\u0007\u0007\u0007\u0002"+
		"\b\u0007\b\u0002\t\u0007\t\u0002\n\u0007\n\u0002\u000b\u0007\u000b\u0002"+
		"\f\u0007\f\u0002\r\u0007\r\u0002\u000e\u0007\u000e\u0002\u000f\u0007\u000f"+
		"\u0002\u0010\u0007\u0010\u0002\u0011\u0007\u0011\u0002\u0012\u0007\u0012"+
		"\u0002\u0013\u0007\u0013\u0002\u0014\u0007\u0014\u0002\u0015\u0007\u0015"+
		"\u0002\u0016\u0007\u0016\u0002\u0017\u0007\u0017\u0002\u0018\u0007\u0018"+
		"\u0002\u0019\u0007\u0019\u0002\u001a\u0007\u001a\u0002\u001b\u0007\u001b"+
		"\u0002\u001c\u0007\u001c\u0002\u001d\u0007\u001d\u0002\u001e\u0007\u001e"+
		"\u0002\u001f\u0007\u001f\u0002 \u0007 \u0002!\u0007!\u0002\"\u0007\"\u0002"+
		"#\u0007#\u0002$\u0007$\u0002%\u0007%\u0002&\u0007&\u0002\'\u0007\'\u0002"+
		"(\u0007(\u0002)\u0007)\u0002*\u0007*\u0002+\u0007+\u0001\u0000\u0001\u0000"+
		"\u0001\u0000\u0001\u0000\u0001\u0001\u0001\u0001\u0005\u0001_\b\u0001"+
		"\n\u0001\f\u0001b\t\u0001\u0001\u0001\u0001\u0001\u0001\u0001\u0005\u0001"+
		"g\b\u0001\n\u0001\f\u0001j\t\u0001\u0001\u0002\u0005\u0002m\b\u0002\n"+
		"\u0002\f\u0002p\t\u0002\u0001\u0002\u0001\u0002\u0001\u0003\u0001\u0003"+
		"\u0003\u0003v\b\u0003\u0001\u0004\u0001\u0004\u0001\u0004\u0001\u0004"+
		"\u0003\u0004|\b\u0004\u0001\u0004\u0001\u0004\u0001\u0004\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0005\u0003\u0005\u0085\b\u0005\u0001\u0005"+
		"\u0001\u0005\u0001\u0005\u0001\u0006\u0001\u0006\u0001\u0006\u0001\u0006"+
		"\u0003\u0006\u008e\b\u0006\u0001\u0006\u0001\u0006\u0001\u0006\u0001\u0007"+
		"\u0001\u0007\u0001\u0007\u0001\u0007\u0003\u0007\u0097\b\u0007\u0001\u0007"+
		"\u0001\u0007\u0001\u0007\u0001\b\u0001\b\u0001\b\u0001\b\u0001\b\u0005"+
		"\b\u00a1\b\b\n\b\f\b\u00a4\t\b\u0003\b\u00a6\b\b\u0001\t\u0001\t\u0001"+
		"\t\u0001\t\u0001\t\u0001\t\u0001\t\u0001\t\u0001\t\u0001\t\u0001\t\u0001"+
		"\t\u0001\t\u0003\t\u00b5\b\t\u0001\n\u0001\n\u0001\u000b\u0001\u000b\u0001"+
		"\u000b\u0001\u000b\u0001\f\u0001\f\u0001\f\u0005\f\u00c0\b\f\n\f\f\f\u00c3"+
		"\t\f\u0001\r\u0001\r\u0001\r\u0001\r\u0001\r\u0001\r\u0001\r\u0001\r\u0001"+
		"\r\u0001\r\u0001\r\u0001\r\u0001\r\u0001\r\u0001\r\u0001\r\u0001\r\u0001"+
		"\r\u0001\r\u0001\r\u0001\r\u0001\r\u0001\r\u0001\r\u0003\r\u00dd\b\r\u0001"+
		"\u000e\u0001\u000e\u0003\u000e\u00e1\b\u000e\u0001\u000e\u0001\u000e\u0001"+
		"\u000f\u0001\u000f\u0001\u000f\u0005\u000f\u00e8\b\u000f\n\u000f\f\u000f"+
		"\u00eb\t\u000f\u0001\u0010\u0001\u0010\u0001\u0011\u0001\u0011\u0001\u0011"+
		"\u0001\u0011\u0001\u0011\u0001\u0011\u0005\u0011\u00f5\b\u0011\n\u0011"+
		"\f\u0011\u00f8\t\u0011\u0001\u0012\u0001\u0012\u0001\u0012\u0001\u0012"+
		"\u0001\u0012\u0001\u0012\u0005\u0012\u0100\b\u0012\n\u0012\f\u0012\u0103"+
		"\t\u0012\u0001\u0013\u0001\u0013\u0001\u0013\u0001\u0013\u0003\u0013\u0109"+
		"\b\u0013\u0001\u0014\u0001\u0014\u0001\u0014\u0001\u0014\u0001\u0014\u0001"+
		"\u0014\u0001\u0014\u0001\u0014\u0001\u0014\u0005\u0014\u0114\b\u0014\n"+
		"\u0014\f\u0014\u0117\t\u0014\u0001\u0015\u0001\u0015\u0001\u0015\u0001"+
		"\u0015\u0001\u0015\u0001\u0015\u0001\u0015\u0001\u0015\u0001\u0015\u0001"+
		"\u0015\u0001\u0015\u0001\u0015\u0005\u0015\u0125\b\u0015\n\u0015\f\u0015"+
		"\u0128\t\u0015\u0001\u0016\u0001\u0016\u0001\u0016\u0001\u0016\u0001\u0016"+
		"\u0003\u0016\u012f\b\u0016\u0001\u0017\u0001\u0017\u0001\u0017\u0001\u0017"+
		"\u0001\u0017\u0001\u0017\u0003\u0017\u0137\b\u0017\u0001\u0018\u0001\u0018"+
		"\u0001\u0018\u0001\u0018\u0001\u0018\u0001\u0018\u0001\u0018\u0001\u0018"+
		"\u0001\u0018\u0003\u0018\u0142\b\u0018\u0001\u0019\u0001\u0019\u0003\u0019"+
		"\u0146\b\u0019\u0001\u0019\u0001\u0019\u0001\u0019\u0001\u0019\u0001\u0019"+
		"\u0001\u0019\u0003\u0019\u014e\b\u0019\u0001\u001a\u0001\u001a\u0001\u001a"+
		"\u0005\u001a\u0153\b\u001a\n\u001a\f\u001a\u0156\t\u001a\u0001\u001b\u0001"+
		"\u001b\u0001\u001c\u0001\u001c\u0001\u001c\u0001\u001c\u0001\u001c\u0001"+
		"\u001c\u0001\u001c\u0001\u001c\u0001\u001c\u0003\u001c\u0163\b\u001c\u0001"+
		"\u001d\u0001\u001d\u0001\u001d\u0001\u001d\u0001\u001e\u0001\u001e\u0001"+
		"\u001e\u0001\u001e\u0001\u001f\u0005\u001f\u016e\b\u001f\n\u001f\f\u001f"+
		"\u0171\t\u001f\u0001 \u0001 \u0001 \u0003 \u0176\b \u0001!\u0001!\u0001"+
		"!\u0001\"\u0001\"\u0001\"\u0001\"\u0001\"\u0001\"\u0001\"\u0001\"\u0001"+
		"\"\u0003\"\u0184\b\"\u0001#\u0001#\u0001#\u0001#\u0001#\u0001#\u0001#"+
		"\u0001#\u0001#\u0001#\u0001#\u0001#\u0001#\u0001#\u0003#\u0194\b#\u0001"+
		"$\u0001$\u0001$\u0001$\u0001$\u0001$\u0001$\u0001$\u0003$\u019e\b$\u0001"+
		"%\u0001%\u0001%\u0001%\u0001%\u0001%\u0001&\u0001&\u0001&\u0003&\u01a9"+
		"\b&\u0001&\u0001&\u0003&\u01ad\b&\u0001&\u0001&\u0003&\u01b1\b&\u0001"+
		"&\u0001&\u0001&\u0001\'\u0001\'\u0001\'\u0001\'\u0003\'\u01ba\b\'\u0001"+
		"(\u0001(\u0001(\u0001(\u0001(\u0001(\u0001(\u0001(\u0001(\u0001(\u0001"+
		"(\u0001(\u0001(\u0001(\u0001(\u0001(\u0001(\u0001(\u0001(\u0001(\u0001"+
		"(\u0001(\u0001(\u0003(\u01d3\b(\u0001)\u0001)\u0001)\u0001)\u0001*\u0001"+
		"*\u0001*\u0001*\u0001*\u0001*\u0003*\u01df\b*\u0001*\u0001*\u0001*\u0001"+
		"*\u0001+\u0001+\u0001+\u0000\u0004\"$(*,\u0000\u0002\u0004\u0006\b\n\f"+
		"\u000e\u0010\u0012\u0014\u0016\u0018\u001a\u001c\u001e \"$&(*,.02468:"+
		"<>@BDFHJLNPRTV\u0000\u0003\u0001\u0000\u0001\u0003\u0001\u0000\u0015\u001a"+
		"\u0002\u0000((--\u01fb\u0000X\u0001\u0000\u0000\u0000\u0002`\u0001\u0000"+
		"\u0000\u0000\u0004n\u0001\u0000\u0000\u0000\u0006u\u0001\u0000\u0000\u0000"+
		"\bw\u0001\u0000\u0000\u0000\n\u0080\u0001\u0000\u0000\u0000\f\u0089\u0001"+
		"\u0000\u0000\u0000\u000e\u0092\u0001\u0000\u0000\u0000\u0010\u00a5\u0001"+
		"\u0000\u0000\u0000\u0012\u00b4\u0001\u0000\u0000\u0000\u0014\u00b6\u0001"+
		"\u0000\u0000\u0000\u0016\u00b8\u0001\u0000\u0000\u0000\u0018\u00bc\u0001"+
		"\u0000\u0000\u0000\u001a\u00dc\u0001\u0000\u0000\u0000\u001c\u00de\u0001"+
		"\u0000\u0000\u0000\u001e\u00e4\u0001\u0000\u0000\u0000 \u00ec\u0001\u0000"+
		"\u0000\u0000\"\u00ee\u0001\u0000\u0000\u0000$\u00f9\u0001\u0000\u0000"+
		"\u0000&\u0104\u0001\u0000\u0000\u0000(\u010a\u0001\u0000\u0000\u0000*"+
		"\u0118\u0001\u0000\u0000\u0000,\u012e\u0001\u0000\u0000\u0000.\u0136\u0001"+
		"\u0000\u0000\u00000\u0141\u0001\u0000\u0000\u00002\u014d\u0001\u0000\u0000"+
		"\u00004\u014f\u0001\u0000\u0000\u00006\u0157\u0001\u0000\u0000\u00008"+
		"\u0162\u0001\u0000\u0000\u0000:\u0164\u0001\u0000\u0000\u0000<\u0168\u0001"+
		"\u0000\u0000\u0000>\u016f\u0001\u0000\u0000\u0000@\u0175\u0001\u0000\u0000"+
		"\u0000B\u0177\u0001\u0000\u0000\u0000D\u0183\u0001\u0000\u0000\u0000F"+
		"\u0193\u0001\u0000\u0000\u0000H\u019d\u0001\u0000\u0000\u0000J\u019f\u0001"+
		"\u0000\u0000\u0000L\u01a5\u0001\u0000\u0000\u0000N\u01b9\u0001\u0000\u0000"+
		"\u0000P\u01d2\u0001\u0000\u0000\u0000R\u01d4\u0001\u0000\u0000\u0000T"+
		"\u01de\u0001\u0000\u0000\u0000V\u01e4\u0001\u0000\u0000\u0000XY\u0003"+
		"\u0002\u0001\u0000YZ\u0003\u0004\u0002\u0000Z[\u0005\u0000\u0000\u0001"+
		"[\u0001\u0001\u0000\u0000\u0000\\_\u0003\b\u0004\u0000]_\u0003\n\u0005"+
		"\u0000^\\\u0001\u0000\u0000\u0000^]\u0001\u0000\u0000\u0000_b\u0001\u0000"+
		"\u0000\u0000`^\u0001\u0000\u0000\u0000`a\u0001\u0000\u0000\u0000ac\u0001"+
		"\u0000\u0000\u0000b`\u0001\u0000\u0000\u0000ch\u0003\n\u0005\u0000dg\u0003"+
		"\b\u0004\u0000eg\u0003\n\u0005\u0000fd\u0001\u0000\u0000\u0000fe\u0001"+
		"\u0000\u0000\u0000gj\u0001\u0000\u0000\u0000hf\u0001\u0000\u0000\u0000"+
		"hi\u0001\u0000\u0000\u0000i\u0003\u0001\u0000\u0000\u0000jh\u0001\u0000"+
		"\u0000\u0000km\u0003\u0006\u0003\u0000lk\u0001\u0000\u0000\u0000mp\u0001"+
		"\u0000\u0000\u0000nl\u0001\u0000\u0000\u0000no\u0001\u0000\u0000\u0000"+
		"oq\u0001\u0000\u0000\u0000pn\u0001\u0000\u0000\u0000qr\u0003\f\u0006\u0000"+
		"r\u0005\u0001\u0000\u0000\u0000sv\u0003\u000e\u0007\u0000tv\u0003\u0016"+
		"\u000b\u0000us\u0001\u0000\u0000\u0000ut\u0001\u0000\u0000\u0000v\u0007"+
		"\u0001\u0000\u0000\u0000wx\u0003\u0014\n\u0000xy\u0005-\u0000\u0000y{"+
		"\u0005%\u0000\u0000z|\u0003\u0010\b\u0000{z\u0001\u0000\u0000\u0000{|"+
		"\u0001\u0000\u0000\u0000|}\u0001\u0000\u0000\u0000}~\u0005&\u0000\u0000"+
		"~\u007f\u0005 \u0000\u0000\u007f\t\u0001\u0000\u0000\u0000\u0080\u0081"+
		"\u0003\u0014\n\u0000\u0081\u0082\u0005\u0004\u0000\u0000\u0082\u0084\u0005"+
		"%\u0000\u0000\u0083\u0085\u0003\u0010\b\u0000\u0084\u0083\u0001\u0000"+
		"\u0000\u0000\u0084\u0085\u0001\u0000\u0000\u0000\u0085\u0086\u0001\u0000"+
		"\u0000\u0000\u0086\u0087\u0005&\u0000\u0000\u0087\u0088\u0005 \u0000\u0000"+
		"\u0088\u000b\u0001\u0000\u0000\u0000\u0089\u008a\u0003\u0014\n\u0000\u008a"+
		"\u008b\u0005\u0004\u0000\u0000\u008b\u008d\u0005%\u0000\u0000\u008c\u008e"+
		"\u0003\u0010\b\u0000\u008d\u008c\u0001\u0000\u0000\u0000\u008d\u008e\u0001"+
		"\u0000\u0000\u0000\u008e\u008f\u0001\u0000\u0000\u0000\u008f\u0090\u0005"+
		"&\u0000\u0000\u0090\u0091\u0003<\u001e\u0000\u0091\r\u0001\u0000\u0000"+
		"\u0000\u0092\u0093\u0003\u0014\n\u0000\u0093\u0094\u0005-\u0000\u0000"+
		"\u0094\u0096\u0005%\u0000\u0000\u0095\u0097\u0003\u0010\b\u0000\u0096"+
		"\u0095\u0001\u0000\u0000\u0000\u0096\u0097\u0001\u0000\u0000\u0000\u0097"+
		"\u0098\u0001\u0000\u0000\u0000\u0098\u0099\u0005&\u0000\u0000\u0099\u009a"+
		"\u0003<\u001e\u0000\u009a\u000f\u0001\u0000\u0000\u0000\u009b\u00a6\u0005"+
		"\u0003\u0000\u0000\u009c\u00a6\u0003\u0014\n\u0000\u009d\u00a2\u0003\u0012"+
		"\t\u0000\u009e\u009f\u0005\u001f\u0000\u0000\u009f\u00a1\u0003\u0012\t"+
		"\u0000\u00a0\u009e\u0001\u0000\u0000\u0000\u00a1\u00a4\u0001\u0000\u0000"+
		"\u0000\u00a2\u00a0\u0001\u0000\u0000\u0000\u00a2\u00a3\u0001\u0000\u0000"+
		"\u0000\u00a3\u00a6\u0001\u0000\u0000\u0000\u00a4\u00a2\u0001\u0000\u0000"+
		"\u0000\u00a5\u009b\u0001\u0000\u0000\u0000\u00a5\u009c\u0001\u0000\u0000"+
		"\u0000\u00a5\u009d\u0001\u0000\u0000\u0000\u00a6\u0011\u0001\u0000\u0000"+
		"\u0000\u00a7\u00b5\u0003\u0014\n\u0000\u00a8\u00a9\u0003\u0014\n\u0000"+
		"\u00a9\u00aa\u0005-\u0000\u0000\u00aa\u00b5\u0001\u0000\u0000\u0000\u00ab"+
		"\u00ac\u0003\u0014\n\u0000\u00ac\u00ad\u0005!\u0000\u0000\u00ad\u00ae"+
		"\u0005\"\u0000\u0000\u00ae\u00b5\u0001\u0000\u0000\u0000\u00af\u00b0\u0003"+
		"\u0014\n\u0000\u00b0\u00b1\u0005-\u0000\u0000\u00b1\u00b2\u0005!\u0000"+
		"\u0000\u00b2\u00b3\u0005\"\u0000\u0000\u00b3\u00b5\u0001\u0000\u0000\u0000"+
		"\u00b4\u00a7\u0001\u0000\u0000\u0000\u00b4\u00a8\u0001\u0000\u0000\u0000"+
		"\u00b4\u00ab\u0001\u0000\u0000\u0000\u00b4\u00af\u0001\u0000\u0000\u0000"+
		"\u00b5\u0013\u0001\u0000\u0000\u0000\u00b6\u00b7\u0007\u0000\u0000\u0000"+
		"\u00b7\u0015\u0001\u0000\u0000\u0000\u00b8\u00b9\u0003\u0014\n\u0000\u00b9"+
		"\u00ba\u0003\u0018\f\u0000\u00ba\u00bb\u0005 \u0000\u0000\u00bb\u0017"+
		"\u0001\u0000\u0000\u0000\u00bc\u00c1\u0003\u001a\r\u0000\u00bd\u00be\u0005"+
		"\u001f\u0000\u0000\u00be\u00c0\u0003\u001a\r\u0000\u00bf\u00bd\u0001\u0000"+
		"\u0000\u0000\u00c0\u00c3\u0001\u0000\u0000\u0000\u00c1\u00bf\u0001\u0000"+
		"\u0000\u0000\u00c1\u00c2\u0001\u0000\u0000\u0000\u00c2\u0019\u0001\u0000"+
		"\u0000\u0000\u00c3\u00c1\u0001\u0000\u0000\u0000\u00c4\u00dd\u0005-\u0000"+
		"\u0000\u00c5\u00c6\u0005-\u0000\u0000\u00c6\u00c7\u0005\u001e\u0000\u0000"+
		"\u00c7\u00dd\u0003 \u0010\u0000\u00c8\u00c9\u0005-\u0000\u0000\u00c9\u00ca"+
		"\u0005!\u0000\u0000\u00ca\u00cb\u0005,\u0000\u0000\u00cb\u00dd\u0005\""+
		"\u0000\u0000\u00cc\u00cd\u0005-\u0000\u0000\u00cd\u00ce\u0005!\u0000\u0000"+
		"\u00ce\u00cf\u0005\"\u0000\u0000\u00cf\u00d0\u0005\u001e\u0000\u0000\u00d0"+
		"\u00dd\u0003:\u001d\u0000\u00d1\u00d2\u0005-\u0000\u0000\u00d2\u00d3\u0005"+
		"!\u0000\u0000\u00d3\u00d4\u0005\"\u0000\u0000\u00d4\u00d5\u0005\u001e"+
		"\u0000\u0000\u00d5\u00dd\u0003\u001c\u000e\u0000\u00d6\u00d7\u0005-\u0000"+
		"\u0000\u00d7\u00d8\u0005!\u0000\u0000\u00d8\u00d9\u0005,\u0000\u0000\u00d9"+
		"\u00da\u0005\"\u0000\u0000\u00da\u00db\u0005\u001e\u0000\u0000\u00db\u00dd"+
		"\u0003\u001c\u000e\u0000\u00dc\u00c4\u0001\u0000\u0000\u0000\u00dc\u00c5"+
		"\u0001\u0000\u0000\u0000\u00dc\u00c8\u0001\u0000\u0000\u0000\u00dc\u00cc"+
		"\u0001\u0000\u0000\u0000\u00dc\u00d1\u0001\u0000\u0000\u0000\u00dc\u00d6"+
		"\u0001\u0000\u0000\u0000\u00dd\u001b\u0001\u0000\u0000\u0000\u00de\u00e0"+
		"\u0005#\u0000\u0000\u00df\u00e1\u0003\u001e\u000f\u0000\u00e0\u00df\u0001"+
		"\u0000\u0000\u0000\u00e0\u00e1\u0001\u0000\u0000\u0000\u00e1\u00e2\u0001"+
		"\u0000\u0000\u0000\u00e2\u00e3\u0005$\u0000\u0000\u00e3\u001d\u0001\u0000"+
		"\u0000\u0000\u00e4\u00e9\u0003 \u0010\u0000\u00e5\u00e6\u0005\u001f\u0000"+
		"\u0000\u00e6\u00e8\u0003 \u0010\u0000\u00e7\u00e5\u0001\u0000\u0000\u0000"+
		"\u00e8\u00eb\u0001\u0000\u0000\u0000\u00e9\u00e7\u0001\u0000\u0000\u0000"+
		"\u00e9\u00ea\u0001\u0000\u0000\u0000\u00ea\u001f\u0001\u0000\u0000\u0000"+
		"\u00eb\u00e9\u0001\u0000\u0000\u0000\u00ec\u00ed\u0003\"\u0011\u0000\u00ed"+
		"!\u0001\u0000\u0000\u0000\u00ee\u00ef\u0006\u0011\uffff\uffff\u0000\u00ef"+
		"\u00f0\u0003$\u0012\u0000\u00f0\u00f6\u0001\u0000\u0000\u0000\u00f1\u00f2"+
		"\n\u0002\u0000\u0000\u00f2\u00f3\u0005\u001c\u0000\u0000\u00f3\u00f5\u0003"+
		"$\u0012\u0000\u00f4\u00f1\u0001\u0000\u0000\u0000\u00f5\u00f8\u0001\u0000"+
		"\u0000\u0000\u00f6\u00f4\u0001\u0000\u0000\u0000\u00f6\u00f7\u0001\u0000"+
		"\u0000\u0000\u00f7#\u0001\u0000\u0000\u0000\u00f8\u00f6\u0001\u0000\u0000"+
		"\u0000\u00f9\u00fa\u0006\u0012\uffff\uffff\u0000\u00fa\u00fb\u0003&\u0013"+
		"\u0000\u00fb\u0101\u0001\u0000\u0000\u0000\u00fc\u00fd\n\u0002\u0000\u0000"+
		"\u00fd\u00fe\u0005\u001b\u0000\u0000\u00fe\u0100\u0003&\u0013\u0000\u00ff"+
		"\u00fc\u0001\u0000\u0000\u0000\u0100\u0103\u0001\u0000\u0000\u0000\u0101"+
		"\u00ff\u0001\u0000\u0000\u0000\u0101\u0102\u0001\u0000\u0000\u0000\u0102"+
		"%\u0001\u0000\u0000\u0000\u0103\u0101\u0001\u0000\u0000\u0000\u0104\u0108"+
		"\u0003(\u0014\u0000\u0105\u0106\u00036\u001b\u0000\u0106\u0107\u0003("+
		"\u0014\u0000\u0107\u0109\u0001\u0000\u0000\u0000\u0108\u0105\u0001\u0000"+
		"\u0000\u0000\u0108\u0109\u0001\u0000\u0000\u0000\u0109\'\u0001\u0000\u0000"+
		"\u0000\u010a\u010b\u0006\u0014\uffff\uffff\u0000\u010b\u010c\u0003*\u0015"+
		"\u0000\u010c\u0115\u0001\u0000\u0000\u0000\u010d\u010e\n\u0003\u0000\u0000"+
		"\u010e\u010f\u0005\u0010\u0000\u0000\u010f\u0114\u0003*\u0015\u0000\u0110"+
		"\u0111\n\u0002\u0000\u0000\u0111\u0112\u0005\u0011\u0000\u0000\u0112\u0114"+
		"\u0003*\u0015\u0000\u0113\u010d\u0001\u0000\u0000\u0000\u0113\u0110\u0001"+
		"\u0000\u0000\u0000\u0114\u0117\u0001\u0000\u0000\u0000\u0115\u0113\u0001"+
		"\u0000\u0000\u0000\u0115\u0116\u0001\u0000\u0000\u0000\u0116)\u0001\u0000"+
		"\u0000\u0000\u0117\u0115\u0001\u0000\u0000\u0000\u0118\u0119\u0006\u0015"+
		"\uffff\uffff\u0000\u0119\u011a\u0003,\u0016\u0000\u011a\u0126\u0001\u0000"+
		"\u0000\u0000\u011b\u011c\n\u0004\u0000\u0000\u011c\u011d\u0005\u0012\u0000"+
		"\u0000\u011d\u0125\u0003,\u0016\u0000\u011e\u011f\n\u0003\u0000\u0000"+
		"\u011f\u0120\u0005\u0013\u0000\u0000\u0120\u0125\u0003,\u0016\u0000\u0121"+
		"\u0122\n\u0002\u0000\u0000\u0122\u0123\u0005\u0014\u0000\u0000\u0123\u0125"+
		"\u0003,\u0016\u0000\u0124\u011b\u0001\u0000\u0000\u0000\u0124\u011e\u0001"+
		"\u0000\u0000\u0000\u0124\u0121\u0001\u0000\u0000\u0000\u0125\u0128\u0001"+
		"\u0000\u0000\u0000\u0126\u0124\u0001\u0000\u0000\u0000\u0126\u0127\u0001"+
		"\u0000\u0000\u0000\u0127+\u0001\u0000\u0000\u0000\u0128\u0126\u0001\u0000"+
		"\u0000\u0000\u0129\u012a\u0005\u001d\u0000\u0000\u012a\u012f\u0003,\u0016"+
		"\u0000\u012b\u012c\u0005\u0011\u0000\u0000\u012c\u012f\u0003,\u0016\u0000"+
		"\u012d\u012f\u0003.\u0017\u0000\u012e\u0129\u0001\u0000\u0000\u0000\u012e"+
		"\u012b\u0001\u0000\u0000\u0000\u012e\u012d\u0001\u0000\u0000\u0000\u012f"+
		"-\u0001\u0000\u0000\u0000\u0130\u0131\u0005%\u0000\u0000\u0131\u0132\u0003"+
		"\u0014\n\u0000\u0132\u0133\u0005&\u0000\u0000\u0133\u0134\u0003.\u0017"+
		"\u0000\u0134\u0137\u0001\u0000\u0000\u0000\u0135\u0137\u00030\u0018\u0000"+
		"\u0136\u0130\u0001\u0000\u0000\u0000\u0136\u0135\u0001\u0000\u0000\u0000"+
		"\u0137/\u0001\u0000\u0000\u0000\u0138\u0139\u0005%\u0000\u0000\u0139\u013a"+
		"\u0003 \u0010\u0000\u013a\u013b\u0005&\u0000\u0000\u013b\u0142\u0001\u0000"+
		"\u0000\u0000\u013c\u0142\u00038\u001c\u0000\u013d\u0142\u0005,\u0000\u0000"+
		"\u013e\u0142\u0005+\u0000\u0000\u013f\u0140\u0005-\u0000\u0000\u0140\u0142"+
		"\u00032\u0019\u0000\u0141\u0138\u0001\u0000\u0000\u0000\u0141\u013c\u0001"+
		"\u0000\u0000\u0000\u0141\u013d\u0001\u0000\u0000\u0000\u0141\u013e\u0001"+
		"\u0000\u0000\u0000\u0141\u013f\u0001\u0000\u0000\u0000\u01421\u0001\u0000"+
		"\u0000\u0000\u0143\u0145\u0005%\u0000\u0000\u0144\u0146\u00034\u001a\u0000"+
		"\u0145\u0144\u0001\u0000\u0000\u0000\u0145\u0146\u0001\u0000\u0000\u0000"+
		"\u0146\u0147\u0001\u0000\u0000\u0000\u0147\u014e\u0005&\u0000\u0000\u0148"+
		"\u0149\u0005!\u0000\u0000\u0149\u014a\u0003 \u0010\u0000\u014a\u014b\u0005"+
		"\"\u0000\u0000\u014b\u014e\u0001\u0000\u0000\u0000\u014c\u014e\u0001\u0000"+
		"\u0000\u0000\u014d\u0143\u0001\u0000\u0000\u0000\u014d\u0148\u0001\u0000"+
		"\u0000\u0000\u014d\u014c\u0001\u0000\u0000\u0000\u014e3\u0001\u0000\u0000"+
		"\u0000\u014f\u0154\u0003 \u0010\u0000\u0150\u0151\u0005\u001f\u0000\u0000"+
		"\u0151\u0153\u0003 \u0010\u0000\u0152\u0150\u0001\u0000\u0000\u0000\u0153"+
		"\u0156\u0001\u0000\u0000\u0000\u0154\u0152\u0001\u0000\u0000\u0000\u0154"+
		"\u0155\u0001\u0000\u0000\u0000\u01555\u0001\u0000\u0000\u0000\u0156\u0154"+
		"\u0001\u0000\u0000\u0000\u0157\u0158\u0007\u0001\u0000\u0000\u01587\u0001"+
		"\u0000\u0000\u0000\u0159\u015a\u0005\u0005\u0000\u0000\u015a\u015b\u0005"+
		"%\u0000\u0000\u015b\u0163\u0005&\u0000\u0000\u015c\u015d\u0005\u0006\u0000"+
		"\u0000\u015d\u015e\u0005%\u0000\u0000\u015e\u0163\u0005&\u0000\u0000\u015f"+
		"\u0160\u0005\u0007\u0000\u0000\u0160\u0161\u0005%\u0000\u0000\u0161\u0163"+
		"\u0005&\u0000\u0000\u0162\u0159\u0001\u0000\u0000\u0000\u0162\u015c\u0001"+
		"\u0000\u0000\u0000\u0162\u015f\u0001\u0000\u0000\u0000\u01639\u0001\u0000"+
		"\u0000\u0000\u0164\u0165\u0005\u0007\u0000\u0000\u0165\u0166\u0005%\u0000"+
		"\u0000\u0166\u0167\u0005&\u0000\u0000\u0167;\u0001\u0000\u0000\u0000\u0168"+
		"\u0169\u0005#\u0000\u0000\u0169\u016a\u0003>\u001f\u0000\u016a\u016b\u0005"+
		"$\u0000\u0000\u016b=\u0001\u0000\u0000\u0000\u016c\u016e\u0003@ \u0000"+
		"\u016d\u016c\u0001\u0000\u0000\u0000\u016e\u0171\u0001\u0000\u0000\u0000"+
		"\u016f\u016d\u0001\u0000\u0000\u0000\u016f\u0170\u0001\u0000\u0000\u0000"+
		"\u0170?\u0001\u0000\u0000\u0000\u0171\u016f\u0001\u0000\u0000\u0000\u0172"+
		"\u0176\u0003D\"\u0000\u0173\u0176\u0003F#\u0000\u0174\u0176\u0003H$\u0000"+
		"\u0175\u0172\u0001\u0000\u0000\u0000\u0175\u0173\u0001\u0000\u0000\u0000"+
		"\u0175\u0174\u0001\u0000\u0000\u0000\u0176A\u0001\u0000\u0000\u0000\u0177"+
		"\u0178\u0003 \u0010\u0000\u0178\u0179\u0005 \u0000\u0000\u0179C\u0001"+
		"\u0000\u0000\u0000\u017a\u017b\u0005\f\u0000\u0000\u017b\u017c\u0005%"+
		"\u0000\u0000\u017c\u017d\u0003 \u0010\u0000\u017d\u017e\u0005&\u0000\u0000"+
		"\u017e\u017f\u0003<\u001e\u0000\u017f\u0180\u0005\r\u0000\u0000\u0180"+
		"\u0181\u0003D\"\u0000\u0181\u0184\u0001\u0000\u0000\u0000\u0182\u0184"+
		"\u0003<\u001e\u0000\u0183\u017a\u0001\u0000\u0000\u0000\u0183\u0182\u0001"+
		"\u0000\u0000\u0000\u0184E\u0001\u0000\u0000\u0000\u0185\u0186\u0005\f"+
		"\u0000\u0000\u0186\u0187\u0005%\u0000\u0000\u0187\u0188\u0003 \u0010\u0000"+
		"\u0188\u0189\u0005&\u0000\u0000\u0189\u018a\u0003<\u001e\u0000\u018a\u0194"+
		"\u0001\u0000\u0000\u0000\u018b\u018c\u0005\f\u0000\u0000\u018c\u018d\u0005"+
		"%\u0000\u0000\u018d\u018e\u0003 \u0010\u0000\u018e\u018f\u0005&\u0000"+
		"\u0000\u018f\u0190\u0003<\u001e\u0000\u0190\u0191\u0005\r\u0000\u0000"+
		"\u0191\u0192\u0003F#\u0000\u0192\u0194\u0001\u0000\u0000\u0000\u0193\u0185"+
		"\u0001\u0000\u0000\u0000\u0193\u018b\u0001\u0000\u0000\u0000\u0194G\u0001"+
		"\u0000\u0000\u0000\u0195\u019e\u0003<\u001e\u0000\u0196\u019e\u0003\u0016"+
		"\u000b\u0000\u0197\u019e\u0003J%\u0000\u0198\u019e\u0003L&\u0000\u0199"+
		"\u019e\u0003P(\u0000\u019a\u019e\u0003R)\u0000\u019b\u019e\u0003T*\u0000"+
		"\u019c\u019e\u0003B!\u0000\u019d\u0195\u0001\u0000\u0000\u0000\u019d\u0196"+
		"\u0001\u0000\u0000\u0000\u019d\u0197\u0001\u0000\u0000\u0000\u019d\u0198"+
		"\u0001\u0000\u0000\u0000\u019d\u0199\u0001\u0000\u0000\u0000\u019d\u019a"+
		"\u0001\u0000\u0000\u0000\u019d\u019b\u0001\u0000\u0000\u0000\u019d\u019c"+
		"\u0001\u0000\u0000\u0000\u019eI\u0001\u0000\u0000\u0000\u019f\u01a0\u0005"+
		"\u000e\u0000\u0000\u01a0\u01a1\u0005%\u0000\u0000\u01a1\u01a2\u0003 \u0010"+
		"\u0000\u01a2\u01a3\u0005&\u0000\u0000\u01a3\u01a4\u0003<\u001e\u0000\u01a4"+
		"K\u0001\u0000\u0000\u0000\u01a5\u01a6\u0005\u000f\u0000\u0000\u01a6\u01a8"+
		"\u0005%\u0000\u0000\u01a7\u01a9\u0003N\'\u0000\u01a8\u01a7\u0001\u0000"+
		"\u0000\u0000\u01a8\u01a9\u0001\u0000\u0000\u0000\u01a9\u01aa\u0001\u0000"+
		"\u0000\u0000\u01aa\u01ac\u0005 \u0000\u0000\u01ab\u01ad\u0003 \u0010\u0000"+
		"\u01ac\u01ab\u0001\u0000\u0000\u0000\u01ac\u01ad\u0001\u0000\u0000\u0000"+
		"\u01ad\u01ae\u0001\u0000\u0000\u0000\u01ae\u01b0\u0005 \u0000\u0000\u01af"+
		"\u01b1\u0003N\'\u0000\u01b0\u01af\u0001\u0000\u0000\u0000\u01b0\u01b1"+
		"\u0001\u0000\u0000\u0000\u01b1\u01b2\u0001\u0000\u0000\u0000\u01b2\u01b3"+
		"\u0005&\u0000\u0000\u01b3\u01b4\u0003<\u001e\u0000\u01b4M\u0001\u0000"+
		"\u0000\u0000\u01b5\u01b6\u0005-\u0000\u0000\u01b6\u01b7\u0005\u001e\u0000"+
		"\u0000\u01b7\u01ba\u0003 \u0010\u0000\u01b8\u01ba\u0003 \u0010\u0000\u01b9"+
		"\u01b5\u0001\u0000\u0000\u0000\u01b9\u01b8\u0001\u0000\u0000\u0000\u01ba"+
		"O\u0001\u0000\u0000\u0000\u01bb\u01bc\u0005\b\u0000\u0000\u01bc\u01bd"+
		"\u0005%\u0000\u0000\u01bd\u01be\u0003 \u0010\u0000\u01be\u01bf\u0005&"+
		"\u0000\u0000\u01bf\u01c0\u0005 \u0000\u0000\u01c0\u01d3\u0001\u0000\u0000"+
		"\u0000\u01c1\u01c2\u0005\t\u0000\u0000\u01c2\u01c3\u0005%\u0000\u0000"+
		"\u01c3\u01c4\u0003 \u0010\u0000\u01c4\u01c5\u0005&\u0000\u0000\u01c5\u01c6"+
		"\u0005 \u0000\u0000\u01c6\u01d3\u0001\u0000\u0000\u0000\u01c7\u01c8\u0005"+
		"\n\u0000\u0000\u01c8\u01c9\u0005%\u0000\u0000\u01c9\u01ca\u0005-\u0000"+
		"\u0000\u01ca\u01cb\u0005&\u0000\u0000\u01cb\u01d3\u0005 \u0000\u0000\u01cc"+
		"\u01cd\u0005\u000b\u0000\u0000\u01cd\u01ce\u0005%\u0000\u0000\u01ce\u01cf"+
		"\u0003V+\u0000\u01cf\u01d0\u0005&\u0000\u0000\u01d0\u01d1\u0005 \u0000"+
		"\u0000\u01d1\u01d3\u0001\u0000\u0000\u0000\u01d2\u01bb\u0001\u0000\u0000"+
		"\u0000\u01d2\u01c1\u0001\u0000\u0000\u0000\u01d2\u01c7\u0001\u0000\u0000"+
		"\u0000\u01d2\u01cc\u0001\u0000\u0000\u0000\u01d3Q\u0001\u0000\u0000\u0000"+
		"\u01d4\u01d5\u0005\'\u0000\u0000\u01d5\u01d6\u0003 \u0010\u0000\u01d6"+
		"\u01d7\u0005 \u0000\u0000\u01d7S\u0001\u0000\u0000\u0000\u01d8\u01df\u0005"+
		"-\u0000\u0000\u01d9\u01da\u0005-\u0000\u0000\u01da\u01db\u0005!\u0000"+
		"\u0000\u01db\u01dc\u0003 \u0010\u0000\u01dc\u01dd\u0005\"\u0000\u0000"+
		"\u01dd\u01df\u0001\u0000\u0000\u0000\u01de\u01d8\u0001\u0000\u0000\u0000"+
		"\u01de\u01d9\u0001\u0000\u0000\u0000\u01df\u01e0\u0001\u0000\u0000\u0000"+
		"\u01e0\u01e1\u0005\u001e\u0000\u0000\u01e1\u01e2\u0003 \u0010\u0000\u01e2"+
		"\u01e3\u0005 \u0000\u0000\u01e3U\u0001\u0000\u0000\u0000\u01e4\u01e5\u0007"+
		"\u0002\u0000\u0000\u01e5W\u0001\u0000\u0000\u0000*^`fhnu{\u0084\u008d"+
		"\u0096\u00a2\u00a5\u00b4\u00c1\u00dc\u00e0\u00e9\u00f6\u0101\u0108\u0113"+
		"\u0115\u0124\u0126\u012e\u0136\u0141\u0145\u014d\u0154\u0162\u016f\u0175"+
		"\u0183\u0193\u019d\u01a8\u01ac\u01b0\u01b9\u01d2\u01de";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}