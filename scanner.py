# + = 0
# * = 1
# - = 2
# / = 3
# && = 4
# || = 5
# < = 6
# > = 7
# != = 8
# == = 9
# = = 10

# int = 101
# float = 102
# palabra = 103
# booleano = 104
# list = 1000

import sys

sys.path.insert(0, "../..")

if sys.version_info[0] >= 3:
    raw_input = input

debug = True

avail = {}
pilaSaltos = []
pilaTipos = []
pilaOper = []
pilaOp = []
cuadruplos = []
dirFunciones = {}
variables = {}
constantes = {}
parametros = []
variablesGlobales = {}
tipoVariable = ""
funcionId = ""
contParams = 0
goSubFuncion = ""
temporalStamp = {}


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


cuboSemantico = [
    [[101, 102, -1, -1], [102, 102, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]],
    [[101, 102, -1, -1], [102, 102, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]],
    [[101, 102, -1, -1], [102, 102, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]],
    [[101, 102, -1, -1], [102, 102, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]],
    [[-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, 104]],
    [[-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, 104]],
    [[-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]],
    [[104, 104, -1, -1], [104, 104, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]],
    [[104, 104, -1, -1], [104, 104, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]],
    [[104, 104, -1, -1], [104, 104, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]],
    [[104, 104, -1, -1], [104, 104, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]],
    [[104, 104, -1, -1], [104, 104, -1, -1], [-1, -1, 104, -1], [-1, -1, -1, 104]],
    [[104, 104, -1, -1], [104, 104, -1, -1], [-1, -1, 104, -1], [-1, -1, -1, 104]]
]


def type2Code(tipo):
    if (tipo == "ENTERO"):
        return 101
    elif (tipo == "DECIMAL"):
        return 102
    elif (tipo == "PALABRA"):
        return 103
    elif (tipo == "BOOLEANO"):
        return 104

def code2Type(code):
    if (code == 101):
        return "ENTERO"
    elif (code == 102):
        return "DECIMAL"
    elif (code == 103):
        return "PALABRA"
    elif (code == 104):
        return "BOOLEANO"


def oper2Code(oper):
    if (oper == '+'):
        return 0
    elif (oper == '*'):
        return 1
    elif (oper == '-'):
        return 2
    elif (oper == '/'):
        return 3
    elif (oper == '&&'):
        return 4
    elif (oper == '||'):
        return 5
    elif (oper == '<'):
        return 6
    elif (oper == '>'):
        return 7
    elif (oper == '!='):
        return 8
    elif (oper == '=='):
        return 9
    elif (oper == '='):
        return 10
    elif (oper == 'goto'):
        return 11
    elif (oper == 'gotoF'):
        return 12
    elif (oper == 'print'):
        return 13
    elif (oper == 'ARRIBA'):
        return 14
    elif (oper == 'ABAJO'):
        return 15
    elif (oper == 'IZQUIERDA'):
        return 16
    elif (oper == 'DERECHA'):
        return 17
    elif (oper == 'endFunc'):
        return 18
    elif (oper == 'era'):
        return 19
    elif (oper == 'gosub'):
        return 20
    elif (oper == 'param'):
        return 21
    elif (oper == 'return'):
        return 22


tokens = (
    'PROGRAMA', 'FUNCION', 'ENTERO', 'DECIMAL', 'PALABRA', 'BOOLEANO', 'MAIN', 'IMPRIME', 'SI', 'SINO', 'MIENTRAS',
    'FIN', 'RETURN', 'COLON', 'SEMI', 'COMMA', 'LPAREN', 'RPAREN', 'AMPERSAND', 'LCURLY', 'RCURLY', 'EQUAL', 'PLUS',
    'MINUS', 'TIMES', 'DIVIDE', 'LT', 'GT', 'LE', 'GE', 'NE', 'EQUALC', 'AND', 'OR', 'LBRACKET', 'RBRACKET', 'DIRECCION', 'ID',
    'CTE_E', 'CTE_F', 'CTE_S', 'CTE_B'
)


# Define regular expressions of tokens

def t_PROGRAMA(t):
    'PROGRAMA'
    return t


def t_FUNCION(t):
    'FUNCION'
    return t


def t_ENTERO(t):
    'ENTERO'
    return t


def t_DECIMAL(t):
    'DECIMAL'
    return t


