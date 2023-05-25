// Generated from /home/bernat/Desktop/Code/AChurch/lc.g4 by ANTLR 4.9.2
import org.antlr.v4.runtime.atn.*;
import org.antlr.v4.runtime.dfa.DFA;
import org.antlr.v4.runtime.*;
import org.antlr.v4.runtime.misc.*;
import org.antlr.v4.runtime.tree.*;
import java.util.List;
import java.util.Iterator;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked", "unused", "cast"})
public class lcParser extends Parser {
	static { RuntimeMetaData.checkVersion("4.9.2", RuntimeMetaData.VERSION); }

	protected static final DFA[] _decisionToDFA;
	protected static final PredictionContextCache _sharedContextCache =
		new PredictionContextCache();
	public static final int
		T__0=1, T__1=2, T__2=3, T__3=4, LLETRA=5, VAR=6, LAMBDA=7, WS=8;
	public static final int
		RULE_root = 0, RULE_instruccio = 1, RULE_terme = 2;
	private static String[] makeRuleNames() {
		return new String[] {
			"root", "instruccio", "terme"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'\u2261'", "'('", "')'", "'.'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, null, null, null, "LLETRA", "VAR", "LAMBDA", "WS"
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
	public String getGrammarFileName() { return "lc.g4"; }

	@Override
	public String[] getRuleNames() { return ruleNames; }

	@Override
	public String getSerializedATN() { return _serializedATN; }

	@Override
	public ATN getATN() { return _ATN; }

	public lcParser(TokenStream input) {
		super(input);
		_interp = new ParserATNSimulator(this,_ATN,_decisionToDFA,_sharedContextCache);
	}

	public static class RootContext extends ParserRuleContext {
		public List<InstruccioContext> instruccio() {
			return getRuleContexts(InstruccioContext.class);
		}
		public InstruccioContext instruccio(int i) {
			return getRuleContext(InstruccioContext.class,i);
		}
		public RootContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_root; }
	}

	public final RootContext root() throws RecognitionException {
		RootContext _localctx = new RootContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_root);
		int _la;
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(7); 
			_errHandler.sync(this);
			_la = _input.LA(1);
			do {
				{
				{
				setState(6);
				instruccio();
				}
				}
				setState(9); 
				_errHandler.sync(this);
				_la = _input.LA(1);
			} while ( (((_la) & ~0x3f) == 0 && ((1L << _la) & ((1L << T__1) | (1L << LLETRA) | (1L << VAR) | (1L << LAMBDA))) != 0) );
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

	public static class InstruccioContext extends ParserRuleContext {
		public InstruccioContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_instruccio; }
	 
		public InstruccioContext() { }
		public void copyFrom(InstruccioContext ctx) {
			super.copyFrom(ctx);
		}
	}
	public static class AssignacioContext extends InstruccioContext {
		public TerminalNode VAR() { return getToken(lcParser.VAR, 0); }
		public TermeContext terme() {
			return getRuleContext(TermeContext.class,0);
		}
		public AssignacioContext(InstruccioContext ctx) { copyFrom(ctx); }
	}
	public static class ExpressioContext extends InstruccioContext {
		public TermeContext terme() {
			return getRuleContext(TermeContext.class,0);
		}
		public ExpressioContext(InstruccioContext ctx) { copyFrom(ctx); }
	}

