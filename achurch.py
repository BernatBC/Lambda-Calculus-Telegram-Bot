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
    var: chr

Arbre = Abstraccio | Aplicacio | Variable

macros = {}

def to_string(arbre: Arbre) -> str:
    match arbre:
        case Abstraccio(variable, expressio):
            return '(λ' + str(to_string(variable)) + '.' + str(to_string(expressio)) + ')'
        case Aplicacio(esquerra, dreta):
            return '(' + str(to_string(esquerra)) + str(to_string(dreta)) + ')'
        case Variable(var):
            return var            

def alpha(arbre:Arbre):

    utilitzades = set()

    def variables_utilitzades(a: Arbre):
        match a:
            case Abstraccio(variable, expression):
                variables_utilitzades(expression)
                utilitzades.add(str(variable.var))
            case Aplicacio(esquerra, dreta):
                variables_utilitzades(esquerra)
                variables_utilitzades(dreta)
            case Variable(var):
                utilitzades.add(var)

    def alpha_conversio(a: Arbre, parametres):
        match a:
            case Abstraccio(variable, expression):
                parametres.add(str(variable.var))
                (a2, lliures, lligades) = alpha_conversio(expression, parametres)
                lligades.add(str(variable.var))
                parametres.remove(str(variable.var))
                return (Abstraccio(variable, a2), lliures, lligades)
            case Aplicacio(esquerra, dreta):
                (esquerra, lliures1, lligades1) = alpha_conversio(esquerra, parametres)
                (dreta, lliures2, lligades2) = alpha_conversio(dreta, parametres)
                lliures = lliures1.union(lliures2)
                lligades = lligades1.union(lligades2)
                interseccio = lligades.intersection(lliures)
                for i in interseccio:
                    nova = assignar_variable()
                    print('α-conversió: ' + i + ' → ' + nova)
                    convertit = conversio(esquerra, i, nova)
                    print(to_string(esquerra) + ' → ' + to_string(convertit))
                    esquerra = convertit
                return (Aplicacio(esquerra, dreta), lliures, lligades)
            case Variable(var):
                lligades = set()
                lliures = set()
                if var in parametres: lligades.add(var)
                else: lliures.add(var)
                return (a, lliures, lligades)
    
    def conversio(a: arbre, antiga, nova):
        match a:
            case Abstraccio(variable, expression):
                exp_convertida = conversio(expression, antiga, nova)
                if (str(variable.var) == antiga): return Abstraccio(Variable(nova), exp_convertida)
                return Abstraccio(variable, exp_convertida)
            case Aplicacio(esquerra, dreta):
                esq = conversio(esquerra, antiga, nova)
                dre = conversio(dreta, antiga, nova)
                return Abstraccio(esq, dre)
            case Variable(var):
                if (var == antiga): return Variable(nova)
                return a

    def assignar_variable():
        for v in range(ord('a'),ord('z')+1):
            if chr(v) in utilitzades: continue
            utilitzades.add(chr(v))
            return chr(v)

    variables_utilitzades(arbre)
    return alpha_conversio(arbre, set())[0]

def beta(a: Arbre):
    reduccio = False
    #ultim_reduit = a

    def beta_reduccio(arbre: Arbre) -> Arbre:
        nonlocal reduccio
        #nonlocal ultim_reduit
        match arbre:
            case Abstraccio(variable, expressio):
                return Abstraccio(variable, beta_reduccio(expressio))
            case Aplicacio(esquerra, dreta):
                match esquerra:
                    case Abstraccio(variable, expressio):
                        print('β-reducció:')
                        reduit = substitucio(expressio, dreta, str(variable.var))
                        print(to_string(arbre) + ' → ' + to_string(reduit))
                        reduccio = True
                        #if len(to_string(reduit)) == len(to_string(ultim_reduit)): return Variable('Nothing')
                        #ultim_reduit = reduit
                        #return beta_reduccio(reduit)
                        return reduit
                    case Aplicacio(_, _):
                        return Aplicacio(beta_reduccio(esquerra), beta_reduccio(dreta))
                    case Variable(_):
                        return Aplicacio(esquerra, beta_reduccio(dreta))
            case Variable(_):
                return arbre

    def substitucio(arbre: Arbre, substitut: Arbre, variable) -> Arbre:
        match arbre:
            case Abstraccio(var, expressio):
                return Abstraccio(var, substitucio(expressio, substitut, variable))
            case Aplicacio(esquerra, dreta):
                return Aplicacio(substitucio(esquerra, substitut, variable), substitucio(dreta, substitut, variable))
            case Variable(var):
                if var == variable: return substitut
                return arbre

    original = a
    while True:
        beta_reduit = beta_reduccio(a)
        if (not reduccio): return original
        if (len(to_string(beta_reduit)) == len(to_string(original))): return Variable('Nothing')
        if (len(to_string(beta_reduit)) == len(to_string(a))): return beta_reduit
        a = beta_reduit


class TreeVisitor(lcVisitor):

    def visitRoot(self, ctx:lcParser.RootContext):
        return self.visitChildren(ctx)

    def visitAssignacio(self, ctx:lcParser.AssignacioContext):
        variable = str(ctx.getChild(0))
        terme = ctx.getChild(2)
        macros[variable] = self.visit(terme)
        return True

    def visitExpressio(self, ctx:lcParser.ExpressioContext):
        return self.visitChildren(ctx)

    def visitParentesis(self, ctx:lcParser.ParentesisContext):
        terme = ctx.getChild(1)
        return self.visit(terme)

    def visitLletra(self, ctx:lcParser.LletraContext):
        lletra = str(ctx.getChild(0))
        return Variable(lletra)

    def visitVariable(self, ctx:lcParser.VariableContext):
        variable = str(ctx.getChild(0))
        return macros[variable]

    def visitAbstraccio(self, ctx:lcParser.AbstraccioContext):
        terme = ctx.getChild(ctx.getChildCount() - 1)
        lletra = ctx.getChild(ctx.getChildCount() - 3)
        n = Abstraccio(Variable(lletra), self.visit(terme))
        # traducció abstracció de múltiples paràmetres
        for i in range(ctx.getChildCount() - 4, 0, -1): n = Abstraccio(Variable(ctx.getChild(i)), n)
        return n

    def visitAplicacio(self, ctx:lcParser.AplicacioContext):
        [terme1, terme2] = list(ctx.getChildren())
        if (str(ctx.getChild(1).getChild(0)) == '+'): return Aplicacio(self.visit(terme2), self.visit(terme1))
        return Aplicacio(self.visit(terme1), self.visit(terme2))

while True:
    try:
        input_stream = InputStream(input('? '))
        lexer = lcLexer(input_stream)
        token_stream = CommonTokenStream(lexer)
        parser = lcParser(token_stream)
        tree = parser.root()

        if parser.getNumberOfSyntaxErrors() == 0:
            visitor = TreeVisitor()
            arbre = visitor.visit(tree)
            match arbre:
                case True:
                    for m in macros:
                        print(m + '≡' + to_string(macros[m]))
                case _:
                    print('Arbre:')
                    print(to_string(arbre))
                    alpha_convertit = alpha(arbre)
                    beta_reduit = beta(alpha_convertit)
                    print('Resultat:')
                    print(to_string(beta_reduit))
        else:
            print(parser.getNumberOfSyntaxErrors(), 'errors de sintaxi.')
            print(tree.toStringTree(recog=parser))
    except EOFError:
        break