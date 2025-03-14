class SymbolTableClass:
    def __init__(self):
        # symbol table is a hashmap with the name of the symbol and the following attributes in this order kind type index. index is 1 indexed
        self.class_level_hmap = {}
        self.subroutine_level_hmap = {}
        
        
        self.index = 0 # we will use this to keep track of what line we are on
        self.xml_output = "" # this we will use as input for the VM writer

        self.arg_counter = 0 # use these to keep track of the number of times we've put something of a particular kind into the symbol table
        self.var_counter = 0 
        self.static_counter = 0
        self.field_counter = 0
        
    
    def startSubroutine(self):
        # Reset the subroutine-level symbol table, but keep the class-level table
        self.subroutine_level_hmap = {}

        self.arg_counter = 0 # the scope of these are reset because they are in subroutine
        self.var_counter = 0
    
    def Define(self, name, kind, type_val):
        # Map kind to the internal representation
        if kind == "ARG":
            self.subroutine_level_hmap[name] = (kind, type_val, self.arg_counter)
            self.arg_counter += 1
        elif kind == "FIELD":
            self.class_level_hmap[name] = (kind, type_val, self.field_counter)
            self.field_counter += 1
        elif kind == "STATIC":
            self.class_level_hmap[name] = (kind, type_val, self.static_counter)
            self.static_counter += 1
        elif kind == "VAR":
            self.subroutine_level_hmap[name] = (kind, type_val, self.var_counter)
            self.var_counter += 1

    def VarCount(self, kind):
        # Return the number of variables of the given kind
        if kind == "ARG":
            return self.arg_counter
        elif kind == "FIELD":
            return self.field_counter
        elif kind == "STATIC":
            return self.static_counter
        elif kind == "VAR":
            return self.var_counter
        return 0
    
    def KindOf(self, name):
        # Return the kind of the named identifier
        if name in self.subroutine_level_hmap:
            return self.subroutine_level_hmap[name][0]
        elif name in self.class_level_hmap:
            return self.class_level_hmap[name][0]
        return None  # Not found
    
    def TypeOf(self, name):
        # Return the type of the named identifier
        if name in self.subroutine_level_hmap:
            return self.subroutine_level_hmap[name][1]
        elif name in self.class_level_hmap:
            return self.class_level_hmap[name][1]
        return None  # Not found

    def IndexOf(self, name):
        # Return the index of the named identifier
        if name in self.subroutine_level_hmap:
            return self.subroutine_level_hmap[name][2]
        elif name in self.class_level_hmap:
            return self.class_level_hmap[name][2]
        return None  # Not found