from __future__ import annotations
from dataclasses import dataclass
from antlr4 import *
from lcLexer import lcLexer
from lcParser import lcParser
from lcVisitor import lcVisitor

@dataclass
class Abstraccio:
    var: Variable
    expr: Arbre

@dataclass
class Aplicacio:
    esq: Arbre
    dre: Arbre

@dataclass
class Variable:
    variable: chr

Arbre = Abstraccio | Aplicacio | Variable

def to_string(a: Arbre) -> str:
    match a:
        case Abstraccio(variable, expressio):
            return '(λ' + str(to_string(variable)) + '.' + str(to_string(expressio)) + ')'
        case Aplicacio(esquerra, dreta):
            return '(' + str(to_string(esquerra)) + str(to_string(dreta)) + ')'
        case Variable(var):
            return var            

def alpha_conversio(a: Arbre) -> Arbre:
    match a:
        case Abstraccio(esquerra, dreta):
            return a
        case Aplicacio(esquerra, dreta):
            return a
        case Variable(var):
            return a

def beta_reduccio(a: Arbre) -> Arbre:
    match a:
        case Abstraccio(_, expressio):
            return beta_reduccio(expressio)
        case Aplicacio(esquerra, dreta):
            match esquerra:
                case Abstraccio(variable, expressio):
                    print('β-reducció:')
                    reduit = substitucio(expressio, dreta, str(variable.variable))
                    print(to_string(a) + '->' + to_string(reduit))
                    return beta_reduccio(reduit)
                case Aplicacio(esquerra2, dreta2):
                    x = beta_reduccio(esquerra2)
                    y = beta_reduccio(dreta2)
                    return Aplicacio(Aplicacio(x, y), beta_reduccio(dreta))
                case Variable(_):
                    return Aplicacio(esquerra, beta_reduccio(dreta))
        case Variable(_):
            return a

def substitucio(a: Arbre, b: Arbre, variable) -> Arbre:
    match a:
        case Abstraccio(esquerra, dreta):
            return Abstraccio(esquerra, substitucio(dreta, b, variable))
        case Aplicacio(esquerra, dreta):
            return Aplicacio(substitucio(esquerra, b, variable), substitucio(dreta, b, variable))
        case Variable(var):
            if var == variable:
                return b
            else: return a

class TreeVisitor(lcVisitor):

    def visitRoot(self, ctx:lcParser.RootContext):
        return self.visitChildren(ctx)

    def visitParentesis(self, ctx:lcParser.ParentesisContext):
        terme = ctx.getChild(1)
        return self.visit(terme)

    def visitLletra(self, ctx:lcParser.LletraContext):
        lletra = str(ctx.getChild(0))
        return Variable(lletra)

    def visitAbstraccio(self, ctx:lcParser.AbstraccioContext):
        terme = ctx.getChild(ctx.getChildCount() - 1)
        lletra = ctx.getChild(ctx.getChildCount() - 3)
        n = Abstraccio(Variable(lletra), self.visit(terme))
        # traducció abstracció de múltiples paràmetres
        for i in range(ctx.getChildCount() - 4, 0, -1):
            n = Abstraccio(Variable(ctx.getChild(i)), n)
        return n

    def visitAplicacio(self, ctx:lcParser.AplicacioContext):
        [terme1, terme2] = list(ctx.getChildren())
        return Aplicacio(self.visit(terme1), self.visit(terme2))


input_stream = InputStream(input('? '))
lexer = lcLexer(input_stream)
token_stream = CommonTokenStream(lexer)
parser = lcParser(token_stream)
tree = parser.root()

if parser.getNumberOfSyntaxErrors() == 0:
    visitor = TreeVisitor()
    a = visitor.visit(tree)
    print('Arbre:')
    print(to_string(a))
    b = beta_reduccio(a)
    print('resultat:')
    print(to_string(b))
else:
    print(parser.getNumberOfSyntaxErrors(), 'errors de sintaxi.')
    print(tree.toStringTree(recog=parser))