def t_PALABRA(t):
    'PALABRA'
    return t


def t_CHAR(t):
    'CHAR'
    return t


def t_BOOLEANO(t):
    'BOOLEANO'
    return t


def t_MAIN(t):
    'MAIN'
    return t


def t_IMPRIME(t):
    'IMPRIME'
    return t


def t_SI(t):
    'SI'
    return t


def t_SINO(t):
    'SINO'
    return t


def t_MIENTRAS(t):
    'MIENTRAS'
    return t


def t_FIN(t):
    'FIN'
    return t


def t_RETURN(t):
    'RETURN'
    return t


def t_COLON(t):
    ':'
    return t


def t_SEMI(t):
    ';'
    return t


def t_COMMA(t):
    ','
    return t


def t_LPAREN(t):
    '\('
    return t


def t_RPAREN(t):
    '\)'
    return t


def t_LCURLY(t):
    '\{'
    return t


def t_RCURLY(t):
    '\}'
    return t


def t_EQUALC(t):
    '=='
    return t


def t_EQUAL(t):
    '='
    return t


def t_PLUS(t):
    '\+'
    return t


def t_MINUS(t):
    '-'
    return t


def t_TIMES(t):
    '\*'
    return t


def t_DIVIDE(t):
    '/'
    return t


def t_LT(t):
    '<'
    return t


def t_GT(t):
    '>'
    return t


def t_LE(t):
    '<='
    return t


def t_GE(t):
    '>='
    return t


def t_NE(t):
    '!='
    return t


def t_AND(t):
    '&&'
    return t


def t_AMPERSAND(t):
    '&'
    return t


def t_OR(t):
    '\|\|'
    return t


def t_LBRACKET(t):
    '\['
    return t


def t_RBRACKET(t):
    '\]'
    return t

def t_DIRECCION(t):
    r'ARRIBA|ABAJO|IZQUIERDA|DERECHA'
    return t

def t_CTE_F(t):
    r'[0-9]+\.[0-9]+'
    return t


def t_CTE_E(t):
    r'[0-9]+'
    return t


def t_CTE_B(t):
    r'VERDADERO|FALSO'
    return t


def t_CTE_S(t):
    r'\"([a-zA-Z]|[0-9]|[ \*\[\]\\\^\-\.\?\+\|\(\)\$\/\{\}\%\<\>=&;,_:\[\]\'!$#@])*\"'
    return t


def t_ID(t):
    r'[a-zA-Z]([a-zA-Z]|[0-9])*(_([a-zA-z]|[0-9])+)*'
    return t


t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    raise LexerError("Caracter ilegal en '%s'" % t.value[0])


# Build the lexer
import ply.lex as lex

lex.lex()

start = 'programa'


def p_programa(p):
    """
	programa : PROGRAMA genera_goto_main ID COLON bloque FIN
	"""

    global dirFunciones, gameSections, constantes
    if (debug):
        dirFunciones["constantes"] = constantes


def p_genera_goto_main(p):
    """
	genera_goto_main :
	"""

    global cuadruplos, pilaSaltos
    cuadruplos.append([oper2Code('goto'), -1, -1, 'pending'])
    pilaSaltos.append(len(cuadruplos))


def p_bloque(p):
    """
	bloque : vars guarda_variables_global funciones bloque_main
	"""

    global variablesGlobales
    variablesGlobales = {}


# Helper function in sintaxis for semantic and compilation (virtual memory)
def p_guarda_variables_global(p):
    """
	guarda_variables_global :
	"""

    global dirFunciones, variablesGlobales, variables, avail
    # Assign virtual memory to variables in global scope
    for key in variables.keys():
        variables[key]["memoria"] = avail[0][variables[key]["tipo"]]
        avail[0][variables[key]["tipo"]] += 1

    # Save global variables with its attributes.
    variablesGlobales = variables
    variables = {}
    if (debug):
        dirFunciones["global"] = variablesGlobales


def p_vars(p):
    """
	vars : var SEMI vars
            |
	"""


