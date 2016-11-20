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
# booleano = 105
# list = 1000

import sys

sys.path.insert(0, "../..")

if sys.version_info[0] >= 3:
    raw_input = input

debug = True

avail = {}
stackJumps = []
stackTipos = []
stackOper = []
stackOp = []
stackOpVisible = []
cuadruplos = []
dirFunciones = {}
variables = {}
constantes = {}
parametros = []
globalVariables = {}
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


semanticCube = [
    [[101, 102, -1, -1], [102, 102, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]],
    [[101, 102, -1, -1], [102, 102, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]],
    [[101, 102, -1, -1], [102, 102, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]],
    [[101, 102, -1, -1], [102, 102, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]],
    [[-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, 105]],
    [[-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, 105]],
    [[-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]],
    [[105, 105, -1, -1], [105, 105, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]],
    [[105, 105, -1, -1], [105, 105, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]],
    [[105, 105, -1, -1], [105, 105, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]],
    [[105, 105, -1, -1], [105, 105, -1, -1], [-1, -1, -1, -1], [-1, -1, -1, -1]],
    [[105, 105, -1, -1], [105, 105, -1, -1], [-1, -1, 105, -1], [-1, -1, -1, 105]],
    [[105, 105, -1, -1], [105, 105, -1, -1], [-1, -1, 105, -1], [-1, -1, -1, 105]]
]


def convertAtomicTypeToCode(tipo):
    if (tipo == "ENTERO"):
        return 101
    elif (tipo == "DECIMAL"):
        return 102
    elif (tipo == "PALABRA"):
        return 103
    elif (tipo == "BOOLEANO"):
        return 105


def convertOperatorToCode(oper):
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
    'MINUS', 'TIMES', 'DIVIDE', 'LT', 'GT', 'LE', 'GE', 'NE', 'EQUALC', 'AND', 'OR', 'LBRACKET', 'RBRACKET', 'ID',
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


def t_CTE_F(t):
    r'[0-9]+\.[0-9]+'
    return t


def t_CTE_E(t):
    r'[0-9]+'
    return t


