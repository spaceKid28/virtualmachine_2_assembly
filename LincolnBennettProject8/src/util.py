import os

def parser(filename):
    lines = []
    # Convert relative path to absolute path
    filename = os.path.abspath(filename)
    with open(filename) as inputfile:
        # Multi Line comments are a little hairy, going to do two passes
        # boolean flag to know if we are in a multi line comment
        multiFlag = False
        for line in inputfile:
            # change the flag if we are at the beginning or end
            if "/*" in line:
                multiFlag = True
            elif "*/" in line: 
                multiFlag = False
            # if we are in multi line comment, skip this line
            elif multiFlag:
                continue
            # append the line if we are outside flag
            else:
                lines.append(line.rstrip())
        # loop through lines again, strip white space
        for idx in range(len(lines)):
            # this should strip all leading white spaces (tabs or space)
            lines[idx] = lines[idx].lstrip()
            # Remove comments that span only one line
            if "//" in lines[idx]:
                lines[idx] = lines[idx].split("//")[0].strip()
        # list comprehension to remove all empty lines
        lines = [line for line in lines if line.strip() != ""]
    return lines

def symbolhandling(input):
    # build initial symbol table
    symbol_table = {f'R{x}':x for x in range(16)}
    symbol_table['SP'] = 0
    symbol_table['LCL'] = 1
    symbol_table['ARG'] = 2
    symbol_table['THIS'] = 3
    symbol_table['THAT'] = 4
    symbol_table['SCREEN'] = 16384
    symbol_table['KBD'] = 24576
    
    # First Pass, build the symbol table for labels
    ROM_counter = 0
    input2 = []
    for line in input:
        # check for labels
        if line[0] == "(" and line[-1] == ")":
            symbol_table[line[1:-1]] = ROM_counter
            continue
        else:
            ROM_counter += 1
            input2.append(line)
    
    # Second Pass
    last_RAM_address = 16
    input = []
    for line in input2:
        if line[0] == "@":
            arg = line[1:]
            # is it a digit?, if so, continue
            if arg.isdigit():
                pass
            # is it in the symbol table? if so, swap and then move on
            elif arg in symbol_table:
                line = "@" + str(symbol_table[arg])
            # if it is not a digit and not in the symbol table, we must add it to the symbol table
            else:
                symbol_table[arg] = last_RAM_address
                line = "@" + str(last_RAM_address)
                last_RAM_address += 1
        input.append(line)
    return input

def symbolless_assembler(input):
    """
    Args: input (list[str]): Input is list of strings, each string represents a line of Hack Assembly code

    Returns: (list[str]): List of binary instructions
    """
    binary_instructions = []
    for hack_line in input:
        # list of 16 char, each will either be 0 or 1
        binary_line = ['0' for _ in range(16)]
        # if first command is "@" this is an A-Instruction, we want binary[0] = 0
        if hack_line[0] == "@":
            # convert number
            number = int(hack_line[1:])
            binary_number = f'{number:015b}'
            binary_line[1:] = binary_number.split()
        # otherwise, C-Instruction
        else:
            binary_line[:3] = ['1','1','1']
            # Parse dest=comp;jump format
            dest, comp, jump = '', '', ''
            if '=' in hack_line:
                dest, rest = hack_line.split('=')
                if ';' in rest:
                    comp, jump = rest.split(';')
                else:
                    comp = rest
            elif ';' in hack_line:
                comp, jump = hack_line.split(';')
            # Strip whitespace from comp, dest, and jump

            comp = comp.strip()
            dest = dest.strip()
            jump = jump.strip()

            # Set comp bits (bits 3-9)
            # Add comp bits mapping
            comp_bits = {
                '0':   '0101010',
                '1':   '0111111',
                '-1':  '0111010',
                'D':   '0001100',
                'A':   '0110000',
                'M':   '1110000',
                '!D':  '0001101',
                '!A':  '0110001',
                '!M':  '1110001',
                '-D':  '0001111',
                '-A':  '0110011',
                '-M':  '1110011',
                'D+1': '0011111',
                'A+1': '0110111',
                'M+1': '1110111',
                'D-1': '0001110',
                'A-1': '0110010',
                'M-1': '1110010',
                'D+A': '0000010',
                'D+M': '1000010',
                'D-A': '0010011',
                'D-M': '1010011',
                'A-D': '0000111',
                'M-D': '1000111',
                'D&A': '0000000',
                'D&M': '1000000',
                'D|A': '0010101',
                'D|M': '1010101'
            }
            
            binary_line[3:10] = list(comp_bits[comp])
            
            # Set dest bits (bits 10-12)
            dest_bits = {
                '':    '000',
                'M':   '001',
                'D':   '010',
                'MD':  '011',
                'A':   '100',
                'AM':  '101',
                'AD':  '110',
                'AMD': '111'
            }
            
            binary_line[10:13] = list(dest_bits[dest])
                
            # Set jump bits (bits 13-15)
            jump_bits = {
                '':    '000',
                'JGT': '001',
                'JEQ': '010',
                'JGE': '011',
                'JLT': '100',
                'JNE': '101',
                'JLE': '110',
                'JMP': '111'
            }
            binary_line[13:16] = list(jump_bits[jump])

        binary_instructions.append("".join(binary_line))
    
    return binary_instructions

