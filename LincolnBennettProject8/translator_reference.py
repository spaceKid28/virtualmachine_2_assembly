"""
This python file converts the given .vm file with hack computer virtual machine code to assembly language code in the
same folder in which the vm file is kept. Following operations are performed on the code:
1. Remove any user comments and whitespace
2. convert vm line to asm line of codes, along with the vm line as comment to show the origin of the code
3. all the new lines are stored in the asm file in the same folder
"""
from lzma import LZMAFile

from commentRemover import slimFile, write_cleaned_file
import sys, os, glob




## variable used to keep track of global variable used along with the file name which are not defined in the asm file
global block_track, retCounter, file_wise_labels
block_track = 0
retCounter = 0
file_wise_labels = {} # location of all the labels in the file
## memory operations
"""
Memory operation have different logic based on the memory segment it need to push or pop into, here we are hadling
1. local
2. Argument
3. this
4. that
5. temp
6. static
7. pointer
8. constant
"""
def convert_push(command, file_name):
    """
    Given a push command converts it to the asm code with proper memory  segmentation  handling
    :param command: vm line of code
    :param filename: name of file that is getting converted used for naming vars
    :return: converted str of asm code
    """
    if "push" not in command:
        return
    cmnd_parts = command.split(" ")  # pop <segment> <something>
    if cmnd_parts[1] == "local":
        conv_lines = f"@LCL\nD=M\n@13\nM=D\n@{cmnd_parts[2]}\nD=A\n@13\nM=D+M\nA=M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
    elif cmnd_parts[1] == "argument":
        conv_lines = f"@ARG\nD=M\n@13\nM=D\n@{cmnd_parts[2]}\nD=A\n@13\nM=D+M\nA=M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
    elif cmnd_parts[1] == "this":
        conv_lines = f"@THIS\nD=M\n@13\nM=D\n@{cmnd_parts[2]}\nD=A\n@13\nM=D+M\nA=M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
    elif cmnd_parts[1] == "that":
        conv_lines = f"@THAT\nD=M\n@13\nM=D\n@{cmnd_parts[2]}\nD=A\n@13\nM=D+M\nA=M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
    elif cmnd_parts[1] == "temp":
        if int(cmnd_parts[2]) >= 0 and int(cmnd_parts[2]) <= 7:
            conv_lines = f"@5\nD=A\n@13\nM=D\n@{cmnd_parts[2]}\nD=A\n@13\nM=D+M\nA=M\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"

    elif cmnd_parts[1] == "static":
        # Check if Static Variable lies within the range 
        if int(cmnd_parts[2]) >= 0 and int(cmnd_parts[2]) <= 238:  # 16-255
            conv_lines = f"@{file_name}.{cmnd_parts[2]}\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
    elif cmnd_parts[1] == "pointer":
        if cmnd_parts[2] in ["0", "1"]:
            if cmnd_parts[2] == "0":
                conv_lines = f"@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
            else:
                conv_lines = f"@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1"
    elif cmnd_parts[1] == "constant":
        conv_lines = f"@{cmnd_parts[2]}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1"
    else:
        raise Exception("Invalid Push Instruction : " + str(command))
    
    return conv_lines