def p_var(p):
    """
	var : tipo ID
        | tipo ID RBRACKET CTE_E RBRACKET
    """

    global variables, tipo, dirFunciones
    if (variables.has_key(p[2])):
        raise SemanticError("Ya existe la variable: " + p[2])
    if (dirFunciones.has_key("variables")):
        if (dirFunciones["variables"].has_value(p[2])):
            raise SemanticError("Ya existe una funcion con el mismo nombre: " + p[2])
    tipoEnNumero = type2Code(tipo)
    try:
        if (p[3] != '['):
            variables[p[2]] = {"tipo": tipoEnNumero + 1000}
    except IndexError:
        variables[p[2]] = {"tipo": tipoEnNumero}


def p_tipo(p):
    """
	tipo : ENTERO
         | DECIMAL
         | PALABRA
         | BOOLEANO
    """

    global tipo
    tipo = p[1]


def p_funciones(p):
    """
	funciones : funcion funciones
                 |
	"""


def p_guarda_funcion(p):
    """
	guarda_funcion : """

    global dirFunciones, variables, parametros, funcionId, tipo, avail, cuadruplos
    # Save the function with its variables
    if (dirFunciones.has_key(funcionId)):
        raise SemanticError("Repeated identifier for function: " + funcionId)
    if (debug):
        dirFunciones[funcionId] = {"variables": variables, "parametros": parametros,
                                   "return": type2Code(tipo),
                                   "memoria": avail[0][type2Code(tipo)],
                                   "start_cuadruplet": len(cuadruplos) + 1}
    avail[0][type2Code(tipo)] += 1
    variables = {}


def p_funcion(p):
    """
	funcion : FUNCION tipo guarda_funcion_id LPAREN parametros RPAREN guarda_funcion codigo_bloque generate_end_func"""


def p_generate_end_func(p):
    """
	generate_end_func : """

    global cuadruplos, temporalStamp, dirFunciones, funcionId, avail
    cuadruplos.append([oper2Code('endFunc'), -1, -1, -1])
    temporalAuxDictionary = {}
    print temporalStamp
    for key in avail[2]:
        temporalAuxDictionary[key] = avail[2][key] - temporalStamp[key]
    dirFunciones[funcionId]["temporales"] = temporalAuxDictionary


def p_guarda_funcion_id(p):
    """
	guarda_funcion_id : ID"""

    global funcionId, temporalStamp, avail
    funcionId = p[1]
    avail[1] = {101: 8000, 102: 9000, 103: 10000, 104: 11000}
    avail[2] = {101: 14000, 102: 15000, 103: 16000, 104: 17000}
    temporalStamp = avail[2].copy()


def p_parametros(p):
    """
	parametros : parametro mas_parametros
                  |
	"""


def p_parametro(p):
    """
	parametro : tipo tipo_parametro"""


def p_tipo_parametro(p):
    """
	tipo_parametro : AMPERSAND ID
                      | ID"""

    global variables, tipo, parametros, avail
    # Get parametro attributes and save it.
    if (p[1] == '&'):
        if (variables.has_key(p[2])):
            raise SemanticError("Repeated identifier for variable: " + p[2])
        variables[p[2]] = {"tipo": type2Code(tipo), "reference_parametro": True,
                           "memoria": avail[1][type2Code(tipo)]}
        parametros.append(type2Code(tipo))
    else:
        if (variables.has_key(p[1])):
            raise SemanticError("Repeated identifier for variable: " + p[1])
        variables[p[1]] = {"tipo": type2Code(tipo), "reference_parametro": False,
                           "memoria": avail[1][type2Code(tipo)]}
        parametros.append(type2Code(tipo))
    avail[1][type2Code(tipo)] += 1


def p_mas_parametros(p):
    """
	mas_parametros : COMMA parametro mas_parametros
                       |
	"""


def p_bloque_main(p):
    """
	bloque_main : MAIN LPAREN RPAREN set_main_id codigo_bloque
	"""

    global dirFunciones, variables, avail
    #if (dirFunciones.has_key(p[1])):
        #raise SemanticError("Repeated identifier for function: " + p[1])
    if (debug):
        dirFunciones["MAIN"]["variables"] = variables
    variables = {}


def p_set_main_id(p):
    """
	set_main_id : """

    global dirFunciones, funcionId, cuadruplos, pilaSaltos, avail
    funcionId = "MAIN"
    dirFunciones[funcionId] = {"variables": {}}
    firstJump = pilaSaltos.pop()
    cuadruplos[firstJump - 1][3] = len(cuadruplos) + 1
    avail[1] = {101: 8000, 102: 9000, 103: 10000, 104: 11000}
    avail[2] = {101: 14000, 102: 15000, 103: 16000, 104: 17000}


