//bootstrap code 
@256
D=A
@SP
M=D
 
// call sys.init 0 operation
//push return address
@call_counter_1
D=A
@SP
AM=M+1
A=A-1
M=D
 
//push LCL
@LCL
D=M
@SP
AM=M+1
A=A-1
M=D
 
//push ARG 
@ARG
D=M
@SP
AM=M+1
A=A-1
M=D
 
//push THIS 
@THIS
D=M
@SP
AM=M+1
A=A-1
M=D
 
//push THAT 
@THAT
D=M
@SP
AM=M+1
A=A-1
M=D
 
//ARG = SP - n - 5
@SP
D=M
@5
D=D-A
@ARG
M=D
 
//LCL = SP
@SP
D=M
@LCL
M=D
@sys.init
0;JMP
(call_counter_1)
 
// function Sys.init 0 operation
(Sys.init)
//push constant operation
@4
D=A
@SP
A=M
M=D
@SP
M=M+1

// call Main.fibonacci 1
@Main.fibonacci$ret.1
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@LCL
M=D
@5
D=D-A
@1
D=D-A
@ARG
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci$ret.1)
 
(WHILE)
// goto WHILE operation
@WHILE
0;JMP
 
// function Main.fibonacci 0 operation
(Main.fibonacci)
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

//push constant operation
@2
D=A
@SP
A=M
M=D
@SP
M=M+1

// lt 
@SP
AM=M-1
D=M
A=A-1
D=M-D
@c0_if_lt
D;JLT
D=0
@c0_else
0;JMP
(c0_if_lt)
D=-1
(c0_else)
@SP
A=M-1
M=D

// if-goto IF_TRUE operation
@SP
M=M-1
A=M
D=M
@IF_TRUE
D;JNE
 
// goto IF_FALSE operation
@IF_FALSE
0;JMP
 
(IF_TRUE)
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

// return 
@LCL
D=M
@R13
M=D
@5
A=D-A
D=M
@R14
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@R13
AM=M-1
D=M
@THAT
M=D
@R13
AM=M-1
D=M
@THIS
M=D
@R13
AM=M-1
D=M
@ARG
M=D
@R13
AM=M-1
D=M
@LCL
M=D
@R14
A=M
0;JMP
 
(IF_FALSE)
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

//push constant operation
@2
D=A
@SP
A=M
M=D
@SP
M=M+1

//sub
@SP
AM=M-1
D=M
A=A-1
M=M-D

// call Main.fibonacci 1
@Main.fibonacci$ret.2
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@LCL
M=D
@5
D=D-A
@1
D=D-A
@ARG
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci$ret.2)
 
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

//push constant operation
@1
D=A
@SP
A=M
M=D
@SP
M=M+1

//sub
@SP
AM=M-1
D=M
A=A-1
M=M-D

// call Main.fibonacci 1
@Main.fibonacci$ret.3
D=A
@SP
A=M
M=D
@SP
M=M+1
@LCL
D=M
@SP
A=M
M=D
@SP
M=M+1
@ARG
D=M
@SP
A=M
M=D
@SP
M=M+1
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1
@SP
D=M
@LCL
M=D
@5
D=D-A
@1
D=D-A
@ARG
M=D
@Main.fibonacci
0;JMP
(Main.fibonacci$ret.3)
 
//add
@SP
AM=M-1
D=M
A=A-1
M=D+M

// return 
@LCL
D=M
@R13
M=D
@5
A=D-A
D=M
@R14
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@R13
AM=M-1
D=M
@THAT
M=D
@R13
AM=M-1
D=M
@THIS
M=D
@R13
AM=M-1
D=M
@ARG
M=D
@R13
AM=M-1
D=M
@LCL
M=D
@R14
A=M
0;JMP
 
(EXIT)
@EXIT
0;JMP