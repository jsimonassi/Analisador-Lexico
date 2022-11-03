from data.constants import STATES, ALL_ELEMENTS, BIN_OPS, TYPE_BY_OPERATORS
import re
from data import utils


class Analyzer:

    def __init__(self):
        self.line = 0
        self.column = 0
        self.state = STATES.INITIAL
        self.response_token = []
        self.token = ""
        self.numeric_token = ""
        self.acumula = ""

    def append_error(self, token):
        """Adiciona o erro na lista de tokens"""
        if token != "\n" and token != " ":
            self.response_token.append(["Token não reconhecido", token])

    def append_token(self, token):
        type = TYPE_BY_OPERATORS.get(token)
        if type is not None:
            self.response_token.append([type, token])
        elif re.match(r"[\d]", token):
            self.response_token.append(["NUMBER", token])
        else:
            self.response_token.append(["ID", token])

    def check_comment(self, cursor):
        self.acumula = self.acumula + cursor
        if re.search(r"(\*\/)", self.acumula):
            self.state = STATES.INITIAL
            self.append_token("*/")

    def check_identifier(self, cursor):
        if re.match(r"([\w])", cursor):
            self.token = self.token + cursor
        if utils.is_special_caracter(cursor):
            self.state = STATES.INITIAL

            if utils.is_reserved_word(self.token):
                self.append_token(self.token)
                if cursor != " ":
                    if not utils.is_error(self.token):
                        self.append_token(self.token)
                    else:
                        self.append_error(self.token)
                self.token = ""
            else:
                self.append_token(self.token)
                if utils.is_special_caracter(cursor):
                    """Vai inserir o k como separador """
                    if cursor != re.match(r"\s", cursor):
                        if not utils.is_error(cursor):
                            self.append_token(cursor)
                        else:
                            self.append_error(cursor)
                    self.state = STATES.INITIAL
                self.token = ""

    def check_literal(self, cursor):
        if re.match(r"[%a-zA-z0-9\"\s]", cursor):
            self.token = self.token + cursor
        if re.match(r"[\"]", cursor):
            lit = re.match(r"[\"]+[%\w\s]+[\"]*", self.token)
            if lit is not None:
                self.append_token(lit.group())
                self.token = ""
                self.state = STATES.INITIAL

    def check_numeric(self, cursor):
        if re.match(r"[\w.]", cursor):
            self.numeric_token = self.numeric_token + cursor
        if utils.is_number(cursor):
            if re.match(r"(^[0-9]*$)", self.numeric_token):
                if re.match(r"(^[0-9]*$)", self.numeric_token) is not None:
                    self.append_token(self.numeric_token)
                    if cursor != " ":
                        if not utils.is_error(cursor):
                            self.append_token(cursor)
                        else:
                            self.append_error(cursor)
                    self.state = STATES.INITIAL
                    self.numeric_token = ""
            else:
                if cursor in ALL_ELEMENTS or re.match(r"\s|\n", cursor) or cursor in BIN_OPS:
                    """Identifica o token inválido"""
                    self.append_error(cursor)
                    self.numeric_token = ""
                    self.state = STATES.INITIAL
        else:
            if utils.is_number(cursor):
                "Armazena token de separadores"
                if cursor != " ":
                    if not utils.is_error(cursor):
                        self.append_token(cursor)
                    else:
                        self.append_error(cursor)
                self.state = STATES.INITIAL