def t_CT_B(t):
    r'true|false'
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
	programa : PROGRAMA generate_initial_goto ID COLON bloque FIN
	"""

    global dirFunciones, gameSections, constantes
    if (debug):
        dirFunciones["constantes"] = constantes


def p_generate_initial_goto(p):
    """
	generate_initial_goto :
	"""

    global cuadruplos, stackJumps
    cuadruplos.append([convertOperatorToCode('goto'), -1, -1, 'pending'])
    stackJumps.append(len(cuadruplos))


def p_bloque(p):
    """
	bloque : vars save_vars_in_global_memory funciones bloque_main
	"""

    global globalVariables
    globalVariables = {}


# Helper function in sintaxis for semantic and compilation (virtual memory)
def p_save_vars_in_global_memory(p):
    """
	save_vars_in_global_memory :
	"""

    global dirFunciones, globalVariables, variables, avail
    # Assign virtual memory to variables in global scope
    for key in variables.keys():
        variables[key]["memory"] = avail[0][variables[key]["tipo"]]
        avail[0][variables[key]["tipo"]] += 1

    # Save global variables with its attributes.
    globalVariables = variables
    variables = {}
    if (debug):
        dirFunciones["global"] = globalVariables


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
        raise SemanticError("Repeated identifier for variable: " + p[2])
    if (dirFunciones.has_key("variables")):
        if (dirFunciones["variables"].has_value(p[2])):
            raise SemanticError("Var identifier has the same name as a function: " + p[2])
    tipoInNumber = convertAtomicTypeToCode(tipo)
    try:
        if (p[3] != '['):
            variables[p[2]] = {"tipo": tipoInNumber + 1000}
    except IndexError:
        variables[p[2]] = {"tipo": tipoInNumber}


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
                                   "return": convertAtomicTypeToCode(tipo),
                                   "memory": avail[0][convertAtomicTypeToCode(tipo)],
                                   "start_cuadruplet": len(cuadruplos) + 1}
    avail[0][convertAtomicTypeToCode(tipo)] += 1
    variables = {}


def p_funcion(p):
    """
	funcion : FUNCION tipo guarda_funcion_id LPAREN parametros RPAREN guarda_funcion codigo_bloque generate_end_func"""


def p_generate_end_func(p):
    """
	generate_end_func : """

    global cuadruplos, temporalStamp, dirFunciones, funcionId, avail
    cuadruplos.append([convertOperatorToCode('endFunc'), -1, -1, -1])
    temporalAuxDictionary = {}
    print temporalStamp
    for key in avail[2]:
        temporalAuxDictionary[key] = avail[2][key] - temporalStamp[key]
    dirFunciones[funcionId]["temporals"] = temporalAuxDictionary


def p_guarda_funcion_id(p):
    """
	guarda_funcion_id : ID"""

    global funcionId, temporalStamp, avail
    funcionId = p[1]
    avail[1] = {101: 8000, 102: 9000, 103: 10000, 104: 11000, 105: 12000, 106: 13000}
    avail[2] = {101: 14000, 102: 15000, 103: 16000, 104: 17000, 105: 18000, 106: 19000}
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
        variables[p[2]] = {"tipo": convertAtomicTypeToCode(tipo), "reference_parametro": True,
                           "memory": avail[1][convertAtomicTypeToCode(tipo)]}
        parametros.append(convertAtomicTypeToCode(tipo))
    else:
        if (variables.has_key(p[1])):
            raise SemanticError("Repeated identifier for variable: " + p[1])
        variables[p[1]] = {"tipo": convertAtomicTypeToCode(tipo), "reference_parametro": False,
                           "memory": avail[1][convertAtomicTypeToCode(tipo)]}
        parametros.append(convertAtomicTypeToCode(tipo))
    avail[1][convertAtomicTypeToCode(tipo)] += 1


def p_mas_parametros(p):
    """
	mas_parametros : COMMA parametro mas_parametros
                       |
	"""


def p_bloque_main(p):
    """
	bloque_main : MAIN LPAREN RPAREN set_function_id_main codigo_bloque
	"""

    global dirFunciones, variables, avail
    if (dirFunciones.has_key(p[1])):
        raise SemanticError("Repeated identifier for function: " + p[1])
    if (debug):
        dirFunciones["main"]["variables"] = variables
    variables = {}


def p_set_function_id_main(p):
    """
	set_function_id_main : """

    global dirFunciones, funcionId, cuadruplos, stackJumps, avail
    funcionId = "main"
    dirFunciones[funcionId] = {"variables": {}}
    firstJump = stackJumps.pop()
    cuadruplos[firstJump - 1][3] = len(cuadruplos) + 1
    avail[1] = {101: 8000, 102: 9000, 103: 10000, 104: 11000, 105: 12000, 106: 13000}
    avail[2] = {101: 14000, 102: 15000, 103: 16000, 104: 17000, 105: 18000, 106: 19000}


def p_codigo_bloque(p):
    """
	codigo_bloque : LCURLY vars save_vars_in_local_memory mini_bloque RCURLY
	"""


# Helper function in sintaxis for semantic and compilation (virtual memory)
def p_save_vars_in_local_memory(p):
    """
	save_vars_in_local_memory :
	"""

    global variables, avail
    # TODO: - Virtual memory for a list

    # Assign virtual memory to variables in local scope
    for key in variables.keys():
        tipoInNumber = variables[key]["tipo"]
        if tipoInNumber < 1000:
            variables[key]["memory"] = avail[1][tipoInNumber]
            avail[1][tipoInNumber] += 1


def p_statute(p):
    """
	statute : assignation check_stack_equal
               | condition
               | printing
               | mientras
               | function_use
               | return
    """


# Helper function in sintaxis for semantic (operators)
def p_check_stack_equal(p):
    """
	check_stack_equal : """

    global stackOper, stackTipos, stackOp, cuadruplos
    if (stackOper):
        if (stackOper[-1] == '='):
            # Different way to generate cuadruplet arithmetic != assignation
            operator = convertOperatorToCode(stackOper.pop())
            op2 = stackOp.pop()
            op1 = stackOp.pop()
            op2Tipo = stackTipos.pop()
            op1Tipo = stackTipos.pop()
            if (op1Tipo != op2Tipo):
                raise SemanticError(
                    "Tipo Mismatch: Trying to assign " + str(op2Tipo) + " to a " + str(op1Tipo) + " var!")
            cuadruplos.append([operator, op2, -1, op1])


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
    cuadruplos.append([convertOperatorToCode('era'), -1, -1, p[1]])
    parametros = dirFunciones[p[1]]["parametros"]
    contParams = 0
    goSubFuncion = p[1]


def p_add_parametro(p):
    """
	add_parametro : expression"""

    global stackOp, stackTipos, parametros, contParams, cuadruplos
    paramTipo = stackTipos.pop()
    operand = stackOp.pop()
    try:
        if (parametros[contParams] != paramTipo):
            raise SemanticError("Diferent tipo of parametro in function. Expected: " + parametros[
                contParams] + " received: " + paramTipo)
    except IndexError:
        raise SemanticError("Use of more parametros than function declaration.")
    contParams += 1
    cuadruplos.append([convertOperatorToCode('param'), operand, -1, contParams])


def p_validate_params_generate_gosub(p):
    """
	validate_params_generate_gosub : """

    global dirFunciones, cuadruplos, goSubFuncion, parametros, contParams, funcionId, avail, stackOp, stackTipos
    if (contParams != len(parametros)):
        raise SemanticError("Use of less parametros than expected in function declaration.")
    cuadruplos.append([convertOperatorToCode('gosub'), -1, -1, goSubFuncion])
    if (funcionId != 'main'):
        cuadruplos.append([convertOperatorToCode('='), dirFunciones[funcionId]['memory'], -1,
                           avail[2][dirFunciones[funcionId]['return']]])
        stackOp.append(avail[2][dirFunciones[funcionId]['return']])
        stackTipos.append(dirFunciones[funcionId]['return'])
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


# Helper function in sintaxis for semantic (operators)
def p_push_equal(p):
    """
	push_equal : EQUAL"""

    global stackOper
    stackOper.append(p[1])


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

    global stackOp, stackTipos, stackOpVisible, cuadruplos
    expression = stackOp.pop()
    stackTipos.pop()
    stackOpVisible.pop()
    cuadruplos.append([convertOperatorToCode("print"), -1, -1, expression])


def p_condition(p):
    """
	condition : SI LPAREN expression RPAREN generate_gotoF_if COLON mini_bloque else_condition generate_end_if
	"""


def p_generate_gotoF_if(p):
    """
	generate_gotoF_if : """

    global stackOp, stackTipos, stackOper, stackOpVisible, stackJumps, cuadruplos
    condtionTipo = stackTipos.pop()
    if (condtionTipo != convertAtomicTypeToCode("boolean")):
        raise SemanticError("Expected boolean in if condition. Received: " + str(condtionType))
    condition = stackOp.pop()
    stackOpVisible.pop()
    cuadruplos.append([convertOperatorToCode("gotoF"), condition, -1, 'pending'])
    stackJumps.append(len(cuadruplos) - 1)  # Make it as a list that starts in 0.


def p_generate_end_if(p):
    """
	generate_end_if : """

    global stackJumps, cuadruplos
    endJump = stackJumps.pop()
    cuadruplos[endJump][3] = len(cuadruplos) + 1  # Because it needs to point to the next one


def p_else_condition(p):
    """
	else_condition : SINO generate_goto_else COLON mini_bloque
                      |"""


def p_generate_goto_else(p):
    """
	generate_goto_else : """
    global stackJumps, cuadruplos
    cuadruplos.append([convertOperatorToCode("goto"), 'null', 'null', 'pending'])
    falseJump = stackJumps.pop()
    cuadruplos[falseJump][3] = len(cuadruplos) + 1
    stackJumps.append(len(cuadruplos) - 1)


def p_mientras(p):
    """
	mientras : MIENTRAS push_cont_in_stackJumps LPAREN expression RPAREN generate_gotoF_while COLON mini_bloque generate_end_while
	"""


def p_push_cont_in_stackJumps(p):
    """
	push_cont_in_stackJumps :
	"""

    global stackJumps, cuadruplos
    stackJumps.append(len(cuadruplos) + 1)


def p_generate_gotoF_while(p):
    """
	generate_gotoF_while :
	"""

    global stackOp, stackTipos, stackOpVisible, stackJumps, cuadruplos
    condtionTipo = stackTipos.pop()
    if (condtionTipo != convertAtomicTypeToCode("boolean")):
        raise SemanticError("Expected boolean in if condition. Received: " + str(condtionTipo))
    condition = stackOp.pop()
    stackOpVisible.pop()
    cuadruplos.append([convertOperatorToCode("gotoF"), condition, -1, 'pending'])
    stackJumps.append(len(cuadruplos) - 1)  # Make it as a list that starts in 0.


def p_generate_end_while(p):
    """
	generate_end_while :
	"""

    global stackJumps, cuadruplos
    falseJump = stackJumps.pop()
    returnJump = stackJumps.pop()
    cuadruplos.append([convertOperatorToCode("goto"), -1, -1, returnJump])
    cuadruplos[falseJump][3] = len(cuadruplos) + 1


def p_return(p):
    """
	return : RETURN expression"""

    global cuadruplos, dirFunciones, funcionId, stackOp, stackTipos
    if (funcionId == 'main'):
        raise SemanticError("Trying to return something inside Main.")
    op = stackOp.pop()
    opTipo = stackTipos.pop()
    if (opTipo != dirFunciones[funcionId]['return']):
        raise SemanticError("Returning a value of tipo: " + opTipo + ", expected: " + dirFunciones[funcionId]['return'])
    cuadruplos.append([convertOperatorToCode('return'), -1, -1, op])


def p_mini_bloque(p):
    """
	mini_bloque : statute SEMI mini_bloque
                  |
	"""


def p_expression(p):
    """
	expression : big_exp or_exp check_stack_or
	"""


# Helper function in sintaxis for semantic (operators)
def p_check_stack_or(p):
    """
	check_stack_or :
	"""

    global stackOper
    if (stackOper):
        if (stackOper[-1] == '||'):
            generateArithmeticCode()


def p_or_exp(p):
    """
	or_exp : OR expression
              |
	"""

    global stackOper
    try:
        # Add operator to the stack
        if (p[1] == '||'):
            stackOper.append(p[1])
    except IndexError:
        return


def p_big_exp(p):
    """
	big_exp : medium_exp and_exp check_stack_and
	"""


# Helper function in sintaxis for semantic (operators)
def p_check_stack_and(p):
    """
	check_stack_and :
	"""

    global stackOper
    if (stackOper):
        if (stackOper[-1] == '&&'):
            generateArithmeticCode()


def p_and_exp(p):
    """
	and_exp : AND big_exp
               |
	"""

    global stackOper
    try:
        # Add operator to the stack
        if (p[1] == '&&'):
            stackOper.append(p[1])
    except IndexError:
        return


def p_medium_exp(p):
    """
	medium_exp : exp relational_exp check_stack_mmdi
	"""


# Helper function in sintaxis for semantic (operators)
def p_check_stack_mmdi(p):
    """
	check_stack_mmdi :
	"""

    global stackOper
    if (stackOper):
        if (stackOper[-1] == '>' or stackOper[-1] == '<' or stackOper[-1] == '!=' or stackOper[-1] == '=='):
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

    global stackOper
    try:
        # Add operator to the stack
        if (p[1] == '>' or p[1] == '<' or p[1] == '!=' or p[1] == '=='):
            stackOper.append(p[1])
    except IndexError:
        return


def p_exp(p):
    """
	exp : term check_stack_pm add_term
	"""


# Helper function in sintaxis for semantic (operators)
def p_check_stack_pm(p):
    """
	check_stack_pm :
	"""

    global stackOper
    if (stackOper):
        if (stackOper[-1] == '+' or stackOper[-1] == '-'):
            generateArithmeticCode()


def p_add_term(p):
    """
	add_term : push_pm exp
                |
	"""


# Helper function in sintaxis for semantic (operators)
def p_push_pm(p):
    """
	push_pm : PLUS
               | MINUS
    """

    global stackOper
    stackOper.append(p[1])


def p_term(p):
    """
	term : factor check_stack_td times_factor
	"""


# Helper function in sintaxis for semantic (operators)
def p_check_stack_td(p):
    """
	check_stack_td :
	"""

    global stackOper
    if (stackOper):
        if (stackOper[-1] == '*' or stackOper[-1] == '/'):
            generateArithmeticCode()


def p_times_factor(p):
    """
	times_factor : push_td term
                    |
	"""


# Helper function in sintaxis for semantic (operators)
def p_push_td(p):
    """
	push_td : TIMES
               | DIVIDE"""

    global stackOper
    stackOper.append(p[1])


def p_factor(p):
    """
	factor : push_pa expression pop_pc
              | var_ct"""


# Helper function in sintaxis for semantic (operators)
def p_push_pa(p):
    """
	push_pa : LPAREN"""

    global stackOper
    stackOper.append(p[1])


# Helper function in sintaxis for semantic (operators)
def p_pop_pc(p):
    """
	pop_pc : RPAREN"""

    global stackOper
    stackOper.pop()


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

    global stackTipos, stackOp, variables, globalVariables, stackOpVisible, dirFunciones, funcionId
    # print variables, dirFunciones, p[1], funcionId
    if (not variables.has_key(p[1]) and not dirFunciones[funcionId]["variables"].has_key(p[1])):
        if (not globalVariables.has_key(p[1])):
            raise SemanticError("Use of undeclared identifier for variable: " + p[1])
        else:
            stackOp.append(globalVariables[p[1]]["memory"])
            stackOpVisible.append(p[1])
            stackTipos.append(globalVariables[p[1]]["tipo"])
    else:
        if (variables.has_key(p[1])):
            stackOp.append(variables[p[1]]["memory"])
            stackOpVisible.append(p[1])
            stackTipos.append(variables[p[1]]["tipo"])
        else:
            stackOp.append(dirFunciones[funcionId]["variables"][p[1]]["memory"])
            stackOpVisible.append(p[1])
            stackTipos.append(dirFunciones[funcionId]["variables"][p[1]]["tipo"])


# the rest of the variables check if they exists in virtual memory, if not, add them.

def p_cte_e_aux(p):
    """
	cte_e_aux : CTE_E"""

    global constantes, avail, stackOp, stackTipos, stackOpVisible
    if (not constantes.has_key(p[1])):
        constantes[p[1]] = {"tipo": 101, "memory": avail[3][101]}
        avail[3][101] += 1
    stackOp.append(constantes[p[1]]["memory"])
    stackOpVisible.append(p[1])
    stackTipos.append(constantes[p[1]]["tipo"])


def p_cte_f_aux(p):
    """
	cte_f_aux : CTE_F"""

    global constantes, avail, stackOp, stackTipos, stackOpVisible
    if (not constantes.has_key(p[1])):
        constantes[p[1]] = {"tipo": 102, "memory": avail[3][102]}
        avail[3][102] += 1
    stackOp.append(constantes[p[1]]["memory"])
    stackOpVisible.append(p[1])
    stackTipos.append(constantes[p[1]]["tipo"])


def p_cte_b_aux(p):
    """
	cte_b_aux : CTE_B"""

    global constantes, avail, stackOp, stackTipos, stackOpVisible
    if (not constantes.has_key(p[1])):
        constantes[p[1]] = {"tipo": 105, "memory": avail[3][105]}
        avail[3][105] += 1
    stackOp.append(constantes[p[1]]["memory"])
    stackOpVisible.append(p[1])
    stackTipos.append(constantes[p[1]]["tipo"])


def p_cte_s_aux(p):
    """
	cte_s_aux : CTE_S"""

    global constantes, avail, stackOp, stackTipos, stackOpVisible
    if (not constantes.has_key(p[1])):
        constantes[p[1]] = {"tipo": 103, "memory": avail[3][103]}
        avail[3][103] += 1
    stackOp.append(constantes[p[1]]["memory"])
    stackOpVisible.append(p[1])
    stackTipos.append(variables[p[1]]["tipo"])


def p_error(p):
    if p:
        raise SyntaxError("Syntax error at '%s'" % p.value, )
    if not p:
        print("EOF")


# Helper function used to generate the code used for arithmetic, logic and relational operations
def generateArithmeticCode():
    global stackOper, stackTipos, stackOp, avail, cuadruplos, stackOpVisible
    if (debug):
        print "stack of operators: ", stackOper
        print "stack of operands: ", stackOpVisible
        print "stack of operands: ", stackOp
        print "stack of tipos: ", stackTipos

    # Get all the variables to test and generate a cuadruplet
    operator = convertOperatorToCode(stackOper.pop())
    op2 = stackOp.pop()
    op1 = stackOp.pop()
    stackOpVisible.pop()
    stackOpVisible.pop()
    op2Tipo = stackTipos.pop()
    op1Tipo = stackTipos.pop()
    newTipo = semanticCube[operator][op1Tipo - 101][op2Tipo - 101]
    # If the semantic cube tell us that the operation is not possible
    if (newTipo == -1):
        raise SemanticError("Tipo Mismatch: Trying to " + str(operator) + " = " + str(op1Tipo) + " :: " + str(op2Tipo))
    result = avail[2][newTipo]
    avail[2][newTipo] += 1
    # Generate the cuadruplet, append result to the stacks
    cuadruplos.append([operator, op1, op2, result])
    stackOp.append(result)
    stackOpVisible.append(result)
    stackTipos.append(newTipo)


# Import yacc
import ply.yacc as yacc

parser = yacc.yacc()

while True:
    try:
        s = raw_input('izilang > ')
    except EOFError:
        break
    dirFunciones = {"global": {}}
    avail = {0: {101: 2000, 102: 3000, 103: 4000, 104: 5000, 105: 6000, 106: 7000},
             1: {101: 8000, 102: 9000, 103: 10000, 104: 11000, 105: 12000, 106: 13000},
             2: {101: 14000, 102: 15000, 103: 16000, 104: 17000, 105: 18000, 106: 19000},
             3: {101: 20000, 102: 21000, 103: 22000, 104: 23000, 105: 24000, 106: 25000}}
    variables = {}
    constantes = {}
    parametros = []
    globalVariables = {}
    cuadruplos = []
    stackTipos = []
    stackOper = []
    stackOp = []
    stackOpVisible = []
    stackJumps = []

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
