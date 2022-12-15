from constants import STATES
import re
import utils


def open_file(filename):
    """Abre o arquivo de entrada"""
    try:
        return open("inputs/" + filename , "r")
    except Exception as e:
        print("Erro ao abrir o arquivo: " + str(e))
        exit(1)


def get_token_list(analyzer, filename):
    lex_analyzer = analyzer
    input_file = open_file(filename)
    for line_iterator in input_file:
        lex_analyzer.line += 1
        lex_analyzer.column = 0
        lex_analyzer.line_iterator = line_iterator

        for cursor in line_iterator:
            lex_analyzer.column += 1
            lex_analyzer.cursor = cursor

            if lex_analyzer.flag == 1:
                lex_analyzer.flag = 0
                continue

            if lex_analyzer.state == STATES.INITIAL:
                # Verifica se o é o inicio de um comentário
                if lex_analyzer.cursor == "/" and lex_analyzer.line_iterator[lex_analyzer.column] == "*" and \
                        lex_analyzer.state == STATES.INITIAL and lex_analyzer.state != STATES.COMMENT:
                    lex_analyzer.state = STATES.COMMENT
                    lex_analyzer.append_identifier("/*")
                # Verifica se é alguma importação
                if re.search(r"^(#)", lex_analyzer.line_iterator) and lex_analyzer.state == STATES.INITIAL and \
                        lex_analyzer.state != STATES.COMMENT:
                    break
                # Verifica se é um identificador (int, char ou variaveis)
                if re.search(r"([A-Za-z_])", lex_analyzer.cursor) and lex_analyzer.state == STATES.INITIAL and \
                        lex_analyzer.state != STATES.COMMENT:
                    lex_analyzer.state = STATES.IDENTIFIER
                # Verifica se é um número
                if re.match(r"[0-9]", lex_analyzer.cursor) and lex_analyzer.state == STATES.INITIAL and \
                        lex_analyzer.state != STATES.COMMENT:
                    lex_analyzer.state = STATES.NUMERIC
                # Verifica se é um uma palavra do tipo char por exemplo
                if re.match(r"[\"]", lex_analyzer.cursor) and lex_analyzer.state == STATES.INITIAL and \
                        lex_analyzer.state != STATES.COMMENT:
                    lex_analyzer.state = STATES.LITERAL

                if utils.is_number(lex_analyzer.cursor) and utils.is_special_caracter(
                        lex_analyzer.cursor) and lex_analyzer.state == STATES.INITIAL and lex_analyzer.state != STATES.COMMENT:

                    if not utils.is_error(lex_analyzer.cursor):

                        lex_analyzer.append_identifier_double(lex_analyzer.cursor)
                        if lex_analyzer.flag == 1:
                            continue

                    else:

                        if lex_analyzer.cursor == '&' and lex_analyzer.line_iterator[lex_analyzer.column] == "&":
                            lex_analyzer.append_identifier_double(lex_analyzer.cursor)

                        elif lex_analyzer.cursor == '|' and lex_analyzer.line_iterator[lex_analyzer.column] == "|":
                            lex_analyzer.append_identifier_double(lex_analyzer.cursor)

                        elif lex_analyzer.cursor == "!" and lex_analyzer.line_iterator[lex_analyzer.column] == "=":
                            lex_analyzer.append_identifier_double(lex_analyzer.cursor)

                        else:
                            lex_analyzer.append_error(lex_analyzer.cursor)

            if lex_analyzer.state == STATES.COMMENT:
                lex_analyzer.run_state_comment()

            if lex_analyzer.state == STATES.IDENTIFIER:
                lex_analyzer.run_state_identifier()

            if lex_analyzer.state == STATES.LITERAL:
                lex_analyzer.run_state_literal()

            if lex_analyzer.state == STATES.NUMERIC:
                lex_analyzer.run_state_numeric()

    return lex_analyzer.response_token
