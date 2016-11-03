import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'ARRIBA','IZQUIERDA','DERECHA', 'BORRAR', 'MIENTRAS', 'REPETIR', 'DIBUJASI', 'DIBUJANO', 'COLOR', 'CUANDO', 'FIN', 'CIRCULO', 'CUADRADO', 'RECTANGULO', 'TRIANGULO', 'LINEA', 'ENTERO', 'PALABRA', 'EN', 'PARATODOS', 'VERDADERO', 'BOOLEANO', 'PROGRAMA', 'FUNCION', 'LISTA', 'FALSO', 'SINO', 'EQUALS', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER', 'LPAREN', 'RPAREN', 'LT', 'LE', 'GT', 'GE', 'NE', 'COMMA', 'SEMI', 'COLON', 'INTEGER', 'CTE_F', 'STRING', 'LCURLY', 'RCURLY', 'LBRACKET', 'RBRACKET', 'NEWLINE', 'CTE_E', 'ID', 'ERROR', 'AND', 'OR', 'CTE_S', 'FLOAT'
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
t_PALABRA = r'PALABRA'
t_FUNCION = r'FUNCION'
t_PARATODOS = r'PARATODOS'
t_PROGRAMA = r'PROGRAMA'
t_SINO = r'SINO'
t_VERDADERO = r'VERDADERO'
t_FALSO = r'FALSO'
t_BOOLEANO = r'BOOLEANO'
t_LISTA = r'LISTA'
t_EN= r'EN'

t_EQUALS = r'[=]'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_POWER = r'\^'
t_DIVIDE = r'\/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LT = r'[<]'
t_LE = r'[<=]'
t_GT = r'[>]'
t_GE = r'[>=]'
t_NE = r'[<>]'
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
    r'[A-Z][A-Z0-9]*'
    if t.value in tokens:
        t.type = t.value
    return t

def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    return t

def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)

t_CTE_S = r'\"[A-Za-z0-9_\(\)\{\}\[\]\<\>\! \t]*\"'

t_ignore = ' \t'

lex.lex(debug=0)

def p_programa(p):
    """
    programa : KW_PROGRAMA ID COLON programa_aux1 programa_aux2 bloque FIN
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
    tipo : entero
           | decimal
           | palabra
           | booleano
    """

def p_bloque(p):
    """
    bloque : LCURLY bloque_aux RCURLY
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
               | dibujo
               | mientras
               | paratodo
    """

def p_asignacion(p):
    """
    asignacion : ID aignacion_aux1 EQUALS expresion SEMI
    """

def p_asignacion_aux1(p):
    """
    asignacion_aux1 : LBRACKET exp RBRACKET
    """

def p_condicion(p):
    """
    condicion : KW_CUANDO LPAREN expresion RPAREN bloque condicion_aux1
    """

def p_condicion_aux1(p):
    """
    condicion_aux1 : KW_SINO bloque
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
    accion_aux1 : arriba
                  | abajo
                  | izquierda
                  | derecha
                  | color
    """

def p_mientras(p):
    """
    mientras : KW_MIENTRAS LPAREN expresion RPAREN bloque
    """

def p_paratodos(p):
    """
    paratodos: KW_PARATODOS LPAREN ID KW_EN lista RPAREN bloque
    """

lexer = lex.lex()

data = '''
MIENTRAS ( (3 + 4 ) * 10)
  + -20 *2
'''

lexer.input(data)

while True:
    tok = lexer.token()
    if not tok:
        break      # No more input
    print(tok)
