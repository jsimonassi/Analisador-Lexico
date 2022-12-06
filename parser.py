import scanner

token_list = []


def var_decl():
    if match("ID"):
        return True
    else:
        return False
    #TODO: id '[' intcon ']'


def _type():
    if match("int") or match("char"):
        return True
    else:
        return False


# dcl ____________________________________________________________
def dcl():
    if _type() and var_decl() and dcl2():
        return True
    elif _type() and dcl3() and dcl4():
        return True
    elif match("extern") and dcl():
        return True
    elif match("void") and dcl3() and dcl4():
        return True
    else:
        return False


def dcl2():
    if match(',') and var_decl() and dcl2():
        return True
    else:
        #TODO: epsilon
        return False


def dcl3():
    pass


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


# end_prog ____________________________________________________________

def match(token):
    global token_list
    if token_list[0][1] == token or token_list[0][0] == "OPEN_COMMENT" or token_list[0][0] == "CLOSE_COMMENT":
        token_list.pop(0)
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
