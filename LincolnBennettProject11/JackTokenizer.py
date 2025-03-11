import re
import os

class Tokenizer:
    keywords = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let', 'do', 'if', 'else', 'while', 'return']
    

    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        # convert the jack file to a string
        self.input_string = open(input_path).read()
        # need to strip the comments on the input string
        self.remove_comments()
        self.tokenize()
        self.write_tokens(output_path)
        # print(self.input_string)
        # print(f"Length of this is: {len(self.input_string)}")
        # print(f"type of self.input_string is : {type(self.input_string)}")

        return
    
    def remove_comments(self):
        # Remove single-line comments using regular expression
        self.input_string = re.sub(r'//.*', '', self.input_string)
        # Remove multi-line comments using regular expression
        # the flags=re.DOTALL allows us to span multiple lines (used this comment: https://stackoverflow.com/questions/32018434/python-re-sub-newline-multiline-dotall)
        self.input_string = re.sub(r'/\*.*?\*/', '', self.input_string, flags=re.DOTALL)
        # remove leading and trailing whitespace
        self.input_string = self.input_string.strip()
        return
    
    def tokenize(self):
        symbols = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']
        self.tokens = []
        # loop through all characters in the string
        i = 0
        while i < len(self.input_string):
            # if character is a space, we continue
            if self.input_string[i].isspace():
                i += 1
                continue
            # if character is in symbols, we add it to list of self.tokens
            if self.input_string[i] in symbols:
                # SPECIAL CASE, < > &
                if self.input_string[i] == '<':
                    self.tokens.append(("symbol", "&lt;"))
                    i += 1
                    continue
                elif self.input_string[i] == '>':
                    self.tokens.append(("symbol", "&gt;"))
                    i += 1
                    continue
                if self.input_string[i] == '&':
                    self.tokens.append(("symbol", "&amp;"))
                    i += 1
                    continue
                # OTHERWISE WE JUST ADD TO TUPLE OF SYMBOLS
                self.tokens.append(("symbol", self.input_string[i]))
                i += 1
                continue
            # integerConstant
            # if it is a digit, then we add until we reach non-digit
            if self.input_string[i].isdigit():
                num = ''
                # add all digits
                while i < len(self.input_string) and self.input_string[i].isdigit():
                    num += self.input_string[i]
                    i += 1
                self.tokens.append(("integerConstant", num))
                continue
            if self.input_string[i] == '"':
                string_const = ''
                i += 1  # Skip the opening quote
                while i < len(self.input_string) and self.input_string[i] != '"':
                    string_const += self.input_string[i]
                    i += 1
                i += 1  # Skip the closing quote
                self.tokens.append(("stringConstant", string_const))
                continue

            # so we now know that it must be an identifier, if none of the other if statements hit
            identifier = ''
            while i < len(self.input_string) and (self.input_string[i].isalnum() or self.input_string[i] == '_'):
                identifier += self.input_string[i]
                i += 1
            if identifier in self.keywords:
                self.tokens.append(("keyword", identifier))
            else:
                self.tokens.append(("identifier", identifier))
        return
    
    def write_tokens(self, output_path):
        # First time we write to the output directory, we have to create it.
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(output_path, "w") as file:
            file.write("<tokens>\n")
            # loop through tokens and write to XML
            for token_tuple in self.tokens:
                token_type = token_tuple[0]
                token = token_tuple[1]
                line = f"<{token_type}> {token} </{token_type}>\n"
                file.write(line)
            file.write("</tokens>\n")

        return
    