def convert_pop(command, filename):
    """
    Given a pop command converts it to the asm code with proper memory  segmentation  handling
    :param command: vm line of code
    :param filename: name of file that is getting converted used for naming vars
    :return: converted str of asm code
    """
    if "pop" not in command:
        return

    cmnd_parts = command.split(" ") # pop <segment> <something>
    if cmnd_parts[1] == "local":
        conv_lines = f"@LCL\nD=M\n@13\nM=D\n@{cmnd_parts[2]}\nD=A\n@13\nM=D+M\n@SP\nM=M-1\nA=M\nD=M\n@13\nA=M\nM=D"
    elif cmnd_parts[1] == "argument":
        conv_lines = f"@ARG\nD=M\n@13\nM=D\n@{cmnd_parts[2]}\nD=A\n@13\nM=D+M\n@SP\nM=M-1\nA=M\nD=M\n@13\nA=M\nM=D"
    elif cmnd_parts[1] == "this":
        conv_lines = f"@THIS\nD=M\n@13\nM=D\n@{cmnd_parts[2]}\nD=A\n@13\nM=D+M\n@SP\nM=M-1\nA=M\nD=M\n@13\nA=M\nM=D"
    elif cmnd_parts[1] == "that":
        conv_lines = f"@THAT\nD=M\n@13\nM=D\n@{cmnd_parts[2]}\nD=A\n@13\nM=D+M\n@SP\nM=M-1\nA=M\nD=M\n@13\nA=M\nM=D"
    elif cmnd_parts[1] == "temp":
        if int(cmnd_parts[2]) >= 0 and int(cmnd_parts[2]) <= 7:
            conv_lines = f"@5\nD=A\n@13\nM=D\n@{cmnd_parts[2]}\nD=A\n@13\nM=D+M\n@SP\nM=M-1\nA=M\nD=M\n@13\nA=M\nM=D"
    elif cmnd_parts[1] == "static":
        # Check if Static Variable lies within the range 
        if int(cmnd_parts[2]) >= 0 and int(cmnd_parts[2]) <= 238:  # 16-255
            conv_lines = f"@{filename}.{cmnd_parts[2]}\nD=A\n@R15\nM=D\n@SP\nAM=M-1\nD=M\n@R15\nA=M\nM=D"

    elif cmnd_parts[1] == "pointer":
        if cmnd_parts[2] in ["0", "1"]:
            if cmnd_parts[2] == "0":
                conv_lines = f"""@SP\nM=M-1\nA=M\nD=M\n@THIS\nM=D"""
            else:
                conv_lines = f"@SP\nM=M-1\nA=M\nD=M\n@THAT\nM=D"
    else:
        raise Exception("Invalid Pop Instruction : " + str(cmnd_parts))

    return conv_lines

## arithemetic, Equality testing and Logical operation conversion to asm

def convert_add(command):
    output = "@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=D+M\n@SP\nM=M+1"
    return output

def convert_sub(command):
    output = "@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=M-D\n@SP\nM=M+1"
    return output

def convert_neg(command):
    output = "@SP\nM=M-1\nA=M\nM=-M\n@SP\nM=M+1"
    return output


def convert_eq(command):
    global block_track
    output = "@SP\nM=M-1\nA=M\nD=M\nA=A-1\nD=M-D\n@block_start_" + str(
        block_track) + "\nD;JEQ\n@SP\nA=M-1\nM=0\n@block_end_" + str(block_track) + "\n0;JMP\n(block_start_" + str(
        block_track) + ")\n@SP\nA=M-1\nM=-1\n(block_end_" + str(block_track) + ")"
    block_track += 1
    return output

def convert_gt(command):
    global block_track
    output = "@SP\nM=M-1\nA=M\nD=M\nA=A-1\nD=M-D\n@block_start_" + str(
        block_track) + "\nD;JGT\n@SP\nA=M-1\nM=0\n@block_end_" + str(block_track) + "\n0;JMP\n(block_start_" + str(
        block_track) + ")\n@SP\nA=M-1\nM=-1\n(block_end_" + str(block_track) + ")"
    block_track += 1
    return output

def convert_lt(command):
    global block_track
    output = "@SP\nM=M-1\nA=M\nD=M\nA=A-1\nD=M-D\n@block_start_" + str(
        block_track) + "\nD;JLT\n@SP\nA=M-1\nM=0\n@block_end_" + str(block_track) + "\n0;JMP\n(block_start_" + str(
        block_track) + ")\n@SP\nA=M-1\nM=-1\n(block_end_" + str(block_track) + ")"
    block_track += 1
    return output
# logical operations

def convert_and(command):
    output = "@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=D&M\n@SP\nM=M+1"
    return output

def convert_or(command):
    output = "@SP\nM=M-1\nA=M\nD=M\n@SP\nM=M-1\nA=M\nM=D|M\n@SP\nM=M+1"
    return output

def convert_not(command):
    output="@SP\nM=M-1\nA=M\nM=!M\n@SP\nM=M+1"
    return output

