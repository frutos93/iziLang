#!/usr/bin/python
# -*- coding: utf-8 -*-
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

sys.path.insert(0, '../..')

if sys.version_info[0] >= 3:
    raw_input = input

memoriaCompilacion = {}
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
tipoVariable = ''
listaAux = ''
lista = ''
funcionId = ''
contParams = 0
goSub = ''
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
    [[101, 102, -1, -1], [102, 102, -1, -1], [-1, -1,  -1, -1], [-1, -1, -1,  -1]],   #   +
    [[101, 102, -1, -1], [102, 102, -1, -1], [-1, -1,  -1, -1], [-1, -1, -1,  -1]],   #   -
    [[101, 102, -1, -1], [102, 102, -1, -1], [-1, -1,  -1, -1], [-1, -1, -1,  -1]],   #   *
    [[101, 102, -1, -1], [102, 102, -1, -1], [-1, -1,  -1, -1], [-1, -1, -1,  -1]],   #   /
    [[-1,   -1, -1, -1], [-1,   -1, -1, -1], [-1, -1,  -1, -1], [-1, -1, -1, 104]],   #   &&
    [[-1,   -1, -1, -1], [-1,   -1, -1, -1], [-1, -1,  -1, -1], [-1, -1, -1, 104]],   #   ||
    [[104, 104, -1, -1], [104, 104, -1, -1], [-1, -1,  -1, -1], [-1, -1, -1,  -1]],   #   >=
    [[104, 104, -1, -1], [104, 104, -1, -1], [-1, -1,  -1, -1], [-1, -1, -1,  -1]],   #   <=
    [[104, 104, -1, -1], [104, 104, -1, -1], [-1, -1,  -1, -1], [-1, -1, -1,  -1]],   #   >
    [[104, 104, -1, -1], [104, 104, -1, -1], [-1, -1,  -1, -1], [-1, -1, -1,  -1]],   #   <
    [[104, 104, -1, -1], [104, 104, -1, -1], [-1, -1, 104, -1], [-1, -1, -1, 104]],   #   <>
    [[104, 104, -1, -1], [104, 104, -1, -1], [-1, -1, 104, -1], [-1, -1, -1, 104]],   #   ==
    [[ -1,  -1, -1, -1], [ -1,  -1, -1, -1], [-1, -1,  -1, -1], [-1, -1, -1,  -1]]    #   =
]


def type2Code(tipo):
    if tipo == 'ENTERO':
        return 101
    elif tipo == 'DECIMAL':
        return 102
    elif tipo == 'PALABRA':
        return 103
    elif tipo == 'BOOLEANO':
        return 104


def code2Type(code):
    if code == 101:
        return 'ENTERO'
    elif code == 102:
        return 'DECIMAL'
    elif code == 103:
        return 'PALABRA'
    elif code == 104:
        return 'BOOLEANO'


def oper2Code(oper):
    if oper == '+':
        return 0
    elif oper == '*':
        return 1
    elif oper == '-':
        return 2
    elif oper == '/':
        return 3
    elif oper == '&&':
        return 4
    elif oper == '||':
        return 5
    elif oper == '<':
        return 6
    elif oper == '>':
        return 7
    elif oper == '!=':
        return 8
    elif oper == '==':
        return 9
    elif oper == '<=':
        return 10
    elif oper == '>=':
        return 11
    elif oper == '=':
        return 12
    elif oper == 'goto':
        return 13
    elif oper == 'gotoF':
        return 14
    elif oper == 'IMPRIME':
        return 15
    elif oper == 'ARRIBA':
        return 16
    elif oper == 'ABAJO':
        return 17
    elif oper == 'IZQUIERDA':
        return 18
    elif oper == 'DERECHA':
        return 19
    elif oper == 'endFunc':
        return 20
    elif oper == 'era':
        return 21
    elif oper == 'gosub':
        return 22
    elif oper == 'param':
        return 23
    elif oper == 'return':
        return 24
    elif oper == 'lista':
        return 25

