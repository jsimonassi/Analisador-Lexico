import scanner

token_list = []
count_position = 0
count_base = 0
error_aux = []
TEST_POSITION = {
    "LEFT": 0,
    "RIGHT": 1,
}


# var_decl ____________________________________________________________
def var_decl():
    global count_position
    base = count_position
    if match("ID") and var_decl1():
        return True
    else:
        count_position = base
    return False


def var_decl1():
    global count_position
    base = count_position
    if match("[") and match("NUMBER") and match("]"):
        return True
    else:
        count_position = base
    return True


# end var_decl ____________________________________________________________

# parm_types ____________________________________________________________

def parm_types():
    global count_position
    base = count_position
    if match('void'):
        return True
    else:
        count_position = base
    if _type() and match("ID") and parm_types2():
        return True
    else:
        count_position = base
    if _type() and match("ID") and match("[") and match("]") and parm_types2():
        return True
    else:
        count_position = base
    return False


def parm_types2():
    global count_position
    base = count_position
    if match(',') and parm_types():
        return True
    else:
        count_position = base
    return True


# end parm_types ____________________________________________________________

def _type():
    global count_position
    base = count_position
    if match("int") or match("char"):
        return True
    else:
        count_position = base
    return False


# dcl ____________________________________________________________
def dcl():
    global count_position
    base = count_position
    if _type() and dcl1():
        return True
    else:
        count_position = base
    if dcl5():
        return True
    else:
        count_position = base
    if match('void') and dcl3() and dcl4():
        return True
    else:
        count_position = base
    return False


def dcl1():
    global count_position
    base = count_position
    if var_decl() and dcl2():
        return True
    else:
        count_position = base
    if dcl3() and dcl4():
        return True
    else:
        count_position = base
    return True


def dcl2():
    global count_position
    base = count_position
    if match(',') and var_decl():
        return True
    else:
        count_position = base
    return True


def dcl3():
    global count_position
    base = count_position
    if match("ID") and match("(") and parm_types() and match(")"):
        return True
    else:
        count_position = base
    return False


def dcl4():
    global count_position
    base = count_position
    if match(',') and dcl3():
        return True
    else:
        count_position = base
    return True


def dcl5():
    global count_position
    base = count_position
    if match('extern') and dcl():
        return True
    else:
        count_position = base
    return False


# end_dcl ____________________________________________________________

# func ____________________________________________________________
def func():
    global count_position
    base = count_position
    if _type() and func1():
        return True
    else:
        count_position = base
    if match('void') and func1():
        return True
    else:
        count_position = base
    return False


def func1():
    global count_position
    base = count_position
    if match("ID") and match("(") and parm_types() and match(")") and match("{") and func2() and func4() and match("}"):
        return True
    else:
        count_position = base
    return False


def func2():
    global count_position
    base = count_position
    if _type() and var_decl() and func3() and match(';'):
        return True
    else:
        count_position = base
    return True


def func3():
    global count_position
    base = count_position
    if match(',') and var_decl():
        return True
    else:
        count_position = base
    return True


def func4():
    global count_position
    base = count_position
    if stmt():
        return True
    else:
        count_position = base
    return True


# end func ____________________________________________________________

# stmt ____________________________________________________________
def stmt():
    global count_position
    base = count_position
    if match("if") and match("(") and expr() and match(")") and stmt():
        return True
    else:
        count_position = base
    if match("if") and match("(") and expr() and match(")") and match("else") and stmt():
        return True
    else:
        count_position = base
    if match("while") and match("(") and expr() and match(")") and stmt():
        return True
    else:
        count_position = base
    if match("for") and match("(") and match(";") and match(";") and match(")") and stmt():
        return True
    else:
        count_position = base
    if match("for") and match("(") and assg() and match(";") and match(";") and match(")") and stmt():
        return True
    else:
        count_position = base
    if match("for") and match("(") and match(";") and expr() and match(";") and match(")") and stmt():
        return True
    else:
        count_position = base
    if match("for") and match("(") and match(";") and match(";") and assg() and match(")") and stmt():
        return True
    else:
        count_position = base
    if match("for") and match("(") and assg() and match(";") and expr() and match(";") and match(")") and stmt():
        return True
    else:
        count_position = base
    if match("for") and match("(") and assg() and match(";") and match(";") and assg() and match(")") and stmt():
        return True
    else:
        count_position = base
    if match("for") and match("(") and match(";") and expr() and match(";") and assg() and match(")") and stmt():
        return True
    else:
        count_position = base
    if match("for") and match("(") and assg() and match(";") and expr() and match(";") and assg() and match(")") and stmt():
        return True
    else:
        count_position = base
    if match("return") and match(";") and stmt():
        return True
    else:
        count_position = base
    if match("return") and expr() and match(";") and stmt():
        return True
    else:
        count_position = base
    if assg() and match(";") and stmt():
        return True
    else:
        count_position = base
    if match("ID") and match("(") and match(")") and match(";") and stmt():
        return True
    else:
        count_position = base
    if match("ID") and match("(") and expr() and stmt2() and match(")") and match(";") and stmt():
        return True
    else:
        count_position = base
    if match("{") and stmt() and match("}") and stmt():
        return True
    else:
        count_position = base
    if match(";") and stmt():
        return True
    else:
        count_position = base
    return True


