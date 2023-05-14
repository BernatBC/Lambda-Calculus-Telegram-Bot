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
		T__0=1, T__1=2, T__2=3, LLETRA=4, LAMBDA=5, WS=6;
	public static final int
		RULE_root = 0, RULE_terme = 1;
	private static String[] makeRuleNames() {
		return new String[] {
			"root", "terme"
		};
	}
	public static final String[] ruleNames = makeRuleNames();

	private static String[] makeLiteralNames() {
		return new String[] {
			null, "'('", "')'", "'.'"
		};
	}
	private static final String[] _LITERAL_NAMES = makeLiteralNames();
	private static String[] makeSymbolicNames() {
		return new String[] {
			null, null, null, null, "LLETRA", "LAMBDA", "WS"
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
		public TermeContext terme() {
			return getRuleContext(TermeContext.class,0);
		}
		public RootContext(ParserRuleContext parent, int invokingState) {
			super(parent, invokingState);
		}
		@Override public int getRuleIndex() { return RULE_root; }
	}

	public final RootContext root() throws RecognitionException {
		RootContext _localctx = new RootContext(_ctx, getState());
		enterRule(_localctx, 0, RULE_root);
		try {
			enterOuterAlt(_localctx, 1);
			{
			setState(4);
			terme(0);
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
		int _startState = 2;
		enterRecursionRule(_localctx, 2, RULE_terme, _p);
		int _la;
		try {
			int _alt;
			enterOuterAlt(_localctx, 1);
			{
			setState(20);
			_errHandler.sync(this);
			switch (_input.LA(1)) {
			case T__0:
				{
				_localctx = new ParentesisContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;

				setState(7);
				match(T__0);
				setState(8);
				terme(0);
				setState(9);
				match(T__1);
				}
				break;
			case LAMBDA:
				{
				_localctx = new AbstraccioContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(11);
				match(LAMBDA);
				setState(13); 
				_errHandler.sync(this);
				_la = _input.LA(1);
				do {
					{
					{
					setState(12);
					match(LLETRA);
					}
					}
					setState(15); 
					_errHandler.sync(this);
					_la = _input.LA(1);
				} while ( _la==LLETRA );
				setState(17);
				match(T__2);
				setState(18);
				terme(2);
				}
				break;
			case LLETRA:
				{
				_localctx = new LletraContext(_localctx);
				_ctx = _localctx;
				_prevctx = _localctx;
				setState(19);
				match(LLETRA);
				}
				break;
			default:
				throw new NoViableAltException(this);
			}
			_ctx.stop = _input.LT(-1);
			setState(26);
			_errHandler.sync(this);
			_alt = getInterpreter().adaptivePredict(_input,2,_ctx);
			while ( _alt!=2 && _alt!=org.antlr.v4.runtime.atn.ATN.INVALID_ALT_NUMBER ) {
				if ( _alt==1 ) {
					if ( _parseListeners!=null ) triggerExitRuleEvent();
					_prevctx = _localctx;
					{
					{
					_localctx = new AplicacioContext(new TermeContext(_parentctx, _parentState));
					pushNewRecursionContext(_localctx, _startState, RULE_terme);
					setState(22);
					if (!(precpred(_ctx, 3))) throw new FailedPredicateException(this, "precpred(_ctx, 3)");
					setState(23);
					terme(4);
					}
					} 
				}
				setState(28);
				_errHandler.sync(this);
				_alt = getInterpreter().adaptivePredict(_input,2,_ctx);
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
		case 1:
			return terme_sempred((TermeContext)_localctx, predIndex);
		}
		return true;
	}
	private boolean terme_sempred(TermeContext _localctx, int predIndex) {
		switch (predIndex) {
		case 0:
			return precpred(_ctx, 3);
		}
		return true;
	}

	public static final String _serializedATN =
		"\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\b \4\2\t\2\4\3\t"+
		"\3\3\2\3\2\3\3\3\3\3\3\3\3\3\3\3\3\3\3\6\3\20\n\3\r\3\16\3\21\3\3\3\3"+
		"\3\3\5\3\27\n\3\3\3\3\3\7\3\33\n\3\f\3\16\3\36\13\3\3\3\2\3\4\4\2\4\2"+
		"\2\2!\2\6\3\2\2\2\4\26\3\2\2\2\6\7\5\4\3\2\7\3\3\2\2\2\b\t\b\3\1\2\t\n"+
		"\7\3\2\2\n\13\5\4\3\2\13\f\7\4\2\2\f\27\3\2\2\2\r\17\7\7\2\2\16\20\7\6"+
		"\2\2\17\16\3\2\2\2\20\21\3\2\2\2\21\17\3\2\2\2\21\22\3\2\2\2\22\23\3\2"+
		"\2\2\23\24\7\5\2\2\24\27\5\4\3\4\25\27\7\6\2\2\26\b\3\2\2\2\26\r\3\2\2"+
		"\2\26\25\3\2\2\2\27\34\3\2\2\2\30\31\f\5\2\2\31\33\5\4\3\6\32\30\3\2\2"+
		"\2\33\36\3\2\2\2\34\32\3\2\2\2\34\35\3\2\2\2\35\5\3\2\2\2\36\34\3\2\2"+
		"\2\5\21\26\34";
	public static final ATN _ATN =
		new ATNDeserializer().deserialize(_serializedATN.toCharArray());
	static {
		_decisionToDFA = new DFA[_ATN.getNumberOfDecisions()];
		for (int i = 0; i < _ATN.getNumberOfDecisions(); i++) {
			_decisionToDFA[i] = new DFA(_ATN.getDecisionState(i), i);
		}
	}
}