def code2Oper(code):
    if code == '+':
        return 0
    elif code == '*':
        return 1
    elif code == '-':
        return 2
    elif code == '/':
        return 3
    elif code == '&&':
        return 4
    elif code == '||':
        return 5
    elif code == '<':
        return 6
    elif code == '>':
        return 7
    elif code == '!=':
        return 8
    elif code == '==':
        return 9
    elif code == '<=':
        return 10
    elif code == '>=':
        return 11
    elif code == '=':
        return 12
    elif code == 'goto':
        return 13
    elif code == 'gotoF':
        return 14
    elif code == 'IMPRIME':
        return 15
    elif code == 'ARRIBA':
        return 16
    elif code == 'ABAJO':
        return 17
    elif code == 'IZQUIERDA':
        return 18
    elif code == 'DERECHA':
        return 19
    elif code == 'endFunc':
        return 20
    elif code == 'era':
        return 21
    elif code == 'gosub':
        return 22
    elif code == 'param':
        return 23
    elif code == 'return':
        return 24
    elif code == 'lista':
        return 25

tokens = (
    'PROGRAMA',
    'FUNCION',
    'ENTERO',
    'DECIMAL',
    'PALABRA',
    'BOOLEANO',
    'MAIN',
    'IMPRIME',
    'SI',
    'SINO',
    'MIENTRAS',
    'FIN',
    'RETURN',
    'COLON',
    'SEMI',
    'COMMA',
    'LPAREN',
    'RPAREN',
    'AMPERSAND',
    'LCURLY',
    'RCURLY',
    'EQUAL',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LT',
    'GT',
    'LE',
    'GE',
    'NE',
    'EQUALC',
    'AND',
    'OR',
    'LBRACKET',
    'RBRACKET',
    'DIRECCION',
    'ID',
    'CTE_E',
    'CTE_F',
    'CTE_S',
    'CTE_B',
    'CUADRADO',
    'RECTANGULO',
    'TRIANGULO',
    'CIRCULO'
    )


# def de tokens

def t_PROGRAMA(t):
    '''PROGRAMA'''

    return t


def t_FUNCION(t):
    '''FUNCION'''

    return t


def t_ENTERO(t):
    '''ENTERO'''

    return t


def t_DECIMAL(t):
    '''DECIMAL'''

    return t


def t_PALABRA(t):
    '''PALABRA'''

    return t


def t_CHAR(t):
    '''CHAR'''

    return t


def t_BOOLEANO(t):
    '''BOOLEANO'''

    return t


def t_MAIN(t):
    '''MAIN'''

    return t


def t_IMPRIME(t):
    '''IMPRIME'''

    return t


def t_SINO(t):
    '''SINO'''

    return t


def t_SI(t):
    '''SI'''

    return t


def t_MIENTRAS(t):
    '''MIENTRAS'''

    return t


def t_FIN(t):
    '''FIN'''

    return t


def t_RETURN(t):
    '''RETURN'''

    return t


def t_COLON(t):
    ''':'''

    return t


def t_SEMI(t):
    ''';'''

    return t


def t_COMMA(t):
    ''','''

    return t


def t_LPAREN(t):
    '''\('''

    return t


def t_RPAREN(t):
    '''\)'''

    return t


def t_LCURLY(t):
    '''\{'''

    return t


def t_RCURLY(t):
    '''\}'''

    return t


def t_EQUALC(t):
    '''=='''

    return t


def t_EQUAL(t):
    '''='''

    return t


def t_PLUS(t):
    '''\+'''

    return t


def t_MINUS(t):
    '''-'''

    return t


def t_TIMES(t):
    '''\*'''

    return t


def t_DIVIDE(t):
    '''/'''

    return t


def t_LT(t):
    '''<'''

    return t


def t_GT(t):
    '''>'''

    return t


def t_LE(t):
    '''<='''

    return t


def t_GE(t):
    '''>='''

    return t


def t_NE(t):
    '''<>'''

    return t


def t_AND(t):
    '''&&'''

    return t


def t_AMPERSAND(t):
    '''&'''

    return t


def t_OR(t):
    '''\|\|'''

    return t


def t_LBRACKET(t):
    '''\['''

    return t


def t_RBRACKET(t):
    '''\]'''

    return t


def t_DIRECCION(t):
    r'''ARRIBA|ABAJO|IZQUIERDA|DERECHA'''

    return t


def t_CUADRADO(t):
    r'''CUADRADO'''

    return t


def t_RECTANGULO(t):
    r'''RECTANGULO'''

    return t


def t_TRIANGULO(t):
    r'''TRIANGULO'''

    return t


def t_CIRCULO(t):
    r'''CIRCULO'''

    return t


def t_CTE_F(t):
    r'''[0-9]+\.[0-9]+'''

    return t


def t_CTE_E(t):
    r'''[0-9]+'''

    return t