def p_codigo_bloque(p):
    """
	codigo_bloque : LCURLY vars guarda_variables_local mini_bloque RCURLY
	"""


# Helper function in sintaxis for semantic and compilation (virtual memory)
def p_guarda_variables_local(p):
    """
	guarda_variables_local :
	"""

    global variables, avail
    # TODO: - Virtual memory for a list

    # Assign virtual memory to variables in local scope
    for key in variables.keys():
        tipoEnNumero = variables[key]["tipo"]
        if tipoEnNumero < 1000:
            variables[key]["memoria"] = avail[1][tipoEnNumero]
            avail[1][tipoEnNumero] += 1


def p_estatuto(p):
    """
	estatuto : assignation checha_pila_equal
               | condicion
               | printing
               | mientras
               | function_use
               | return
               | accion
    """

def p_checha_pila_equal(p):
    """
	checha_pila_equal : """

    global pilaOper, pilaTipos, pilaOp, cuadruplos
    if (pilaOper):
        if (pilaOper[-1] == '='):
            # Different way to generate cuadruplet arithmetic != assignation
            operador = oper2Code(pilaOper.pop())
            op2 = pilaOp.pop()
            op1 = pilaOp.pop()
            op2Tipo = pilaTipos.pop()
            op1Tipo = pilaTipos.pop()
            if (op1Tipo != op2Tipo):
                raise SemanticError(
                    "Tipos incompatibles: " + str(op2Tipo) + " y " + str(op1Tipo))
            cuadruplos.append([operador, op2, -1, op1])


def p_function_use(p):
    """
	function_use : validate_function_id_do_era LPAREN add_parametro more_ids RPAREN validate_params_generate_gosub
                    | validate_function_id_do_era LPAREN RPAREN validate_params_generate_gosub
    """


def p_validate_function_id_do_era(p):
    """
	validate_function_id_do_era : ID"""

    global cuadruplos, dirFunciones, parametros, contParams, goSubFuncion
    if (not dirFunciones.has_key(p[1])):
        raise SemanticError("Use of undeclared function identifier: " + p[1])
    cuadruplos.append([oper2Code('era'), -1, -1, p[1]])
    parametros = dirFunciones[p[1]]["parametros"]
    contParams = 0
    goSubFuncion = p[1]


def p_add_parametro(p):
    """
	add_parametro : expression"""

    global pilaOp, pilaTipos, parametros, contParams, cuadruplos
    paramTipo = pilaTipos.pop()
    operand = pilaOp.pop()
    try:
        if (parametros[contParams] != paramTipo):
            raise SemanticError("Diferent tipo of parametro in function. Expected: " + parametros[
                contParams] + " received: " + paramTipo)
    except IndexError:
        raise SemanticError("Use of more parametros than function declaration.")
    contParams += 1
    cuadruplos.append([oper2Code('param'), operand, -1, contParams])


def p_validate_params_generate_gosub(p):
    """
	validate_params_generate_gosub : """

    global dirFunciones, cuadruplos, goSubFuncion, parametros, contParams, funcionId, avail, pilaOp, pilaTipos
    if (contParams != len(parametros)):
        raise SemanticError("Use of less parametros than expected in function declaration.")
    cuadruplos.append([oper2Code('gosub'), -1, -1, goSubFuncion])
    if (funcionId != 'MAIN'):
        cuadruplos.append([oper2Code('='), dirFunciones[funcionId]['memoria'], -1,
                           avail[2][dirFunciones[funcionId]['return']]])
        pilaOp.append(avail[2][dirFunciones[funcionId]['return']])
        pilaTipos.append(dirFunciones[funcionId]['return'])
        avail[2][dirFunciones[funcionId]['return']] += 1
    goSubFuncion = ""
    parametros = []
    contParams = 0


def p_more_ids(p):
    """
	more_ids : COMMA add_parametro more_ids
                |
	"""


def p_assignation(p):
    """
	assignation : id_aux value_list push_equal expression"""

def p_push_equal(p):
    """
	push_equal : EQUAL"""

    global pilaOper
    pilaOper.append(p[1])


def p_value_list(p):
    """
	value_list : LBRACKET expression RBRACKET
                  |
	"""


def p_printing(p):
    """
	printing : IMPRIME LPAREN printable RPAREN"""


