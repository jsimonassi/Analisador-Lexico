from constants import STATES, ALL_ELEMENTS, BIN_OPS
import re
import utils

line = 0
column = 0
state = STATES.INITIAL
response_token = []
token = ""
numeric_token = ""


def open_file():
    """Abre o arquivo de entrada"""
    try:
        return open("teste.c", "r")
    except Exception as e:
        print("Erro ao abrir o arquivo")
        exit(1)


input_file = open_file()
if __name__ == '__main__':

    for line_iterator in input_file:
        line = line + 1
        column = 0
        for cursor in line_iterator:
            column = column + 1


            if state == STATES.INITIAL: #OK
                if cursor == "/" and line_iterator[column] == "*" and state == STATES.INITIAL and state != STATES.COMMENT:
                    state = STATES.COMMENT
                    response_token.append(["/*"])

                if re.search(r"^(#)", line_iterator) and state == STATES.INITIAL and state != STATES.COMMENT:
                    break

                if re.search(r"([A-Za-z_])", cursor) and state == STATES.INITIAL and state != STATES.COMMENT:
                    state = STATES.IDENTIFIER

                if re.match(r"[0-9]", cursor) and state == STATES.INITIAL and state != STATES.COMMENT:
                    state = STATES.NUMERIC  # Constante Numérica
                if re.match(r"[\"]", cursor) and state == STATES.INITIAL and state != STATES.COMMENT:
                    state = STATES.LITERAL
                if utils.is_number(cursor) and utils.is_special_caracter(cursor) and state == STATES.INITIAL and state != STATES.COMMENT:
                    if not utils.is_error(cursor):
                        response_token.append([cursor])
                    else:
                        response_token.append(["Token não reconhecido", cursor])



            if state == STATES.COMMENT: #OK
                # TODO: Validar se comentário não ficou com / pendente
                if cursor == "*" and line_iterator[column] == "/":
                    state = STATES.INITIAL
                    response_token.append(["*/"])



            if state == STATES.IDENTIFIER:
                if re.match(r"([\w])", cursor):
                    token = token + cursor
                if utils.is_special_caracter(cursor):
                    state = STATES.INITIAL

                    if utils.is_reserved_word(token):
                        response_token.append([token])
                        if cursor != " ":
                            if not utils.is_error(token):
                                response_token.append([token])
                            else:
                                response_token.append(["Token não reconhecido", token])
                        token = ""
                    else:
                        response_token.append(["ID", token])
                        if utils.is_special_caracter(cursor):
                            """Vai inserir o k como separador """
                            if cursor != re.match(r"\s", cursor):
                                if not utils.is_error(cursor):
                                    response_token.append([cursor])
                                else:
                                    response_token.append(["Token não reconhecido", cursor])
                            state = STATES.INITIAL
                        token = ""

            if state == STATES.LITERAL: #OK
                if re.match(r"[%a-zA-z0-9\"\s]", cursor):
                    token = token + cursor
                if re.match(r"[\"]", cursor):
                    lit = re.match(r"[\"]+[%\w\s]+[\"]*", token)
                    if lit is not None:
                        response_token.append(["Literal", lit.group()])
                        token = ""
                        state = STATES.INITIAL



            if state == STATES.NUMERIC: #OK
                if re.match(r"[\w.]", cursor):
                    numeric_token = numeric_token + cursor
                if utils.is_number(cursor):
                    if re.match(r"([0-9]+)", numeric_token):
                        if re.match(r"([0-9]+)", numeric_token) is not None:
                            response_token.append(["NUM", numeric_token])
                            if cursor != " ":
                                if not utils.is_error(cursor):
                                    response_token.append([cursor])
                                else:
                                    response_token.append(["Token não reconhecido", cursor])
                            state = STATES.INITIAL
                            numeric_token = ""
                    else:
                        if cursor in ALL_ELEMENTS or re.match(r"\s|\n", cursor) or cursor in BIN_OPS:
                            """Identifica o token inválido"""
                            response_token.append(["Token não reconhecido", cursor])
                            numeric_token = ""
                            state = STATES.INITIAL
                else:
                    if utils.is_number(cursor):
                        "Armazena token de separadores"
                        if cursor != " ":
                            if not utils.is_error(cursor):
                                response_token.append([cursor])
                            else:
                                response_token.append(["Token não reconhecido", cursor])
                        state = STATES.INITIAL




    print(response_token)