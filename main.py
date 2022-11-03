from data.constants import STATES
import re
import data.utils
from analyzer import Analyzer

line = 0
column = 0


def open_file():
    try:
        # return open("inputs/full_example.c", "r")
        # return open("inputs/full_example.c", "r")
        return open("inputs/error_example.c", "r")
    except Exception as e:
        print("Erro ao abrir o arquivo", e)
        exit(1)


input_file = open_file()
if __name__ == '__main__':

    lex_analyzer = Analyzer()

    for line_iterator in input_file:
        line = line + 1
        column = 0
        for cursor in line_iterator:
            column = column + 1

            if lex_analyzer.state == STATES.INITIAL:  # OK
                if cursor == "/" and line_iterator[column] == "*" and lex_analyzer.state == STATES.INITIAL and lex_analyzer.state != STATES.COMMENT:
                    lex_analyzer.state = STATES.COMMENT
                    lex_analyzer.append_token("/*")

                if re.search(r"^(#)", line_iterator) and lex_analyzer.state == STATES.INITIAL and lex_analyzer.state != STATES.COMMENT:
                    break

                if re.search(r"([A-Za-z_])", cursor) and lex_analyzer.state == STATES.INITIAL and lex_analyzer.state != STATES.COMMENT:
                    lex_analyzer.state = STATES.IDENTIFIER

                if re.match(r"[0-9]", cursor) and lex_analyzer.state == STATES.INITIAL and lex_analyzer.state != STATES.COMMENT:
                    lex_analyzer.state = STATES.NUMERIC  # Constante Numérica
                if re.match(r"[\"]", cursor) and lex_analyzer.state == STATES.INITIAL and lex_analyzer.state != STATES.COMMENT:
                    lex_analyzer.state = STATES.LITERAL
                if utils.is_number(cursor) and utils.is_special_caracter(cursor) and lex_analyzer.state == STATES.INITIAL and lex_analyzer.state != STATES.COMMENT:
                    if not utils.is_error(cursor):
                        lex_analyzer.append_token(cursor)
                    else:
                        lex_analyzer.append_error(cursor)

            if lex_analyzer.state == STATES.COMMENT:
                lex_analyzer.check_comment(cursor)

            if lex_analyzer.state == STATES.IDENTIFIER:
                lex_analyzer.check_identifier(cursor)

            if lex_analyzer.state == STATES.LITERAL:
                lex_analyzer.check_literal(cursor)

            if lex_analyzer.state == STATES.NUMERIC:
                lex_analyzer.check_numeric(cursor)

    print(lex_analyzer.response_token)
