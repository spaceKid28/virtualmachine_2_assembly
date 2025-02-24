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

//pop pointer 1 operation
@SP
AM=M-1
D=M
@THAT
M=D

//push constant operation
@0
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop THAT 0 operation
@THAT
D=M
@0
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
 
//push constant operation
@1
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop THAT 1 operation
@THAT
D=M
@1
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
 
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

//pop ARG 0 operation
@ARG
D=M
@0
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
 
(MAIN_LOOP_START)
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

// if-goto COMPUTE_ELEMENT operation
@SP
AM=M-1
D=M
@COMPUTE_ELEMENT
D;JNE
 
// goto END_PROGRAM operation
@END_PROGRAM
0;JMP
 
(COMPUTE_ELEMENT)
//push THAT 0 operation
@THAT
D=M
@0
A=D+A
D=M //stores value in D register of RAM[{mem_location} + x]
@SP
A=M
M=D //set value at top of stack to D
@SP
M=M+1 //increment stack pointer

//push THAT 1 operation
@THAT
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

//pop THAT 2 operation
@THAT
D=M
@2
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
 
//push pointer 1 operation
@THAT
D=M
@SP
A=M
M=D
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

//add
@SP
AM=M-1
D=M
A=A-1
M=D+M

//pop pointer 1 operation
@SP
AM=M-1
D=M
@THAT
M=D

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

//pop ARG 0 operation
@ARG
D=M
@0
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
 
// goto MAIN_LOOP_START operation
@MAIN_LOOP_START
0;JMP
 
(END_PROGRAM)
(EXIT)
@EXIT
0;JMP
