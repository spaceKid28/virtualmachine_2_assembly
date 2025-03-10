import os
from src.util import parser, write_file, constant, arithmetic_operations, stackvar, pointer, static_helper, ifgoto, goto, func, ret, call, get_vm_file_paths


def main(path, boot_strap_flag = True):
    # create multiple continues that we can use later
    continues = [f"continue{x}" for x in range(10000)]
    call_counter = 1
    # delete_flag = False
    if path.endswith('.vm'):
        filenames = [path]
    # if the file doesn't end with .vm we assume it is a folder
    # our function will combine all of the .vm files into one .vm file and return the address to this .vm file
    else:
        filenames = get_vm_file_paths(path)
    
    new_lines = []
    if boot_strap_flag:
        new_lines = ["//bootstrap code ", "@256", "D=A", "@SP", "M=D", " "]
    for filename in filenames:
        lines = parser(filename)

        # new lines is list of lines that we will pass to write_file
        # FOR THE FIRST FILE ONLY, we had the VM instruction to call Sys.init 0
        # The if statement with the Flag does this
        if boot_strap_flag:
            lines = ["call Sys.init 0"] + lines
            boot_strap_flag = False

        operators = ["local", "argument", "this", "that", "temp"]
        for line in lines:
            # check if line is an arithmetic operation
            if line in arithmetic_operations:
                commands = [f"//{line}"] + arithmetic_operations[line]
                # I can't use the same continue for all the JMPs, have to create continue0, continue1, continue3...
                new_continue = continues.pop(0)
                commands = [x.replace("continue", new_continue) if "continue" in x else x for x in commands]
                new_lines = new_lines + commands
            # use the constant helper from util.py
            elif "constant" in line:
                new_lines = new_lines + constant(line)
            # use the pointer helper from util.py
            elif "pointer" in line:
                new_lines = new_lines + pointer(line)
            # use the static helper from util.py
            elif "static" in line:
                new_lines = new_lines + static_helper(line, filename)
            # below predicate: if any element in the line is a stack varaiable, use the stack variable helper
            # for example push local 5 would evalute to true, as local is a stack variable (and in operators list)
            elif any(x in line for x in operators):
                new_lines = new_lines + stackvar(line)
            
            elif "label" in line:
                # label command is easy
                new_lines = new_lines + ["(" + line.split(" ")[-1] + ")"]

            # if-goto
            elif "if-goto" in line:
                new_lines = new_lines + ifgoto(line)
            
            #goto command, we put it after if-goto because we don't want it to match on a if-goto
            elif "goto" in line:
                new_lines = new_lines + goto(line)
            
            elif "function" in line:
                new_lines = new_lines + func(line)
            
            elif "return" in line:
                new_lines = new_lines + ret(line)
            
            elif "call" in line:
                label = "call_counter_"+str(call_counter)
                call_counter += 1 
                new_lines = new_lines + call(line, label)

            else:
                new_lines = new_lines + [line]

    # add exit loop at the end
    new_lines = new_lines + ["(EXIT)", "@EXIT", "0;JMP"]
    write_file(path, new_lines, "asm")
    return

if __name__ == '__main__':
    main()

    