def write_file(filename, lines, extension):
    # Convert relative path to absolute path and strip .in extension

    filename = os.path.splitext(filename)[0]
    filename = os.path.abspath(filename)
    
    with open(f"{filename}.{extension}", "w") as outputfile:
        for line in lines:
            # add new line character at the end of each line
            outputfile.write(f"{line + '\n'}")

def constant(line):
    line = line.split(" ")
    num = line[-1]
    if "push" in line[0]:
        new_lines = ["//push constant operation", f"@{num}", "D=A", "@SP", "A=M", "M=D", "@SP", "M=M+1", ""]
        return new_lines
    elif "pop" in line[0]:
        raise Exception(f"pop constant {num} is not a valid command")

# define push and pop for stack variables
def stackvar(line):
    # create a hashmap for VM to Assembly memory locations
    mem_hmap = {"temp": "5", "local": "LCL", "argument":"ARG", "this": "THIS", "that":"THAT"}
    line = line.split(" ")
    # num represents the offset, for example. num = 5 in "push local 5"
    num = line[-1]
    # changes local to LCL in "push local 5"
    mem_location = mem_hmap[line[1]]
    # if statements to write push and pop
    if "push" in line[0]:
        # temp has slightly different command
        if mem_location != "5":
            new_lines = [f"//push {mem_location} {num} operation", f"@{mem_location}", "D=M", f"@{num}", f"A=D+A", "D=M //stores value in D register of RAM[{mem_location} + x]", "@SP", "A=M", "M=D //set value at top of stack to D", "@SP", "M=M+1 //increment stack pointer", ""]
        else:
            new_lines = [f"//push {mem_location} {num} operation", f"@{mem_location}", "D=A", f"@{num}", f"A=D+A", "D=M //stores value in D register of RAM[{mem_location} + x]", "@SP", "A=M", "M=D //set value at top of stack to D", "@SP", "M=M+1 //increment stack pointer", ""]
    # same logic fo pop
    elif "pop" in line[0]:
        if mem_location != "5":
            new_lines = [f"//pop {mem_location} {num} operation", f"@{mem_location}", "D=M", f"@{num}", "D=D+A", "@R13", "M=D", "@SP", "AM=M-1", "D=M", "@R13", "A=M", "M=D", ""]
        else:
            new_lines = [f"//pop {mem_location} {num} operation", f"@{mem_location}", "D=A", f"@{num}", "D=D+A", "@R13", "M=D", "@SP", "AM=M-1", "D=M", "@R13", "A=M", "M=D", ""]
    return new_lines

# define push and pop for pointer
def pointer(line):
    # again, we use hash map to translate VM language location to assembly location
    pattern_match = {"pointer 0": "THIS", "pointer 1":"THAT"}
    line = line.split(" ")
    thisThat = pattern_match[" ".join(line[1:])]
