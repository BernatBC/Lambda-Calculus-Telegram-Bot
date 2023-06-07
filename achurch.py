from __future__ import annotations
from dataclasses import dataclass
from antlr4 import *
from lcLexer import lcLexer
from lcParser import lcParser
from lcVisitor import lcVisitor

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler
import math

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

# Diccionari que emmagatzema els arbres de cada macro. Clau: Nom de la macro, Valor: Arbre de la macro
macros = {}

steps = []

# Retorna l'arbre en format de string
def to_string(arbre: Arbre) -> str:
    match arbre:
        case Abstraccio(variable, expressio):
            return '(λ' + str(to_string(variable)) + '.' + str(to_string(expressio)) + ')'
        case Aplicacio(esquerra, dreta):
            return '(' + str(to_string(esquerra)) + str(to_string(dreta)) + ')'
        case Variable(var):
            return var            

# Retrona l'arbre després d'aplicar les alpha-conversions
def alpha(arbre: Arbre):

    # Conjunt que emmagatzema els noms de totes les variables que apareixen a l'arbre abans d'aplicar l'alpha-conversió
    utilitzades = set()

    # Mètode que afageix al conjunt "utilitzades" les variables que apareixen a l'arbre abans d'aplicar l'alpha-conversió
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

    # Mètode que fa les alpha-conversions
    def alpha_conversio(a: Arbre, parametres):
        match a:
            case Abstraccio(variable, expression):
                v = str(variable.var)
                # alpha-conversió λx.λx.x → λx.λa.a
                if (v in parametres):
                    nova = assignar_variable()
                    convertit = conversio(expression, v, nova)
                    steps.append(to_string(Abstraccio(Variable(v), expression)) + ' → β → ' + to_string(Abstraccio(Variable(nova), convertit)))
                    v = nova
                    expression = convertit
                parametres.add(v)
                (a2, lliures, lligades) = alpha_conversio(expression, parametres)
                lligades.add(v)
                parametres.remove(v)
                return (Abstraccio(Variable(v), a2), lliures, lligades)
            case Aplicacio(esquerra, dreta):
                # alpha-conversió conflicte variable lligada i variable lliure
                (esquerra, lliures1, lligades1) = alpha_conversio(esquerra, parametres)
                (dreta, lliures2, lligades2) = alpha_conversio(dreta, parametres)
                lliures = lliures1.union(lliures2)
                lligades = lligades1.union(lligades2)
                interseccio = lligades.intersection(lliures)
                for i in interseccio:
                    nova = assignar_variable()
                    convertit = conversio(esquerra, i, nova)
                    steps.append(to_string(esquerra) + ' → β → ' + to_string(convertit))
                    esquerra = convertit
                # alpha-conversió prevenir possible conflicte després de beta-reducció
                interseccio2 = lligades1.intersection(lligades2)
                for i in interseccio2:
                    if i in parametres:
                        continue
                    nova = assignar_variable()
                    convertit = conversio(esquerra, i, nova)
                    steps.append(to_string(esquerra) + ' → β → ' + to_string(convertit))
                    esquerra = convertit
                return (Aplicacio(esquerra, dreta), lliures, lligades)
            case Variable(var):
                lligades = set()
                lliures = set()
                if var in parametres:
                    lligades.add(var)
                else:
                    lliures.add(var)
                return (a, lliures, lligades)
    
    # Substitueix els noms de les variables d'antiga a nove del arbre
    def conversio(a: arbre, antiga, nova):
        match a:
            case Abstraccio(variable, expression):
                exp_convertida = conversio(expression, antiga, nova)
                if (str(variable.var) == antiga):
                    return Abstraccio(Variable(nova), exp_convertida)
                return Abstraccio(variable, exp_convertida)
            case Aplicacio(esquerra, dreta):
                esq = conversio(esquerra, antiga, nova)
                dre = conversio(dreta, antiga, nova)
                return Aplicacio(esq, dre)
            case Variable(var):
                if (var == antiga):
                    return Variable(nova)
                return a

    # Retorna un nom de variable sense utilitzar, i el marca com a utilitzada
    def assignar_variable():
        for v in range(ord('a'),ord('z')+1):
            if chr(v) in utilitzades:
                continue
            utilitzades.add(chr(v))
            return chr(v)

    variables_utilitzades(arbre)
    return alpha_conversio(arbre, set())[0]

