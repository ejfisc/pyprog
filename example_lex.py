import sys

COMMA = 0
EQUAL = 1
LE = 2
LT = 3
ARROW = 4
MINUS = 5
INT = 6
KEYWORD = 7
ID = 8
END_OF_INPUT = 9
ERROR = 10

KEYWORDS = ["get", "print", "sum", "product", "modulo", "divide", "if", "while", "end"]

line = 1

def next_line():
    global line
    line = line + 1

def error(msg):
    return (ERROR, "Error on line " + str(line) + ": " + msg)

def lex_int(input, sign):
    i = 0
    lexeme = ""
    while i < len(input) and input[i].isdigit():
        lexeme = lexeme + input[i]
        i = i + 1
    return ((INT, sign*int(lexeme)), input[i:])

def lookup(lexeme):
    if lexeme in KEYWORDS:
        return (KEYWORD, lexeme)
    else:
        return (ID, lexeme)

def lex_keyword_or_id(input):
    i = 0
    lexeme = ""
    while i < len(input) and (input[i] == "_" or input[i].isalpha() or input[i].isdigit()):
        lexeme = lexeme + input[i]
        i = i + 1
    return (lookup(lexeme), input[i:])

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
    if i >= len(input):
        return ((END_OF_INPUT, None), [])
    if input[i] == ",":
        return ((COMMA,None), input[i+1:])
    elif input[i] == "=":
        return ((EQUAL,None), input[i+1:])
    elif input[i] == "<":
        i = i + 1
        if i < len(input) and input[i] == "=":
            return ((LE,None), input[i+1:])
        else:
            return ((LT,None), input[i:])
    elif input[i] == "-":
        i = i + 1
        if i < len(input) and input[i] == ">":
            return ((ARROW,None), input[i+1:])
        elif input[i].isdigit():
            return lex_int(input[i:], -1)
        else:
            return ((MINUS,None), input[i:])
    elif input[i] == "+":
        i = i + 1
        if i < len(input) and input[i].isdigit():
            return lex_int(input[i:], 1)
        else:
            return (error("Expected Integer after '+'"), input[i:])
    elif input[i].isdigit():
        return lex_int(input[i:], 1)
    elif input[i] == "_" or input[i].isalpha():
        return lex_keyword_or_id(input[i:])

# Driver Progam

input = list(sys.stdin.read())

tmp = lex(input)

while tmp[0][0] != ERROR and tmp[0][0] != END_OF_INPUT:
    print(tmp[0][1])
    tmp = lex(tmp[1])
print(tmp[0])
