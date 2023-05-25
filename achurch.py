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

def to_string(arbre: Arbre) -> str:
    match arbre:
        case Abstraccio(variable, expressio):
            return '(λ' + str(to_string(variable)) + '.' + str(to_string(expressio)) + ')'
        case Aplicacio(esquerra, dreta):
            return '(' + str(to_string(esquerra)) + str(to_string(dreta)) + ')'
        case Variable(var):
            return var            

def alpha(arbre:Arbre):

    used_vars = set()
    vars_dictionary = {}
    convertit = False

    def get_free_variables(a: Arbre, bounded):
        match a:
            case Abstraccio(_, _):
                return
            case Aplicacio(esquerra, dreta):
                get_free_variables(esquerra, bounded)
                get_free_variables(dreta, bounded)
                return
            case Variable(var):
                if var in bounded: return
                used_vars.add(var)
                return

    def alpha_conversio(a: Arbre, bounded_vars) -> Arbre:
        nonlocal convertit
        match a:
            case Abstraccio(variable, expressio):
                old_var = str(variable.var)
                bounded_vars.append(old_var)
                if old_var in used_vars:
                    new_var = assign_variable()
                    variable = Variable(new_var)
                    vars_dictionary[old_var] = new_var
                    convertit = True
                    print('α-conversió: ' + old_var + ' → ' + new_var)
                abstracted = Abstraccio(variable, alpha_conversio(expressio, bounded_vars))
                bounded_vars.remove(old_var)
                return abstracted
            case Aplicacio(esquerra, dreta):
                return Aplicacio(alpha_conversio(esquerra, bounded_vars), alpha_conversio(dreta, bounded_vars))
            case Variable(var):
                if var in used_vars and var in bounded_vars: var = vars_dictionary[var]
                return Variable(var)

    def assign_variable():
        for v in range(ord('a'),ord('z')+1):
            if chr(v) in used_vars: continue
            used_vars.add(chr(v))
            return chr(v)
        
    get_free_variables(arbre,set())
    alpha_convertit = alpha_conversio(arbre, [])
    # TODO: imprimir alpha-reduccio
    if convertit: print(to_string(arbre) + ' → ' + to_string(alpha_convertit))
    return alpha_convertit

def beta_reduccio(arbre: Arbre) -> Arbre:
    match arbre:
        case Abstraccio(variable, expressio):
            return Abstraccio(variable, beta_reduccio(expressio))
        case Aplicacio(esquerra, dreta):
            match esquerra:
                case Abstraccio(variable, expressio):
                    print('β-reducció:')
                    reduit = substitucio(expressio, dreta, str(variable.var))
                    print(to_string(arbre) + ' → ' + to_string(reduit))
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
        for i in range(ctx.getChildCount() - 4, 0, -1): n = Abstraccio(Variable(ctx.getChild(i)), n)
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
    arbre = visitor.visit(tree)
    print('Arbre:')
    print(to_string(arbre))

    alpha_convertit = alpha(arbre)
    arbre = alpha_convertit
    while True: 
        beta_reduit = beta_reduccio(arbre)
        if len(to_string(beta_reduit)) == len(to_string(alpha_convertit)):
            print('Resultat:')
            print('Nothing')
            break
        if len(to_string(beta_reduit)) == len(to_string(arbre)):
            print('Resultat:')
            print(to_string(beta_reduit))
            break
        arbre = beta_reduit

else:
    print(parser.getNumberOfSyntaxErrors(), 'errors de sintaxi.')
    print(tree.toStringTree(recog=parser))