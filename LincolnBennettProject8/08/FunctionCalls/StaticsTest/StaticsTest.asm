//bootstrap code 
@256
D=A
@SP
M=D
 
// call Sys.init 0 operation
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
@Sys.init
0;JMP
(call_counter_1)
 
// function Sys.init 0 operation
(Sys.init)
//push constant operation
@6
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant operation
@8
D=A
@SP
A=M
M=D
@SP
M=M+1

// call Class1.set 2 operation
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
@7
D=D-A
@ARG
M=D
 
//LCL = SP
@SP
D=M
@LCL
M=D
@Class1.set
0;JMP
(call_counter_2)
 
//pop 5 0 operation
@5
D=A
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
@23
D=A
@SP
A=M
M=D
@SP
M=M+1

//push constant operation
@15
D=A
@SP
A=M
M=D
@SP
M=M+1

// call Class2.set 2 operation
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
@7
D=D-A
@ARG
M=D
 
//LCL = SP
@SP
D=M
@LCL
M=D
@Class2.set
0;JMP
(call_counter_3)
 
//pop 5 0 operation
@5
D=A
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
 
// call Class1.get 0 operation
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
@5
D=D-A
@ARG
M=D
 
//LCL = SP
@SP
D=M
@LCL
M=D
@Class1.get
0;JMP
(call_counter_4)
 
// call Class2.get 0 operation
//push return address
@call_counter_5
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
@Class2.get
0;JMP
(call_counter_5)
 
(WHILE)
// goto WHILE operation
@WHILE
0;JMP
 
// function Class2.set 0 operation
(Class2.set)
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

//pop static 0 operation
@SP
AM=M-1
D=M
@StaticsTest.0
M=D

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

//pop static 1 operation
@SP
AM=M-1
D=M
@StaticsTest.1
M=D

//push constant operation
@0
D=A
@SP
A=M
M=D
@SP
M=M+1

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
D=M
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
AM=M-1
D=M
@THAT
M=D
//THIS = *(R13-2), restore THIS of the caller
@R13
AM=M-1
D=M
@THIS
M=D
//ARG = *(R13-3), restore ARG of the caller
@R13
AM=M-1
D=M
@ARG
M=D
//LCL = *(R13-4), restore ARG of the caller
@R13
AM=M-1
D=M
@LCL
M=D
//goto *R14
@R14
A=M
0;JMP
 
// function Class2.get 0 operation
(Class2.get)
//push static 0 operation
@StaticsTest.0
D=M
@SP
A=M
M=D
@SP
M=M+1 //increment stack pointer

//push static 1 operation
@StaticsTest.1
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
D=M
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
AM=M-1
D=M
@THAT
M=D
//THIS = *(R13-2), restore THIS of the caller
@R13
AM=M-1
D=M
@THIS
M=D
//ARG = *(R13-3), restore ARG of the caller
@R13
AM=M-1
D=M
@ARG
M=D
//LCL = *(R13-4), restore ARG of the caller
@R13
AM=M-1
D=M
@LCL
M=D
//goto *R14
@R14
A=M
0;JMP
 
// function Class1.set 0 operation
(Class1.set)
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

//pop static 0 operation
@SP
AM=M-1
D=M
@StaticsTest.0
M=D

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

//pop static 1 operation
@SP
AM=M-1
D=M
@StaticsTest.1
M=D

//push constant operation
@0
D=A
@SP
A=M
M=D
@SP
M=M+1

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
D=M
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
AM=M-1
D=M
@THAT
M=D
//THIS = *(R13-2), restore THIS of the caller
@R13
AM=M-1
D=M
@THIS
M=D
//ARG = *(R13-3), restore ARG of the caller
@R13
AM=M-1
D=M
@ARG
M=D
//LCL = *(R13-4), restore ARG of the caller
@R13
AM=M-1
D=M
@LCL
M=D
//goto *R14
@R14
A=M
0;JMP
 
// function Class1.get 0 operation
(Class1.get)
//push static 0 operation
@StaticsTest.0
D=M
@SP
A=M
M=D
@SP
M=M+1 //increment stack pointer

//push static 1 operation
@StaticsTest.1
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
D=M
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
AM=M-1
D=M
@THAT
M=D
//THIS = *(R13-2), restore THIS of the caller
@R13
AM=M-1
D=M
@THIS
M=D
//ARG = *(R13-3), restore ARG of the caller
@R13
AM=M-1
D=M
@ARG
M=D
//LCL = *(R13-4), restore ARG of the caller
@R13
AM=M-1
D=M
@LCL
M=D
//goto *R14
@R14
A=M
0;JMP
 