def p_printable(p):
    """
	printable : expression more_printable"""


def p_more_printable(p):
    """
	more_printable : COMMA printable
                      |
	"""

    global pilaOp, pilaTipos, cuadruplos
    expression = pilaOp.pop()
    pilaTipos.pop()
    cuadruplos.append([oper2Code("print"), -1, -1, expression])


def p_condicion(p):
    """
	condicion : SI LPAREN expression RPAREN generate_gotoF_if COLON mini_bloque else_condicion generate_end_if
	"""


def p_generate_gotoF_if(p):
    """
	generate_gotoF_if : """

    global pilaOp, pilaTipos, pilaOper, pilaSaltos, cuadruplos
    condicionTipo = pilaTipos.pop()
    if (condicionTipo != type2Code("boolean")):
        raise SemanticError("Se esparaba un booleano en la condicion. Se recibio: " + str(condicionTipo))
    condicion = pilaOp.pop()
    cuadruplos.append([oper2Code("gotoF"), condicion, -1, 'pending'])
    pilaSaltos.append(len(cuadruplos) - 1) 


def p_generate_end_if(p):
    """
	generate_end_if : """

    global pilaSaltos, cuadruplos
    endJump = pilaSaltos.pop()
    cuadruplos[endJump][3] = len(cuadruplos) + 1  # Because it needs to point to the next one


def p_else_condicion(p):
    """
	else_condicion : SINO generate_goto_else COLON mini_bloque
                      |"""


def p_generate_goto_else(p):
    """
	generate_goto_else : """
    global pilaSaltos, cuadruplos
    cuadruplos.append([oper2Code("goto"), 'null', 'null', 'pending'])
    falseJump = pilaSaltos.pop()
    cuadruplos[falseJump][3] = len(cuadruplos) + 1
    pilaSaltos.append(len(cuadruplos) - 1)


def p_mientras(p):
    """
	mientras : MIENTRAS push_cont_in_pilaSaltos LPAREN expression RPAREN generate_gotoF_while COLON mini_bloque generate_end_while
	"""


def p_push_cont_in_pilaSaltos(p):
    """
	push_cont_in_pilaSaltos :
	"""

    global pilaSaltos, cuadruplos
    pilaSaltos.append(len(cuadruplos) + 1)


def p_generate_gotoF_while(p):
    """
	generate_gotoF_while :
	"""

    global pilaOp, pilaTipos, pilaSaltos, cuadruplos
    condicionTipo = pilaTipos.pop()
    if (condicionTipo != type2Code("boolean")):
        raise SemanticError("Expected boolean in if condicion. Received: " + str(condicionTipo))
    condicion = pilaOp.pop()
    cuadruplos.append([oper2Code("gotoF"), condicion, -1, 'pending'])
    pilaSaltos.append(len(cuadruplos) - 1)  # Make it as a list that starts in 0.


def p_generate_end_while(p):
    """
	generate_end_while :
	"""

    global pilaSaltos, cuadruplos
    falseJump = pilaSaltos.pop()
    returnJump = pilaSaltos.pop()
    cuadruplos.append([oper2Code("goto"), -1, -1, returnJump])
    cuadruplos[falseJump][3] = len(cuadruplos) + 1


def p_return(p):
    """
	return : RETURN expression"""

    global cuadruplos, dirFunciones, funcionId, pilaOp, pilaTipos
    if (funcionId == 'MAIN'):
        raise SemanticError("Trying to return something inside Main.")
    op = pilaOp.pop()
    opTipo = pilaTipos.pop()
    if (opTipo != dirFunciones[funcionId]['return']):
        raise SemanticError("Returning a value of tipo: " + opTipo + ", expected: " + dirFunciones[funcionId]['return'])
    cuadruplos.append([oper2Code('return'), -1, -1, op])

def p_accion(p):
    """
    accion : DIRECCION LPAREN expression RPAREN 
    
    """
    global pilaOp, pilaTipos, cuadruplos
    expression = pilaOp.pop()
    opTipo = pilaTipos.pop()
    if( opTipo != 101):
        raise SemanticError("Se esperaba un entero. Se recibio: " + code2Type(opTipo))
    else:
        cuadruplos.append([oper2Code(p[1]), -1, -1, expression])


def p_mini_bloque(p):
    """
	mini_bloque : estatuto SEMI mini_bloque
                  |
	"""


