from scanner import *
from analyzer import Analyzer
from parser import Parser

if __name__ == '__main__':
    analyzer = Analyzer()
    token_list = get_token_list(analyzer, "case_incorrect_3.c--")

    print("Received tokens: " + str(token_list))

    filtered_list = token_list.copy()
    for item in token_list:
        if item[0] == "UNKNOWN_TOKEN":
            print("Unknown token: " + item[1] + " at line " + str(item[2]))
            exit(1)

        if item[0] == "OPEN_COMMENT" or item[0] == "CLOSE_COMMENT":
            filtered_list.remove(item)

    print("Filtered tokens: " + str(filtered_list))
    parser = Parser(filtered_list)
    parser.start_parser()
