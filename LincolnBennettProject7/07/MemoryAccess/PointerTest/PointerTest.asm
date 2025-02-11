//push constant operation
@3030
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop pointer 0 operation
@SP
AM=M-1
D=M
@THIS
M=D //increment stack pointer

//push constant operation
@3040
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop pointer 1 operation
@SP
AM=M-1
D=M
@THAT
M=D //increment stack pointer

//push constant operation
@32
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop THIS 2 operation
@THIS
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

//push constant operation
@46
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop THAT 6 operation
@THAT
D=M
@6
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D

//push pointer 0 operation
@THIS
D=M
@SP
A=M
M=D
@SP
M=M+1 //increment stack pointer

//push pointer 1 operation
@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1 //increment stack pointer

//add
@SP
AM=M-1
D=M
A=A-1
M=D+M

//push THIS 2 operation
@THIS
D=M
@2
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

//push THAT 6 operation
@THAT
D=M
@6
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

