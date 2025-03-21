from SymbolTable import SymbolTableClass
from VMWriter import VMWriter
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

        self.symbol_table_obj = SymbolTableClass() # Create SymbolTable Object 
        self.current_subroutine = "" # keep track of both current subroutine and current class for current token self.tokens[self.index] is pointing to
        self.current_class_name = "" 

        output_file = output_filepath.replace('.xml', 'testing2.vm') #write to vm instead of .xml
        self.vmWriter = VMWriter(output_file)
    
    # we run this method first, everytime
    def compileClass(self):
        self.nonterminal('class')
        self.writeToken() # note, this will be the class keyword
        self.current_class_name = self.peek() # for seven this should be "MAIN"
        self.writeToken() # note, this will be the class name (for example: main)
        self.writeToken() # note, this will always be {

        self.symbol_table_obj.startSubroutine() # Everytime we start a class, we reset subroutine variables as well

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

        self.vmWriter.close() # write the output

    def writeToken(self): # note that this method both increments to the next token (via self.index) and returns the token
        
        tag, token = self.tokens[self.index]

        if tag == "identifier": # added for project 11
            return self.writeIdentifier(token)
        
        self.xml_output += f"<{tag}> {token} </{tag}>\n"
        self.index += 1
        return token # added for project 11, cuz I need it for the symbol table
    
    def writeIdentifier(self, token): # added for project 11
        # must treat identifier's specially, we need their symbol table info to translate correctly

        category = "" # is this a var, arg, static, field, class
        used = True # are using this identifier or are we defining it
        index = -1 # Needs to be some integers (type error otherwise)

        if token in self.symbol_table_obj.subroutine_level_hmap: # check subroutine, then check class
            category, type_val, index = self.symbol_table_obj.subroutine_level_hmap[token]
        elif token in self.symbol_table_obj.class_level_hmap:
            category, type_val, index = self.symbol_table_obj.class_level_hmap[token]
        else: # symbol isn't in either symbol table
            if token == self.current_class_name:
                category = "class"
            elif token == self.current_subroutine:
                category = "subroutine"
        
        # Add the identifier with its additional information to the XML output
        self.xml_output += f"<identifier> {token} </identifier>\n"
        self.xml_output += f"<!-- category: {category}, defining: {not used}, index: {index if index is not None else 'None'} -->\n"

        self.index += 1
        return token

    def write_output(self):
        with open(self.output_filepath, 'w') as file:
            file.write(self.xml_output)
        return

    def compileClassVarDec(self):
        tmp_hmap = {"static": "STATIC", "field": "FIELD"} # need to convert Jack static to VM STATIC....

        self.nonterminal("classVarDec")
        kind = self.peek() # project 11 add, need to know this stuff for symbol table
        kind = tmp_hmap[kind]
        self.writeToken() # need to write 'var'
        type = self.peek()
        self.writeToken() # write type
        name = self.peek() 
        self.writeToken() # write the name of var
        used = False

        self.symbol_table_obj.Define(name, type, kind) # project 11, we know its a class variable declaration so we call define

        # going to peek and see if we have more variables (var int age, int grade)
        while self.peek() == ",":
            self.writeToken() # write the comman
            name = self.peek() # if there are multiple variables being declared, then we add all of them to symbol table
            used = False
            self.writeToken() # write the var name
            self.symbol_table_obj.Define(name, type, kind) # project 11, we know its a class variable declaration so we call define
        self.writeToken() # write the ;
        
        # gotta close <varDer> tag here we end nonterminal by popping of our list of nonterminal tags
        self.xml_output += self.nonterminal_tails.pop()
    
    def compileParameterList(self):# here we write the parameters "main (int a, char b)"
        self.nonterminal('parameterList')
        # if the token is not )
        if self.peek() != ")":
            type_val = self.peek()
            self.writeToken()  # Parameter type
            name = self.peek()
            self.writeToken()  # Parameter name
            self.symbol_table_obj.Define(name, "ARG", type_val)
            
            # Handle multiple parameters
            while self.peek() == ",":
                self.writeToken()  # Write comma
                type_val = self.peek()
                self.writeToken()  # Parameter type
                name = self.peek()
                self.writeToken()  # Parameter name
                self.symbol_table_obj.Define(name, "ARG", type_val)
        # here we end nonterminal by popping of our list of nonterminal tags
        self.xml_output += self.nonterminal_tails.pop()
    
    def writeParam(self):
        type_val = self.peek()
        self.writeToken() # write the parameter type (int)
        name = self.peek()
        self.writeToken() # wriet the parameter (a)
        self.symbol_table_obj.Define(name, "ARG", type_val)
        # if there is a comma, we add it
        if self.peek() == ",":
            self.writeToken()
        

    def compileSubroutine(self):
        self.symbol_table_obj.startSubroutine() # must reset the subroutine symbol table

        self.nonterminal("subroutineDec")
        subroutine_type = self.peek()
        self.writeToken() # we write the type of subroutine: "constructor, method, function"
        self.writeToken() #  we write the return type of the function type (ie <keyword> void </keyword> or int)
        self.current_subroutine = self.peek()
        self.writeToken() # we write the name of the function (ie main)
        full_function_name = f"{self.current_class_name}.{self.current_subroutine}"
        self.writeToken() # we write (

        # If this is a method, add 'this' as first argument
        if subroutine_type == "method":
            self.symbol_table_obj.Define("this", "ARG", self.current_class_name)

        self.compileParameterList()
        self.writeToken() # we write )

        # Next we compile everything inside the brackets {...}
        self.nonterminal('subroutineBody')
        self.writeToken() # we write the open bracket {

        # Here we look for varDec
        var_count = 0
        while self.peek() == "var":
            var_count += self.compileVarDec()
            
        # Write the VM function declaration
        self.vmWriter.writeFunction(full_function_name, var_count)


        self.CompileStatements()
        self.writeToken() # we write the close bracket }

        # here we end nonterminal by popping of our list of nonterminal tags
        self.xml_output += self.nonterminal_tails.pop()

        # here we end nonterminal by popping of our list of nonterminal tags
        self.xml_output += self.nonterminal_tails.pop()

        # Reset the current subroutine name
        self.current_subroutine = None


    def compileVarDec(self):
        self.nonterminal('varDec')
        self.writeToken()  # get 'var' keyword
        type_val = self.writeToken()  # get var type
        name = self.peek()
        self.writeToken()  # get var name
        self.symbol_table_obj.Define(name, "VAR", type_val)

        var_count = 1
        
        while self.peek() == ",":
            self.writeToken()  # get ',' symbol
            name = self.peek()
            self.writeToken()  # get var name
            self.symbol_table_obj.Define(name, "VAR", type_val)
            var_count += 1
        self.writeToken()  # get ';' symbol
        # here we end nonterminal by popping of our list of nonterminal tags
        self.xml_output += self.nonterminal_tails.pop()

        return var_count
        

    def peek(self):
        return self.tokens[self.index][1]
    
    def peekTag(self):
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
        nArgs = 0  # Count the number of arguments
        
        if self.existExpression():
            self.compileExpression()
            nArgs += 1
            
        while self.peek() == ",":  # case of multiple expressions
            self.writeToken()  # get ',' symbol
            self.compileExpression()
            nArgs += 1
            
        # gotta close tag
        self.xml_output += self.nonterminal_tails.pop()
        return nArgs
    
    def writeArrayIndex(self):
        self.writeToken() # write bracket
        self.compileExpression()
        self.writeToken() # write closing bracket

    def compileTerm(self):
        self.nonterminal("term")
        if self.peekTag() == "integerConstant":
            # Push integer constant to the stack
            value = self.peek()
            self.writeToken()
            self.vmWriter.writePush("constant", value)
        elif self.peekTag() == "stringConstant" or self.peek() in self.keywordConstant:
            self.writeToken() # write the constant
        elif self.peekTag() == 'identifier':
            identifier = self.writeToken()  # Could be variable, array, or subroutine call
            
            if self.peek() == "[":
                self.writeArrayIndex()
            elif self.peek() == "(":
                self.writeToken()  # get '(' symbol
                nArgs = self.CompileExpressionList()
                self.writeToken()  # get ')' symbol
                # Call the function
                self.vmWriter.writeCall(f"{identifier}", nArgs)
            elif self.peek() == ".":  # case of subroutine call
                self.writeToken()  # get '.' symbol
                subroutine_name = self.writeToken()  # get subroutine name
                self.writeToken()  # get '(' symbol
                nArgs = self.CompileExpressionList()
                self.writeToken()  # get ')' symbol
                # Call the function with the class/object name
                self.vmWriter.writeCall(f"{identifier}.{subroutine_name}", nArgs)
        elif self.peek() in self.unaryOp:
            op = self.writeToken()  # get unary operation symbol
            self.compileTerm()
            # Write the VM command for the unary operation
            if op == '-':
                self.vmWriter.writeArithmetic('neg')
            elif op == '~':
                self.vmWriter.writeArithmetic('~')
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
            # Save the binary operator
            op = self.writeToken()
            self.compileTerm()
            
            # Generate VM code for the binary operation
            self.vmWriter.writeArithmetic(op)
            
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
        class_or_var_name = self.writeToken() # get name of class/variable
        
        if self.peek() == '.':
            self.writeToken() # get .
            subroutine_name = self.writeToken()  # write subroutine name
            full_name = f"{class_or_var_name}.{subroutine_name}"
        else:
            # Method call on this class
            full_name = f"{self.current_class_name}.{class_or_var_name}"
            
        self.writeToken() # get the '('
        nArgs = self.CompileExpressionList()
        self.writeToken() # write ')'
        
        # Generate VM code for the call
        self.vmWriter.writeCall(full_name, nArgs)
        
        # For do statements, we need to pop the return value which is not used
        self.vmWriter.writePop("temp", 0)
        
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
        
        if self.existExpression():
            self.compileExpression()
        else:
            # If no expression after return, push 0
            self.vmWriter.writePush("constant", 0)
            
        # Write the VM return command
        self.vmWriter.writeReturn()
        
        self.writeToken() # write ';'
        # close tag
        self.xml_output += self.nonterminal_tails.pop()

    def nonterminal(self, tag):
        self.xml_output += f"<{tag}>\n"
        self.nonterminal_tails.append(f"</{tag}>\n")

    