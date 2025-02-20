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

// call Main.fibonacci 1 operation
//push return address
@call_counter_2
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
@6
D=D-A
@ARG
M=D
 
//LCL = SP
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(call_counter_2)
 
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

//lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
M=-1
@continue0
D;JLT
@SP
A=M-1
M=0
(continue0)

// if-goto IF_TRUE operation
@SP
AM=M-1
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

@LCL
D=M
@13
M=D

@5
A=D-A
D=M
@14
M=D

@SP
AM=M-1
D=M
@ARG
A=M
M=D

@ARG
D=M+1
@SP
M=D
@13
AM=M-1
D=M
@THAT
M=D

@13
AM=M-1
D=M
@THIS
M=D

@13
AM=M-1
D=M
@ARG
M=D

@13
AM=M-1
D=M
@LCL
M=D

@14
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

// call Main.fibonacci 1 operation
//push return address
@call_counter_3
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
@6
D=D-A
@ARG
M=D
 
//LCL = SP
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(call_counter_3)
 
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

// call Main.fibonacci 1 operation
//push return address
@call_counter_4
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
@6
D=D-A
@ARG
M=D
 
//LCL = SP
@SP
D=M
@LCL
M=D
@Main.fibonacci
0;JMP
(call_counter_4)
 
//add
@SP
AM=M-1
D=M
A=A-1
M=D+M

@LCL
D=M
@13
M=D

@5
A=D-A
D=M
@14
M=D

@SP
AM=M-1
D=M
@ARG
A=M
M=D

@ARG
D=M+1
@SP
M=D
@13
AM=M-1
D=M
@THAT
M=D

@13
AM=M-1
D=M
@THIS
M=D

@13
AM=M-1
D=M
@ARG
M=D

@13
AM=M-1
D=M
@LCL
M=D

@14
A=M
0;JMP