def t_CTE_B(t):
    r'''VERDADERO|FALSO'''

    return t


def t_CTE_S(t):
    r'''\"([a-zA-Z]|[0-9]|[ \*\[\]\\\^\-\.\?\+\|\(\)\$\/\{\}\%\<\>=&;,_:\[\]\'!$#@])*\"'''

    return t


def t_ID(t):
    r'''[a-zA-Z]([a-zA-Z]|[0-9])*(_([a-zA-z]|[0-9])+)*'''

    return t


t_ignore = ' \t'


def t_newline(t):
    r'''\n+'''

    t.lexer.lineno += t.value.count('\n')


def t_error(t):
    raise LexerError("Caracter ilegal en '%s'" % t.value[0])


# Build the lexer

import ply.lex as lex

lex.lex()

start = 'programa'


def p_programa(p):
    """
    programa : PROGRAMA goto_main ID COLON bloque FIN
    """

    global dirFunciones, gameSections, constantes
    dirFunciones['constantes'] = constantes


def p_goto_main(p):
    """
    goto_main :
    """

    global cuadruplos, pilaSaltos
    cuadruplos.append([oper2Code('goto'), -1, -1, 'espera'])
    pilaSaltos.append(len(cuadruplos))


def p_bloque(p):
    """
    bloque : vars guarda_variables_global funciones bloque_main
    """

    global variablesGlobales
    variablesGlobales = {}


def p_guarda_variables_global(p):
    """
    guarda_variables_global :
    """

    global dirFunciones, variablesGlobales, variables, \
        memoriaCompilacion

    for key in variables.keys():
        variables[key]['memoria'] = \
            memoriaCompilacion[0][variables[key]['tipo']]
        memoriaCompilacion[0][variables[key]['tipo']] += 1

    variablesGlobales = variables
    variables = {}
    dirFunciones['global'] = variablesGlobales


def p_vars(p):
    """
    vars : var SEMI vars
         |
    """


