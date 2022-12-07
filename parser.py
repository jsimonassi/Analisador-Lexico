import scanner

token_list = []
current_consumed = 0

TEST_POSITION = {
    "LEFT": 0,
    "RIGHT": 1,
}


def var_decl():
    if match("ID") and var_decl2():
        increment_consumed(1)
        return True
    else:
        #Error


def _type():
    if match("int") or match("char"):
        increment_consumed(1)
        return True
    else:
        reset_consumed()
        return False


# dcl ____________________________________________________________
def dcl():
    if _type() and var_decl() and dcl2():
        return True
    if _type() and dcl3() and dcl4():
        return True

    if match("extern") and dcl():
        increment_consumed(1)
        return True
    else:
        reset_consumed()

    if match("void") and dcl3() and dcl4():
        increment_consumed(1)
        return True
    else:
        reset_consumed()
        return False


def dcl2():
    if (match(',') and var_decl() and dcl2()) or (match(',') and var_decl()):
        return True
    else:
        return False



def dcl3():
    #id '(' parm_types ')'
    if match("ID", 0) and match("(", 1) and parm_types() and match(")", 2):
        increment_consumed(3)
        return True
    else:
        reset_consumed()
        return False



def dcl4():
    pass


# end_dcl ____________________________________________________________


def func():
    pass


# prog ____________________________________________________________
def prog():
    if dcl() and match(';'):
        return True
    elif func():
        return True
    else:
        return False


#Helper
def clear_consumed():
    global current_consumed
    for i in range(current_consumed):
        token_list.pop(0)
    current_consumed = 0


def increment_consumed(consumed_tokens):
    global current_consumed
    current_consumed += consumed_tokens


def reset_consumed():
    global current_consumed
    current_consumed = 0

# end_prog ____________________________________________________________


#Verifica o match com o token atual
def match(token, offset=0, is_type_token=1):
    global token_list
    if token_list[offset][is_type_token] == token or token_list[offset][0] == "OPEN_COMMENT" or token_list[offset][0] == "CLOSE_COMMENT":
        return True
    else:
        return False


def parser():
    global token_list
    token_list = scanner.get_tokens()
    if prog():
        print("Parsing successful")
    else:
        raise Exception("Unpexpected token: " + token_list[0][1])


parser()
