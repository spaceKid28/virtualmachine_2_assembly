class Parser:
    
    binaryOp = {'+', '-', '*', '/', '|', '=', '&lt;', '&gt;', '&amp;'}
    unaryOp = {'-', '~'}
    keywordConstant = {'true', 'false', 'null', 'this'}
    
    def __init__(self, tokens, output_filepath):
        self.tokens = tokens
        self.index = 0
        self.num_tokens = len(tokens)
        # keeping track of all the rules we are currently parsing
        self.nonterminal_tails = []
        self.output_filepath = output_filepath
        # this is what we are eventually writing to
        self.xml_output = ""
    
    # we run this method first, everytime
    def compileClass(self):
        self.nonterminal('class')
        self.writeToken() # note, this will be the class keyword
        self.writeToken() # note, this will be the class name (for example: main)
        self.writeToken() # note, this will always be {

        
        # Now we check for a classVarDec*
        # here we want to *peek* and see if it is either "static" or "field" without moving the index
        while self.peek() == "static" or self.peek() == "field":
            self.compileClassVarDec()
        # Now we check for a classVarDec*
        # here we want to *peek* and see if it is either "constructor, method, function" without moving the index
        while self.peek() == "constructor" or self.peek() == "function" or self.peek() == "method":
            self.compileSubroutine()
        self.writeToken()

        # gotta close <varDer> tag here we end nonterminal by popping of our list of nonterminal tags
        self.xml_output += self.nonterminal_tails.pop()

        # write the output
        # self.write_output()

    def writeToken(self): # note that this method both increments to the next token (via self.index) and returns the token
        tag, token = self.tokens[self.index]
        self.xml_output += f"<{tag}> {token} </{tag}>\n"
        self.index += 1
        return token # added for project 11, cuz I need it for the symbol table
    
    def write_output(self):
        
        with open(self.output_filepath, 'w') as file:
            file.write(self.xml_output)
        return

    def compileClassVarDec(self):
        self.nonterminal("classVarDec")
        kind = self.peek() # project 11 add, need to know this stuff for symbol table
        self.writeToken() # need to write 'var'
        type = self.peek()
        self.writeToken() # write type
        name = self.peek() 
        self.writeToken() # write the name of var
        self.symbolTable.define(name, type, kind) # project 11, we know its a class variable declaration so we call define

        # going to peek and see if we have more variables (var int age, int grade)
        while self.peek() == ",":
            self.writeToken() # write the comman
            name = self.peek() # if there are multiple variables being declared, then we add all of them to symbol table
            self.writeToken() # write the var name
            self.symbolTable.define(name, type, kind) # project 11, we know its a class variable declaration so we call define
        self.writeToken() # write the ;
        
        # gotta close <varDer> tag here we end nonterminal by popping of our list of nonterminal tags
        self.xml_output += self.nonterminal_tails.pop()
    
    def compileParameterList(self):# here we write the parameters "main (int a, char b)"
        self.nonterminal('parameterList')
        # if the token is not )
        while self.peekToken() != "symbol":
            self.writeParam()
        # here we end nonterminal by popping of our list of nonterminal tags
        self.xml_output += self.nonterminal_tails.pop()
    
    def writeParam(self):
        self.writeToken() # write the parameter type (int)
        self.writeToken() # wriet the parameter (a)
        # if there is a comma, we add it
        if self.peek() == ",":
            self.writeToken()
        

    def compileSubroutine(self):
        self.nonterminal("subroutineDec")
        self.writeToken() # we write the type of subroutine: "constructor, method, function"
        self.writeToken() #  we write the return type of the function type (ie <keyword> void </keyword> or int)
        self.writeToken() # we write the name of the function (ie main)
        self.writeToken() # we write (
        self.compileParameterList()
        self.writeToken() # we write )

        # Next we compile everything inside the brackets {...}
        self.nonterminal('subroutineBody')
        self.writeToken() # we write the open bracket {

        # Here we look for varDec
        while self.peek() == "var":
            self.compileVarDec()
        self.CompileStatements()
        self.writeToken() # we write the close bracket }

        # here we end nonterminal by popping of our list of nonterminal tags
        self.xml_output += self.nonterminal_tails.pop()

        # here we end nonterminal by popping of our list of nonterminal tags
        self.xml_output += self.nonterminal_tails.pop()
    def compileVarDec(self):
        self.nonterminal('varDec')
        self.writeToken()  # get 'var' keyword
        self.writeToken()  # get var type
        self.writeToken()  # get var name
        while self.peek() == ",":
            self.writeToken()  # get ',' symbol
            self.writeToken()  # get var name
        self.writeToken()  # get ';' symbol
        # here we end nonterminal by popping of our list of nonterminal tags
        self.xml_output += self.nonterminal_tails.pop()
        

    def peek(self):
        return self.tokens[self.index][1]
    
    def peekToken(self):
        return self.tokens[self.index][0]
    
    def CompileStatements(self):
       self.nonterminal('statements')
       while self.peek() in ['do', 'let', 'if', 'while', 'return']: # check if current token is one of these
           if self.peek() == 'do':
                self.compileDo()
           elif self.peek() == 'let':
                self.compileLet()
           elif self.peek() == 'if':
                self.compileIf()
           elif self.peek() == 'while':
                self.compileWhile()
           elif self.peek() == 'return':
                self.compileReturn()
        # gotta close tag
       self.xml_output += self.nonterminal_tails.pop()
    
    def CompileExpressionList(self):
        self.nonterminal("expressionList")
        if self.existExpression():
            self.compileExpression()
        while self.peek() == ",":  # case of multiple expressions
            self.writeToken()  # get ',' symbol
            self.compileExpression()
        # gotta close tag
        self.xml_output += self.nonterminal_tails.pop()
    
    def writeArrayIndex(self):
        self.writeToken() # write bracket
        self.compileExpression()
        self.writeToken() # write closing bracket

    def compileTerm(self):
        self.nonterminal("term")
        if self.peekToken() in ["stringConstant", "integerConstant"] or self.peek() in self.keywordConstant:
            self.writeToken() # write the constant
        elif self.peekToken() == 'identifier':
            self.writeToken()
            if self.peek() == "[":
                self.writeArrayIndex()
            if self.peek() == "(":
                self.writeToken()  # get '(' symbol
                self.CompileExpressionList()
                self.writeToken()  # get ')' symbol
            if self.peek() == ".":  # case of subroutine call
                self.writeToken()  # get '.' symbol
                self.writeToken()  # get subroutine name
                self.writeToken()  # get '(' symbol
                self.CompileExpressionList()
                self.writeToken()  # get ')' symbol
        elif self.peek() in self.unaryOp:
            self.writeToken()  # get unary operation symbol
            self.compileTerm()
        elif self.peek() == "(":
            self.writeToken()  # get '(' symbol
            self.compileExpression()
            self.writeToken()  # get ')' symbol
            
        # gotta close tag
        self.xml_output += self.nonterminal_tails.pop()

    def compileExpression(self):
        self.nonterminal('expression')
        self.compileTerm()
        while self.peek() in self.binaryOp:
            self.writeToken()
            self.compileTerm()
        # gotta close tag
        self.xml_output += self.nonterminal_tails.pop()
         
    def existExpression(self):
        token, value = self.tokens[self.index]
        bool_val = (token in ["integerConstant", "stringConstant", "identifier"]) or (value in self.unaryOp) or (value in self.keywordConstant) or (value == '(')
        return bool_val

    def compileDo(self):
        self.nonterminal('doStatement')
        self.writeToken() # write the do word
        
        # here we write the subroutine call
        self.writeToken() # get name of subroutine
        if self.peek() == '.':
            self.writeToken() # get .
            self.writeToken()  # write subroutine name
        self.writeToken() # get the '('
        self.CompileExpressionList()
        self.writeToken() # write ')'
        
        self.writeToken() # write the ';'
        # close tag
        self.xml_output += self.nonterminal_tails.pop()

    def compileLet(self):
        self.nonterminal("letStatement")
        self.writeToken()
        self.writeToken()
        if self.peek() == '[':
            self.writeArrayIndex()
        self.writeToken()
        self.compileExpression()
        self.writeToken()

        # close tag
        self.xml_output += self.nonterminal_tails.pop()


    def compileIf(self):
        self.nonterminal("ifStatement")
        self.writeToken()  # write 'if' 
        self.writeToken()  # write '(' 
        self.compileExpression()
        self.writeToken()  # write ')' 
        self.writeToken()  # write '{' 
        self.CompileStatements()
        self.writeToken()  # write '}' 
        if self.peek() == "else":
            self.writeToken()  # write 'else'
            self.writeToken()  # write '{' 
            self.CompileStatements()
            self.writeToken()  # write '}'
        # close tag
        self.xml_output += self.nonterminal_tails.pop()

    def compileWhile(self):
        self.nonterminal("whileStatement")
        self.writeToken() # need 'while' and '(
        self.writeToken()
        self.compileExpression()
        self.writeToken()  # write ')'
        self.writeToken()  # write '{'
        self.CompileStatements()
        self.writeToken()  # write '}'

        # close tag
        self.xml_output += self.nonterminal_tails.pop()

    def compileReturn(self):
        self.nonterminal("returnStatement")
        self.writeToken() # write 'return'
        while self.existExpression():
            self.compileExpression()
        self.writeToken() # write ';'
        # close tag
        self.xml_output += self.nonterminal_tails.pop()

    def nonterminal(self, tag):
        self.xml_output += f"<{tag}>\n"
        self.nonterminal_tails.append(f"</{tag}>\n")

    