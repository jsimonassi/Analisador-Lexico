import inspect
from tree import Node

class Parser:

    def __init__(self, filtered_list):
        self.token_list = filtered_list
        self.position = 0
        self.error_point = 0
        self.list_id = []
        self.derivation_tree = []
        self.tree_items = []

    def start_parser(self):
        """Inicia o processo de parser pelo símbolo não terminal inicial"""
        compile_success, derivation_tree = self.prog()
        if compile_success:
            print("Código compilado com sucesso!")
            return derivation_tree
        else:
            print("Identificador inexistente ou inesperado próximo a: " + self.token_list[self.error_point][
                1] + "'" + " na linha:" + str(
                self.token_list[self.error_point][2]))
            exit(1)

# Utils
    def append_new_identifier(self, token):
        """Adiciona o token na lista de identificadores"""
        if token[1] in self.list_id:
            print("A variável: '" + str(token[1]) + "' já existe e foi redeclarada na linha: " + str(token[2]))
            exit(1)
        self.list_id.append(token[1])

    def update_error_point(self, safe_point):
        """Atualiza o ponto de erro. Isto é, veio até aqui sem error!"""
        if self.error_point < safe_point:
            self.error_point = safe_point

    def check_token(self, token, is_new_id=False):
        """Verifica se o token atual é valido. Verifica também se o token do tipo ID já foi declarado."""
        if not is_new_id and self.token_list[self.position][0] == 'ID' and self.token_list[self.position][1] not in self.list_id:
            print("A variável '" + self.token_list[self.position][1] + "' ainda não foi declarada e está sendo usada na linha: " + str(
                self.token_list[self.position][2]))
            exit(1)

        if self.token_list[self.position][1] == token or self.token_list[self.position][0] == token:
            self.append_branch(self.token_list[self.position][1])
            self.position += 1
            return True
        return False

    def append_branch(self, token):
        """Adiciona o token na árvore de derivação"""
        flag_add_list = False
        recursive_stack = []
        for i in range(len(inspect.stack()) - 1, 0, -1):
            _, _, _, function_name, _, _ = inspect.stack()[i]
            if function_name == 'prog':
                flag_add_list = True

            if function_name == 'check_token':
                recursive_stack.append(token)
                flag_add_list = False

            if flag_add_list:
                recursive_stack.append(function_name)

        branch = Node.make_node_by_recursive_list(recursive_stack)
        self.derivation_tree, self.tree_items = Node.append_child(self.derivation_tree, branch, self.tree_items)

