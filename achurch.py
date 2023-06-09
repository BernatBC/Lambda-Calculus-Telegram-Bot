from __future__ import annotations
from dataclasses import dataclass
from antlr4 import *
from lcLexer import lcLexer
from lcParser import lcParser
from lcVisitor import lcVisitor
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler
import math
import pydot
import sys

# Definició de l'arbre d'una expressió
@dataclass
class Abstraccio:
    """Node abstracció
    """

    var: Variable
    expr: Arbre

@dataclass
class Aplicacio:
    """Node aplicació
    """

    esq: Arbre
    dre: Arbre

@dataclass
class Variable:
    """Node variable
    """

    var: str

# Definició d'arbre com a subclasse dels nodes definits
Arbre = Abstraccio | Aplicacio | Variable

# Diccionari que emmagatzema els arbres de cada macro. Clau: Nom de la macro, Valor: Arbre de la macro
macros = {}

# Llista de passos fets, utilitzat per imprimir-los per telegram
steps = []


class TreeVisitor(lcVisitor):
    """Visitador de la gramàtica

    Args:
        lcVisitor (lcVisitor): lcVisitador de la gramàtica
    """

    def visitAssignacio(self, ctx:lcParser.AssignacioContext):
        """Visitador de l'assignació d'una macro

        Args:
            ctx (lcParser.AssignacioContext): Node de la gramàtica

        Returns:
            Bool: True -> s'ha produït l'assignació
        """

        variable = str(ctx.getChild(0))
        terme = ctx.getChild(2)
        macros[variable] = self.visit(terme)
        return True

    def visitParentesis(self, ctx:lcParser.ParentesisContext):
        """Visitador d'un terme entre parèntesis

        Args:
            ctx (lcParser.ParentesisContext): Node de la gramàtica

        Returns:
            Arbre: Arbre resultant del terme introduït
        """

        terme = ctx.getChild(1)
        return self.visit(terme)

    def visitLletra(self, ctx:lcParser.LletraContext):
        """Visitador d'una variable

        Args:
            ctx (lcParser.ParentesisContext): Node de la gramàtica

        Returns:
            Variable: Variable del node
        """
                
        lletra = str(ctx.getChild(0))
        return Variable(lletra)

    def visitVariable(self, ctx:lcParser.VariableContext):
        """Visitador d'una variable de macro

        Args:
            ctx (lcParser.ParentesisContext): Node de la gramàtica

        Returns:
            Arbre: Arbre corresponent al nom de la macro
        """

        variable = str(ctx.getChild(0))
        return macros[variable]

    def visitAbstraccio(self, ctx:lcParser.AbstraccioContext):
        """Visitador d'una abstracció.

        Args:
            ctx (lcParser.ParentesisContext): Node de la gramàtica

        Returns:
            Abstraccio: Node abstraccio resultant
        """

        terme = ctx.getChild(ctx.getChildCount() - 1)
        lletra = ctx.getChild(ctx.getChildCount() - 3)
        n = Abstraccio(Variable(lletra), self.visit(terme))
        # traducció abstracció de múltiples paràmetres
        for i in range(ctx.getChildCount() - 4, 0, -1): n = Abstraccio(Variable(ctx.getChild(i)), n)
        return n

    def visitAplicacio(self, ctx:lcParser.AplicacioContext):
        """Visitador d'una aplicació

        Args:
            ctx (lcParser.ParentesisContext): Node de la gramàtica

        Returns:
            Abstraccio: Node aplicació resultant
        """

        [terme1, terme2] = list(ctx.getChildren())
        x = str(terme2.getChild(0))
        # En el cas que es detecti una macro en notació infixa, convertir-la en notació prefixa
        if (len(x) == 1 and not x.isalpha() and x != '(' and x != '\u005C' and x != 'λ'): 
            return Aplicacio(self.visit(terme2), self.visit(terme1))
        return Aplicacio(self.visit(terme1), self.visit(terme2))


def to_string(arbre: Arbre) -> str:
    """Retorna l'arbre en format de string

    Args:
        arbre (Arbre): Arbre a convertir

    Returns:
        str: Cadena de caràcters que representa l'arbre
    """
    match arbre:
        case Abstraccio(variable, expressio):
            return '(λ' + str(to_string(variable)) + '.' + str(to_string(expressio)) + ')'
        case Aplicacio(esquerra, dreta):
            return '(' + str(to_string(esquerra)) + str(to_string(dreta)) + ')'
        case Variable(var):
            return var


