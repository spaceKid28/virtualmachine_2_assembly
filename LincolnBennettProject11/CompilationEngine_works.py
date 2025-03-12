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
        
        # Initialize the symbol table
        self.symbolTable = SymbolTableClass()
        self.currentSubroutine = None
        self.currentClass = None
        
        # Initialize the VM writer
        vm_file = output_filepath.replace('.xml', 'TESTING.vm')
        self.vmWriter = VMWriter(vm_file)
    
    # we run this method first, everytime
    def compileClass(self):
        self.nonterminal('class')
        self.writeToken() # note, this will be the class keyword
        self.currentClass = self.writeToken() # note, this will be the class name (for example: main)
        self.writeToken() # note, this will always be {

        # Reset the symbol table for this class
        self.symbolTable.startSubroutine()
        
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

        # Close the VM writer
        self.vmWriter.close()

    def writeToken(self): # note that this method both increments to the next token (via self.index) and returns the token
        tag, token = self.tokens[self.index]
        
        # Special handling for identifiers - check if we need to add symbol table info
        if tag == "identifier":
            return self.writeIdentifier(token)
        
        self.xml_output += f"<{tag}> {token} </{tag}>\n"
        self.index += 1
        return token # added for project 11, cuz I need it for the symbol table
    
    def writeIdentifier(self, token):
        # This is a new method that writes identifiers with their symbol table information
        
        # Default values if not defined
        category = "NONE"  # var, argument, static, field, class, subroutine
        defining = False   # Whether the identifier is being defined or used
        index = None       # Running index assigned by the symbol table
        
        # Try to determine identifier information based on context
        try:
            if token in self.symbolTable.subroutine_level_hmap:
                kind, type_val, idx = self.symbolTable.subroutine_level_hmap[token]
                category = kind
                index = idx
            elif token in self.symbolTable.class_level_hmap:
                kind, type_val, idx = self.symbolTable.class_level_hmap[token]
                category = kind
                index = idx
        except:
            # If token isn't in the symbol table, it could be a class or subroutine name
            if token == self.currentClass:
                category = "class"
            elif token == self.currentSubroutine:
                category = "subroutine"
        
        # Add the identifier with its additional information to the XML output
        self.xml_output += f"<identifier> {token} </identifier>\n"
        self.xml_output += f"<!-- category: {category}, defining: {defining}, index: {index if index is not None else 'None'} -->\n"
        
        self.index += 1
        return token
    
    def write_output(self):
        with open(self.output_filepath, 'w') as file:
            file.write(self.xml_output)
        return

    def compileClassVarDec(self):
        self.nonterminal("classVarDec")
        kind = self.writeToken() # need to write 'static' or 'field'
        type_val = self.writeToken() # write type
        
        # Convert the Jack variable kind to symbol table kind
        if kind == "static":
            st_kind = "STATIC"
        else:  # field
            st_kind = "FIELD"
        
        # Mark the next identifier as being defined
        name = self.peek()
        defining = True
        
        self.writeToken() # write the name of var
        # Add to symbol table
        self.symbolTable.Define(name, st_kind, type_val)

        # going to peek and see if we have more variables (var int age, int grade)
        while self.peek() == ",":
            self.writeToken() # write the comma
            name = self.peek() # if there are multiple variables being declared, then we add all of them to symbol table
            defining = True
            self.writeToken() # write the var name
            self.symbolTable.Define(name, st_kind, type_val)
        self.writeToken() # write the ;
        
        # gotta close <varDer> tag here we end nonterminal by popping of our list of nonterminal tags
        self.xml_output += self.nonterminal_tails.pop()
    
    def compileParameterList(self):# here we write the parameters "main (int a, char b)"
        self.nonterminal('parameterList')
        # if the token is not )
        if self.peek() != ")":
            type_val = self.writeToken()  # Parameter type
            name = self.peek()
            self.writeToken()  # Parameter name
            self.symbolTable.Define(name, "ARG", type_val)
            
            # Handle multiple parameters
            while self.peek() == ",":
                self.writeToken()  # Write comma
                type_val = self.writeToken()  # Parameter type
                name = self.peek()
                self.writeToken()  # Parameter name
                self.symbolTable.Define(name, "ARG", type_val)
                
        # here we end nonterminal by popping of our list of nonterminal tags
        self.xml_output += self.nonterminal_tails.pop()
    
    def writeParam(self):
        type_val = self.writeToken() # write the parameter type (int)
        name = self.peek()
        self.writeToken() # write the parameter (a)
        self.symbolTable.Define(name, "ARG", type_val)
        
        # if there is a comma, we add it
        if self.peek() == ",":
            self.writeToken()
        

    def compileSubroutine(self):
        # Reset the subroutine-level symbol table
        self.symbolTable.startSubroutine()
        
        self.nonterminal("subroutineDec")
        subroutine_type = self.writeToken() # we write the type of subroutine: "constructor, method, function"
        self.writeToken() # we write the return type of the function type (ie <keyword> void </keyword> or int)
        self.currentSubroutine = self.writeToken() # we write the name of the function (ie main)
        full_function_name = f"{self.currentClass}.{self.currentSubroutine}"
        self.writeToken() # we write (
        
        # If this is a method, add 'this' as first argument
        if subroutine_type == "method":
            self.symbolTable.Define("this", "ARG", self.currentClass)
            
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
        self.currentSubroutine = None
        
    def compileVarDec(self):
        self.nonterminal('varDec')
        self.writeToken()  # get 'var' keyword
        type_val = self.writeToken()  # get var type
        name = self.peek()
        self.writeToken()  # get var name
        self.symbolTable.Define(name, "VAR", type_val)
        
        var_count = 1  # Count variables in this declaration
        
        while self.peek() == ",":
            self.writeToken()  # get ',' symbol
            name = self.peek()
            self.writeToken()  # get var name
            self.symbolTable.Define(name, "VAR", type_val)
            var_count += 1
            
        self.writeToken()  # get ';' symbol
        # here we end nonterminal by popping of our list of nonterminal tags
        self.xml_output += self.nonterminal_tails.pop()
        
        return var_count  # Return the number of variables declared
        

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
        if self.peekToken() == "integerConstant":
            # Push integer constant to the stack
            value = self.peek()
            self.writeToken()
            self.vmWriter.writePush("constant", value)
        elif self.peekToken() == "stringConstant" or self.peek() in self.keywordConstant:
            self.writeToken() # write the constant
        elif self.peekToken() == 'identifier':
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
            full_name = f"{self.currentClass}.{class_or_var_name}"
            
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
        self.writeToken()  # write 'let'
        self.writeToken()  # write variable name (already handled by writeIdentifier)
        if self.peek() == '[':
            self.writeArrayIndex()
        self.writeToken()  # write '='
        self.compileExpression()
        self.writeToken()  # write ';'

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