# Funções extraídas da EBNF fatorada:
    def var_decl(self):
        safe_point = self.position
        self.update_error_point(safe_point)
        if self.check_token("ID", is_new_id=True) and self.var_decl1():
            self.append_new_identifier(self.token_list[safe_point])
            return True
        else:
            self.position = safe_point
        return False

    def var_decl1(self):
        safe_point = self.position
        self.update_error_point(safe_point)
        if self.check_token("[") and self.check_token("INTCON") and self.check_token("]"):
            return True
        else:
            self.position = safe_point
        return True

    def parm_types(self):
        safe_point = self.position
        self.update_error_point(safe_point)
        if self.check_token('void'):
            return True
        else:
            self.position = safe_point
        if self._type() and self.check_token("ID", is_new_id=True) and self.check_token("[") and self.check_token(
                "]") and self.parm_types2():
            self.append_new_identifier(self.token_list[safe_point + 1])
            return True
        else:
            self.position = safe_point
        if self._type() and self.check_token("ID", is_new_id=True) and self.parm_types2():
            self.append_new_identifier(self.token_list[safe_point + 1])
            return True
        else:
            self.position = safe_point
        return False

    def parm_types2(self):
        safe_point = self.position
        self.update_error_point(safe_point)
        if self.check_token(',') and self.parm_types():
            return True
        else:
            self.position = safe_point
        return True

    def _type(self):
        safe_point = self.position
        self.update_error_point(safe_point)
        if self.check_token("int") or self.check_token("char"):
            return True
        else:
            self.position = safe_point
        return False

    def dcl(self):
        safe_point = self.position
        self.update_error_point(safe_point)
        if self._type() and self.dcl1():
            return True
        else:
            self.position = safe_point
        if self.dcl5():
            return True
        else:
            self.position = safe_point
        if self.check_token('void') and self.dcl3() and self.dcl4():
            return True
        else:
            self.position = safe_point
        return False

    def dcl1(self):
        safe_point = self.position
        self.update_error_point(safe_point)
        if self.var_decl() and self.dcl2():
            return True
        else:
            self.position = safe_point
        if self.dcl3() and self.dcl4():
            return True
        else:
            self.position = safe_point
        return True

    def dcl2(self):
        safe_point = self.position
        self.update_error_point(safe_point)
        if self.check_token(',') and self.var_decl():
            return True
        else:
            self.position = safe_point
        return True

    def dcl3(self):
        safe_point = self.position
        self.update_error_point(safe_point)
        if self.check_token("ID") and self.check_token("(") and self.parm_types() and self.check_token(")"):
            return True
        else:
            self.position = safe_point
        return False

    def dcl4(self):
        safe_point = self.position
        self.update_error_point(safe_point)
        if self.check_token(',') and self.dcl3():
            return True
        else:
            self.position = safe_point
        return True

    def dcl5(self):
        safe_point = self.position
        self.update_error_point(safe_point)
        if self.check_token('extern') and self.dcl():
            return True
        else:
            self.position = safe_point
        return False

    def func(self):
        safe_point = self.position
        self.update_error_point(safe_point)
        if self._type() and self.func1():
            return True
        else:
            self.position = safe_point
        if self.check_token('void') and self.func1():
            return True
        else:
            self.position = safe_point
        return False

    def func1(self):
        safe_point = self.position
        self.update_error_point(safe_point)
        if self.check_token("ID") and self.check_token("(") and self.parm_types() and self.check_token(")") and self.check_token(
                "{") and self.func2() and self.func4() and self.check_token("}"):
            return True
        else:
            self.position = safe_point
        return False

    def func2(self):
        safe_point = self.position
        self.update_error_point(safe_point)
        if self._type() and self.var_decl() and self.func3() and self.check_token(';') and self.func2():
            return True
        else:
            self.position = safe_point
        return True

    def func3(self):
        safe_point = self.position
        self.update_error_point(safe_point)
        if self.check_token(',') and self.var_decl() and self.func3():
            return True
        else:
            self.position = safe_point
        return True

    def func4(self):
        safe_point = self.position
        self.update_error_point(safe_point)
        if self.stmt() and self.func2():
            return True
        else:
            self.position = safe_point
        return True

    def else_case(self):
        safe_point = self.position
        self.update_error_point(safe_point)
        if self.check_token('else'):
            return True
        else:
            self.position = safe_point
        return True

    def stmt(self):
        safe_point = self.position
        self.update_error_point(safe_point)
        if self.check_token("if") and self.check_token("(") and self.expr() and self.check_token(
                ")") and self.stmt() and self.else_case() and self.stmt():
            return True
        else:
            self.position = safe_point
        if self.check_token("if") and self.check_token("(") and self.expr() and self.check_token(")") and self.check_token(
                "else") and self.stmt():
            return True
        else:
            self.position = safe_point
        if self.check_token("while") and self.check_token("(") and self.expr() and self.check_token(")") and self.stmt():
            return True
        else:
            self.position = safe_point
        if self.check_token("for") and self.check_token("(") and self.check_token(";") and self.check_token(";") and self.check_token(
                ")") and self.stmt():
            return True
        else:
            self.position = safe_point
        if self.check_token("for") and self.check_token("(") and self.assg() and self.check_token(";") and self.check_token(";") and self.check_token(
                ")") and self.stmt():
            return True
        else:
            self.position = safe_point
        if self.check_token("for") and self.check_token("(") and self.check_token(";") and self.expr() and self.check_token(";") and self.check_token(
                ")") and self.stmt():
            return True
        else:
            self.position = safe_point
        if self.check_token("for") and self.check_token("(") and self.check_token(";") and self.check_token(";") and self.assg() and self.check_token(
                ")") and self.stmt():
            return True
        else:
            self.position = safe_point
        if self.check_token("for") and self.check_token("(") and self.assg() and self.check_token(";") and self.expr() and self.check_token(
                ";") and self.check_token(")") and self.stmt():
            return True
        else:
            self.position = safe_point
        if self.check_token("for") and self.check_token("(") and self.assg() and self.check_token(";") and self.check_token(
                ";") and self.assg() and self.check_token(")") and self.stmt():
            return True
        else:
            self.position = safe_point
        if self.check_token("for") and self.check_token("(") and self.check_token(";") and self.expr() and self.check_token(
                ";") and self.assg() and self.check_token(")") and self.stmt():
            return True
        else:
            self.position = safe_point
        if self.check_token("for") and self.check_token("(") and self.assg() and self.check_token(";") and self.expr() and self.check_token(
                ";") and self.assg() and self.check_token(")") and self.stmt():
            return True
        else:
            self.position = safe_point
        if self.check_token("return") and self.check_token(";") and self.stmt():
            return True
        else:
            self.position = safe_point
        if self.check_token("return") and self.expr() and self.check_token(";") and self.stmt():
            return True
        else:
            self.position = safe_point
        if self.assg() and self.check_token(";") and self.stmt():
            return True
        else:
            self.position = safe_point
        if self.check_token("ID") and self.check_token("(") and self.check_token(")") and self.check_token(";") and self.stmt():
            return True
        else:
            self.position = safe_point
        if self.check_token("ID") and self.check_token("(") and self.expr() and self.stmt2() and self.check_token(")") and self.check_token(
                ";") and self.stmt():
            return True
        else:
            self.position = safe_point
        if self.check_token("{") and self.stmt() and self.check_token("}") and self.stmt():
            return True
        else:
            self.position = safe_point
        if self.check_token(";") and self.stmt():
            return True
        else:
            self.position = safe_point
        return True

    def stmt2(self):
        safe_point = self.position
        self.update_error_point(safe_point)
        if self.check_token(",") and self.expr() and self.stmt2():
            return True
        else:
            self.position = safe_point
        return True

    def assg(self):
        safe_point = self.position
        self.update_error_point(safe_point)
        if self.check_token("ID") and self.check_token("=") and self.expr():
            return True
        else:
            self.position = safe_point
        if self.check_token("ID") and self.check_token("[") and self.expr() and self.check_token("]") and self.check_token("=") and self.expr():
            return True
        else:
            self.position = safe_point
        return False

    def expr(self):
        safe_point = self.position
        self.update_error_point(safe_point)
        if self.check_token("-") and self.expr3():
            return True
        else:
            self.position = safe_point
        if self.check_token("!") and self.expr3():
            return True
        else:
            self.position = safe_point
        if self.check_token("ID") and self.expr3():
            return True
        else:
            self.position = safe_point
        if self.check_token("ID") and self.check_token("(") and self.check_token(")") and self.expr3():
            return True
        else:
            self.position = safe_point
        if self.check_token("ID") and self.check_token("(") and self.expr() and self.check_token(")") and self.expr3():
            return True
        else:
            self.position = safe_point
        if self.check_token("ID") and self.check_token("(") and self.expr() and self.expr2() and self.check_token(")") and self.expr3():
            return True
        else:
            self.position = safe_point
        if self.check_token("ID") and self.check_token("[") and self.expr() and self.check_token("]") and self.expr3():
            return True
        else:
            self.position = safe_point
        if self.check_token("(") and self.expr() and self.check_token(")") and self.expr3():
            return True
        else:
            self.position = safe_point
        if self.check_token("INTCON") and self.expr3():
            return True
        else:
            self.position = safe_point
        if self.check_token("CHAR") and self.expr3():
            return True
        else:
            self.position = safe_point
        if self.check_token("STRINGCON") and self.expr3():
            return True
        else:
            self.position = safe_point
        return False

    def expr2(self):
        safe_point = self.position
        self.update_error_point(safe_point)
        if self.check_token(",") and self.expr() and self.expr3():
            return True
        else:
            self.position = safe_point
        return True

    def expr3(self):
        safe_point = self.position
        self.update_error_point(safe_point)
        if self.binop() and self.expr() and self.expr3():
            return True
        else:
            self.position = safe_point
        if self.relop() and self.expr() and self.expr3():
            return True
        else:
            self.position = safe_point
        if self.logical_op() and self.expr() and self.expr3():
            return True
        else:
            self.position = safe_point
            return True

    def binop(self):
        safe_point = self.position
        self.update_error_point(safe_point)
        if self.check_token("+") or self.check_token("-") or self.check_token("*") or self.check_token("/") or self.check_token("%"):
            return True
        else:
            self.position = safe_point
        return False

    def relop(self):
        safe_point = self.position
        self.update_error_point(safe_point)
        if self.check_token("<") or self.check_token(">") or self.check_token("<=") or self.check_token(">=") or self.check_token("==") or self.check_token(
                "!="):
            return True
        else:
            self.position = safe_point
        return False

    def logical_op(self):
        safe_point = self.position
        self.update_error_point(safe_point)
        if self.check_token("&&") or self.check_token("||"):
            return True
        else:
            self.position = safe_point
        return False

    def prog(self):
        safe_point = self.position
        self.update_error_point(safe_point)
        if self.dcl() and self.check_token(';'):
            return True, self.derivation_tree
        else:
            self.position = safe_point
        if self.func():
            return True, self.derivation_tree
        else:
            self.position = safe_point
        return False, None

