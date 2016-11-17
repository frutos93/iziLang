import ply.lex as lex
import ply.yacc as yacc

# + = 0
# - = 1
# * = 2
# / = 3
# && = 4
# || = 5
# = = 6
# >= = 7
# <= = 8
# > = 9
# < = 10
# <> = 11
# == = 12

# ENTERO = 101
# DECIMAL = 102
# PALABRA = 103
# BOOLEANO = 104

funciones = {}
variables = {}
variablesGlobales = {}
constants = {}
tipoDeVariable = ""
stackTipos = []
stackOper = []
stackOp = []
stackJumps = []
stackOpVisible = []
avail = {}
cuadruplos = []
parametros = []

def oper2Code (oper):
    if (oper == '+'):
        return 0
    if (oper == '-'):
        return 1
    if (oper == '*'):
        return 2
    if (oper == '/'):
        return 3
    if (oper == '&&'):
        return 4
    if (oper == '||'):
        return 5
    if (oper == '='):
        return 6
    if (oper == '>='):
        return 7
    if (oper == '<='):
        return 8
    if (oper == '>'):
        return 9
    if (oper == '<'):
        return 10
    if (oper == '<>'):
        return 11
    if (oper == '=='):
        return 12
    if (oper == 'goto'):
       return 13
    if (oper == 'gotoF'):
         return 14
    if (oper == 'print'):
         return 15
    if (oper == 'getValue'):
         return 16
    if (oper == 'getLine'):
         return 17
    if (oper == 'getBoolean'):
         return 16
    if (oper == 'getString'):
         return 18

cuboSemantico = [
                [[101,102, -1, -1], [102,102, -1, -1], [ -1, -1, -1, -1], [ -1, -1, -1, -1]],
                [[101,102, -1, -1], [102,102, -1, -1], [ -1, -1, -1, -1], [ -1, -1, -1, -1]],
                [[101,102, -1, -1], [102,102, -1, -1], [ -1, -1, -1, -1], [ -1, -1, -1, -1]],
                [[101,102, -1, -1], [102,102, -1, -1], [ -1, -1, -1, -1], [ -1, -1, -1, -1]],
                [[ -1, -1, -1, -1], [ -1, -1, -1, -1], [ -1, -1, -1, -1], [ -1, -1, -1,104]],
                [[ -1, -1, -1, -1], [ -1, -1, -1, -1], [ -1, -1, -1, -1], [ -1, -1, -1,104]],
                [[ -1, -1, -1, -1], [ -1, -1, -1, -1], [ -1, -1, -1, -1], [ -1, -1, -1, -1]],
                [[104,104, -1, -1], [104,104, -1, -1], [ -1, -1, -1, -1], [ -1, -1, -1, -1]],
                [[104,104, -1, -1], [104,104, -1, -1], [ -1, -1, -1, -1], [ -1, -1, -1, -1]],
                [[104,104, -1, -1], [104,104, -1, -1], [ -1, -1, -1, -1], [ -1, -1, -1, -1]],
                [[104,104, -1, -1], [104,104, -1, -1], [ -1, -1, -1, -1], [ -1, -1, -1, -1]],
                [[104,104, -1, -1], [104,104, -1, -1], [ -1, -1,104, -1], [ -1, -1, -1,104]],
                [[104,104, -1, -1], [104,104, -1, -1], [ -1, -1,104, -1], [ -1, -1, -1,104]]
		        ]

def Type2Code(tipo):
    if (tipo == "ENTERO"):
        return 101
    elif (tipo == "DECIMAL"):
        return 102
    elif (tipo == "PALABRA"):
        return 103
    elif (tipo == "BOOLEANO"):
        return 104

class LexerError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class SyntaxError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class SemanticError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

