import os
import sys
from JackTokenizer import Tokenizer
from CompilationEngine import Parser
from SymbolTable import SymbolTableClass

"""
Terminal Commands: diff -w LincolnBennettProject10/10/ArrayTest/Main.xmla LincolnBennettProject10/10/ArrayTest/Main.xml
python LincolnBennettProject10/ex10/JackAnalyzer.py LincolnBennettProject10/10/Arraytest/Main.jack
"""

def main():
    # filepath is either single .jack file or directory, containing multiple .jack file
    file_path = sys.argv[1]
    # if single .jack file
    if os.path.isfile(file_path):
        # gives us immediate parent folder
        folder = os.path.dirname(file_path)
        # gives us just the file name
        filename = os.path.basename(file_path)
        filename = os.path.splitext(filename)[0]
        # removes extension
        file = os.path.splitext(file_path)[0]
        # we are inputing a .jack file, then writing to a file with the same name, but ".xml" extension
        tokens = Tokenizer(file + ".jack", folder + "/output/" + filename + "T.xml")
        # Now we run the Parser, (the book calls it CompilationEngine)
        parsed = Parser(tokens.tokens, folder + "/output/" + filename + ".xml")
        parsed.compileClass()
        
    # Otherwise we assume we got a directory
    else:
        # silly, but add a '/' if we didn't get one in the input
        if file_path[-1] != '/':
            file_path += '/'
        
        # list all the jack files in the directory
        all_files = os.listdir(file_path)
        all_jack_files = [os.path.splitext(file)[0] for file in all_files if os.path.splitext(file)[1] == ".jack"]
        # remove the jack extension
        for file in all_jack_files:
            tokens = Tokenizer(file_path + file + ".jack", file_path + "output/" + file + "T.xml")
            parsed = Parser(tokens.tokens, file_path + "/output/" + file + ".xml")
            parsed.compileClass()
            symbolTabled = SymbolTableClass(parsed.xml_output)
            print(symbolTabled.xml_input)
    return

if __name__ == "__main__":
    main()