def p_expression(p):
    """
	expression : big_exp or_exp checha_pila_or
	"""

def p_checha_pila_or(p):
    """
	checha_pila_or :
	"""

    global pilaOper
    if (pilaOper):
        if (pilaOper[-1] == '||'):
            generateArithmeticCode()


def p_or_exp(p):
    """
	or_exp : OR expression
              |
	"""

    global pilaOper
    try:
        if (p[1] == '||'):
            pilaOper.append(p[1])
    except IndexError:
        return


def p_big_exp(p):
    """
	big_exp : medium_exp and_exp checha_pila_and
	"""

def p_checha_pila_and(p):
    """
	checha_pila_and :
	"""

    global pilaOper
    if (pilaOper):
        if (pilaOper[-1] == '&&'):
            generateArithmeticCode()


def p_and_exp(p):
    """
	and_exp : AND big_exp
               |
	"""

    global pilaOper
    try:
        if (p[1] == '&&'):
            pilaOper.append(p[1])
    except IndexError:
        return


def p_medium_exp(p):
    """
	medium_exp : exp relational_exp checha_pila_mmdi
	"""


def p_checha_pila_mmdi(p):
    """
	checha_pila_mmdi :
	"""

    global pilaOper
    if (pilaOper):
        if (pilaOper[-1] == '>' or pilaOper[-1] == '<' or pilaOper[-1] == '!=' or pilaOper[-1] == '=='):
            generateArithmeticCode()


def p_relational_exp(p):
    """
	relational_exp : GT exp
                   | LT exp
                   | GE exp
                   | LE exp
                   | NE exp
                   | EQUALC exp
                   |
	"""

    global pilaOper
    try:
        if (p[1] == '>' or p[1] == '<' or p[1] == '!=' or p[1] == '=='):
            pilaOper.append(p[1])
    except IndexError:
        return


def p_exp(p):
    """
	exp : term checha_pila_pm add_term
	"""


def p_checha_pila_pm(p):
    """
	checha_pila_pm :
	"""

    global pilaOper
    if (pilaOper):
        if (pilaOper[-1] == '+' or pilaOper[-1] == '-'):
            generateArithmeticCode()


def p_add_term(p):
    """
	add_term : push_pm exp
                |
	"""


def p_push_pm(p):
    """
	push_pm : PLUS
               | MINUS
    """

    global pilaOper
    pilaOper.append(p[1])


def p_term(p):
    """
	term : factor checha_pila_td times_factor
	"""


def p_checha_pila_td(p):
    """
	checha_pila_td :
	"""

    global pilaOper
    if (pilaOper):
        if (pilaOper[-1] == '*' or pilaOper[-1] == '/'):
            generateArithmeticCode()


def p_times_factor(p):
    """
	times_factor : push_td term
                    |
	"""


def p_push_td(p):
    """
	push_td : TIMES
               | DIVIDE"""

    global pilaOper
    pilaOper.append(p[1])


def p_factor(p):
    """
	factor : push_pa expression pop_pc
              | var_ct"""


def p_push_pa(p):
    """
	push_pa : LPAREN"""

    global pilaOper
    pilaOper.append(p[1])


def p_pop_pc(p):
    """
	pop_pc : RPAREN"""

    global pilaOper
    pilaOper.pop()


def p_var_ct(p):
    """
	var_ct : id_aux value_list
           | cte_e_aux
           | cte_f_aux
           | cte_b_aux
           | cte_s_aux
           | function_use
    """

    # TODO: - What happens when you receive a function


# Helper functions of var_ct for semantic analysis (operands)
# id checks if the id was declared, if not, there is an error.
def p_id_aux(p):
    """
	id_aux : ID
	"""

    global pilaTipos, pilaOp, variables, variablesGlobales, dirFunciones, funcionId
    # print variables, dirFunciones, p[1], funcionId
    if (not variables.has_key(p[1]) and not dirFunciones[funcionId]["variables"].has_key(p[1])):
        if (not variablesGlobales.has_key(p[1])):
            raise SemanticError("Use of undeclared identifier for variable: " + p[1])
        else:
            pilaOp.append(variablesGlobales[p[1]]["memoria"])
            pilaTipos.append(variablesGlobales[p[1]]["tipo"])
    else:
        if (variables.has_key(p[1])):
            pilaOp.append(variables[p[1]]["memoria"])
            pilaTipos.append(variables[p[1]]["tipo"])
        else:
            pilaOp.append(dirFunciones[funcionId]["variables"][p[1]]["memoria"])
            pilaTipos.append(dirFunciones[funcionId]["variables"][p[1]]["tipo"])


