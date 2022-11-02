import re
import constants


def is_special_caracter(caracter):
    return not re.match(r"[\w]", caracter)


def is_reserved_word(word):
    return word in constants.RESERVED_WORDS


def is_number(token):
    return re.match(r"[\d.]", token)


def is_error(token):
    if not re.match(r"[\w]", token):
        if token not in constants.ALL_ELEMENTS:
            if not re.search(r"\s", token):
                return True
    return False
