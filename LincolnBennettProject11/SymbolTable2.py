class SymbolTableClass:
    def __init__(self, xml_input):
        # symbol table is a hashmap with the name of the symbol and the following attributes in this order kind type index. index is 1 indexed
        self.class_level_hmap = {}
        self.method_level_hmap = {}

        self.index = 0 # we will use this to keep track of what line we are on
        self.xml_output = "" # this we will use as input for the VM writer

        self.arg_counter = 0 # use these to keep track of the number of times we've put something of a particular kind into the symbol table
        self.var_counter= 0 
        self.static_counter = 0
        self.field_counter = 0
        
    
    def startSubroutine(self):
        self.subroutine_level_hmap = {} # only reset ONE of the symboltables

        self.arg_counter = 0 # the scope of these are reset because they are in subroutine, while STATIC and FIELD scope is the class level
        self.var_counter= 0
    
    def Define(self, name : str, kind : str, type : str): # to calculate memory location offset, go through and calculate the number of that kind
        if kind == 'ARG':
            self.subroutine_level_hmap[name] = (kind, type, self.arg_counter)
            self.arg_counter += 1
        elif kind == 'FIELD':
            self.subroutine_level_hmap[name] = (kind, type, self.field_counter)
            self.field_counter += 1
        elif kind == 'STATIC':
            self.subroutine_level_hmap[name] = (kind, type, self.static_counter)
            self.static_counter += 1
        elif kind == 'VAR':
            self.subroutine_level_hmap[name] = (kind, type, self.var_counter)
            self.var_counter += 1

    def VarCount(self, kind):
        if kind == "ARG":
            return self.arg_counter
        elif kind == "FIELD":
            return self.field_counter
        elif kind == "STATIC":
            return self.static_counter
        elif kind == "VAR":
            return self.var_counter
        return 0
    
    def KindOf(self, name : str): # Note: 0 is used because my symboltable is a hashmap of tuples, where "name" of identifier is the key, and 0 index represents kind
        if name in self.subroutine_level_hmap:
            return self.subroutine_level_hmap[name][0]
        elif name in self.class_level_hmap:
            return self.class_level_hmap[name][0]
        else:
            return None
    
    def TypeOf(self, name : str): # type is 1st index of tuple in hashmap
        if name in self.subroutine_level_hmap:
            return self.subroutine_level_hmap[name][1]
        elif name in self.class_level_hmap:
            return self.class_level_hmap[name][1]
        else:
            return None  # Not found
    def IndexOf(self, name : str):
        # Return the index of the named identifier
        if name in self.subroutine_level_hmap:
            return self.subroutine_level_hmap[name][2]
        elif name in self.class_level_hmap:
            return self.class_level_hmap[name][2]
        else:
            return None  # Not found
        
