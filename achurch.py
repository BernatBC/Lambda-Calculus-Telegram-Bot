from antlr4 import *
from lcLexer import lcLexer
from lcParser import lcParser

input_stream = InputStream(input('? '))
lexer = lcLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = lcParser(token_stream)
tree = parser.root()

print(parser.getNumberOfSyntaxErrors(), 'errors de sintaxi.')
print(tree.toStringTree(recog=parser))