import sys, lexer

def error(msg):
    print(f'Error on line {lexer.line}: {msg}')

def lex():
    global input
    global nextToken
    (nextToken,input) = lexer.lex(input)
    if nextToken[0] == lexer.ERROR:
        print(nextToken[1])

# <v_expr> -> 𝜀
#             ">" <value>
#             ">=" <value>
#             "<" <value>
#             "<=" <value>
#             "==" <value>
#             "!=" <value>
def parseVExpr():
    lex()
    if nextToken[0] in [lexer.GT, lexer.GE, lexer.LT, lexer.LE, lexer.SAME, lexer.NOT_EQUAL]:
        res = parseVal()
        if res:
            lex()
            return True
        else:
            return False
    # 𝜀 empty substitution, return true without advancing the program
    else:
        return True

# <factor> -> <value> <v_expr>
def parseFactor():
    res = parseVal()
    if res:
        res = parseVExpr()
        if res:
            lex()
            return True
        else:
            return False
    else:
        return False

# <f_expr> -> 𝜀
#             "*" <term>
#             "/" <term>
#             "%" <term>
def parseFExpr():
    lex()
    # "*" <term>, "/" <term>, "%" <term>
    if nextToken[0] in [lexer.TIMES, lexer.DIVIDE, lexer.MODULO]:
        res = parseTerm()
        if res:
            lex()
            return True
        else:
            return False
    # 𝜀 empty substitution, return true without advancing the program
    else:
        return True

# <term> -> <factor> <f_expr>
def parseTerm():
    res = parseFactor()
    if res:
        res = parseFExpr()
        if res:
            lex()
            return True
        else:
            return False
    else:
        return False

# <t_expr> -> 𝜀
#             "+" <n_expr>
#             "-" <n_expr>
def parseTExpr():
    lex()
    # "+" <n_expr>, "-" <n_expr>
    if nextToken[0] in [lexer.PLUS, lexer.MINUS]:
        res = parseNExpr()
        if res:
            lex()
            return True
        else:
            return False
    # 𝜀 empty substitution, return true without advancing the program
    else:
        return True

# <n_expr> -> <term> <t_expr>
def parseNExpr():
    lex()
    res = parseTerm()
    if res:
        res = parseTExpr()
        if res:
            lex()
            return True
        else:
            return False
    else:
        return False

# <b_expr> -> 𝜀
#             "and" <n_expr>
#             "or" <n_expr>
def parseBExpr():
    lex()
    # "and" <n_expr>, "or" <n_expr>
    if nextToken[0] == lexer.KEYWORD and nextToken[1] in ['and', 'or']:
        res = parseNExpr()
        if res:
            lex()
            return True
        else:
            return False
    # 𝜀 empty substitution, return true without advancing the program
    else:
        return True

# <expr> -> <n_expr> <b_expr>
def parseExpression():
    res = parseNExpr()
    if res:
        res = parseBExpr()
        if res:
            lex()
            return True
        else:
            error('Invalid B Expression')
            return False
    else:
        error('Invalid N Expression')
        return False

# <value> -> "(" <expr> ")"
#            "not" <value>
#            "-" <value>
#            ID
#            INT
def parseVal():
    lex()
    # "(" <expr> ")"
    if nextToken[0] == lexer.OPEN_PAR:
        res = parseExpression()
        if res:
            lex()
            if nextToken[0] == lexer.CLOSE_PAR:
                lex()
                return True
            else:
                error('Expected close parentheses')
                return False
        else:
            return False
    # "not" <value>
    elif nextToken[0] == lexer.KEYWORD and nextToken[1] == 'not':
        return parseVal()
    # "-" <value>
    elif nextToken[0] == lexer.MINUS:
        return parseVal()
    # ID or INT
    elif nextToken[0] in [lexer.INT, lexer.ID]:
        lex()
        return True
    else:
        error('Expected Value')
        return False

# <print> -> "print" <p-arg>
# <p-arg> -> STRING
#            <expr>
def parsePrint():
    lex()
    # "print" STRING
    if nextToken[0] == lexer.STRING:
        lex()
        if nextToken[0] == lexer.SEMICOLON:
            lex()
            return True
        else:
            error('Expected a semicolon')
            return False
    # "print" <expr>
    else:
        res = parseExpression()
        if res:
            lex()
            if nextToken[0] == lexer.SEMICOLON:
                lex()
                return True
            else:
                error('Expected a semicolon')
                return False
        else:
            return False

# <input> -> "get" ID
def parseInput():
    lex()
    if nextToken[0] != lexer.ID:
        error('Expected ID')
        return False
    else:
        lex()
        if nextToken[0] == lexer.SEMICOLON:
            lex()
            return True
        else:
            error('Expected a semicolon')
            return False

