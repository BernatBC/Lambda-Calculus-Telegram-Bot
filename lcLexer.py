# Generated from lc.g4 by ANTLR 4.12.0
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4,0,9,51,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,
        6,7,6,2,7,7,7,2,8,7,8,1,0,1,0,1,1,1,1,1,2,1,2,1,3,1,3,1,4,1,4,1,
        5,1,5,5,5,32,8,5,10,5,12,5,35,9,5,1,5,3,5,38,8,5,1,6,3,6,41,8,6,
        1,7,1,7,1,8,4,8,46,8,8,11,8,12,8,47,1,8,1,8,0,0,9,1,1,3,2,5,3,7,
        4,9,5,11,6,13,7,15,8,17,9,1,0,7,2,0,61,61,8801,8801,1,0,97,122,1,
        0,65,90,3,0,44,44,48,57,65,90,11,0,33,39,42,45,47,47,58,60,62,64,
        91,91,93,96,123,126,160,172,174,239,247,247,2,0,92,92,955,955,3,
        0,9,10,13,13,32,32,53,0,1,1,0,0,0,0,3,1,0,0,0,0,5,1,0,0,0,0,7,1,
        0,0,0,0,9,1,0,0,0,0,11,1,0,0,0,0,13,1,0,0,0,0,15,1,0,0,0,0,17,1,
        0,0,0,1,19,1,0,0,0,3,21,1,0,0,0,5,23,1,0,0,0,7,25,1,0,0,0,9,27,1,
        0,0,0,11,37,1,0,0,0,13,40,1,0,0,0,15,42,1,0,0,0,17,45,1,0,0,0,19,
        20,5,40,0,0,20,2,1,0,0,0,21,22,5,41,0,0,22,4,1,0,0,0,23,24,5,46,
        0,0,24,6,1,0,0,0,25,26,7,0,0,0,26,8,1,0,0,0,27,28,7,1,0,0,28,10,
        1,0,0,0,29,33,7,2,0,0,30,32,7,3,0,0,31,30,1,0,0,0,32,35,1,0,0,0,
        33,31,1,0,0,0,33,34,1,0,0,0,34,38,1,0,0,0,35,33,1,0,0,0,36,38,3,
        13,6,0,37,29,1,0,0,0,37,36,1,0,0,0,38,12,1,0,0,0,39,41,7,4,0,0,40,
        39,1,0,0,0,41,14,1,0,0,0,42,43,7,5,0,0,43,16,1,0,0,0,44,46,7,6,0,
        0,45,44,1,0,0,0,46,47,1,0,0,0,47,45,1,0,0,0,47,48,1,0,0,0,48,49,
        1,0,0,0,49,50,6,8,0,0,50,18,1,0,0,0,5,0,33,37,40,47,1,6,0,0
    ]

class lcLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    EQ = 4
    LLETRA = 5
    VAR = 6
    SYMBOL = 7
    LAMBDA = 8
    WS = 9

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'('", "')'", "'.'" ]

    symbolicNames = [ "<INVALID>",
            "EQ", "LLETRA", "VAR", "SYMBOL", "LAMBDA", "WS" ]

    ruleNames = [ "T__0", "T__1", "T__2", "EQ", "LLETRA", "VAR", "SYMBOL", 
                  "LAMBDA", "WS" ]

    grammarFileName = "lc.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.12.0")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


