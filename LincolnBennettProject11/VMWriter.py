class VMWriter:
    def __init__(self, output_filepath):
        self.output_filepath = output_filepath
        self.output = []  # Store VM commands here
    
    def writePush(self, segment, index):
        """Write a VM push command"""
        self.output.append(f"push {segment} {index}")
    
    def writePop(self, segment, index):
        """Write a VM pop command"""
        self.output.append(f"pop {segment} {index}")

    def writeArithmetic(self, command):
        """Write a VM arithmetic command"""
        # Map Jack operations to VM commands
        arithmetic_map = {
            '+': 'add',
            '-': 'sub',
            '*': 'call Math.multiply 2',
            '/': 'call Math.divide 2',
            '&': 'and',
            '|': 'or',
            '&lt;': 'lt',
            '&gt;': 'gt',
            '&amp;':'&',
            '=': 'eq',
            '~': 'not',
            'neg': 'neg'
        }
        
        if command in arithmetic_map:
            self.output.append(arithmetic_map[command])
        else:
            # For any unsupported operation, we'll throw an error
            raise ValueError(f"Unsupported arithmetic operation: {command}")

    def writeCall(self, name, nArgs):
        """Write a VM call command"""
        self.output.append(f"call {name} {nArgs}")

    def writeFunction(self, name, nLocals):
        """Write a VM function command"""
        self.output.append(f"function {name} {nLocals}")

    def writeReturn(self):
        """Write a VM return command"""
        self.output.append("return")

    def close(self):
        """Write the output to a file and close it"""
        with open(self.output_filepath, 'w') as file:
            file.write('\n'.join(self.output))
        return self.output