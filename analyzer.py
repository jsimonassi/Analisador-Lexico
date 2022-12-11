from constants import STATES, TYPE_BY_OPERATORS, ALL_ELEMENTS, BIN_OPS
import re
import utils


class Analyzer:

    def __init__(self):
        self.flag = 0
        self.line = 0
        self.column = 0
        self.state = STATES.INITIAL
        self.response_token = []
        self.token = ""
        self.numeric_token = ""
        self.acc = ""
        self.cursor = ""
        self.line_iterator = ""

    def append_identifier(self, token):
        type = TYPE_BY_OPERATORS.get(token)
        if type is not None:
            self.response_token.append([type, token, self.line])
        elif re.match(r"[\d]", token):
            self.response_token.append(["NUMBER", token, self.line])
        else:
            self.response_token.append(["ID", token, self.line])

    def append_identifier_double(self, token):
        if re.match(r"[\=]", token) and self.line_iterator[self.column] == "=":

            self.flag = 1
            self.append_identifier("==")
            self.cursor = self.line_iterator[self.column]

        elif re.match(r"[\<]", token) and self.line_iterator[self.column] == "=":
            self.flag = 1
            self.append_identifier("<=")
            self.cursor = self.line_iterator[self.column]

        elif re.match(r"[\>]", self.token) and self.line_iterator[self.column] == "=":
            self.flag = 1
            self.append_identifier(">=")
            self.cursor = self.line_iterator[self.column]

        elif re.match(r"[\&]", token) and self.line_iterator[self.column] == "&":
            self.flag = 1
            self.append_identifier("&&")
            self.cursor = self.line_iterator[self.column]

        elif re.match(r"[\|]", token) and self.line_iterator[self.column] == "|":
            self.flag = 1
            self.append_identifier("||")
            self.cursor = self.line_iterator[self.column]

        elif re.match(r"[\!]", token) and self.line_iterator[self.column] == "=":
            self.flag = 1
            self.append_identifier("!=")
            self.cursor = self.line_iterator[self.column]

        else:
            self.append_identifier(token)

    def append_error(self, token):
        """Adiciona o erro na lista de tokens"""
        if token != "\n" and token != " ":
            self.response_token.append(["Token não reconhecido", token, self.line])

    """State Methods"""
    def run_state_comment(self):
        self.acc = self.acc + self.cursor
        if re.search(r"(\*\/)", self.acc):
            self.state = STATES.INITIAL
            self.append_identifier("*/")

    def run_state_identifier(self):
        if re.match(r"([\w])", self.cursor):
            self.token = self.token + self.cursor
        if utils.is_special_caracter(self.cursor):
            self.state = STATES.INITIAL
            if utils.is_reserved_word(self.token):
                self.append_identifier(self.token)
                if self.cursor != " ":
                    if not utils.is_error(self.token):
                        self.append_identifier_double(self.cursor)
                    else:
                        self.append_error(self.token)
                self.token = ""
            else:
                self.append_identifier(self.token)
                if utils.is_special_caracter(self.cursor):
                    """Vai inserir o k como separador """
                    if self.cursor != re.match(r"\s", self.cursor):
                        if not utils.is_error(self.cursor):
                            self.append_identifier_double(self.cursor)
                        else:
                            if self.cursor == "!" and self.line_iterator[self.column] == "=":
                                self.append_identifier_double(self.cursor)
                            else:
                                self.append_error(self.cursor)
                    self.state = STATES.INITIAL
                self.token = ""

    def run_state_literal(self):
        if re.match(r"[%a-zA-z0-9\"\s]", self.cursor):
            self.token = self.token + self.cursor
        if re.match(r"[\"]", self.cursor):
            lit = re.match(r"[\"]+[%\w\s]+[\"]*", self.token)
            if lit is not None:
                self.append_identifier(lit.group())
                self.token = ""
                self.state = STATES.INITIAL

    def run_state_numeric(self):
        if re.match(r"[\w.]", self.cursor):
            self.numeric_token = self.numeric_token + self.cursor
        if utils.is_number(self.cursor):
            if re.match(r"(^[0-9]*$)", self.numeric_token):
                if re.match(r"(^[0-9]*$)", self.numeric_token) is not None:
                    self.append_identifier(self.numeric_token)
                    if self.cursor != " ":
                        if not utils.is_error(self.cursor):
                            self.append_identifier_double(self.cursor)
                        else:
                            self.append_error(self.cursor)
                    self.state = STATES.INITIAL
                    self.numeric_token = ""
            else:
                if self.cursor in ALL_ELEMENTS or re.match(r"\s|\n", self.cursor) or self.cursor in BIN_OPS:
                    """Identifica o token inválido"""
                    self.append_error(self.cursor)
                    self.numeric_token = ""
                    self.state = STATES.INITIAL
        else:
            if utils.is_number(self.cursor):
                "Armazena token de separadores"
                if self.cursor != " ":
                    if not utils.is_error(self.cursor):
                        self.append_identifier_double(self.cursor)
                    else:
                        self.append_error(self.cursor)
                self.state = STATES.INITIAL

