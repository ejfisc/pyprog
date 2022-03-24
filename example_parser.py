import sys
import lexer

def error(msg):
    print("Error on line " + str(lexer.line) + ": " + msg)

def lex():
    global input
    global nextToken
    (nextToken,input)=lexer.lex(input)
    if nextToken[0] == lexer.ERROR:
        print(nextToken[1])

def parseVal():
    if nextToken[0] == lexer.MINUS:
        lex()
        if nextToken[0] == lexer.ID:
            lex()
        else:
            error("Expected ID")
            return False
    elif nextToken[0] in [lexer.INT, lexer.ID]:
        lex()
    else:
        error("Expected Value")
        return False
    return True

def parseCompare():
    if nextToken[0] in [lexer.EQUAL, lexer.LE, lexer.LT]:
        lex()
    else:
        error("Expected comparison operator")
        return False
    return True

def parseValList():
    res = parseVal()
    if res:
        if nextToken[0] == lexer.COMMA:
            lex()
            res = parseValList()
    return res

def sum_product_helper():
    lex()
    res = parseValList()
    if not res:
        return False
    if nextToken[0] == lexer.ARROW:
        lex()
    else:
        error("Expected '->' after value list")
        return False
    if nextToken[0] == lexer.ID:
        lex()
    else:
        error("Expected ID after '->'")
        return False
    return True

def modulo_divide_helper():
    lex()
    res = parseVal()
    if res:
        res = parseVal()
        if res:
            if nextToken[0] == lexer.ARROW:
                lex()
            else:
                error("Expected '->' after second value")
                return False
            if nextToken[0] == lexer.ID:
                lex()
            else:
                error("Expected ID after '->'")
                return False
    return res

def if_while_helper():
    lex()
    res = parseCompare()
    if res:
        res = parseVal()
        if res:
            res = parseProg()
            if res:
                if nextToken[0] == lexer.KEYWORD and nextToken[1] == "end":
                    lex()
                else:
                    error("Expected 'end'")
                    return False
    return res

def parseCmd():
    if nextToken[0] == lexer.KEYWORD:
        if nextToken[1] == "get":
            lex()
            if nextToken[0] != lexer.ID:
                error("Expected ID")
                return False
            else:
                lex()
        elif nextToken[1] == "print":
            lex()
            return parseVal()
        elif nextToken[1] == "sum":
            return sum_product_helper()
        elif nextToken[1] == "product":
            return sum_product_helper()
        elif nextToken[1] == "modulo":
            return modulo_divide_helper()
        elif nextToken[1] == "divide":
            return modulo_divide_helper()
        elif nextToken[1] == "if":
            return if_while_helper()
        elif nextToken[1] == "while":
            return if_while_helper()
        else:
            error("Expected Command")
            return False
    else:
        error("Expected Command")
        return False
    return True

def parseProg():
    res = parseCmd()
    if res:
        if nextToken[0] != lexer.END_OF_INPUT and not (nextToken[0] == lexer.KEYWORD and nextToken[1] == "end"):
            res = parseProg()
    return res

# Driver
input = list(sys.stdin.read())
lex()

if parseProg():
    print("Program is Correct")
