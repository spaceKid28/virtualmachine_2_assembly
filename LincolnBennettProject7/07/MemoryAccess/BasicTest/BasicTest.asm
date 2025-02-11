//push constant operation
@10
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop LCL 0 operation
@LCL
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
@21
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant operation
@22
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop ARG 2 operation
@ARG
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

//pop ARG 1 operation
@ARG
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

//push constant operation
@36
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop THIS 6 operation
@THIS
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

//push constant operation
@42
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant operation
@45
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop THAT 5 operation
@THAT
D=M
@5
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D

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

//push constant operation
@510
D=A
@SP
A=M
M=D
@SP
M=M+1

//pop 5 6 operation
@5
D=A
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

//push THAT 5 operation
@THAT
D=M
@5
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

//push THIS 6 operation
@THIS
D=M
@6
A=D+A
D=M //stores value in D register of RAM[{mem_location} + x]
@SP
A=M
M=D //set value at top of stack to D
@SP
M=M+1 //increment stack pointer

//push THIS 6 operation
@THIS
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

//sub
@SP
AM=M-1
D=M
A=A-1
M=M-D

//push 5 6 operation
@5
D=A
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