def alpha(arbre: Arbre):
    """Aplica alpha-conversions en un arbre

    Args:
        arbre (Arbre): Arbre a alpha-convertir

    Returns:
        Arbre: Retrona l'arbre després d'aplicar les alpha-conversions
    """

    # Conjunt que emmagatzema els noms de totes les variables que apareixen a l'arbre abans d'aplicar l'alpha-conversió
    utilitzades = set()

    def variables_utilitzades(a: Arbre):
        """Mètode que afageix al conjunt "utilitzades" les variables que apareixen a l'arbre abans d'aplicar l'alpha-conversió

        Args:
            a (Arbre): Arbre a visitar
        """

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
        """Mètode que fa les alpha-conversions

        Args:
            a (Arbre): Arbre a alpha-convertir
            parametres (_type_): Llista dels paràmetres de les funcions lambda tals que fa afecte a l'arbre a

        Returns:
            Arbre: Arbre alpha-convertit
        """

        match a:
            case Abstraccio(variable, expression):
                v = str(variable.var)
                # alpha-conversió λx.λx.x → λx.λa.a
                if (v in parametres):
                    nova = assignar_variable()
                    print('α-conversió: ' + v + ' → ' + nova)
                    convertit = conversio(expression, v, nova)
                    print(to_string(Abstraccio(Variable(v), expression)) + ' → ' + to_string(Abstraccio(Variable(nova), convertit)))
                    steps.append(to_string(Abstraccio(Variable(v), expression)) + ' → α → ' + to_string(Abstraccio(Variable(nova), convertit)))
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
                    print('α-conversió: ' + i + ' → ' + nova)
                    convertit = conversio(esquerra, i, nova)
                    print(to_string(esquerra) + ' → ' + to_string(convertit))
                    steps.append(to_string(esquerra) + ' → α → ' + to_string(convertit))
                    esquerra = convertit
                # alpha-conversió prevenir possible conflicte després de beta-reducció
                interseccio2 = lligades1.intersection(lligades2)
                for i in interseccio2:
                    if i in parametres:
                        continue
                    nova = assignar_variable()
                    print('α-conversió: ' + i + ' → ' + nova)
                    convertit = conversio(esquerra, i, nova)
                    print(to_string(esquerra) + ' → ' + to_string(convertit))
                    steps.append(to_string(esquerra) + ' → α → ' + to_string(convertit))
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
    
    def conversio(a: arbre, antiga, nova):
        """Substitueix els noms de les variables d'antiga a nove del arbre

        Args:
            a (arbre): Arbre a convertir
            antiga (str): nom de la variable per substituir
            nova (str): nom de la variable substituda

        Returns:
            Arbre: Arbre convertit
        """

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

    def assignar_variable():
        """Retorna un nom de variable sense utilitzar, i el marca com a utilitzada

        Returns:
            str: nom de la variable
        """

        # Si ens quedem sense variables, afegim cometes al final de la variable
        n_cometes = 0
        while True:
            for v in range(ord('a'),ord('z')+1):
                variable = chr(v) + n_cometes*"'"
                if variable in utilitzades:
                    continue
                utilitzades.add(variable)
                return variable
            n_cometes += 1

    variables_utilitzades(arbre)
    return alpha_conversio(arbre, set())[0]


def beta(a: Arbre):
    """Mètode que aplica beta-reduccions

    Args:
        a (Arbre): Arbre a beta-reduir

    Returns:
        Arbre: Arbre beta-reduit
    """

    # Compta el nombre de beta-reduccions fetes
    n_reduccions = 0

    def beta_reduccio(arbre: Arbre) -> Arbre:
        """Mètode que aplica una beta-reducció (o cap si no n'hi ha cap de possible)

        Args:
            arbre (Arbre): Arbre a beta-reduit

        Returns:
            Arbre: Arbre beta-reduit
        """

        nonlocal n_reduccions
        match arbre:
            case Abstraccio(variable, expressio):
                return Abstraccio(variable, beta_reduccio(expressio))
            case Aplicacio(esquerra, dreta):
                match esquerra:
                    case Abstraccio(variable, expressio):
                        print('β-reducció:')
                        reduit = substitucio(expressio, dreta, str(variable.var))
                        print(to_string(arbre) + ' → ' + to_string(reduit))
                        steps.append(to_string(arbre) + ' → β → ' + to_string(reduit))
                        n_reduccions += 1
                        return reduit
                    case Aplicacio(_, _):
                        return Aplicacio(beta_reduccio(esquerra), beta_reduccio(dreta))
                    case Variable(_):
                        return Aplicacio(esquerra, beta_reduccio(dreta))
            case Variable(_):
                return arbre

    def substitucio(arbre: Arbre, substitut: Arbre, variable) -> Arbre:
        """Aplica la substitució d'una beta-reducció

        Args:
            arbre (Arbre): _description_
            substitut (Arbre): Arbre substitut
            variable (_type_): Variable substituida

        Returns:
            Arbre: Arbre resultant de la substitució
        """

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


