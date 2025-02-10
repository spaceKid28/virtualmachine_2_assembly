//push constant operation
@17
D=A
@SP
AM=M+1
A=A-1
M=D

//push constant operation
@17
D=A
@SP
AM=M+1
A=A-1
M=D

//eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
M=-1
@continue0
D;JEQ
@SP
A=M-1
M=0
(continue0)

//push constant operation
@17
D=A
@SP
AM=M+1
A=A-1
M=D

//push constant operation
@16
D=A
@SP
AM=M+1
A=A-1
M=D

//eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
M=-1
@continue1
D;JEQ
@SP
A=M-1
M=0
(continue1)

//push constant operation
@16
D=A
@SP
AM=M+1
A=A-1
M=D

//push constant operation
@17
D=A
@SP
AM=M+1
A=A-1
M=D

//eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
M=-1
@continue2
D;JEQ
@SP
A=M-1
M=0
(continue2)

//push constant operation
@892
D=A
@SP
AM=M+1
A=A-1
M=D

//push constant operation
@891
D=A
@SP
AM=M+1
A=A-1
M=D

//lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
M=-1
@continue3
D;JLT
@SP
A=M-1
M=0
(continue3)

//push constant operation
@891
D=A
@SP
AM=M+1
A=A-1
M=D

//push constant operation
@892
D=A
@SP
AM=M+1
A=A-1
M=D

//lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
M=-1
@continue4
D;JLT
@SP
A=M-1
M=0
(continue4)

//push constant operation
@891
D=A
@SP
AM=M+1
A=A-1
M=D

//push constant operation
@891
D=A
@SP
AM=M+1
A=A-1
M=D

//lt
@SP
AM=M-1
D=M
A=A-1
D=M-D
M=-1
@continue5
D;JLT
@SP
A=M-1
M=0
(continue5)

//push constant operation
@32767
D=A
@SP
AM=M+1
A=A-1
M=D

//push constant operation
@32766
D=A
@SP
AM=M+1
A=A-1
M=D

//gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
M=-1
@continue6
D;JGT
@SP
A=M-1
M=0
(continue6)

//push constant operation
@32766
D=A
@SP
AM=M+1
A=A-1
M=D

//push constant operation
@32767
D=A
@SP
AM=M+1
A=A-1
M=D

//gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
M=-1
@continue7
D;JGT
@SP
A=M-1
M=0
(continue7)

//push constant operation
@32766
D=A
@SP
AM=M+1
A=A-1
M=D

//push constant operation
@32766
D=A
@SP
AM=M+1
A=A-1
M=D

//gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
M=-1
@continue8
D;JGT
@SP
A=M-1
M=0
(continue8)

//push constant operation
@57
D=A
@SP
AM=M+1
A=A-1
M=D

//push constant operation
@31
D=A
@SP
AM=M+1
A=A-1
M=D

//push constant operation
@53
D=A
@SP
AM=M+1
A=A-1
M=D

//add
@SP
AM=M-1
D=M
A=A-1
M=D+M
//push constant operation
@112
D=A
@SP
AM=M+1
A=A-1
M=D

//sub
@SP
AM=M-1
D=M
A=A-1
M=D-M
//neg
@SP
A=M-1
M=-M

//and
@SP
AM=M-1
D=M
A=A-1
M=D&M

//push constant operation
@82
D=A
@SP
AM=M+1
A=A-1
M=D

//or
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
M=D|M
@SP
M=M+1

//not
@SP
A=M-1
A=M
M=!M
@SP
M=M+1