# branching commands
def convert_branching_command(command):
    """
    converts a given branching command in the vm file to the asm file
    :param command:
    :return: asm_code: str
    """
    asm_code = None
    parts = command.split(" ")
    if parts[1] not in file_wise_labels: # key is part-1 - has to be there
        raise Exception("Label Not Found", command)

    elif parts[0] == "label": # this define label - we have pre-processed them for the file
        # the scope of the label has to be in the file itself - this can't jump directly to other file label - verify
        asm_code = f"({file_wise_labels.get(parts[1])})"
        # Goto : Unconditional Jump
    elif parts[0] == "goto":
        label_asm_name = file_wise_labels.get(parts[1])
        asm_code = f"@{label_asm_name}\n0;JMP\n"
        # If-goto : Conditional Jump
    elif parts[0] == "if-goto":
        # ToDo redo this
        label_asm_name = file_wise_labels.get(parts[1])
        asm_code = f"\n@SP\nM=M-1\nA=M\nD=M\n@{label_asm_name}\nD;JNE\n"
    else:
        raise Exception("Invalid Branching statement!!", command)
    return asm_code

def convert_function_define_command(command):
    #  function <funcName> nLocals -> function Main.fibonacci 0
    if "function" not in command:
        raise Exception("Not a valid define function command: ", command)
    parts = command.split(" ")
    funcName = parts[1]
    num_locals = int(parts[2])
    # Making the function as a label in Hack Assembly
    funcCode = f"({funcName})\n"
    for i in range(num_locals):
        # Making Space for Local Variables
        funcCode += "@SP\nA=M\nM=0\n@SP\nM=M+1\n"
    return funcCode


def convert_function_call_command(command):
    """
    call <funcname> nArgs -> something
    call Main.fibonacci 1
    :param command:
    :return:
    """
    global retCounter
    parts = command.split(" ")
    func_name = parts[1] # name of function
    nArgs = int(parts[2])
    return_adr = f"{func_name}$ret.{retCounter}"
    retCounter += 1
    # Saving the frame [Return Address; LCL; ARG; THIS; THAT] - will reuse at time of return
    asm_code = f"@{return_adr}\nD=A\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" # 1. Push the return address to the stack
    asm_code += "@LCL\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" # 2. Save the LCL pointer (Local Segment)
    asm_code += "@ARG\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" # 3. Save the ARG pointer
    asm_code += "@THIS\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n"# 4. Save the THIS pointer
    asm_code += "@THAT\nD=M\n@SP\nA=M\nM=D\n@SP\nM=M+1\n" # 5. Save the THAT pointer
    asm_code += f"@SP\nD=M\n@{nArgs}\nD=D-A\n@5\nD=D-A\n@ARG\nM=D\n" # 6. Reposition the ARG pointer for the function call's arguments
    # ARG = SP - (nArgs + 5)
    asm_code += f"@SP\nD=M\n@LCL\nM=D\n"  # 7. Reposition the LCL pointer
    asm_code += f"@{func_name}\n0;JMP\n" # 8. Jump to the callee function - this is the address of the callee function
    # when we define a function this will be declared explicitly
    asm_code += f"({return_adr})\n" # 8. defining-Jump back address to the function
    # we have set this address as the first value in our frame, when the callee is done we will return to this line here
    # because this address is defined here, to-return-back pointer will always be defined by caller function.
    # we have the Main.fibonacci$ret.2 a counter at the end of it because multiple function can call a same function
    # so we need to store where to go back - though this can be based on the current function line number as well.
    # but make call more readable that we are expecting which callee function to end here.
    return asm_code


