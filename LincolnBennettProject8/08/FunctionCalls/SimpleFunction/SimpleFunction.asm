//bootstrap code 
@256
D=A
@SP
M=D
@Sys.init
0;JMP
 
// function SimpleFunction.test 2 operation
@SP
AM=M+1 //increment stack pointer and address in A
A=A-1 //Note, we have already incremented SP, we adjust to set to 0
M=0
 
@SP
AM=M+1 //increment stack pointer and address in A
A=A-1 //Note, we have already incremented SP, we adjust to set to 0
M=0
 
//push LCL 0 operation
@LCL
D=M
@0
A=D+A
D=M //stores value in D register of RAM[{mem_location} + x]
@SP
A=M
M=D //set value at top of stack to D
@SP
M=M+1 //increment stack pointer

//push LCL 1 operation
@LCL
D=M
@1
A=D+A
D=M //stores value in D register of RAM[{mem_location} + x]
@SP
A=M
M=D //set value at top of stack to D
@SP
M=M+1 //increment stack pointer

//add
@SP
AM=M-1
D=M
A=A-1
M=D+M

//not
@SP
A=M-1
M=!M

//push ARG 0 operation
@ARG
D=M
@0
A=D+A
D=M //stores value in D register of RAM[{mem_location} + x]
@SP
A=M
M=D //set value at top of stack to D
@SP
M=M+1 //increment stack pointer

//add
@SP
AM=M-1
D=M
A=A-1
M=D+M

//push ARG 1 operation
@ARG
D=M
@1
A=D+A
D=M //stores value in D register of RAM[{mem_location} + x]
@SP
A=M
M=D //set value at top of stack to D
@SP
M=M+1 //increment stack pointer

//sub
@SP
AM=M-1
D=M
A=A-1
M=M-D

// return operation
//R13=LCL
@LCL
D=M
@R13
M=D
//R14 = *(R13 - 5)
@LCL
D=M
@5
A=D-A
D=M
@R14
M=D
//*ARG = pop(), 
@SP
A=M-1
@ARG
A=M
M=D
//SP =ARG+1 restore the SP of the caller
@ARG
D=M+1
@SP
M=D
//THAT = *(R13-1), restore THAT of the caller
@R13
AM = M-1
D=M
@THAT
M=D
//THIS = *(R13-2), restore THIS of the caller
@R13
AM = M-1
D=M
@THIS
M=D
//ARG = *(R13-3), restore ARG of the caller
@R13
AM = M-1
D=M
@ARG
M=D
//LCL = *(R13-4), restore ARG of the caller
@R13
AM = M-1
D=M
@LCL
M=D
//goto *R14
@R14
A=M
0;JMP
 