def stmt2():
    global count_position
    base = count_position
    if match(",") and expr() and stmt2():
        return True
    else:
        count_position = base
    return True

# end stmt ____________________________________________________________

# assg
def assg():
    global count_position
    base = count_position
    if match("ID") and match("=") and expr():
        return True
    else:
        count_position = base
    if match("ID") and match("[") and expr() and match("]") and match("=") and expr():
        return True
    else:
        count_position = base
    return False


# end assg ____________________________________________________________

# expr ____________________________________________________________

def expr():
    global count_position
    base = count_position
    if match("-") and expr3():
        return True
    else:
        count_position = base
    if match("!") and expr3():
        return True
    else:
        count_position = base
    if match("ID") and expr3():
        return True
    else:
        count_position = base
    if match("ID") and match("(") and match(")") and expr3():
        return True
    else:
        count_position = base
    if match("ID") and match("(") and expr() and match(")") and expr3():
        return True
    else:
        count_position = base
    if match("ID") and match("(") and expr() and expr2() and match(")") and expr3():
        return True
    else:
        count_position = base
    if match("ID") and match("[") and expr() and match("]") and expr3():
        return True
    else:
        count_position = base
    if match("(") and expr() and match(")") and expr3():
        return True
    else:
        count_position = base
    if match("NUMBER") and expr3():
        return True
    else:
        count_position = base
    if match("charcon") and expr3():
        return True
    else:
        count_position = base
    if match("stringcon") and expr3():
        return True
    else:
        count_position = base
    return False


def expr2():
    global count_position
    base = count_position
    if match(",") and expr() and expr3():
        return True
    else:
        count_position = base
    return True


def expr3():
    global count_position
    base = count_position
    if binop() and expr() and expr3():
        return True
    else:
        count_position = base
    if relop() and expr() and expr3():
        return True
    else:
        count_position = base
    if logicalOp() and expr() and expr3():
        return True
    else:
        count_position = base
        return True


# end expr ____________________________________________________________

# binop ____________________________________________________________

def binop():
    global count_position
    base = count_position
    if match("+") or match("-") or match("*") or match("/") or match("%"):
        return True
    else:
        count_position = base
    return False


# end binop ____________________________________________________________

# relop ____________________________________________________________

def relop():
    global count_position
    base = count_position
    if match("<") or match(">") or match("<=") or match(">=") or match("==") or match("!="):
        return True
    else:
        count_position = base
    return False


# end relop ____________________________________________________________


# logicalOp ____________________________________________________________

def logicalOp():
    global count_position
    base = count_position
    if match("&&") or match("||"):
        return True
    else:
        count_position = base
    return False


# end logicalOp ____________________________________________________________

# prog ____________________________________________________________
def prog():
    global count_position
    base = count_position
    if dcl() and match(';'):
        return True
    else:
        count_position = base
    if func():
        return True
    else:
        count_position = base
    return False


# Helper functions --------------------------------------------------
def countIncremental(amount):
    global count_position
    count_position += amount


# end_prog ____________________________________________________________


# Verifica o match com o token atual
def match(token):
    global token_list
    global count_position
    global error_aux
    if count_position + 1 > len(token_list):
        raise Exception("Erro de sintaxe")
    if token_list[count_position][1] == token or token_list[count_position][0] == token:
        countIncremental(1)
        return True
    else:
        error_aux.append(token_list[count_position][1])
        return False


def parser():
    global token_list
    token_list = scanner.lexical()
    print(token_list)
    # if prog():
    #     print("Parsing successful")
    # else:
    #     raise Exception("Unpexpected token: " + str(error_aux))


parser()

