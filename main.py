from scanner import *
from analyzer import Analyzer
from parser import Parser
import os


def menu():
    base_path = "./inputs"
    paths = [os.path.join(base_path, filename) for filename in os.listdir(base_path)]
    files = [arq for arq in paths if os.path.isfile(arq)]
    filtered_file_list = [arq for arq in files if arq.lower().endswith(".c--")]

    for filepath in filtered_file_list:
        print(filepath + " - " + str(filtered_file_list.index(filepath)))

    print("\nEscolha um arquivo para compilar: ")

    op = int(input())

    if 0 <= op < len(filtered_file_list):
        filepath = filtered_file_list[op]
        print("Compilando arquivo: " + filepath)
        compile(filepath)
    else:
        print("Opção inválida!")


def compile(filepath):
    analyzer = Analyzer()
    filtered_list = get_token_list(analyzer, filepath, True)

    Parser(filtered_list).start_parser()


if __name__ == '__main__':
    menu()