def convert_function_return_command(command):
    """ Given a function return command perform the operation to return the caller function by Doing
    1. Reset SP to the ARG[0]
    2. set the return value in SP-1 address
    3. flush out the current function stack and jump back to the caller function in ROM
    """
    # call return; handle it properly
    asm_code = (
        "@LCL\nD=M\n@13\nM=D\n"  # Save the current LCL (frame pointer) in R13
        "@5\nA=D-A\nD=M\n@14\nM=D\n"  # Save return address (LCL-5) in R14
        "@SP\nAM=M-1\nD=M\n@ARG\nA=M\nM=D\n"  # Move return value to ARG[0] - note return value is current at *SP-1, top of current function stack 
        "@ARG\nD=M+1\n@SP\nM=D\n"  # Reposition SP to ARG+1
        "@13\nAM=M-1\nD=M\n@THAT\nM=D\n"  # Restore THAT of the caller
        "@13\nAM=M-1\nD=M\n@THIS\nM=D\n"  # Restore THIS of the caller
        "@13\nAM=M-1\nD=M\n@ARG\nM=D\n"  # Restore ARG of the caller
        "@13\nAM=M-1\nD=M\n@LCL\nM=D\n"  # Restore LCL of the caller
        "@14\nA=M\n0;JMP\n"  # Jump to the return address saved in R14
    )
    return asm_code


def convert_push_pop_command(line, file_name):
    """
    handles the push and pop command of the function
    :param line:
    :param file_name:
    :return:
    """
    asm_code = None
    file_base_name = file_name.split(".")[0]
    if 'push' in line:
        asm_code = convert_push(line, file_base_name)

    elif 'pop' in line:
        asm_code = convert_pop(line, file_base_name)
    else:
        raise Exception("Invalid: Push/Pop Command Detected: " + str(line))

    return asm_code



def convert_Arithmetic_logical_command(line):
    """
    This function aggregate all the arithmetic operations output in one place

    Raise Exception if line doesn't contain any valid operations.
    :param line: has to be valid arithemetic operation
    :return: asm lines
    """
    asm_code = None;
    if 'add' in line:
        asm_code = convert_add(line)
    elif 'sub' in line:
        asm_code = convert_sub(line)
    elif 'neg' in line:
        asm_code = convert_neg(line)
    elif 'eq' in line:
        asm_code = convert_eq(line)
    elif 'gt' in line:
        asm_code = convert_gt(line)
    elif 'lt' in line:
        asm_code = convert_lt(line)
    elif 'and' in line:
        asm_code = convert_and(line)
    elif 'or' in line:
        asm_code = convert_or(line)
    elif 'not' in line:
        asm_code = convert_not(line)
    else:
        raise Exception("UnRecognised Command Detected: " + str(line))

    return asm_code


def convert_vmcode_line_to_asm_code(line, file_name):
    """
    Given a line of vm code this function converts it to the asm code line
    :param line: vm code line
    :return: asm_code:str -  string of asm code
    """

    parts = line.split(" ")
    asm_code = None
    if len(parts)==1:
        #  single part command can be either return or mathematical operations only
        if "return" in line:
            asm_code = convert_function_return_command(line)
        else:
            asm_code = convert_Arithmetic_logical_command(line)
        # can throw error if the command is not valid

    elif len(parts)==2:
        # only Branching Statements-have two parts so this must be branching command
        asm_code = convert_branching_command(line)
        # will throw error if not a valid branching command
    elif len(parts)==3:
        # Function Declaration - function Main.fibonacci 0
        if parts[0]=="function":
            asm_code = convert_function_define_command(line)
        # Function Call - call Main.fibonacci 1
        elif parts[0]=="call":
            asm_code = convert_function_call_command(line)
        # Push / Pop
        else:
            # this will throw error if command passed is not push and pop
            asm_code = convert_push_pop_command(line, file_name)
    else:
        raise Exception("Invalid VM Command Detected:  " + str(line))

    return asm_code




def convert_vmfile_to_asmfile(vm_file_lines, file_name):
    """
    given a vm file, this function converts it to asm code

    :param vm_file_lines:
    :param file_path:
    :return:
    """
    converted_lines = [f"// converting file: {file_name} ------> "]
    for line in vm_file_lines:
        # Memory type
        comment_line = "\n//" + line
        converted_lines.append(comment_line) # add this as comment
        new_asm_code_lines = "// failed command here "
        new_asm_code_lines = convert_vmcode_line_to_asm_code(line, file_name)
        converted_lines.append(new_asm_code_lines)
    converted_lines.append("\n")
    return converted_lines

