import ply.lex as lex
import ply.yacc as yacc

class LexerError(Exception):
    def __init__(self, value):
       self.value = value

    def __str__(self):
        return repr(self.value)


class SemanticError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

tokens = (
    'ARRIBA', 'ABAJO', 'IZQUIERDA','DERECHA', 'DECIMAL', 'BORRAR', 'MIENTRAS', 'REPETIR', 'DIBUJASI', 'DIBUJANO', 'COLOR', 'CUANDO', 'FIN', 'CIRCULO', 'CUADRADO', 'RECTANGULO', 'TRIANGULO', 'LINEA', 'ENTERO', 'PALABRA', 'EN', 'PARATODOS', 'VERDADERO', 'BOOLEANO', 'PROGRAMA', 'FUNCION', 'MAIN', 'LISTA', 'FALSO', 'SINO', 'EQUALS', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER', 'LPAREN', 'RPAREN', 'EQUALSC' , 'LT', 'LE', 'GT', 'GE', 'NE', 'COMMA', 'SEMI', 'COLON', 'INTEGER', 'CTE_F', 'STRING', 'LCURLY', 'RCURLY', 'LBRACKET', 'RBRACKET', 'CTE_E', 'ID', 'ERROR', 'AND', 'OR', 'CTE_S', 'FLOAT'
)

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
t_VERDADERO = r'VERDADERO'
t_FALSO = r'FALSO'
t_BOOLEANO = r'BOOLEANO'
t_LISTA = r'LISTA'
t_EN= r'EN'

t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_POWER = r'\^'
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
    programa : PROGRAMA ID COLON programa_aux1 programa_aux2 main FIN
    """


def p_programa_aux1(p):
    """
    programa_aux1 : variables
                    |
    """


def p_programa_aux2(p):
    """
    programa_aux2 : funciones
                    |
    """


def p_variables(p):
    """
    variables : tipo variables_aux1 SEMI variables_aux2
    """


def p_variables_aux1(p):
    """
    variables_aux1 : ID variables_aux3 variables_aux4
    """


def p_variables_aux2(p):
    """
    variables_aux2 : variables
                     |
    """


def p_variables_aux3(p):
    """variables_aux3 : lista
                        |
    """


def p_variables_aux4(p):
    """variables_aux4 : COMMA variables_aux1
                        |
    """

def p_main(p):
    """
    main : MAIN tipo LPAREN RPAREN bloque
    """


def p_funciones(p):
    """
    funciones : FUNCION tipo ID LPAREN funciones_aux1 RPAREN bloque funciones_aux2
    """


def p_funciones_aux1(p):
    """
    funciones_aux1 : tipo ID funciones_aux3
    """


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


def p_bloque(p):
    """
    bloque : LCURLY bloque_aux1 RCURLY
    """


def p_bloque_aux1(p):
    """
    bloque_aux1 : bloque_aux2
                  |
    """


def p_bloque_aux2(p):
    """
    bloque_aux2 : estatuto bloque_aux2
                  |
    """


def p_estatuto(p):
    """
    estatuto : asignacion
               | condicion
               | accion
               | mientras
               | paratodos
    """


def p_asignacion(p):
    """
    asignacion : ID asignacion_aux1 EQUALS expresion SEMI
    """


def p_asignacion_aux1(p):
    """
    asignacion_aux1 : LBRACKET exp RBRACKET
    """


def p_condicion(p):
    """
    condicion : CUANDO LPAREN expresion RPAREN bloque condicion_aux1
    """


def p_condicion_aux1(p):
    """
    condicion_aux1 : SINO bloque
    |
    """


def p_expresion(p):
    """
    expresion : exp expresion_aux1
    """


def p_expresion_aux1(p):
    """
    expresion_aux1 : expresion_aux2 exp
    """


def p_expresion_aux2(p):
    """
    expresion_aux2 : AND
                     | OR
    """


def p_exp(p):
    """
    exp : termino exp_aux1
    """


def p_exp_aux1(p):
    """
    exp_aux1 : exp_aux2 termino
    """


def p_exp_aux2(p):
    """
    exp_aux2 : PLUS
               | MINUS
    """


def p_termino(p):
    """
    termino : factor termino_aux1
    """


def p_termino_aux1(p):
    """
    termino_aux1 : termino_aux2 factor
    """


def p_termino_aux2(p):
    """
    termino_aux2 : TIMES
                   | DIVIDE
    """


def p_factor(p):
    """
    factor : LPAREN expresion RPAREN
    | cte
    """


def p_cte(p):
    """
    cte : ID cte_aux1
          | CTE_E
          | CTE_F
    """


def p_cte_aux1(p):
    """
    cte_aux1 : LBRACKET exp RBRACKET
               | LPAREN exp RPAREN
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
    mientras : MIENTRAS LPAREN expresion RPAREN bloque
    """


def p_paratodos(p):
    """
    paratodos : PARATODOS LPAREN ID EN lista RPAREN bloque
    """

def p_error(p):
    if p:
        raise SyntaxError("Syntax error at) '%s'" % p.value)
    if not p:
        print("EOF")


lexer = lex.lex()

parser = yacc.yacc()
while True:
    try:
        s = raw_input('iziLang > ')
    except EOFError:
        break
    # Start the scanning and parsing
    with open(s) as fp:
        completeString = ""
        for line in fp:
            completeString += line
        try:
            parser.parse(completeString)
            print("Correct program")
        except EOFError:
            break
