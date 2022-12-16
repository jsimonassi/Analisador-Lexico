from scanner import *
from analyzer import Analyzer
from parser import Parser

if __name__ == '__main__':
    analyzer = Analyzer()
    filtered_list = get_token_list(analyzer, "case_correct.c--", True)

    Parser(filtered_list).start_parser()
