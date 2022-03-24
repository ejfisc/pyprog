#! python3
import sys

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
TIMES = 10
DIVIDE = 11
MODULO = 12
GT = 13
GE = 14
LT = 15
LE = 16
SAME = 17
NOT_EQUAL = 18
OPEN_PAR = 19
CLOSE_PAR = 20

KEYWORDS = ['print', 'get', 'and', 'or', 'if', 'while', 'then', 'else', 'end', 'not']

line = 1

def next_line():
    global line
    line += 1

def error(msg):
    return (ERROR, 'Error on line {line}: {msg}') # return error

def lookup(lexeme):
    if lexeme in KEYWORDS:
        return (KEYWORD, lexeme) # lexeme is a keyword
    else:
        return (ID, lexeme) # lexeme is an ID

def lex_int(input, sign):
    lexeme = ''
    i = 0
    while i < len(input) and input[i].isdigit():
        lexeme += input[i]
        i += 1
    return ((INT, sign*int(lexeme)), input[i:])

def lex_string(input):
    i = 0
    lexeme = ''
    while i < len(input):
        if input[i] == '\\':
            i += 1
            if input[i] == 't':
                lexeme += '\t'
            elif input[i] == 'n':
                lexeme += '\n'
            elif input[i] == '"':
                lexeme += '"'
            else:
                lexeme += '\\'
        elif input[i] == '"':
            break
        else:
            lexeme += input[i]
        i += 1
    return ((STRING, lexeme), input[i+1:])

def lex_keyword_or_id(input):
    lexeme = ''
    i = 0
    while i < len(input) and (input[i] == '_' or input[i].isalpha() or input[i].isdigit()):
        lexeme += input[i]
        i += 1
    return (lookup(lexeme), input[i:])

def lex(input):
    i = 0
    while i < len(input) and (input[i].isspace() or input[i] == '#'):
        i += 1
        if input[i-1] == '#':
            while i < len(input) and input[i] != '\n':
                i += 1
        elif input[i-1] == '\n':
            next_line()
    
    if i >= len(input):
        return ((END_OF_INPUT, None), [])

    match input[i]:
        case ';':
            return ((SEMICOLON, None), input[i+1:])
        case '%':
            return ((MODULO, None), input[i+1:])
        case '/':
            return ((DIVIDE, None), input[i+1:])
        case '*':
            return ((TIMES, None), input[i+1:])
        case '(':
            return ((OPEN_PAR, None), input[i+1:])
        case ')':
            return ((CLOSE_PAR, None), input[i+1:])
        case '=':
            i += 1
            if i < len(input) and input[i] == '=':
                return ((SAME, None), input[i+1:])
            else:
                return ((EQUAL, None), input[i:])
        case '>':
            i += 1
            if i < len(input) and input[i] == '=':
                return ((GE, None), input[i+1:])
            else:
                return ((GT, None), input[i:])
        case '<':
            i += 1
            if i < len(input) and input[i] == '=':
                return ((LE, None), input[i+1:])
            else:
                return ((LT, None), input[i:])
        case '!':
            i += 1
            if i < len(input) and input[i] == '=':
                return ((NOT_EQUAL, None), input[i+1:])
            else:
                return (error('Unexpected "!"'), input)
        case '-':
            i += 1
            if i < len(input) and input[i].isdigit():
                return lex_int(input[i:], -1)
            else:
                return ((MINUS, None), input[i:])
        case '+':
            i += 1
            if i < len(input) and input[i].isdigit():
                return lex_int(input[i:], 1)
            else:
                return ((PLUS, None), input[i:])
        case '"':
            return lex_string(input[i+1:])
        case _:
            if input[i].isdigit():
                return lex_int(input[i:], 1)
            elif input[i] == '_' or input[i].isalpha():
                return lex_keyword_or_id(input[i:])

# driver program

input = list(sys.stdin.read())

tmp = lex(input)

while tmp[0][0] != ERROR and tmp[0][0] != END_OF_INPUT:
    print(tmp[0])
    tmp = lex(tmp[1])

print(tmp[0])