tokens = ('PRINT', 'RETURN', 'ARRIBA', 'ABAJO', 'IZQUIERDA','DERECHA', 'DECIMAL', 'BORRAR', 'MIENTRAS', 'REPETIR', 'DIBUJASI', 'DIBUJANO', 'COLOR', 'CUANDO', 'FIN', 'CIRCULO', 'CUADRADO', 'RECTANGULO', 'TRIANGULO', 'LINEA', 'ENTERO', 'PALABRA', 'EN', 'PARATODOS', 'BOOLEANO', 'PROGRAMA', 'FUNCION', 'MAIN', 'LISTA', 'FALSO', 'SINO', 'EQUALS', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN', 'EQUALSC' , 'LT', 'LE', 'GT', 'GE', 'NE', 'COMMA', 'SEMI', 'COLON', 'INTEGER', 'CTE_F', 'STRING', 'LCURLY', 'RCURLY', 'LBRACKET', 'RBRACKET', 'CTE_E', 'CTE_B', 'ID', 'ERROR', 'AND', 'OR', 'CTE_S', 'FLOAT', 'AMPERSAND', 'QM')

t_PRINT = r'PRINT'
t_RETURN = r'RETURN'
t_ARRIBA = r'ARRIBA'
t_IZQUIERDA = r'IZQUIERDA'
t_DERECHA = r'DERECHA'
t_BORRAR = r'BORRAR'
t_MIENTRAS = r'MIENTRAS'
t_REPETIR = r'REPETIR'
t_DIBUJASI = r'DIBUJASI'
t_DIBUJANO = r'DIBUJANO'
t_COLOR = r'COLOR'
t_CUANDO = r'CUANDO'
t_FIN = r'FIN'
t_CIRCULO = r'CIRCULO'
t_CUADRADO = r'CUADRADO'
t_RECTANGULO = r'RECTANGULO'
t_TRIANGULO = r'TRIANGULO'
t_LINEA = r'LINEA'
t_ENTERO = r'ENTERO'
t_DECIMAL = r'DECIMAL'
t_PALABRA = r'PALABRA'
t_FUNCION = r'FUNCION'
t_MAIN = r'MAIN'
t_PARATODOS = r'PARATODOS'
t_PROGRAMA = r'PROGRAMA'
t_SINO = r'SINO'
t_BOOLEANO = r'BOOLEANO'
t_LISTA = r'LISTA'
t_EN = r'EN'

t_QM = r'\"'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_EQUALS = r'\='
t_EQUALSC = r'\=\='
t_LT = r'[<]'
t_LE = r'\<\='
t_GT = r'[>]'
t_GE = r'\>\='
t_NE = r'\<\>'
t_COMMA = r'\,'
t_SEMI = r';'
t_COLON = r':'
t_INTEGER = r'\d+'
t_FLOAT = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'
t_STRING = r'\".*?\"'
t_LCURLY = r'\{'
t_RCURLY = r'\}'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_AND = r'[&][&]'
t_OR = r'[|][|]'
t_AMPERSAND = r'\&'

def t_CTE_F(t):
    r'[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t


def t_CTE_E(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[a-z][a-zA-Z0-9]*'
    if t.value in tokens:
        t.type = t.value
    return t

def t_CTE_B(t):
    r'VERDADERO|FALSO'
    return t

#def t_NEWLINE(t):
#    r'\n'
#    t.lexer.lineno += 1
#    return t

def t_error(t):
    raise LexerError("Illegal character at '%s'" % t.value[0])

t_CTE_S = r'\"[A-Za-z0-9_\(\)\{\}\[\]\<\>\! \t]*\"'

t_ignore = ' \n'

lex.lex(debug=0)


def p_programa(p):
    """
    programa : PROGRAMA ID COLON programa_aux1 guarda_variables_global programa_aux1_1 programa_aux2 main FIN
    """
    global variablesGlobales, constants
    variablesGlobales = {}
    funciones["constants"] = constants

def p_guarda_variables_global(p):
    """
    guarda_variables_global :
    """
    global funciones, variablesGlobales, variables, avail
    for key in variables.keys():
        variables[key]["memoria"] = avail[0][variables[key]["tipo"]]
        avail[0][variables[key]["tipo"]]+= 1
    variablesGlobales = variables
    variables = {}
    funciones["global"] = variablesGlobales
def p_programa_aux1(p):
    """
    programa_aux1 : variables
                    |
    """


def p_programa_aux1_1(p):
    """
    programa_aux1_1 : asignacion
                    |
    """

def p_programa_aux2(p):
    """
    programa_aux2 : funciones
                    |
    """


def p_variables(p):
    """
    variables : variables_aux1 SEMI variables_aux2
    """


def p_variables_aux1(p):
    """
    variables_aux1 : tipo ID variables_aux3
    """
    global variables, tipo
    if (variables.has_key(p[2])):
        raise SemanticError("Ya existe esa variable: " + p[2])
    variables[p[2]] = {"tipo": Type2Code(tipo)}


def p_variables_aux2(p):
    """
    variables_aux2 : variables
                     |
    """


def p_variables_aux3(p):
    """variables_aux3 : lista
                        |
    """

def p_main(p):
    """
    main : MAIN LPAREN RPAREN bloque
    """
    global funciones, variables, avail
    if (funciones.has_key(p[1])):
        raise SemanticError("Solo puede haber una funcion main")
    funciones[p[1]] = {"variables": variables}
    variables = {}

def p_funciones(p):
    """
    funciones : FUNCION tipo ID LPAREN funciones_aux1 RPAREN bloque funciones_aux2
    """
    global funciones, variables, parametros
    if(funciones.has_key(p[3])):
        raise SemanticError("Ya existe esa funcion: " + p[3])
    funciones[p[3]] = {"variables": variables,"parametros": parametros}
    variables = {}

def p_funciones_aux1(p):
    """
    funciones_aux1 : tipo arg funciones_aux3
    |
    """

def p_arg(p):
    """
    arg : AMPERSAND ID
         | ID
    """
    global variables, tipo, parametros
    if (p[1] == '&'):
        if(variables.has_key(p[2])):
            raise SemanticError("Ya existe esa variable: " + p[2])
        variables[p[2]] = {"tipo": Type2Code(tipo), "porReferencia": True}
        parametros.append(Type2Code(tipo))
    else:
        if (variables.has_key(p[1])):
            raise SemanticError("Ya existe esa variable: " + p[1])
        variables[p[1]] = {"tipo": Type2Code(tipo), "porReferencia": False}
        parametros.append(Type2Code(tipo))

def p_funciones_aux2(p):
    """funciones_aux2 : funciones
                        |
    """

def p_funciones_aux3(p):
    """
    funciones_aux3 : COMMA funciones_aux1
                     |
    """

def p_lista(p):
    """
    lista : LBRACKET cte RBRACKET
    """

def p_tipo(p):
    """
    tipo : ENTERO
           | DECIMAL
           | PALABRA
           | BOOLEANO
    """
    global tipo
    tipo = p[1]

def p_bloque(p):
    """
    bloque : LCURLY bloque_aux1 guarda_variables_local bloque_aux2 RCURLY
    """

def p_guarda_variables_local(p):
    """
    guarda_variables_local :
    """
    global variables, avail
    for key in variables.keys():
        tipoNumero = variables[key]["tipo"]
        if tipoNumero < 1000:
            variables[key]["memoria"] = avail[1][tipoNumero]
            avail[1][tipoNumero] += 1

def p_bloque_aux1(p):
    """
    bloque_aux1 : variables
                  |
    """

def p_bloque_aux2(p):
    """
    bloque_aux2 : estatuto bloque_aux2
                  |
    """

def p_estatuto(p):
    """
    estatuto : asignacion checa_stack_a
             | condicion
             | accion
             | mientras
             | paratodos
             | print
             | return
    """

def p_print(p):
    """
    print : PRINT LPAREN print_aux RPAREN
    """

def p_print_aux(p):
    """
    print_aux : expresion print_aux2
    """

def p_print_aux2(p):
    """
    print_aux2 : COMMA print_aux
               |
    """
    global stackOp, stackTipos, stackOpVisible, cuadruplos
    expresion = stackOp.pop()
    stackTipos.pop()
    stackOpVisible.pop()
    cuadruplos.append([oper2Code('print'), 'null', 'null', expression])

def p_checa_stack_a(p):
     """
     checa_stack_a :
     """
     global stackOper, stackTipos, stackOp, cuadruplos
     print (stackOp)
     if (stackOper):
         if (stackOper[-1] == '='):
             operador = oper2Code(stackOper.pop())
             op2 = stackOp.pop()
             op1 = stackOp.pop()
             op2Tipo = stackTipos.pop()
             op1Tipo = stackTipos.pop()
             if (op1Tipo != op2Tipo):
                 raise SemanticError("Tipos incompatibles: " + str(op2Tipo) + " y " + str(op1Tipo))
             cuadruplos.append([operador, op2, 'null', op1])

def p_asignacion(p):
    """
    asignacion : id_aux asignacion_aux1 push_a expresion SEMI
    """

def p_push_a(p):
    """push_a : EQUALS"""
    global stackOper
    stackOper.append(p[1])

def p_asignacion_aux1(p):
    """
    asignacion_aux1 : LBRACKET exp RBRACKET
                      |
    """

def p_condicion(p):
    """
    condicion : CUANDO LPAREN expresion RPAREN genera_gotoF_if bloque condicion_aux1 genera_fin_if
    """

def p_condicion_aux1(p):
    """
    condicion_aux1 : SINO genera_goto_sino bloque
    |
    """

def p_genera_goto_sino(p):
    """
    genera_goto_sino :
    """
    global stackJumps, cuadruplos
    cuadruplos.append([oper2Code("goto"),'null','null','espera'])
    falseJump = stackJumps.pop()
    cuadruplos[falseJump][3] = len(cuadruplos) + 1
    stackJumps.append(len(cuadruplos) - 1)

def p_genera_gotoF_if(p):
    """
    genera_gotoF_if :
    """
    global stackOp, stackTipos, stackOpVisible, stackJumps, cuadruplos
    tipoActual = stackTipos.pop()
    if (tipoActual != Type2Code("boolean")):
        raise SemanticError("Se espera un booleano en la condicion. Se recibio un: " + str(tipoActual))
    condicion = stackOp.pop()
    stackOpVisible.pop()
    cuadruplos.append([oper2Code("gotoF"), condicion, 'null', 'espera'])
    stackJumps.append(len(cuadruplos) - 1)

def p_genera_fin_if(p):
    """
    genera_fin_if :
    """
    global stackJumps, cuadruplos
    finJump = stackJumps.pop()
    cuadruplos[finJump][3] = len(cuadruplos) + 1

def p_expresion(p):
    """
    expresion : exp_and checa_stack_or expresion_aux1
    """

def p_checa_stack_or(p):
    """
    checa_stack_or :
    """
    global stackOper
    if (stackOper):
        if (stackOper[-1] == '||'):
            generateArithmeticCode()

def p_expresion_aux1(p):
    """
    expresion_aux1 : OR exp_and
                     |
    """
    global stackOper
    try:
        if(p[1] == '||'):
            stackOper.append(p[1])
    except IndexError:
        return

def p_exp_and(p):
    """
    exp_and : exp_comp checa_stack_and exp_and_aux1
    """

def p_checa_stack_and(p):
    """
    checa_stack_and :
    """
    global stackOper
    if (stackOper):
        if (stackOper[-1] == '&&'):
            generateArithmeticCode()

def p_exp_and_aux1(p):
    """
    exp_and_aux1 : AND exp_comp
                  |
    """
    global stackOper
    try:
        if (p[1] == '&&'):
            stackOper.append(p[1])
    except IndexError:
        return

def p_exp_comp(p):
    """
    exp_comp : exp exp_comp_aux1 checa_stack_comp
    """

def p_checa_stack_comp(p):
    """
    checa_stack_comp :
    """
    global stackOper
    if (stackOper):
        if (stackOper[-1] == '>' or stackOper[-1] == '>=' or stackOper[-1] == '<' or stackOper[-1] == '<=' or stackOper[-1] == '<>' or stackOper[-1] == '=='):
            generateArithmeticCode()

def p_exp_comp_aux1(p):
    """
    exp_comp_aux1 : GT
                  | GE
                  | LT
                  | LE
                  | NE
                  | EQUALSC
                  |
    """
    global stackOper
    try:
        if (p[1] == '>' or p[1] == '>=' or p[1] == '<' or p[1] == '<=' or p[1] == '<>' or p[1] == '=='):
            stackOper.append(p[1])
    except IndexError:
        return

def p_exp(p):
    """
    exp : termino checa_stack_pm exp_aux1
    """

def p_checa_stack_pm(p):
     """
     checa_stack_pm :
     """
     global stackOper
     if (stackOper):
         if (stackOper[-1] == '+' or stackOper[-1] == '-'):
             generateArithmeticCode()

def p_exp_aux1(p):
    """
    exp_aux1 : push_pm exp
               |
    """

def p_push_pm(p):
    """
    push_pm : PLUS
            | MINUS
    """
    global stackOper
    stackOper.append(p[1])

def p_termino(p):
    """
    termino : factor checa_stack_td termino_aux1
    """

def p_checa_stack_td(p):
    """
    checa_stack_td :
    """
    global stackOper
    print stackOper
    if (stackOper):
        if (stackOper[-1] == '*' or stackOper[-1] == '/'):
            generateArithmeticCode()

def p_termino_aux1(p):
    """
    termino_aux1 : push_td termino
                 |
    """

def p_push_td(p):
    """
    push_td : TIMES
            | DIVIDE
    """
    global stackOper
    stackOper.append(p[1])

def p_factor(p):
    """
    factor : push_lparen expresion pop_rparen
    | cte
    """

def p_push_lparen(p):
    """
    push_lparen : LPAREN
    """
    global stackOper
    stackOper.append(p[1])

def p_pop_rparen(p):
    """
    pop_rparen : RPAREN
    """
    global stackOper
    stackOper.pop()

def p_cte(p):
    """
    cte : id_aux lista_aux
        | cte_e_aux
        | cte_f_aux
        | cte_b_aux
        | cte_s_aux
    """

def p_id_aux(p):
    """
    id_aux : ID
    """
    global stackTipos, stackOp, variables, variablesGlobales, stackOpVisible
    if (not variables.has_key(p[1])):
        if (not variablesGlobales.has_key(p[1])):
            raise SemanticError("No se ha declarado variable: " + p[1])
        else:
            stackOp.append(variablesGlobales[p[1]]["memoria"])
            stackOpVisible.append(p[1])
            stackTipos.append(variablesGlobales[p[1]]["tipo"])
    else:
        stackOp.append(variables[p[1]]["memoria"])
        stackOpVisible.append(p[1])
        stackTipos.append(variables[p[1]]["tipo"])

def p_cte_e_aux(p):
    """
    cte_e_aux : CTE_E
    """
    global avail, stackOp, stackTipos, constants, stackOpVisible
    if (not constants.has_key(p[1])):
        constants[p[1]] = {"tipo": 101, "memoria": avail[3][101]}
        avail[3][101] += 1
    stackOp.append(constants[p[1]]["memoria"])
    stackOpVisible.append(p[1])
    stackTipos.append(constants[p[1]]["tipo"])

def p_cte_f_aux(p):
    """
    cte_f_aux : CTE_F
    """
    global avail, stackOp, stackTipos, constants, stackOpVisible
    if (not constants.has_key(p[1])):
        constants[p[1]] = {"tipo": 102, "memoria": avail[3][102]}
        avail[3][102] += 1
    stackOp.append(constants[p[1]]["memoria"])
    stackOpVisible.append(p[1])
    stackTipos.append(constants[p[1]]["tipo"])


def p_cte_s_aux(p):
    """
    cte_s_aux : CTE_S
    """
    global avail, stackOp, stackTipos, constants, stackOpVisible
    if (not constants.has_key(p[1])):
        constants[p[1]] = {"tipo": 103, "memoria": avail[3][103]}
        avail[3][103] += 1
    stackOp.append(constants[p[1]]["memoria"])
    stackOpVisible.append(p[1])
    stackTipos.append(constants[p[1]]["tipo"])


def p_cte_b_aux(p):
    """
    cte_b_aux : CTE_B
    """
    global avail, stackOp, stackTipos, constants, stackOpVisible
    if (not constants.has_key(p[1])):
        constants[p[1]] = {"tipo": 104, "memoria": avail[3][104]}
        avail[3][104] += 1
    stackOp.append(constants[p[1]]["memoria"])
    stackOpVisible.append(p[1])
    stackTipos.append(constants[p[1]]["tipo"])


def p_lista_aux(p):
    """
    lista_aux : LBRACKET exp RBRACKET
              |
    """

def p_accion(p):
    """
    accion : accion_aux1 LPAREN exp RPAREN
    """

def p_accion_aux1(p):
    """
    accion_aux1 : ARRIBA
                | ABAJO
                | IZQUIERDA
                | DERECHA
                | COLOR
    """

def p_mientras(p):
    """
    mientras : MIENTRAS push_a_stackJumps LPAREN expresion RPAREN genera_gotoF_mientras bloque genera_fin_mientras
    """

def p_push_a_stackJumps(p):
    """push_a_stackJumps :
    """
    global stackJumps, cuadruplos
    stackJumps.append(len(cuadruplos) + 1)

def p_genera_gotoF_mientras(p):
    """
    genera_gotoF_mientras :
    """
    global stackOp, stackTipos, stackOpVisible, stackJumps, cuadruplos, stackOpVisible
    tipoActual = stackTipos.pop()
    if (tipoActual != Type2Code("booleano")):
        raise SemanticError("Se esperaba un booleano en la condicion. Se recibio: " + str(tipoActual))
    condicion = stackOp.pop()
    stackOpVisible.pop()
    cuadruplos.append([oper2Code("gotoF"), condicion, 'null', 'espera'])
    stackJumps.append(len(cuadruplos) - 1)

def p_genera_fin_mientras(p):
    """
    genera_fin_mientras :
    """
    global stackJumps, cuadruplos
    falseJump = stackJumps.pop()
    returnJump = stackJumps.pop()
    cuadruplos.append([oper2Code("goto"), 'null', 'null', returnJump])
    cuadruplos[falseJump][3] = len(cuadruplos) + 1

def p_return(p):
    '''return : RETURN expresion'''

def p_paratodos(p):
    """
    paratodos : PARATODOS LPAREN ID EN lista RPAREN bloque
    """

def p_error(p):
    if p:
        raise SyntaxError("Syntax error at '%s'" % p.value)
    if not p:
        print("EOF")


def generateArithmeticCode():
    global stackOper, stackTipos, stackOp, avail, cuadruplos
#    if (debug):
    print "stack operadores: ", stackOper
    print "stack operandos: ", stackOp
    print "stack tipos: ", stackTipos

    operador = oper2Code(stackOper.pop())
    op2 = stackOp.pop()
    op1 = stackOp.pop()
    stackOpVisible.pop()
    stackOpVisible.pop()
    op2Tipo = stackTipos.pop()
    op1Tipo = stackTipos.pop()
    nuevoTipo = cuboSemantico[op1Tipo-100][op2Tipo-100][operador]
    if (nuevoTipo == -1):
        raise SemanticError("Tipos incompatibles: " + str(op1Tipo) + str(operador) + str(op2tipo))
    resultado = avail[2][nuevoTipo]
    avail[2][nuevoTipo] += 1
    cuadruplos.append([operador, op1, op2, resultado])
    stackOp.append(resultado)
    stackOpVisible.append(resultado)
    stackTipos.append(nuevoTipo)


lexer = lex.lex()

parser = yacc.yacc()
while True:
    try:
        s = input('iziLang > ')
    except EOFError:
        break
    funciones = {"global": {}}
    avail = {0: {101: 2000, 102:3000, 103:4000, 104:5000}, 1: {101: 8000, 102:9000, 103:10000, 104:11000}, 2: {101: 14000, 102:15000, 103:16000, 104:17000}, 3: {101: 20000, 102:21000, 103:22000, 104:23000}}
    variables = {}
    constants = {}
    variablesGlobales = {}
    parametros = []
    cuadruplos = []
    stackTipos = []
    stackOper = []
    stackOp = []
    stackOpVisible = []
    stackJumps = []

    # Start the scanning and parsing
    with open(s) as fp:
        completeString = ""
        for line in fp:
            completeString += line
        try:
            parser.parse(completeString)
            print(funciones)
            print (cuadruplos)
            print("El programa se ejecuto con exito")
        except EOFError:
            break
