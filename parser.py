class Parser:

    def __init__(self, filtered_tokens):
        self.token_list = filtered_tokens
        self.count_position = 0
        self.count_base = 0
        self.error_aux = []
        self.max_base = 0
        self.list_id = []

    def append_new_identifier(self, token):
        """Adiciona o token na lista de identificadores"""
        if token[1] in self.list_id:
            print("Token '" + str(token[1]) + "' already exists. Redeclaration in line: " + str(token[2]))
            exit(1)
        self.list_id.append(token[1])

    def update_max_base(self, base):
        """Atualiza o valor da base. Base é a posição do token antes de uma validação"""
        if self.max_base < base:
            self.max_base = base

    # Funções extraídas da EBNF fatorada:
    def var_decl(self):
        base = self.count_position
        self.update_max_base(base)
        if self.match("ID", isDecl=True) and self.var_decl1():
            self.append_new_identifier(self.token_list[base])
            return True
        else:
            self.count_position = base
        return False

    def var_decl1(self):
        base = self.count_position
        self.update_max_base(base)
        if self.match("[") and self.match("INTCON") and self.match("]"):
            return True
        else:
            self.count_position = base
        return True

    def parm_types(self):
        base = self.count_position
        self.update_max_base(base)
        if self.match('void'):
            return True
        else:
            count_position = base
        if self._type() and self.match("ID", isDecl=True) and self.match("[") and self.match(
                "]") and self.parm_types2():
            self.append_new_identifier(self.token_list[base + 1])
            return True
        else:
            self.count_position = base
        if self._type() and self.match("ID", isDecl=True) and self.parm_types2():
            self.append_new_identifier(self.token_list[base + 1])
            return True
        else:
            self.count_position = base
        return False

    def parm_types2(self):
        base = self.count_position
        self.update_max_base(base)
        if self.match(',') and self.parm_types():
            return True
        else:
            self.count_position = base
        return True

    def _type(self):
        base = self.count_position
        self.update_max_base(base)
        if self.match("int") or self.match("char"):
            return True
        else:
            self.count_position = base
        return False

    def dcl(self):
        base = self.count_position
        self.update_max_base(base)
        if self._type() and self.dcl1():
            return True
        else:
            self.count_position = base
        if self.dcl5():
            return True
        else:
            self.count_position = base
        if self.match('void') and self.dcl3() and self.dcl4():
            return True
        else:
            self.count_position = base
        return False

    def dcl1(self):
        base = self.count_position
        self.update_max_base(base)
        if self.var_decl() and self.dcl2():
            return True
        else:
            self.count_position = base
        if self.dcl3() and self.dcl4():
            return True
        else:
            self.count_position = base
        return True

    def dcl2(self):
        base = self.count_position
        self.update_max_base(base)
        if self.match(',') and self.var_decl():
            return True
        else:
            self.count_position = base
        return True

    def dcl3(self):
        base = self.count_position
        self.update_max_base(base)
        if self.match("ID") and self.match("(") and self.parm_types() and self.match(")"):
            return True
        else:
            self.count_position = base
        return False

    def dcl4(self):
        base = self.count_position
        self.update_max_base(base)
        if self.match(',') and self.dcl3():
            return True
        else:
            self.count_position = base
        return True

    def dcl5(self):
        base = self.count_position
        self.update_max_base(base)
        if self.match('extern') and self.dcl():
            return True
        else:
            self.count_position = base
        return False

    def func(self):
        base = self.count_position
        self.update_max_base(base)
        if self._type() and self.func1():
            return True
        else:
            count_position = base
        if self.match('void') and self.func1():
            return True
        else:
            self.count_position = base
        return False

    def func1(self):
        base = self.count_position
        self.update_max_base(base)
        if self.match("ID") and self.match("(") and self.parm_types() and self.match(")") and self.match(
                "{") and self.func2() and self.func4() and self.match("}"):
            return True
        else:
            self.count_position = base
        return False

    def func2(self):
        base = self.count_position
        self.update_max_base(base)
        if self._type() and self.var_decl() and self.func3() and self.match(';') and self.func2():
            return True
        else:
            self.count_position = base
        return True

    def func3(self):
        base = self.count_position
        self.update_max_base(base)
        if self.match(',') and self.var_decl() and self.func3():
            return True
        else:
            self.count_position = base
        return True

    def func4(self):
        base = self.count_position
        self.update_max_base(base)
        if self.stmt() and self.func2():
            return True
        else:
            self.count_position = base
        return True

    def caseElse(self):  # TODO: Utils
        base = self.count_position
        self.update_max_base(base)
        if self.match('else'):
            return True
        else:
            self.count_position = base
        return True

    def stmt(self):
        base = self.count_position
        self.update_max_base(base)
        if self.match("if") and self.match("(") and self.expr() and self.match(
                ")") and self.stmt() and self.caseElse() and self.stmt():
            return True
        else:
            self.count_position = base
        if self.match("if") and self.match("(") and self.expr() and self.match(")") and self.match(
                "else") and self.stmt():
            return True
        else:
            self.count_position = base
        if self.match("while") and self.match("(") and self.expr() and self.match(")") and self.stmt():
            return True
        else:
            self.count_position = base
        if self.match("for") and self.match("(") and self.match(";") and self.match(";") and self.match(
                ")") and self.stmt():
            return True
        else:
            self.count_position = base
        if self.match("for") and self.match("(") and self.assg() and self.match(";") and self.match(";") and self.match(
                ")") and self.stmt():
            return True
        else:
            self.count_position = base
        if self.match("for") and self.match("(") and self.match(";") and self.expr() and self.match(";") and self.match(
                ")") and self.stmt():
            return True
        else:
            self.count_position = base
        if self.match("for") and self.match("(") and self.match(";") and self.match(";") and self.assg() and self.match(
                ")") and self.stmt():
            return True
        else:
            self.count_position = base
        if self.match("for") and self.match("(") and self.assg() and self.match(";") and self.expr() and self.match(
                ";") and self.match(")") and self.stmt():
            return True
        else:
            self.count_position = base
        if self.match("for") and self.match("(") and self.assg() and self.match(";") and self.match(
                ";") and self.assg() and self.match(")") and self.stmt():
            return True
        else:
            self.count_position = base
        if self.match("for") and self.match("(") and self.match(";") and self.expr() and self.match(
                ";") and self.assg() and self.match(")") and self.stmt():
            return True
        else:
            self.count_position = base
        if self.match("for") and self.match("(") and self.assg() and self.match(";") and self.expr() and self.match(
                ";") and self.assg() and self.match(")") and self.stmt():
            return True
        else:
            self.count_position = base
        if self.match("return") and self.match(";") and self.stmt():
            return True
        else:
            self.count_position = base
        if self.match("return") and self.expr() and self.match(";") and self.stmt():
            return True
        else:
            self.count_position = base
        if self.assg() and self.match(";") and self.stmt():
            return True
        else:
            self.count_position = base
        if self.match("ID") and self.match("(") and self.match(")") and self.match(";") and self.stmt():
            return True
        else:
            self.count_position = base
        if self.match("ID") and self.match("(") and self.expr() and self.stmt2() and self.match(")") and self.match(
                ";") and self.stmt():
            return True
        else:
            self.count_position = base
        if self.match("{") and self.stmt() and self.match("}") and self.stmt():
            return True
        else:
            self.count_position = base
        if self.match(";") and self.stmt():
            return True
        else:
            self.count_position = base
        return True

    def stmt2(self):
        base = self.count_position
        self.update_max_base(base)
        if self.match(",") and self.expr() and self.stmt2():
            return True
        else:
            self.count_position = base
        return True

    def assg(self):
        base = self.count_position
        self.update_max_base(base)
        if self.match("ID") and self.match("=") and self.expr():
            return True
        else:
            self.count_position = base
        if self.match("ID") and self.match("[") and self.expr() and self.match("]") and self.match("=") and self.expr():
            return True
        else:
            self.count_position = base
        return False

    def expr(self):
        base = self.count_position
        self.update_max_base(base)
        if self.match("-") and self.expr3():
            return True
        else:
            self.count_position = base
        if self.match("!") and self.expr3():
            return True
        else:
            self.count_position = base
        if self.match("ID") and self.expr3():
            return True
        else:
            self.count_position = base
        if self.match("ID") and self.match("(") and self.match(")") and self.expr3():
            return True
        else:
            self.count_position = base
        if self.match("ID") and self.match("(") and self.expr() and self.match(")") and self.expr3():
            return True
        else:
            count_position = base
        if self.match("ID") and self.match("(") and self.expr() and self.expr2() and self.match(")") and self.expr3():
            return True
        else:
            self.count_position = base
        if self.match("ID") and self.match("[") and self.expr() and self.match("]") and self.expr3():
            return True
        else:
            self.count_position = base
        if self.match("(") and self.expr() and self.match(")") and self.expr3():
            return True
        else:
            self.count_position = base
        if self.match("INTCON") and self.expr3():
            return True
        else:
            self.count_position = base
        if self.match("CHAR") and self.expr3():
            return True
        else:
            self.count_position = base
        if self.match("STRINGCON") and self.expr3():
            return True
        else:
            self.count_position = base
        return False

    def expr2(self):
        base = self.count_position
        self.update_max_base(base)
        if self.match(",") and self.expr() and self.expr3():
            return True
        else:
            self.count_position = base
        return True

    def expr3(self):
        base = self.count_position
        self.update_max_base(base)
        if self.binop() and self.expr() and self.expr3():
            return True
        else:
            self.count_position = base
        if self.relop() and self.expr() and self.expr3():
            return True
        else:
            self.count_position = base
        if self.logicalOp() and self.expr() and self.expr3():
            return True
        else:
            self.count_position = base
            return True

    def binop(self):
        base = self.count_position
        self.update_max_base(base)
        if self.match("+") or self.match("-") or self.match("*") or self.match("/") or self.match("%"):
            return True
        else:
            self.count_position = base
        return False

    def relop(self):
        base = self.count_position
        self.update_max_base(base)
        if self.match("<") or self.match(">") or self.match("<=") or self.match(">=") or self.match("==") or self.match(
                "!="):
            return True
        else:
            self.count_position = base
        return False

    def logicalOp(self):
        base = self.count_position
        self.update_max_base(base)
        if self.match("&&") or self.match("||"):
            return True
        else:
            self.count_position = base
        return False

    def prog(self):
        base = self.count_position
        self.update_max_base(base)
        if self.dcl() and self.match(';'):
            return True
        else:
            self.count_position = base
        if self.func():
            return True
        else:
            self.count_position = base
        return False

    def countIncremental(self, amount):
        self.count_position += amount

    def match(self, token, isDecl=False):
        if not isDecl and self.token_list[self.count_position][0] == 'ID' and self.token_list[self.count_position][
            1] not in self.list_id:
            print("Token '" + self.token_list[self.count_position][1] + "' was not declared at line " + str(
                self.token_list[self.count_position][2]))
            exit(1)

        if self.token_list[self.count_position][1] == token or self.token_list[self.count_position][0] == token:
            self.countIncremental(1)
            return True
        else:
            self.error_aux.append(self.token_list[self.count_position][1])
            return False

    def start_parser(self):
        if self.prog():
            print("Accepted")
        else:
            # TODO texto merda
            print("Error at token " + self.token_list[self.max_base][1] + "'" + " on line: " + str(
                self.token_list[self.max_base][2]))
            exit(1)