	public final InstruccioContext instruccio() throws RecognitionException {
		InstruccioContext _localctx = new InstruccioContext(_ctx, getState());
		enterRule(_localctx, 2, RULE_instruccio);
		try {
			setState(15);
			_errHandler.sync(this);
			switch ( getInterpreter().adaptivePredict(_input,1,_ctx) ) {
			case 1:
				_localctx = new AssignacioContext(_localctx);
				enterOuterAlt(_localctx, 1);
				{
				setState(11);
				match(VAR);
				setState(12);
				match(T__0);
				setState(13);
				terme(0);
				}
				break;
			case 2:
				_localctx = new ExpressioContext(_localctx);
				enterOuterAlt(_localctx, 2);
				{
				setState(14);
				terme(0);
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

	public static class TermeContext extends ParserRuleContext {
		public TermeContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_terme; }
	 
		public TermeContext() { }
		public void copyFrom(TermeContext ctx) {
			super.copyFrom(ctx);
		}
	}
	public static class ParentesisContext extends TermeContext {
		public TermeContext terme() {
			return getRuleContext(TermeContext.class,0);
		}
		public ParentesisContext(TermeContext ctx) { copyFrom(ctx); }
	}
	public static class LletraContext extends TermeContext {
		public TerminalNode LLETRA() { return getToken(lcParser.LLETRA, 0); }
		public LletraContext(TermeContext ctx) { copyFrom(ctx); }
	}
	public static class VariableContext extends TermeContext {
		public TerminalNode VAR() { return getToken(lcParser.VAR, 0); }
		public VariableContext(TermeContext ctx) { copyFrom(ctx); }
	}
	public static class AbstraccioContext extends TermeContext {
		public TerminalNode LAMBDA() { return getToken(lcParser.LAMBDA, 0); }
		public TermeContext terme() {
			return getRuleContext(TermeContext.class,0);
		}
		public List<TerminalNode> LLETRA() { return getTokens(lcParser.LLETRA); }
		public TerminalNode LLETRA(int i) {
			return getToken(lcParser.LLETRA, i);
		}
		public AbstraccioContext(TermeContext ctx) { copyFrom(ctx); }
	}
	public static class AplicacioContext extends TermeContext {
		public List<TermeContext> terme() {
			return getRuleContexts(TermeContext.class);
		}
		public TermeContext terme(int i) {
			return getRuleContext(TermeContext.class,i);
		}
		public AplicacioContext(TermeContext ctx) { copyFrom(ctx); }
	}

	public final TermeContext terme() throws RecognitionException {
		return terme(0);
	}

	private TermeContext terme(int _p) throws RecognitionException {
		ParserRuleContext _parentctx = _ctx;
		int _parentState = getState();
		TermeContext _localctx = new TermeContext(_ctx, _parentState);
		TermeContext _prevctx = _localctx;
		int _startState = 4;
		enterRecursionRule(_localctx, 4, RULE_terme, _p);
		int _la;
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(32);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__1:
				{
				_localctx = new ParentesisContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;

				setState(18);
				match(T__1);
				setState(19);
				terme(0);
				setState(20);
				match(T__2);
				}
				break;
			case LAMBDA:
				{
				_localctx = new AbstraccioContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(22);
				match(LAMBDA);
				setState(24); 
				_errHandler.sync(this);
				_la = _input.LA(1);
				do {
					{
					{
					setState(23);
					match(LLETRA);
					}
					}
					setState(26); 
					_errHandler.sync(this);
					_la = _input.LA(1);
				} while ( _la==LLETRA );
				setState(28);
				match(T__3);
				setState(29);
				terme(3);
				}
				break;
			case VAR:
				{
				_localctx = new VariableContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(30);
				match(VAR);
				}
				break;
			case LLETRA:
				{
				_localctx = new LletraContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(31);
				match(LLETRA);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
			_ctx.stop = _input.LT(-1);
			setState(38);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,4,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					{
					_localctx = new AplicacioContext(new TermeContext(_parentctx, _parentState));
					pushNewRecursionContext(_localctx, _startState, RULE_terme);
					setState(34);
					if (!(precpred(_ctx, 4))) throw new FailedPredicateException(this, "precpred(_ctx, 4)");
					setState(35);
					terme(5);
					}
					} 
				}
				setState(40);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,4,_ctx);
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

	public boolean sempred(RuleContext _localctx, int ruleIndex, int predIndex) {
		switch (ruleIndex) {
		case 2:
			return terme_sempred((TermeContext)_localctx, predIndex);
		}
		return true;
	}
	private boolean terme_sempred(TermeContext _localctx, int predIndex) {
		switch (predIndex) {
		case 0:
			return precpred(_ctx, 4);
		}
		return true;
	}

	public static final String _serializedATN =
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\n,\4\2\t\2\4\3\t"+
		"\3\4\4\t\4\3\2\6\2\n\n\2\r\2\16\2\13\3\3\3\3\3\3\3\3\5\3\22\n\3\3\4\3"+
		"\4\3\4\3\4\3\4\3\4\3\4\6\4\33\n\4\r\4\16\4\34\3\4\3\4\3\4\3\4\5\4#\n\4"+
		"\3\4\3\4\7\4\'\n\4\f\4\16\4*\13\4\3\4\2\3\6\5\2\4\6\2\2\2/\2\t\3\2\2\2"+
		"\4\21\3\2\2\2\6\"\3\2\2\2\b\n\5\4\3\2\t\b\3\2\2\2\n\13\3\2\2\2\13\t\3"+
		"\2\2\2\13\f\3\2\2\2\f\3\3\2\2\2\r\16\7\b\2\2\16\17\7\3\2\2\17\22\5\6\4"+
		"\2\20\22\5\6\4\2\21\r\3\2\2\2\21\20\3\2\2\2\22\5\3\2\2\2\23\24\b\4\1\2"+
		"\24\25\7\4\2\2\25\26\5\6\4\2\26\27\7\5\2\2\27#\3\2\2\2\30\32\7\t\2\2\31"+
		"\33\7\7\2\2\32\31\3\2\2\2\33\34\3\2\2\2\34\32\3\2\2\2\34\35\3\2\2\2\35"+
		"\36\3\2\2\2\36\37\7\6\2\2\37#\5\6\4\5 #\7\b\2\2!#\7\7\2\2\"\23\3\2\2\2"+
		"\"\30\3\2\2\2\" \3\2\2\2\"!\3\2\2\2#(\3\2\2\2$%\f\6\2\2%\'\5\6\4\7&$\3"+
		"\2\2\2\'*\3\2\2\2(&\3\2\2\2()\3\2\2\2)\7\3\2\2\2*(\3\2\2\2\7\13\21\34"+
		"\"(";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}