# if statements to write push and pop
    if "push" in line[0]:
        new_lines = [f"//push {" ".join(line[1:])} operation", f"@{thisThat}", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1 //increment stack pointer", ""]
       
    elif "pop" in line[0]:
        new_lines = [f"//pop {" ".join(line[1:])} operation", "@SP", "AM=M-1", "D=M", f"@{thisThat}", "M=D", ""]
    return new_lines

# define push and pop for static
def static_helper(line, filename):
    # we want to take ONLY the filename for our static variable location "filename.5"
    filename = filename.split('/')[-1].replace('.vm', '')
    line = line.split(" ")

    if "push" in line[0]:
        new_lines = [f"//{" ".join(line)} operation", f"@{filename}.{line[-1]}", "D=M", "@SP", "A=M", "M=D", "@SP", "M=M+1 //increment stack pointer", ""]
       
    elif "pop" in line[0]:
        new_lines = [f"//{" ".join(line)} operation", "@SP", "AM=M-1", "D=M", f"@{filename}.{line[-1]}", "M=D", ""]
    return new_lines

# if-goto LOOP_START  // If counter != 0, goto LOOP_START
def ifgoto(line):
    label = line.split(" ")[-1]
    new_lines = [f"// {line} operation", "@SP", "AM=M-1", "D=M", f"@{label}", "D;JNE", " "]
    return new_lines

def goto(line):
    label = line.split(" ")[-1]
    new_lines = [f"// {line} operation", f"@{label}", "D;JMP", " "]
    return new_lines

def func(line):
    k = int(line.split(" ")[-1])
    new_lines = [f"// {line} operation"] +  k * ["@SP", "AM=M+1 //increment stack pointer and address in A", "A=A-1 //Note, we have already incremented SP, we adjust to set to 0", "M=0", " "]
    return new_lines

def ret(line):
    new_lines = [f"// {line} operation", "//R13=LCL", "@LCL", "D=M", "@R13", "M=D",
                "//R14 = *(R13 - 5)", "@LCL", "D=M", "@5", "A=D-A", "D=M", "@R14", "M=D",
                "//*ARG = pop(), ", "@SP", "A=M-1", "D=M", "@ARG", "A=M", "M=D",
                "//SP =ARG+1 restore the SP of the caller", "@ARG", "D=M+1", "@SP", "M=D",
                "//THAT = *(R13-1), restore THAT of the caller", "@R13", "AM=M-1", "D=M", "@THAT", "M=D",
                "//THIS = *(R13-2), restore THIS of the caller", "@R13", "AM=M-1", "D=M", "@THIS", "M=D",
                "//ARG = *(R13-3), restore ARG of the caller", "@R13", "AM=M-1", "D=M", "@ARG", "M=D",
                "//LCL = *(R13-4), restore ARG of the caller", "@13", "AM=M-1", "D=M", "@LCL", "M=D",
                "//goto *R14", "@R14", "A=M", "0;JMP", " "
    ]
    return new_lines

# arithmetic oeparations, I hardcoded into a hashmap
arithmetic_operations = {
    "add" : ["@SP", "AM=M-1", "D=M", "A=A-1", "M=D+M", ""],
    "sub" : ["@SP", "AM=M-1", "D=M", "A=A-1", "M=M-D", ""], 
    "gt" : ["@SP", "AM=M-1", "D=M", "A=A-1", "D=M-D", "M=-1", "@continue", "D;JGT", "@SP", "A=M-1","M=0", "(continue)", ""], 
    "not" : ["@SP", "A=M-1", "M=!M", ""],
    "or": ["@SP", "M=M-1", "A=M", "D=M", "@SP", "M=M-1", "A=M", "M=D|M", "@SP", "M=M+1", ""],

    "neg": ["@SP", "A=M-1", "M=-M", ""],
    "eq": ["@SP", "AM=M-1", "D=M", "A=A-1", "D=M-D", "M=-1", "@continue", "D;JEQ", "@SP", "A=M-1", "M=0", "(continue)", ""],
    "lt": ["@SP", "AM=M-1", "D=M", "A=A-1", "D=M-D", "M=-1", "@continue", "D;JLT", "@SP", "A=M-1", "M=0", "(continue)", ""],
    "and": ["@SP", "AM=M-1", "D=M", "A=A-1", "M=D&M", ""]
}