# <assign> -> ID "=" <expr>
def parseAssign():
    lex()
    if nextToken[0] == lexer.EQUAL:
        lex()
        res = parseExpression()
        if res:
            lex()
            if nextToken[0] == lexer.SEMICOLON:
                lex()
                return True
            else:
                error('Expected a semicolon')
                return False
        else:
            return False
    else:
        error('Expected "="')
        return False

# <stmt> -> <print>
#           <input>
#           <assign>
#           <if>
#           <while>
#           <for>
def parseStmt():
    if nextToken[0] == lexer.KEYWORD:
        match nextToken[1]:
            case 'print':
                return parsePrint()
            case 'get':
                return parseInput()
            case 'and':
                error('"and" must be part of an expression.')
                return False
            case 'do':
                error('"do" must be part of a while or for loop.')
                return False
            case 'or':
                error('"or" must be part of an expression.')
                return False
            case 'if':
                return parseIf()
            case 'while':
                return parseWhile()
            case 'for':
                return parseFor()
            case 'then':
                error('"then" must be part of an if statement.')
                return False
            case 'else':
                error('"else" must be part of an if statement.')
                return False
            case 'end':
                error('"end" must be part of an if statement, or a loop.')
                return False
            case 'not':
                error('"not" must be part of a value')
                return False
            case _:
                error('Expected Command')
                return False    
    elif nextToken[0] == lexer.ID:
        return parseAssign()
    else:
        error('Expected Statement')
        return False

# <prog> -> <stmt_list>
# <stmt_list> -> <stmt> ";" <stmt_list>
def parseProg():
    res = parseStmt()
    if res:
        if nextToken[0] != lexer.END_OF_INPUT:
            res = parseProg()
    return res

# <if> -> "if" <expr> "then" <stmt_list> "else" <stmt_list> "end"
def parseIf():
    lex()
    res = parseExpression()
    # "if" <expr>
    if res:
        lex()
        # "if" <expr> "then"
        if nextToken[0] == lexer.KEYWORD and nextToken[1] == 'then':
            lex()
            res = parseProg()
            # "if" <expr> "then" <stmt_list>
            if res:
                # "if" <expr> "then" <stmt_list> "else"
                if nextToken[0] == lexer.KEYWORD and nextToken[1] == 'else':
                    lex()
                    res = parseProg()
                    # "if" <expr> "then" <stmt_list> "else" <stmt_list>
                    if res:
                        # "if" <expr> "then" <stmt_list> "else" <stmt_list> "end"
                        if nextToken[0] == lexer.KEYWORD and nextToken[1] == 'end':
                            lex()
                            if nextToken[0] == lexer.SEMICOLON:
                                lex()
                                return True
                            else:
                                error('Expected a semicolon')
                                return False
                        else:
                            error('Expected "end"')
                            return False
                    else:
                        return False
                # "if" <expr> "then" <stmt_list> "end"
                elif nextToken[0] == lexer.KEYWORD and nextToken[1] == 'end':
                    lex()
                    if nextToken[0] == lexer.SEMICOLON:
                        lex()
                        return True
                    else:
                        error('Expected a semicolon')
                        return False
                else:
                    error('Expected "end"')
                    return False
            else:
                return False
        else:
            error('Expected "then"')
            return False
    else:
        return False

# <while> -> "while" <expr> "do" <stmt_list> "end"
def parseWhile():
    lex()
    res = parseExpression()
    if res:
        lex()
        if nextToken[0] == lexer.KEYWORD and nextToken[1] == 'do':
            lex()
            res = parseProg()
            if res:
                lex()
                if nextToken[0] == lexer.KEYWORD and nextToken[1] == 'end':
                    lex()
                    if nextToken[0] == lexer.SEMICOLON:
                        lex()
                        return True
                    else:
                        error('Expected a semicolon')
                        return False
                else:
                    error('Expected "end"')
                    return False
            else:
                return False
        else:
            error('Expected "do"')
            return False
    else:
        return False

# <for> -> "for" ID INT "do" <stmt_list> "end"
def parseFor():
    lex()
    if nextToken[0] == lexer.ID:
        lex()
        if nextToken[0] == lexer.INT:
            lex()
            if nextToken[0] == lexer.KEYWORD and nextToken[1] == 'do':
                res = parseProg()
                if res:
                    lex()
                    if nextToken[0] == lexer.KEYWORD and nextToken[1] == 'end':
                        lex()
                        if nextToken[0] == lexer.SEMICOLON:
                            lex()
                            return True
                        else:
                            error('Expected a semicolon')
                            return False
                    else:
                        error('Expected "end"')
                        return False
                else:
                    return False
            else:
                error('Expected "end"')
                return False
        else:
            error('Expected INT')
            return False
    else:
        error('Expected ID')
        return False        

# Driver
input = list(sys.stdin.read())
lex()

if parseProg():
    print('Program is correct.')