def genera_imatge(a: Arbre):
    """Funció que genera la imatge output.png de l'arbre

    Args:
        a (Arbre): Arbre a imprimir
    """
     
    graph = pydot.Dot('my_graph', graph_type='digraph', bgcolor='white')

    # Visitador per generar la imatge
    def visitador(arbre: Arbre, id):
        match arbre:
            # Els nodes abstracció tindran l'id del seu paràmetre
            case Abstraccio(variable, expressio):
                id_node = id + str(to_string(variable))
                graph.add_node(pydot.Node(id_node, label='λ'+str(to_string(variable)),shape='none'))
                id_fill = visitador(expressio, id_node)
                graph.add_edge(pydot.Edge(id_node, id_fill,arrowsize=0.75))
                return id_node
            # Els nodes aplicació tindran l'id d'una @, i a més a més a cada fill se li afageix un número per distingir-los
            case Aplicacio(esquerra, dreta):
                id_node = id + '@'
                graph.add_node(pydot.Node(id_node, label='@',shape='none'))
                id_fill1 = visitador(esquerra, id_node + '1')
                id_fill2 = visitador(dreta, id_node + '2')
                graph.add_edge(pydot.Edge(id_node, id_fill1,arrowsize=0.75))
                graph.add_edge(pydot.Edge(id_node, id_fill2,arrowsize=0.75))
                return id_node
            # Els nodes variable tindran l'id de -
            case Variable(var):
                id_node = id + '-'
                graph.add_node(pydot.Node(id_node, label=var,shape='none'))
                # Trobar variables lligades. Si tenen la variable a l'id, significa que hi ha una funció amb aquest paràmetre, i només ens cal agafar el seu node
                if var in id:
                    last_ocurrence = id.rfind(var) + 1
                    id_parametre = id_node[:last_ocurrence]
                    graph.add_edge(pydot.Edge(id_node, id_parametre,style='dotted', arrowsize=0.75))
                return id_node

    visitador(a, '')
    graph.write_png('output.png')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Definició de la comanda de telegram /start

    Args:
        update (Update): Actualització entrant
        context (ContextTypes.DEFAULT_TYPE): Context
    """

    name = update.effective_user.first_name
    await update.message.reply_text('Welcome ' + name + '!')
    await update.message.reply_text('Write /help to list the available commands')


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Definició de la comanda de telegram /help

    Args:
        update (Update): Actualització entrant
        context (ContextTypes.DEFAULT_TYPE): Context
    """
        
    await update.message.reply_text('/start - shows a welcome message\
                                    \n/help - shows this message\
                                    \n/author - author information \
                                    \n/macros - shows list of macros\
                                    \n/clear - clears list of macros\
                                    \nλ-calculus expression\
                                    \ndefine a macro')
    await update.message.reply_text('Examples of λ-calculus expression:\
                                    \nλx.y\
                                    \nλxy.z\
                                    \n(\y.x(yz))(ab)\
                                    \n(λx.x((λz.zz)x))t\
                                    \n\
                                    \nnote that variables must be lowercase letters, expressions might contain macros')
    await update.message.reply_text('Defining macros:\
                                    \nMACRO_NAME=expression\
                                    \nMACRO_NAME≡expression\
                                    \n\
                                    \nMACRO_NAME:\
                                    \n -prefix macro → uppercase letters and numbers, first charachter must be an uppercase letter\
                                    \n - infix macro → symbols such as +,-,*')


async def author(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Definició de la comanda de telegram /author

    Args:
        update (Update): Actualització entrant
        context (ContextTypes.DEFAULT_TYPE): Context
    """
        
    await update.message.reply_text('λ-Calculus Bot\
                                    \nBernat Borràs Civil, 2023\
                                    \nTelegram/GitHub: @BernatBC')


async def tracta_expressio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Tractament de l'expressió introduida per telegram

    Args:
        update (Update): Actualització entrant
        context (ContextTypes.DEFAULT_TYPE): Context
    """
        
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
                genera_imatge(arbre)
                await update.message.reply_photo(photo=open('output.png', 'rb'))
                steps.clear()
                alpha_convertit = alpha(arbre)
                beta_reduit = beta(alpha_convertit)
                for s in steps:
                    await update.message.reply_text(s)
                await update.message.reply_text(to_string(beta_reduit))
                genera_imatge(beta_reduit)
                await update.message.reply_photo(photo=open('output.png', 'rb'))
    else:
        print(parser.getNumberOfSyntaxErrors(), 'errors de sintaxi.')
        print(tree.toStringTree(recog=parser))


async def llista_macros(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Definició de la comanda de telegram /macros

    Args:
        update (Update): Actualització entrant
        context (ContextTypes.DEFAULT_TYPE): Context
    """
        
    message = ''
    for m in macros:
        message = message + '\n' + m + ' ≡ ' + to_string(macros[m])
    if message == '':
        message = 'The list of macros is empty\n'
    await update.message.reply_text(message)


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Definició de la comanda de telegram /clear

    Args:
        update (Update): Actualització entrant
        context (ContextTypes.DEFAULT_TYPE): Context
    """
        
    macros.clear()
    await update.message.reply_text('Macros have been cleared')


def run_telegram():
    """Funció que permet executar l'intèrpret mitjançant telegram
    """

    TOKEN = open('token.txt').read().strip()
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("author", author))
    app.add_handler(CommandHandler("clear", clear))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("macros", llista_macros))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, tracta_expressio))

    app.run_polling()


def run_terminal():
    """Funció que permet executar l'intèrpret mitjançant la terminal
    """

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
                            print(m + ' ≡ ' + to_string(macros[m]))
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
        except (EOFError, KeyboardInterrupt):
            break


# Inici execució intèrpret. Seleccionar entre execució per terminal o al telegram
if (len(sys.argv) >= 2 and sys.argv[1] == 'terminal'):
    run_terminal()
else:
    run_telegram()