import sys, lexer

def error(msg):
    print(f'Error on line {lexer.line}: {msg}')

def lex():
    global input
    global nextToken
    (nextToken,input) = lexer.lex(input)
    if nextToken[0] == lexer.ERROR:
        print(nextToken[1])

def parseVal():
    if nextToken[0] == lexer.MINUS:
        lex()
        if nextToken[0] == lexer.ID:
            lex()
        else:
            error('Expected ID')
            return False 
    if nextToken[0] in [lexer.INT, lexer.ID]:
        lex()
        return True
    else:
        error('Expected Value')
        return False

def parseCmd():
    if nextToken[0] == lexer.KEYWORD:
        match nextToken[1]:
            case 'print':
                lex()
                return parseVal()
            case 'get':
                lex()
                if nextToken[0] != lexer.ID:
                    error('Expected ID')
                    return False
                else:
                    lex()
            case 'and':
                pass
            case 'do':
                pass
            case 'or':
                pass
            case 'if':
                pass
            case 'while':
                pass
            case 'for':
                pass
            case 'then':
                pass
            case 'else':
                pass
            case 'end':
                pass
            case 'not':
                pass
            case _:
                error('Expected Command')
                return False    
    else:
        error('Expected Command')
        return False
    return True

def parseProg():
    res = parseCmd()
    if res:
        if nextToken[0] != lexer.END_OF_INPUT:
            res = parseProg()
    return res        

# Driver
input = list(sys.stdin.read())
lex()

if parseProg():
    print('Program is correct.')
