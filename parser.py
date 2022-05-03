import sys, lexer

if_state = False
while_state = False
for_state = False

def error(msg):
    print(f'Error on line {lexer.line}: {msg}')

def lex():
    global input
    global next_token
    (next_token,input) = lexer.lex(input)
    if next_token[0] == lexer.ERROR:
        print(next_token[1])

# <v_expr> -> 𝜀
#             ">" <value>
#             ">=" <value>
#             "<" <value>
#             "<=" <value>
#             "==" <value>
#             "!=" <value>
def parse_v_expr():
    if next_token[0] in [lexer.GT, lexer.GE, lexer.LT, lexer.LE, lexer.SAME, lexer.NOT_EQUAL]:
        lex()
        if parse_value():
            return True
        else:
            return False
    # 𝜀 empty substitution, return true without advancing the program
    else:
        return True

# <factor> -> <value> <v_expr>
def parse_factor():
    if parse_value():
        if parse_v_expr():
            return True
        else:
            return False
    else:
        return False

# <f_expr> -> 𝜀
#             "*" <term>
#             "/" <term>
#             "%" <term>
def parse_f_expr():
    # "*" <term>, "/" <term>, "%" <term>
    if next_token[0] in [lexer.TIMES, lexer.DIVIDE, lexer.MODULO]:
        lex()
        if parse_term():
            return True
        else:
            return False
    # 𝜀 empty substitution, return true without advancing the program
    else:
        return True

# <term> -> <factor> <f_expr>
def parse_term():
    if parse_factor():
        if parse_f_expr():
            return True
        else:
            return False
    else:
        return False

# <t_expr> -> 𝜀
#             "+" <n_expr>
#             "-" <n_expr>
def parse_t_expr():
    # "+" <n_expr>, "-" <n_expr>
    if next_token[0] in [lexer.PLUS, lexer.MINUS]:
        lex()
        if parse_n_expr():
            return True
        else:
            return False
    # 𝜀 empty substitution, return true without advancing the program
    else:
        return True

# <n_expr> -> <term> <t_expr>
def parse_n_expr():
    if parse_term():
        if parse_t_expr():
            return True
        else:
            return False
    else:
        return False

# <b_expr> -> 𝜀
#             "and" <n_expr>
#             "or" <n_expr>
def parse_b_expr():
    # "and" <n_expr>, "or" <n_expr>
    if next_token[0] == lexer.KEYWORD and next_token[1] in ['and', 'or']:
        lex()
        if parse_n_expr():
            return True
        else:
            return False
    # 𝜀 empty substitution, return true without advancing the program
    else:
        return True

# <expr> -> <n_expr> <b_expr>
def parse_expr():
    if parse_n_expr():
        if parse_b_expr():
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
def parse_value():
    # "(" <expr> ")"
    if next_token[0] == lexer.OPEN_PAR:
        lex()
        if parse_expr():
            if next_token[0] == lexer.CLOSE_PAR:
                lex()
                return True
            else:
                error('Expected close parentheses')
                return False
        else:
            return False
    # "not" <value>
    elif next_token[0] == lexer.KEYWORD and next_token[1] == 'not':
        lex()
        return parse_value()
    # "-" <value>
    elif next_token[0] == lexer.MINUS:
        lex()
        return parse_value()
    # ID or INT
    elif next_token[0] in [lexer.INT, lexer.ID]:
        lex()
        return True
    else:
        error('Expected Value')
        return False

# <print> -> "print" <p-arg>
# <p-arg> -> STRING
#            <expr>
def parse_print():
    # "print" STRING
    if next_token[0] == lexer.STRING:
        lex()
        if next_token[0] == lexer.SEMICOLON:
            lex()
            return True
        else:
            error('Expected a semicolon')
            return False
    # "print" <expr>
    else:
        if parse_expr():
            if next_token[0] == lexer.SEMICOLON:
                lex()
                return True
            else:
                error('Expected a semicolon')
                return False
        else:
            return False

# <input> -> "get" ID
def parse_input():
    if next_token[0] == lexer.ID:
        lex()
        if next_token[0] == lexer.SEMICOLON:
            lex()
            return True
        else:
            error('Expected a semicolon')
            return False
    else:
        error('Expected ID')
        return False

# <assign> -> ID "=" <expr>
def parse_assign():
    if next_token[0] == lexer.EQUAL:
        lex()
        if parse_expr():
            if next_token[0] == lexer.SEMICOLON:
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
def parse_stmt():
    global if_state, while_state, for_state
    if next_token[0] == lexer.KEYWORD:
        match next_token[1]:
            case 'print':
                lex()
                return parse_print()
            case 'get':
                lex()
                return parse_input()
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
                return parse_if()
            case 'while':
                lex()
                while_state = True
                return parse_while()
            case 'for':
                lex()
                for_state = True
                return parse_for()
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
    elif next_token[0] == lexer.ID:
        lex()
        return parse_assign()
    else:
        error('Expected Statement')
        return False

# <prog> -> <stmt_list>
# <stmt_list> -> <stmt> ";" <stmt_list>
def parse_prog():
    res = parse_stmt()
    if res == None:
        return True
    elif res:
        if next_token[0] != lexer.END_OF_INPUT:
            res = parse_prog()
    return res

# <if> -> "if" <expr> "then" <stmt_list> "else" <stmt_list> "end"
def parse_if():
    global if_state
    # "if" <expr>
    if parse_expr():
        # "if" <expr> "then"
        if next_token[0] == lexer.KEYWORD and next_token[1] == 'then':
            lex()
            # "if" <expr> "then" <stmt_list>
            if parse_prog():
                # "if" <expr> "then" <stmt_list> "else"
                if next_token[0] == lexer.KEYWORD and next_token[1] == 'else':
                    lex()
                    # "if" <expr> "then" <stmt_list> "else" <stmt_list>
                    if parse_prog():
                        # "if" <expr> "then" <stmt_list> "else" <stmt_list> "end"
                        if next_token[0] == lexer.KEYWORD and next_token[1] == 'end':
                            lex()
                            if next_token[0] == lexer.SEMICOLON:
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
                elif next_token[0] == lexer.KEYWORD and next_token[1] == 'end':
                    lex()
                    if next_token[0] == lexer.SEMICOLON:
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
def parse_while():
    global while_state
    # "while" <expr>
    if parse_expr():
        # "while" <expr> "do"
        if next_token[0] == lexer.KEYWORD and next_token[1] == 'do':
            lex()
            # "while" <expr> "do" <stmt_list>
            if parse_prog():
                # while <expr> "do" <stmt_list> "end"
                if next_token[0] == lexer.KEYWORD and next_token[1] == 'end':
                    lex()
                    if next_token[0] == lexer.SEMICOLON:
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
def parse_for():
    global for_state
    # "for" ID
    if next_token[0] == lexer.ID:
        lex()
        # "for" ID INT
        if next_token[0] == lexer.INT:
            lex()
            # "for" ID INT "do"
            if next_token[0] == lexer.KEYWORD and next_token[1] == 'do':
                lex()
                # "for" ID INT "do" <stmt_list>
                if parse_prog():
                    # "for" ID INT "do" <stmt_list> "end"
                    if next_token[0] == lexer.KEYWORD and next_token[1] == 'end':
                        lex()
                        if next_token[0] == lexer.SEMICOLON:
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
                error('Expected "do"')
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
if parse_prog():
    print('Program is correct.')
