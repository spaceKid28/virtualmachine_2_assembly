//push constant operation
@0
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

(LOOP_START)
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

//add
@SP
AM=M-1
D=M
A=A-1
M=D+M

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

// if-goto LOOP_START opeartion
@SP
AM=M-1
D=M
@LOOP_START
D;JNE
 
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

