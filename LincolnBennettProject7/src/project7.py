import os
from src.util import parser, write_file, push_constant, arithmetic_operations


def main():
    import sys
    filename = sys.argv[1]
    lines = parser(filename)

    # new lines is list of lines that we will pass to write_file
    new_lines = []
    continues = [f"continue{x}" for x in range(10000)]
    for line in lines:
        if line in arithmetic_operations:
            commands = [f"//{line}"] + arithmetic_operations[line]
            # I can't use the same continue for all the JMPs, have to create continue0, continue1, continue3...
            new_continue = continues.pop(0)
            commands = [x.replace("continue", new_continue) if "continue" in x else x for x in commands]
            new_lines = new_lines + commands
        elif "push constant" in line:
            new_lines = new_lines + push_constant(line)
    # lines = symbolhandling(lines)
    # lines = symbolless_assembler(lines)
    write_file(filename, new_lines, "asm")
    return

if __name__ == '__main__':
    main()