from ply import *


keywords = {
    'arriba': 'KW_ARRIBA',
    'izquierda': 'KW_IZQUIERDA',
    'derecha': 'KW_DERECHA',
    'borrarPantalla': 'KW_BOORAR',
    'mientras': 'KW_MIENTRAS',
    'repetir': 'KW_REPETIR',
    'dibujaSi': 'KW_DIBUJASI',
    'dibujaNo': 'KW_DIBUJANO',
    'color': 'KW_COLOR',
    'cuando': 'KW_CUANDO',
    'fin': 'KW_FIN',
    'circulo': 'KW_CIRCULO',
    'cuadrado': 'KW_CUADRADO',
    'rectangulo': 'KW_RECTANGULO',
    'triangulo': 'KW_TRIANGULO',
    'linea': 'KW_LINEA',
    'entero': 'KW_ENTERO',
    'palabra': 'KW_PALABRA',
    'funcion': 'KW_FUNCION',
    'paraTodos': 'KW_PARATODOS',
    'programa': 'KW_PROGRAMA',
    'siNo': 'KW_SINO',
    'verdadero': 'KW_VERDADERO',
    'falso': 'KW_FALSO',
    'booleano': 'KW_BOOLEANO',
    'lista': 'KW_LISTA',
}

tokens = {
    'KW_ARRIBA','KW_IZQUIERDA','KW_DERECHA', 'KW_BORRAR', 'KW_MIENTRAS', 'KW_REPETIR',
    'KW_DIBUJASI', 'KW_DIBUJANO', 'KW_COLOR', 'KW_CUANDO', 'KW_FIN', 'KW_CIRCULO', 'KW_CUADRADO',
    'KW_RECTANGULO', 'KW_TRIANGULO', 'KW_LINEA', 'KW_ENTERO', 'KW_PALABRA',
    'EQUALS', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER',
    'LPAREN', 'RPAREN', 'LT', 'LE', 'GT', 'GE', 'NE',
    'COMMA', 'SEMI', 'INTEGER', 'FLOAT', 'STRING',
    'ID', 'NEWLINE'
}

t_ignore = ' \t'


def t_ID(t):
    r'[A-Z][A-Z0-9]*'
    if t.value in keywords:
        t.type = t.value
    return t

t_EQUALS = r'='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_POWER = r'\^'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LT = r'<'
t_LE = r'<='
t_GT = r'>'
t_GE = r'>='
t_NE = r'<>'
t_COMMA = r'\,'
t_SEMI = r';'
t_INTEGER = r'\d+'
t_FLOAT = r'((\d*\.\d+)(E[\+-]?\d+)?|([1-9]\d*E[\+-]?\d+))'
t_STRING = r'\".*?\"'


def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1
    return t


def t_error(t):
    print("Illegal character %s" % t.value[0])
    t.lexer.skip(1)

lex.lex(debug=0)
