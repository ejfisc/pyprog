import sys, lexer

if_state = False
while_state = False
for_state = False

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
    if nextToken[0] in [lexer.GT, lexer.GE, lexer.LT, lexer.LE, lexer.SAME, lexer.NOT_EQUAL]:
        lex()
        if parseVal():
            return True
        else:
            return False
    # 𝜀 empty substitution, return true without advancing the program
    else:
        return True

# <factor> -> <value> <v_expr>
def parseFactor():
    if parseVal():
        if parseVExpr():
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
    # "*" <term>, "/" <term>, "%" <term>
    if nextToken[0] in [lexer.TIMES, lexer.DIVIDE, lexer.MODULO]:
        lex()
        if parseTerm():
            return True
        else:
            return False
    # 𝜀 empty substitution, return true without advancing the program
    else:
        return True

# <term> -> <factor> <f_expr>
def parseTerm():
    if parseFactor():
        if parseFExpr():
            return True
        else:
            return False
    else:
        return False

# <t_expr> -> 𝜀
#             "+" <n_expr>
#             "-" <n_expr>
def parseTExpr():
    # "+" <n_expr>, "-" <n_expr>
    if nextToken[0] in [lexer.PLUS, lexer.MINUS]:
        lex()
        if parseNExpr():
            return True
        else:
            return False
    # 𝜀 empty substitution, return true without advancing the program
    else:
        return True

# <n_expr> -> <term> <t_expr>
def parseNExpr():
    if parseTerm():
        if parseTExpr():
            return True
        else:
            return False
    else:
        return False

# <b_expr> -> 𝜀
#             "and" <n_expr>
#             "or" <n_expr>
def parseBExpr():
    # "and" <n_expr>, "or" <n_expr>
    if nextToken[0] == lexer.KEYWORD and nextToken[1] in ['and', 'or']:
        lex()
        if parseNExpr():
            return True
        else:
            return False
    # 𝜀 empty substitution, return true without advancing the program
    else:
        return True

# <expr> -> <n_expr> <b_expr>
def parseExpression():
    if parseNExpr():
        if parseBExpr():
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
    # "(" <expr> ")"
    if nextToken[0] == lexer.OPEN_PAR:
        lex()
        if parseExpression():
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
        lex()
        return parseVal()
    # "-" <value>
    elif nextToken[0] == lexer.MINUS:
        lex()
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
        if parseExpression():
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
    if nextToken[0] == lexer.ID:
        lex()
        if nextToken[0] == lexer.SEMICOLON:
            lex()
            return True
        else:
            error('Expected a semicolon')
            return False
    else:
        error('Expected ID')
        return False

# <assign> -> ID "=" <expr>
def parseAssign():
    if nextToken[0] == lexer.EQUAL:
        lex()
        if parseExpression():
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
    global if_state, while_state, for_state
    if nextToken[0] == lexer.KEYWORD:
        match nextToken[1]:
            case 'print':
                lex()
                return parsePrint()
            case 'get':
                lex()
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
                lex()
                if_state = True
                return parseIf()
            case 'while':
                lex()
                while_state = True
                return parseWhile()
            case 'for':
                lex()
                for_state = True
                return parseFor()
            case 'then':
                if if_state:
                    return None
                else:
                    error('"then" must be part of an if statement.')
                    return False
            case 'else':
                if if_state:
                    return None
                else:
                    error('"else" must be part of an if statement.')
                    return False
            case 'end':
                if if_state or while_state or for_state:
                    return None
                else:
                    error('"end" must be part of an if statement, or a loop.')
                    return False
            case 'not':
                error('"not" must be part of a value')
                return False
            case _:
                error('Expected Command')
                return False    
    elif nextToken[0] == lexer.ID:
        lex()
        return parseAssign()
    else:
        error('Expected Statement')
        return False

# <prog> -> <stmt_list>
# <stmt_list> -> <stmt> ";" <stmt_list>
def parseProg():
    res = parseStmt()
    if res == None:
        return True
    elif res:
        if nextToken[0] != lexer.END_OF_INPUT:
            res = parseProg()
    return res

# <if> -> "if" <expr> "then" <stmt_list> "else" <stmt_list> "end"
def parseIf():
    global if_state
    # "if" <expr>
    if parseExpression():
        # "if" <expr> "then"
        if nextToken[0] == lexer.KEYWORD and nextToken[1] == 'then':
            lex()
            # "if" <expr> "then" <stmt_list>
            if parseProg():
                # "if" <expr> "then" <stmt_list> "else"
                if nextToken[0] == lexer.KEYWORD and nextToken[1] == 'else':
                    lex()
                    # "if" <expr> "then" <stmt_list> "else" <stmt_list>
                    if parseProg():
                        # "if" <expr> "then" <stmt_list> "else" <stmt_list> "end"
                        if nextToken[0] == lexer.KEYWORD and nextToken[1] == 'end':
                            lex()
                            if nextToken[0] == lexer.SEMICOLON:
                                lex()
                                if_state = False
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
                        if_state = False
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
    global while_state
    # "while" <expr>
    if parseExpression():
        # "while" <expr> "do"
        if nextToken[0] == lexer.KEYWORD and nextToken[1] == 'do':
            lex()
            # "while" <expr> "do" <stmt_list>
            if parseProg():
                # while <expr> "do" <stmt_list> "end"
                if nextToken[0] == lexer.KEYWORD and nextToken[1] == 'end':
                    lex()
                    if nextToken[0] == lexer.SEMICOLON:
                        lex()
                        while_state = False
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
    global for_state
    # "for" ID
    if nextToken[0] == lexer.ID:
        lex()
        # "for" ID INT
        if nextToken[0] == lexer.INT:
            lex()
            # "for" ID INT "do"
            if nextToken[0] == lexer.KEYWORD and nextToken[1] == 'do':
                lex()
                # "for" ID INT "do" <stmt_list>
                if parseProg():
                    # "for" ID INT "do" <stmt_list> "end"
                    if nextToken[0] == lexer.KEYWORD and nextToken[1] == 'end':
                        lex()
                        if nextToken[0] == lexer.SEMICOLON:
                            lex()
                            for_state = False
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