# the rest of the variables check if they exists in virtual memory, if not, add them.

def p_cte_e_aux(p):
    """
	cte_e_aux : CTE_E"""

    global constantes, avail, pilaOp, pilaTipos
    if (not constantes.has_key(p[1])):
        constantes[p[1]] = {"tipo": 101, "memoria": avail[3][101]}
        avail[3][101] += 1
    pilaOp.append(constantes[p[1]]["memoria"])
    pilaTipos.append(constantes[p[1]]["tipo"])


def p_cte_f_aux(p):
    """
	cte_f_aux : CTE_F"""

    global constantes, avail, pilaOp, pilaTipos
    if (not constantes.has_key(p[1])):
        constantes[p[1]] = {"tipo": 102, "memoria": avail[3][102]}
        avail[3][102] += 1
    pilaOp.append(constantes[p[1]]["memoria"])
    pilaTipos.append(constantes[p[1]]["tipo"])

def p_cte_s_aux(p):
    """
    cte_s_aux : CTE_S"""

    global constantes, avail, pilaOp, pilaTipos
    if (not constantes.has_key(p[1])):
        constantes[p[1]] = {"tipo": 103, "memoria": avail[3][103]}
        avail[3][103] += 1
    pilaOp.append(constantes[p[1]]["memoria"])
    pilaTipos.append(variables[p[1]]["tipo"])

def p_cte_b_aux(p):
    """
	cte_b_aux : CTE_B"""

    global constantes, avail, pilaOp, pilaTipos
    if (not constantes.has_key(p[1])):
        constantes[p[1]] = {"tipo": 104, "memoria": avail[3][104]}
        avail[3][104] += 1
    pilaOp.append(constantes[p[1]]["memoria"])
    pilaTipos.append(constantes[p[1]]["tipo"])

def p_error(p):
    if p:
        raise SyntaxError("Syntax error at '%s'" % p.value, )
    if not p:
        print("EOF")

def generateArithmeticCode():
    global pilaOper, pilaTipos, pilaOp, avail, cuadruplos
    if (debug):
        print "pila de operadores: ", pilaOper
        print "pila de operandos: ", pilaOp
        print "pila de tipos: ", pilaTipos

    #Creacion de cuadruplos
    operador = oper2Code(pilaOper.pop())
    op2 = pilaOp.pop()
    op1 = pilaOp.pop()
    op2Tipo = pilaTipos.pop()
    op1Tipo = pilaTipos.pop()
    newTipo = cuboSemantico[operador][op1Tipo - 101][op2Tipo - 101]
    if (newTipo == -1):
        raise SemanticError("Tipos incompatibles: " + str(op1Tipo) + str(operador) + str(op2Tipo))
    result = avail[2][newTipo]
    avail[2][newTipo] += 1
    # Generate the cuadruplet, append result to the stacks
    cuadruplos.append([operador, op1, op2, result])
    pilaOp.append(result)
    pilaTipos.append(newTipo)


# Import yacc
import ply.yacc as yacc

parser = yacc.yacc()

while True:
    try:
        s = raw_input('izilang > ')
    except EOFError:
        break
    dirFunciones = {"global": {}}
    avail = {0: {101: 2000, 102: 3000, 103: 4000, 104: 5000},
             1: {101: 8000, 102: 9000, 103: 10000, 104: 11000},
             2: {101: 14000, 102: 15000, 103: 16000, 104: 17000},
             3: {101: 20000, 102: 21000, 103: 22000, 104: 23000}}
    variables = {}
    constantes = {}
    parametros = []
    variablesGlobales = {}
    cuadruplos = []
    pilaTipos = []
    pilaOper = []
    pilaOp = []
    pilaSaltos = []

    with open(s) as fp:
        completeString = ""
        for line in fp:
            completeString += line
        try:
            parser.parse(completeString)
            if (debug):
                print "Funciones: ", dirFunciones
                print "Cuadruplos: ", cuadruplos
            print("El programa se ejecuto correctamente")
        except EOFError:
            break