def process_labels(file_lines, file_name):
    """
    Step-2: convert all the label used in the file to a dictionary to be use later
    :param file_lines: all lines in the file
    :param file_name: given file name
    :return: None
    """
    global file_wise_labels
    file_wise_labels = {}
    crnt_func_name = None # if the label is inside a function save its name
    for line in file_lines:
        parts = line.split(" ")
        if "function" in line: # function Main.fibonacci 0
            crnt_func_name = parts[1] # middle parts become function name
        elif "label" in line:
            # label N_LT_2 --> Main.fibonacci$N_LT_2
            if crnt_func_name is not None:
                file_wise_labels[parts[1]] = f"{crnt_func_name}${parts[1]}"
            else:
                file_wise_labels[parts[1]] = parts[1]

def process_single_file(file_path):
    """ End to end handling for single file
    1. remove comments
    2. Process labels
    3. convert the raw vm code to asm
    :param file_path:
    :return: list[str] - of asm code of the file
    """

    file_name = os.path.basename(file_path)
    # step-1 remove comment and white spaces
    slim_file_lines = slimFile(file_path)

    # step-2 process all labels
    process_labels(slim_file_lines, file_name)

    # step-3
    asm_file_lines = convert_vmfile_to_asmfile(slim_file_lines, file_name)

    return asm_file_lines

"""
This is the main function for handling the translation the order of execution of function is as follows:
1. Loop handles multiple file case
2. process_single_file - convert a single file code to asm, remove comments, process labels and convert vm code to asm
3. convert_vmfile_to_asmfile- line by line process the vm code and convert it to asm code
4. convert_vmcode_line_to_asm_code: given a single line of vm code convert it to asm code lines
5. there are multiple case by case function to support all the conversions

"""

if __name__ == '__main__':
    argumentList = sys.argv[1:]
    #
    # main_path = sys.argv[1]

    # initial code needed to start the pre-defined variable to expected value
    # used only when the sys file is given.
    start_code = "\n//Start proces -->\n"  # comment only needed when there is a sys file
    start_code += "\n// Set SP\n@256\nD=A\n@SP\nM=D\n\n"  # set SP pointer
    start_code += "//call Sys.init 0 \n"
    start_code += convert_function_call_command("call Sys.init 0") # call sys by default
    """ Optional - not doing for now 
    start_code += "\n// Set local\n@600\nD=A\n@LCL\nM=D\n"  # set local pointer
    start_code += "\n// Set ARG\n@700\nD=A\n@ARG\nM=D\n"  # set ARG pointer
    start_code += "\n// Set this\n@3000\nD=A\n@THIS\nM=D\n"  # set this
    start_code += "\n// Set that\n@3010\nD=A\n@THAT\nM=D\n"  # set that
    """
    total_asm_file_lines = []  # set SP to 256 at the start of the code

    for main_path in glob.glob("../input_file/*/*/"):
        folder_name = os.path.basename(os.path.normpath(main_path))
        total_asm_file_lines = []

        if (os.path.isfile(main_path)):
            folder_path = os.path.dirname(main_path)
            total_asm_file_lines += process_single_file(main_path)
            main_path = folder_path

        else:
            all_vm_files = glob.glob(os.path.join(main_path, "*.vm"))
            non_sys_asm_file_lines = []
            for file_path in all_vm_files: # take all the vm file in the current folder
                single_file_asm_code = process_single_file(file_path)
                if "Sys.vm" in file_path:
                    total_asm_file_lines = [start_code]
                    total_asm_file_lines+=single_file_asm_code
                else:
                   non_sys_asm_file_lines+=single_file_asm_code

            total_asm_file_lines+=non_sys_asm_file_lines # non sys file comes below sys

            total_asm_file_lines.append("\n(END)\n@END\n0;JMP\n") # End of the program, stays at this line

        # step-4: Write the output content to a new file
        out_file_path = os.path.join(main_path, f"{folder_name}.asm")
        write_cleaned_file(out_file_path, total_asm_file_lines)