def p_var(p):
    """
    var : tipo ID
        | tipo ID LBRACKET CTE_E RBRACKET
    """

    global variables, tipo, dirFunciones
    if (len(p) > 3):
        if (variables.has_key(p[2])):
            raise SemanticError("Ya existe la variable: " + p[2])
        if (dirFunciones.has_key("variables")):
            if (dirFunciones["variables"].has_value(p[2])):
                raise SemanticError("Ya existe una funcion con el mismo nombre: " + p[2])
        variables[p[2]] = {"tipo": type2Code(tipo), "tamano": {"inf": 0, "sup": int(p[4]), "K": 0}}
    else:
        if (variables.has_key(p[2])):
            raise SemanticError("Ya existe la variable: " + p[2])
        if (dirFunciones.has_key("variables")):
            if (dirFunciones["variables"].has_value(p[2])):
                raise SemanticError("Ya existe una funcion con el mismo nombre: " + p[2])
        tipoEnNumero = type2Code(tipo)
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
    guarda_funcion : 
    """

    global dirFunciones, variables, parametros, funcionId, tipo, \
        memoriaCompilacion, cuadruplos

    # Guarda variables de la funcion

    if funcionId in dirFunciones:
        raise SemanticError('Ya existe la funcion: ' + funcionId)
    dirFunciones[funcionId] = {
        'variables': variables,
        'parametros': parametros,
        'return': type2Code(tipo),
        'memoria': memoriaCompilacion[0][type2Code(tipo)],
        'cuadruploIndice': len(cuadruplos) + 1,
        }
    memoriaCompilacion[0][type2Code(tipo)] += 1
    variables = {}


def p_funcion(p):
    """
    funcion : FUNCION tipo guarda_funcion_id LPAREN parametros RPAREN guarda_funcion codigo_bloque fin_funcion
    """


def p_fin_funcion(p):
    """
    fin_funcion : 
    """

    global dirFunciones, funcionId, memoriaCompilacion, cuadruplos, \
        temporalStamp
    cuadruplos.append([oper2Code('endFunc'), -1, -1, -1])
    temporalAuxDictionary = {}
    for key in memoriaCompilacion[2]:
        temporalAuxDictionary[key] = memoriaCompilacion[2][key] \
            - temporalStamp[key]
    dirFunciones[funcionId]['temporales'] = temporalAuxDictionary


def p_guarda_funcion_id(p):
    """
    guarda_funcion_id : ID
    """

    global temporalStamp, memoriaCompilacion, funcionId
    funcionId = p[1]
    memoriaCompilacion[1] = {
        101: 8000,
        102: 9000,
        103: 10000,
        104: 11000,
        }
    memoriaCompilacion[2] = {
        101: 14000,
        102: 15000,
        103: 16000,
        104: 17000,
        }
    temporalStamp = memoriaCompilacion[2].copy()


def p_parametros(p):
    """
    parametros : parametro mas_parametros
               |
    """


def p_parametro(p):
    """
    parametro : tipo tipo_parametro
    """


def p_tipo_parametro(p):
    """
    tipo_parametro : AMPERSAND ID
                   | ID
    """

    global tipo, parametros, memoriaCompilacion, variables

    if p[1] == '&':
        if p[2] in variables:
            raise SemanticError('Ya existe la variable: '
                                + p[2])
        variables[p[2]] = {'tipo': type2Code(tipo),
                           'reference_parametro': True,
                           'memoria': memoriaCompilacion[1][type2Code(tipo)]}
        parametros.append(type2Code(tipo))
    else:
        if p[1] in variables:
            raise SemanticError('Ya existe la variable: '
                                + p[1])
        variables[p[1]] = {'tipo': type2Code(tipo),
                           'reference_parametro': False,
                           'memoria': memoriaCompilacion[1][type2Code(tipo)]}
        parametros.append(type2Code(tipo))
    memoriaCompilacion[1][type2Code(tipo)] += 1


def p_mas_parametros(p):
    """
    mas_parametros : COMMA parametro mas_parametros
                       |
    """


def p_bloque_main(p):
    """
    bloque_main : MAIN LPAREN RPAREN set_main_id codigo_bloque
    """

    global variables, memoriaCompilacion, dirFunciones

    # if (p[1] in dirFunciones):
        # raise SemanticError("Ya existe la funcion: " + p[1])

    dirFunciones['MAIN']['variables'] = variables
    variables = {}


def p_set_main_id(p):
    """
    set_main_id : 
    """

    global cuadruplos, pilaSaltos, memoriaCompilacion, dirFunciones, \
        funcionId
    funcionId = 'MAIN'
    dirFunciones[funcionId] = {'variables': {}}
    saltoM = pilaSaltos.pop()
    cuadruplos[saltoM - 1][3] = len(cuadruplos) + 1
    memoriaCompilacion[1] = {
        101: 8000,
        102: 9000,
        103: 10000,
        104: 11000,
        }
    memoriaCompilacion[2] = {
        101: 14000,
        102: 15000,
        103: 16000,
        104: 17000,
        }


def p_codigo_bloque(p):
    """
    codigo_bloque : LCURLY vars guarda_variables_local estatutos RCURLY
    """

def p_guarda_variables_local(p):
    """
    guarda_variables_local :
    """

    global variables, memoriaCompilacion
    for variable in variables.keys():
        tipo = variables[variable]['tipo']
        if(variables[variable].has_key('tamano')):
            variables[variable]['memoria'] = memoriaCompilacion[1][tipo]
            memoriaCompilacion[1][tipo] += variables[variable]['tamano']['sup']
        else:
            variables[variable]['memoria'] = memoriaCompilacion[1][tipo]
            memoriaCompilacion[1][tipo] += 1


def p_estatuto(p):
    """
    estatuto : assignation checa_pila_a
               | condicion
               | imprime
               | mientras
               | function_use
               | return
               | accion
               | dibujo
    """


def p_checa_pila_a(p):
    """
    checa_pila_a : 
    """

    global pilaOp, cuadruplos, pilaOper, pilaTipos
    if pilaOper:
        if pilaOper[-1] == '=':
            operador = oper2Code(pilaOper.pop())
            op2 = pilaOp.pop()
            op1 = pilaOp.pop()
            op2Tipo = pilaTipos.pop()
            op1Tipo = pilaTipos.pop()
            if op1Tipo != op2Tipo:
                raise SemanticError('Tipos incompatibles: '
                                    + code2Type(op2Tipo) + ' y '
                                    + code2Type(op1Tipo))
            cuadruplos.append([operador, op2, -1, op1])


def p_function_use(p):
    """
    function_use : validar_funcion LPAREN add_parametro more_ids RPAREN validar_parametros
                    | validar_funcion LPAREN RPAREN validar_parametros
    """


def p_validar_funcion(p):
    """
    validar_funcion : ID
    """

    global parametros, contParams, goSub, cuadruplos, \
        dirFunciones
    if not p[1] in dirFunciones:
        raise SemanticError('No existe la funcion: '
                            + p[1])
    cuadruplos.append([oper2Code('era'), -1, -1, p[1]])
    parametros = dirFunciones[p[1]]['parametros']
    contParams = 0
    goSub = p[1]


def p_add_parametro(p):
    """
    add_parametro : expresion
    """

    global parametros, contParams, cuadruplos, pilaOp, pilaTipos
    paramTipo = pilaTipos.pop()
    operand = pilaOp.pop()
    try:
        if parametros[contParams] != paramTipo:
            raise SemanticError('Se esperaba parametro de tipo: '
                                 + parametros[contParams]
                                + ' se recibio: ' + paramTipo)
    except IndexError:
        raise SemanticError('Mas parametros de lo esperado')
    contParams += 1
    cuadruplos.append([oper2Code('param'), operand, -1, contParams])


def p_validar_parametros(p):
    """
    validar_parametros : 
    """

    global contParams, memoriaCompilacion, pilaOp, pilaTipos, \
        dirFunciones, cuadruplos, goSub, parametros
    if contParams != len(parametros):
        raise SemanticError('Menos parametros de lo esperado')

    # Con goSub se permite asignar el resultado de una funcion a una varible

    cuadruplos.append([oper2Code('gosub'), -1, -1, goSub])
    cuadruplos.append([oper2Code('='),
                      dirFunciones[goSub]['memoria'], -1,
                      memoriaCompilacion[2][dirFunciones[goSub]['return'
                      ]]])
    pilaOp.append(memoriaCompilacion[2][dirFunciones[goSub]['return'
                  ]])
    pilaTipos.append(dirFunciones[goSub]['return'])
    memoriaCompilacion[2][dirFunciones[goSub]['return']] += 1

    goSub = ''
    parametros = []
    contParams = 0


def p_more_ids(p):
    """
    more_ids : COMMA add_parametro more_ids
             |
    """


def p_assignation(p):
    """
    assignation : id_aux value_list actualiza_pilaOper_a expresion
    """


def p_actualiza_pilaOper_a(p):
    """
    actualiza_pilaOper_a : EQUAL
    """

    global pilaOper
    pilaOper.append(p[1])


def p_value_list(p):
    """
    value_list : value_list_aux LBRACKET expresion RBRACKET
               |
    """

    if(len(p)> 2):
        if(p[2] == '['):
            op1 = pilaOp.pop()
            tipoActual = pilaTipos.pop()
            if(tipoActual != 101):
                raise SemanticError("Necesitas un entero para accesar la lista: ", tipoActual)
            cuadruplos.append([code2Type('lista'), op1,0, variables [lista]['tamano']['sup']])
            if(not(constantes.has_key(variables[lista]['memoria']))):
                constantes[variables[lista]['memoria']] = {'tipo': 101, 'memoria': memoriaCompilacion[3][101]}
                memoriaCompilacion[3][101] +=1
            cuadruplo = [0, op1, constantes[variables[lista]['memoria']], memoriaCompilacion[2][101]]
            cuadruplos.append(cuadruplo)
            pilaOp.append(-memoriaCompilacion[2][101])
            pilaTipos.append(variables[lista]['tipo'])
            memoriaCompilacion[2][101] += 1

def p_value_list_aux(p):
    """
    value_list_aux :
    """

    global listaAux, lista, pilaOp, pilaTipos
    if(variables[listaAux].has_key('tamano')):
        pilaOp.pop()
        pilaTipos.pop()
        lista = listaAux
    else:
        raise SemanticError("Esta variable no es una lista")


def p_imprime(p):
    """
    imprime : IMPRIME LPAREN imprimir RPAREN
    """


def p_imprimir(p):
    """
    imprimir : expresion imprimir_mas
    """


def p_imprimir_mas(p):
    """
    imprimir_mas : COMMA imprimir
                   |
    """

    global pilaTipos, cuadruplos, pilaOp
    expresion = pilaOp.pop()
    pilaTipos.pop()
    cuadruplos.append([oper2Code('IMPRIME'), -1, -1, expresion])


def p_condicion(p):
    """
    condicion : SI LPAREN expresion RPAREN gotoF_condicion LCURLY estatutos RCURLY else_condicion fin_condicion
    """


def p_gotoF_condicion(p):
    """
    gotoF_condicion : 
    """

    global pilaOper, pilaSaltos, cuadruplos, pilaOp, pilaTipos
    condicionTipo = pilaTipos.pop()
    if condicionTipo != type2Code('BOOLEANO'):
        raise SemanticError('Se esparaba un booleano en la condicion. Se recibio: '
                             + code2Type(condicionTipo))
    condicion = pilaOp.pop()
    cuadruplos.append([oper2Code('gotoF'), condicion, -1, 'espera'])
    pilaSaltos.append(len(cuadruplos) - 1)


def p_fin_condicion(p):
    """
    fin_condicion : 
    """

    global pilaSaltos, cuadruplos
    endJump = pilaSaltos.pop()
    cuadruplos[endJump][3] = len(cuadruplos) + 1  # Apuntar a la siguiente


def p_else_condicion(p):
    """
    else_condicion : SINO LCURLY goto_else estatutos RCURLY
                   |
    """


def p_goto_else(p):
    """
    goto_else : 
    """

    global pilaSaltos, cuadruplos
    cuadruplos.append([oper2Code('goto'), -1, -1, 'espera'])
    saltoF = pilaSaltos.pop()
    cuadruplos[saltoF][3] = len(cuadruplos) + 1
    pilaSaltos.append(len(cuadruplos) - 1)


def p_mientras(p):
    """
    mientras : MIENTRAS actualiza_pilaSaltos LPAREN expresion RPAREN gotoF_while LCURLY estatutos RCURLY fin_while
    """


def p_actualiza_pilaSaltos(p):
    """
    actualiza_pilaSaltos :
    """

    global pilaSaltos, cuadruplos
    pilaSaltos.append(len(cuadruplos) + 1)


def p_gotoF_while(p):
    """
    gotoF_while :
    """

    global pilaSaltos, cuadruplos, pilaOp, pilaTipos
    condicionTipo = pilaTipos.pop()
    if condicionTipo != type2Code('BOOLEANO'):
        raise SemanticError('Se esperaba booleano en la condicion. Se recibio: '
                             + code2Type(condicionTipo))
    condicion = pilaOp.pop()
    cuadruplos.append([oper2Code('gotoF'), condicion, -1, 'espera'])
    pilaSaltos.append(len(cuadruplos) - 1) 


def p_fin_while(p):
    """
    fin_while :
    """

    global pilaSaltos, cuadruplos
    saltoF = pilaSaltos.pop()
    saltoR = pilaSaltos.pop()
    cuadruplos.append([oper2Code('goto'), -1, -1, saltoR])
    cuadruplos[saltoF][3] = len(cuadruplos) + 1


def p_return(p):
    """
    return : RETURN expresion
    """

    global funcionId, pilaOp, pilaTipos, cuadruplos, dirFunciones
    if funcionId == 'MAIN':
        raise SemanticError('Main no debe tener return')
    op = pilaOp.pop()
    opTipo = pilaTipos.pop()
    if opTipo != dirFunciones[funcionId]['return']:
        raise SemanticError('Se esta retornando: ' + opTipo
                            + ', cuando se esperaba: '
                            + dirFunciones[funcionId]['return'])
    cuadruplos.append([oper2Code('return'), -1, -1, op])


def p_accion(p):
    """
    accion : DIRECCION LPAREN expresion RPAREN 

    """

    global pilaTipos, cuadruplos, pilaOp
    expresion = pilaOp.pop()
    opTipo = pilaTipos.pop()
    if opTipo != 101:
        raise SemanticError('Se esperaba un entero. Se recibio: '
                            + code2Type(opTipo))
    cuadruplos.append([oper2Code(p[1]), -1, -1, expresion])


def p_dibujo(p):
    """
    dibujo : CUADRADO LPAREN expresion RPAREN
           | RECTANGULO LPAREN expresion COMMA expresion RPAREN
           | TRIANGULO LPAREN expresion COMMA expresion COMMA expresion RPAREN
           | CIRCULO LPAREN expresion RPAREN
    """

    global pilaTipos, cuadruplos, pilaOp
    if p[1] == 'CUADRADO' or p[1] == 'CIRCULO':
        expresion = pilaOp.pop()
        opTipo = pilaTipos.pop()
        if opTipo != 101:
            raise SemanticError('Se esperaba un entero. Se recibio: '
                                + code2Type(opTipo))
        cuadruplos.append([oper2Code(p[1]), -1, -1, expresion])


def p_estatutos(p):
    """
    estatutos : estatuto SEMI estatutos
                |
    """


def p_expresion(p):
    """
    expresion : big_exp or_exp checa_pila_or
    """


def p_checa_pila_or(p):
    """
    checa_pila_or :
    """

    global pilaOper
    if pilaOper:
        if pilaOper[-1] == '||':
            creaCuadruplos()


def p_or_exp(p):
    """
    or_exp : OR expresion
           |
    """

    global pilaOper
    try:
        if p[1] == '||':
            pilaOper.append(p[1])
    except IndexError:
        return


def p_big_exp(p):
    """
    big_exp : medium_exp and_exp checa_pila_and
    """


def p_checa_pila_and(p):
    """
    checa_pila_and :
    """

    global pilaOper
    if pilaOper:
        if pilaOper[-1] == '&&':
            creaCuadruplos()


def p_and_exp(p):
    """
    and_exp : AND big_exp
               |
    """

    global pilaOper
    try:
        if p[1] == '&&':
            pilaOper.append(p[1])
    except IndexError:
        return


def p_medium_exp(p):
    """
    medium_exp : exp comp_exp checa_pila_comp
    """


def p_checa_pila_comp(p):
    """
    checa_pila_comp :
    """

    global pilaOper
    if pilaOper:
        if pilaOper[-1] == '>' or pilaOper[-1] == '<' or pilaOper[-1] \
            == '<>' or pilaOper[-1] == '==' or pilaOper[-1] == '>=' \
            or pilaOper[-1] == '<=':
            creaCuadruplos()


def p_comp_exp(p):
    """
    comp_exp : GT exp
             | LT exp
             | GE exp
             | LE exp
             | NE exp
             | EQUALC exp
             |
    """

    global pilaOper
    try:
        if p[1] == '>' or p[1] == '<' or p[1] == '!=' or p[1] == '==':
            pilaOper.append(p[1])
    except IndexError:
        return


def p_exp(p):
    """
    exp : termino checa_pila_mm termino_mm
    """


def p_checa_pila_mm(p):
    """
    checa_pila_mm :
    """

    global pilaOper
    if pilaOper:
        if pilaOper[-1] == '+' or pilaOper[-1] == '-':
            creaCuadruplos()


def p_termino_mm(p):
    """
    termino_mm : actualiza_pilaOper_mm exp
               |
    """


def p_actualiza_pilaOper_mm(p):
    """
    actualiza_pilaOper_mm : PLUS
                          | MINUS
    """

    global pilaOper
    pilaOper.append(p[1])


def p_termino(p):
    """
    termino : factor checa_pila_md factor_md
    """


def p_checa_pila_md(p):
    """
    checa_pila_md :
    """

    global pilaOper
    if pilaOper:
        if pilaOper[-1] == '*' or pilaOper[-1] == '/':
            creaCuadruplos()


def p_factor_md(p):
    """
    factor_md : actualiza_pilaOper_md termino
              |
    """


def p_actualiza_pilaOper_md(p):
    """
    actualiza_pilaOper_md : TIMES
                          | DIVIDE
    """

    global pilaOper
    pilaOper.append(p[1])


def p_factor(p):
    """
    factor : actualiza_pilaOper_lparen expresion actualiza_pilaOper_rparen
           | constante
    """


def p_actualiza_pilaOper_lparen(p):
    """
    actualiza_pilaOper_lparen : LPAREN
    """

    global pilaOper
    pilaOper.append(p[1])


def p_actualiza_pilaOper_rparen(p):
    """
    actualiza_pilaOper_rparen : RPAREN
    """

    global pilaOper
    pilaOper.pop()


def p_constante(p):
    """
    constante : id_aux value_list
           | cte_e_aux
           | cte_f_aux
           | cte_b_aux
           | cte_s_aux
           | function_use
    """


def p_id_aux(p):
    """
    id_aux : ID
    """

    global variablesGlobales, dirFunciones, funcionId, pilaTipos, \
        pilaOp, variables,  listaAux
    listaAux = p[1]
    if not p[1] in variables and not p[1] \
        in dirFunciones[funcionId]['variables']:
        if not p[1] in variablesGlobales:
            raise SemanticError('La variable no ha sido declarada: '
                                + p[1])
        else:
            pilaOp.append(variablesGlobales[p[1]]['memoria'])
            pilaTipos.append(variablesGlobales[p[1]]['tipo'])
    else:
        if p[1] in variables:
            pilaOp.append(variables[p[1]]['memoria'])
            pilaTipos.append(variables[p[1]]['tipo'])
        else:
            pilaOp.append(dirFunciones[funcionId]['variables'
                          ][p[1]]['memoria'])
            pilaTipos.append(dirFunciones[funcionId]['variables'
                             ][p[1]]['tipo'])


def p_cte_e_aux(p):
    """
    cte_e_aux : CTE_E
    """

    global pilaOp, pilaTipos, constantes, memoriaCompilacion
    if not p[1] in constantes:
        constantes[p[1]] = {'tipo': 101,
                            'memoria': memoriaCompilacion[3][101]}
        memoriaCompilacion[3][101] += 1
    pilaOp.append(constantes[p[1]]['memoria'])
    pilaTipos.append(constantes[p[1]]['tipo'])


def p_cte_f_aux(p):
    """
    cte_f_aux : CTE_F
    """

    global pilaOp, pilaTipos, constantes, memoriaCompilacion
    if not p[1] in constantes:
        constantes[p[1]] = {'tipo': 102,
                            'memoria': memoriaCompilacion[3][102]}
        memoriaCompilacion[3][102] += 1
    pilaOp.append(constantes[p[1]]['memoria'])
    pilaTipos.append(constantes[p[1]]['tipo'])


def p_cte_s_aux(p):
    """
    cte_s_aux : CTE_S
    """

    global pilaOp, pilaTipos, constantes, memoriaCompilacion
    if not p[1] in constantes:
        constantes[p[1]] = {'tipo': 103,
                            'memoria': memoriaCompilacion[3][103]}
        memoriaCompilacion[3][103] += 1
    pilaOp.append(constantes[p[1]]['memoria'])
    pilaTipos.append(variables[p[1]]['tipo'])


def p_cte_b_aux(p):
    """
    cte_b_aux : CTE_B
    """

    global pilaOp, pilaTipos, constantes, memoriaCompilacion
    if not p[1] in constantes:
        constantes[p[1]] = {'tipo': 104,
                            'memoria': memoriaCompilacion[3][104]}
        memoriaCompilacion[3][104] += 1
    pilaOp.append(constantes[p[1]]['memoria'])
    pilaTipos.append(constantes[p[1]]['tipo'])


def p_error(p):
    if p:
        raise SyntaxError("Error de sintaxis en '%s'" % p.value)
    if not p:
        print ('EOF')


def creaCuadruplos():
    global pilaOper, pilaTipos, pilaOp, memoriaCompilacion, cuadruplos
    operador = oper2Code(pilaOper.pop())
    op2 = pilaOp.pop()
    op1 = pilaOp.pop()
    op2Tipo = pilaTipos.pop()
    op1Tipo = pilaTipos.pop()
    cuboTipo = cuboSemantico[operador][op1Tipo - 101][op2Tipo - 101]
    if cuboTipo == -1:
        raise SemanticError('Tipos incompatibles: ' + code2Type(op1Tipo)
                            + code2Oper(operador) + code2Type(op2Tipo))
    resultado = memoriaCompilacion[2][cuboTipo]
    memoriaCompilacion[2][cuboTipo] += 1

    # creacion del cuadruplo

    cuadruplos.append([operador, op1, op2, resultado])
    pilaOp.append(resultado)
    pilaTipos.append(cuboTipo)


# Import yacc

import ply.yacc as yacc

parser = yacc.yacc()


def parse():
    global dirFunciones, memoriaCompilacion, variables, constantes, \
        parametros, variablesGlobales, cuadruplos, pilaTipos, pilaOper, \
        pilaOp, actualiza_pilaSaltos

    try:
        s = raw_input('izilang > ')
    except EOFError:
        return
    dirFunciones = {'global': {}}
    memoriaCompilacion = {
        0: {
            101: 2000,
            102: 3000,
            103: 4000,
            104: 5000,
            },
        1: {
            101: 8000,
            102: 9000,
            103: 10000,
            104: 11000,
            },
        2: {
            101: 14000,
            102: 15000,
            103: 16000,
            104: 17000,
            },
        3: {
            101: 20000,
            102: 21000,
            103: 22000,
            104: 23000,
            },
        }

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
        string = ''
        for line in fp:
            string += line
        try:
            parser.parse(string)
            print ('El programa se ejecuto correctamente')
        except EOFError:
            return
