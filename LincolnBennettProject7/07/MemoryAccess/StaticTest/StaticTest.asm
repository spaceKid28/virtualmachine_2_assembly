//push constant operation
@111
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant operation
@333
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant operation
@888
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop static 8 operation
@SP
AM=M-1
D=M
@StaticTest.8
M=D

//pop static 3 operation
@SP
AM=M-1
D=M
@StaticTest.3
M=D

//pop static 1 operation
@SP
AM=M-1
D=M
@StaticTest.1
M=D

//push static 3 operation
@StaticTest.3
D=M
@SP
A=M
M=D
@SP
M=M+1 //increment stack pointer

//push static 1 operation
@StaticTest.1
D=M
@SP
A=M
M=D
@SP
M=M+1 //increment stack pointer

//sub
@SP
AM=M-1
D=M
A=A-1
M=M-D

//push static 8 operation
@StaticTest.8
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

