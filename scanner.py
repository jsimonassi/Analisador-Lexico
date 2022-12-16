from constants import STATES
import re
import utils


def open_file(filepath):
    """Abre o arquivo de entrada"""
    try:
        return open(filepath, "r")
    except Exception as e:
        print("Erro ao abrir o arquivo: " + str(e))
        exit(1)


def filter_token_list(token_list, verbose=False):
    """Verifica se existem tokens desconhecidos e filtra tokens de comentários"""
    filtered_list = token_list.copy()
    for item in token_list:
        if item[0] == "UNKNOWN_TOKEN":
            print("ERRO LÉXICO: O token '" + item[1] + "' na linha: " + str(item[2]) + " não foi reconhecido")
            exit(1)

        if item[0] == "OPEN_COMMENT" or item[0] == "CLOSE_COMMENT":
            filtered_list.remove(item)

    if verbose:
        print("Tokens lidos: " + str(token_list))
        print("Tokens filtrados: " + str(filtered_list))

    return filtered_list


def get_token_list(analyzer, filepath, verbose=False):
    """Percorre o arquivo obtendo tokens de entrada"""
    lex_analyzer = analyzer
    input_file = open_file(filepath)
    for line_iterator in input_file:
        lex_analyzer.line += 1
        lex_analyzer.column = 0
        lex_analyzer.line_iterator = line_iterator

        for cursor in line_iterator:
            lex_analyzer.column += 1
            lex_analyzer.cursor = cursor

            if lex_analyzer.is_look_ahead == 1:
                lex_analyzer.is_look_ahead = 0
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
                # Verifica se é um uma palavra do tipo char. Identifica aspas (Início ou término de um literal)
                if re.match(r"[\"]", lex_analyzer.cursor) and lex_analyzer.state == STATES.INITIAL and \
                        lex_analyzer.state != STATES.COMMENT:
                    lex_analyzer.state = STATES.LITERAL

                if utils.is_number(lex_analyzer.cursor) and utils.is_special_caracter(
                        lex_analyzer.cursor) and lex_analyzer.state == STATES.INITIAL and lex_analyzer.state != STATES.COMMENT:

                    if not utils.is_error(lex_analyzer.cursor):
                        lex_analyzer.append_identifier_look_ahead(lex_analyzer.cursor)
                        if lex_analyzer.is_look_ahead == 1:
                            continue
                    else:
                        if lex_analyzer.cursor == '&' and lex_analyzer.line_iterator[lex_analyzer.column] == "&":
                            lex_analyzer.append_identifier_look_ahead(lex_analyzer.cursor)

                        elif lex_analyzer.cursor == '|' and lex_analyzer.line_iterator[lex_analyzer.column] == "|":
                            lex_analyzer.append_identifier_look_ahead(lex_analyzer.cursor)

                        elif lex_analyzer.cursor == "!" and lex_analyzer.line_iterator[lex_analyzer.column] == "=":
                            lex_analyzer.append_identifier_look_ahead(lex_analyzer.cursor)

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

    return filter_token_list(lex_analyzer.response_token, verbose)
