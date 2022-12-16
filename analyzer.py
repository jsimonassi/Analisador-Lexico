from constants import STATES, TYPE_BY_OPERATORS, ALL_ELEMENTS, BIN_OPS
import re
import utils


class Analyzer:

    def __init__(self):
        self.is_look_ahead = 0
        self.line = 0
        self.column = 0
        self.state = STATES.INITIAL
        self.response_token = []
        self.token = ""
        self.numeric_token = ""
        self.acc = ""
        self.cursor = ""
        self.line_iterator = ""

    #Utils
    def append_identifier(self, token):
        type = TYPE_BY_OPERATORS.get(token)
        if type is not None:
            self.response_token.append([type, token, self.line])
        elif re.match(r"[\d]", token):
            self.response_token.append(["INTCON", token, self.line])
        elif re.match(r"[\"]+[%\w\s]+[\"]*", token):
            self.response_token.append(["STRINGCON", token, self.line])
        else:
            self.response_token.append(["ID", token, self.line])

    def append_identifier_look_ahead(self, token):
        """Identificação de tokens com caracters ambiguos"""
        if re.match(r"[\=]", token) and self.line_iterator[self.column] == "=":
            self.is_look_ahead = 1
            self.append_identifier("==")
            self.cursor = self.line_iterator[self.column]

        elif re.match(r"[\<]", token) and self.line_iterator[self.column] == "=":
            self.is_look_ahead = 1
            self.append_identifier("<=")
            self.cursor = self.line_iterator[self.column]

        elif re.match(r"[\>]", token) and self.line_iterator[self.column] == "=":
            self.is_look_ahead = 1
            self.append_identifier(">=")
            self.cursor = self.line_iterator[self.column]

        elif re.match(r"[\&]", token) and self.line_iterator[self.column] == "&":
            self.is_look_ahead = 1
            self.append_identifier("&&")
            self.cursor = self.line_iterator[self.column]

        elif re.match(r"[\|]", token) and self.line_iterator[self.column] == "|":
            self.is_look_ahead = 1
            self.append_identifier("||")
            self.cursor = self.line_iterator[self.column]

        elif re.match(r"[\!]", token) and self.line_iterator[self.column] == "=":
            self.is_look_ahead = 1
            self.append_identifier("!=")
            self.cursor = self.line_iterator[self.column]

        else:
            self.append_identifier(token)

    def append_error(self, token):
        """Adiciona o erro na lista de tokens"""
        if token != "\n" and token != " ":
            self.response_token.append(["UNKNOWN_TOKEN", token, self.line])

    #State Methods
    def run_state_comment(self):
        """Acumula o token até encontrar o fim do comentário"""
        self.acc = self.acc + self.cursor
        if re.search(r"(\*\/)", self.acc):
            self.state = STATES.INITIAL
            self.append_identifier("*/")

    def run_state_identifier(self):
        """Identifica qualquer caracter do tipo texto ou número"""
        if re.match(r"([\w])", self.cursor):
            self.token = self.token + self.cursor
        if utils.is_special_caracter(self.cursor): # No cursor! Marca o término do token
            self.state = STATES.INITIAL
            if utils.is_reserved_word(self.token):
                self.append_identifier(self.token)
                if self.cursor != " ":
                    if not utils.is_error(self.token):
                        self.append_identifier_look_ahead(self.cursor)
                    else:
                        self.append_error(self.token)
                self.token = ""
            else:
                self.append_identifier(self.token)
                if utils.is_special_caracter(self.cursor):
                    if self.cursor != re.match(r"\s", self.cursor):
                        if not utils.is_error(self.cursor):
                            self.append_identifier_look_ahead(self.cursor)
                        else:
                            if self.cursor == "!" and self.line_iterator[self.column] == "=":
                                self.append_identifier_look_ahead(self.cursor)
                            else:
                                self.append_error(self.cursor)
                    self.state = STATES.INITIAL
                self.token = ""

    def run_state_literal(self):
        """Identifica qualquer caracter do tipo texto ou número"""
        if re.match(r"[%a-zA-z0-9\"\s]", self.cursor):
            self.token = self.token + self.cursor
        """Verifica se token começa com aspas duplas"""
        if re.match(r"[\"]", self.cursor):
            """Verifica se token está entre aspas"""
            lit = re.match(r"[\"]+[%\w\s]+[\"]*", self.token)
            if lit is not None:
                self.append_identifier(lit.group())
                self.token = ""
                self.state = STATES.INITIAL

    def run_state_numeric(self):
        """Identifica qualquer caracter do tipo texto ou número"""
        if re.match(r"[.\w]", self.cursor):
            self.numeric_token = self.numeric_token + self.cursor

        if utils.is_number(self.cursor):
            """Verifica se o token só tem números"""
            if re.match(r"(^[0-9]*$)", self.numeric_token):
                if re.match(r"(^[0-9]*$)", self.numeric_token) is not None:
                    self.append_identifier(self.numeric_token)
                    if self.cursor != " ":
                        if not utils.is_error(self.cursor):
                            self.append_identifier_look_ahead(self.cursor)
                        else:
                            self.append_error(self.cursor)
                    self.state = STATES.INITIAL
                    self.numeric_token = ""
            else:
                """Identifica o token inválido"""
                if self.cursor in ALL_ELEMENTS or re.match(r"\s|\n", self.cursor) or self.cursor in BIN_OPS:
                    self.append_error(self.cursor)
                    self.numeric_token = ""
                    self.state = STATES.INITIAL
