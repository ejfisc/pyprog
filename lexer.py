import sys

# tokens
STRING = 0
ID = 1
INT = 2
KEYWORD = 3
ERROR = 4
END_OF_INPUT = 5
SEMICOLON = 6
EQUAL = 7
PLUS = 8
MINUS = 9
MULT = 10
DIV = 11
MOD = 12
GT = 13
GE = 14
LT = 15
LE = 16
SAME = 17
NOTEQUAL = 18
OPENPAR = 19
CLOSEPAR = 20

KEYWORDS = ['print', 'get', 'and', 'or', 'if', 'while', 'then', 'else', 'end', 'not']

line = 1

def next_line():
    global line
    line += 1

def error(msg):
    return (ERROR, 'Error on line {line}: {msg}')

def lookup(lexeme):
    if lexeme in KEYWORDS:
        return (KEYWORD, lexeme)
    else:
        return (ID, lexeme)

def lex(input):
    i = 0
    while i < len(input) and (input[i].isspace() or input[i] == "/"):
        i = i + 1
        if input[i-1] == "/":
          if i < len(input) and input[i] == "/":
              while i < len(input) and input[i] != "\n":
                  i = i + 1
          else:
              return (error("Unexpected Character '" + input[i] + "'"), input[i:])
        elif input[i-1] == "\n":
            next_line()
    