# Retrona l'arbre després d'aplicar una alpha-conversió
def beta(a: Arbre):

    # Compta el nombre de beta-reduccions fetes
    n_reduccions = 0

    # Mètode que aplica una beta-reducció (o cap si no n'hi ha cap de possible)
    def beta_reduccio(arbre: Arbre) -> Arbre:
        nonlocal n_reduccions
        match arbre:
            case Abstraccio(variable, expressio):
                return Abstraccio(variable, beta_reduccio(expressio))
            case Aplicacio(esquerra, dreta):
                match esquerra:
                    case Abstraccio(variable, expressio):
                        reduit = substitucio(expressio, dreta, str(variable.var))
                        steps.append(to_string(arbre) + ' → β → ' + to_string(reduit))
                        n_reduccions += 1
                        return reduit
                    case Aplicacio(_, _):
                        return Aplicacio(beta_reduccio(esquerra), beta_reduccio(dreta))
                    case Variable(_):
                        return Aplicacio(esquerra, beta_reduccio(dreta))
            case Variable(_):
                return arbre

    # Aplica la substitució d'una beta-reducció
    def substitucio(arbre: Arbre, substitut: Arbre, variable) -> Arbre:
        match arbre:
            case Abstraccio(var, expressio):
                return Abstraccio(var, substitucio(expressio, substitut, variable))
            case Aplicacio(esquerra, dreta):
                return Aplicacio(substitucio(esquerra, substitut, variable), substitucio(dreta, substitut, variable))
            case Variable(var):
                if var == variable:
                    return substitut
                return arbre

    # Bucle que fa les betes-reduccions possibles mentres no es superi un nombre determinat 
    original = a
    iterations = math.ceil(len(str(to_string(original)))/2)
    for i in range(0,iterations):
        beta_reduit = beta_reduccio(a)
        if (n_reduccions == 0):
            return original
        if (i > n_reduccions):
            return beta_reduit
        a = beta_reduit
    return Variable('Nothing')

# Visitador de la gramàtica
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
        x = str(terme2.getChild(0))
        # En el cas que es detecti una macro en notació infixa, convertir-la en notació prefixa
        if (len(x) == 1 and not x.isalpha() and x != '(' and x != '\u005C' and x != 'λ'): 
            return Aplicacio(self.visit(terme2), self.visit(terme1))
        return Aplicacio(self.visit(terme1), self.visit(terme2))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('/start\n/author\n/help\n/macros\nλ-calculus expression')

async def author(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('λ-Calculus Bot\nBernat Borràs Civil, 2023\nTelegram/GitHub: @BernatBC')

async def tracta_expressio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    input_stream = InputStream(update.message.text)
    lexer = lcLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = lcParser(token_stream)
    tree = parser.root()

    if parser.getNumberOfSyntaxErrors() == 0:
        visitor = TreeVisitor()
        arbre = visitor.visit(tree)
        match arbre:
            case True:
                return
            case _:
                await update.message.reply_text(to_string(arbre))
                alpha_convertit = alpha(arbre)
                beta_reduit = beta(alpha_convertit)
                for s in steps:
                    await update.message.reply_text(s)
                await update.message.reply_text(to_string(beta_reduit))
                steps.clear()
    else:
        print(parser.getNumberOfSyntaxErrors(), 'errors de sintaxi.')
        print(tree.toStringTree(recog=parser))

async def llista_macros(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = ''
    for m in macros:
        message = message + '\n' + m + ' ≡ ' + to_string(macros[m])
    await update.message.reply_text(message)

TOKEN = open('token.txt').read().strip()

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help))
app.add_handler(CommandHandler("author", author))
app.add_handler(CommandHandler("macros", llista_macros))
app.add_handler(MessageHandler(filters.TEXT, tracta_expressio))

app.run_polling()