@256
D=A
@SP
M=D
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
@EQ_0_TRUE
D;JEQ
@SP
A=M-1
M=0
@EQ_0_END
0;JMP
(EQ_0_TRUE)
@SP
A=M-1
M=-1
(EQ_0_END)
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
@EQ_1_TRUE
D;JEQ
@SP
A=M-1
M=0
@EQ_1_END
0;JMP
(EQ_1_TRUE)
@SP
A=M-1
M=-1
(EQ_1_END)
// push constant 16
@16
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 17
@17
D=A
@SP
A=M
M=D
@SP
M=M+1
// eq
@SP
AM=M-1
D=M
A=A-1
D=M-D
@EQ_2_TRUE
D;JEQ
@SP
A=M-1
M=0
@EQ_2_END
0;JMP
(EQ_2_TRUE)
@SP
A=M-1
M=-1
(EQ_2_END)
// push constant 892
@892
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 891
@891
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
@LT_3_TRUE
D;JLT
@SP
A=M-1
M=0
@LT_3_END
0;JMP
(LT_3_TRUE)
@SP
A=M-1
M=-1
(LT_3_END)
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 892
@892
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
@LT_4_TRUE
D;JLT
@SP
A=M-1
M=0
@LT_4_END
0;JMP
(LT_4_TRUE)
@SP
A=M-1
M=-1
(LT_4_END)
// push constant 891
@891
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 891
@891
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
@LT_5_TRUE
D;JLT
@SP
A=M-1
M=0
@LT_5_END
0;JMP
(LT_5_TRUE)
@SP
A=M-1
M=-1
(LT_5_END)
// push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@GT_6_TRUE
D;JGT
@SP
A=M-1
M=0
@GT_6_END
0;JMP
(GT_6_TRUE)
@SP
A=M-1
M=-1
(GT_6_END)
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32767
@32767
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@GT_7_TRUE
D;JGT
@SP
A=M-1
M=0
@GT_7_END
0;JMP
(GT_7_TRUE)
@SP
A=M-1
M=-1
(GT_7_END)
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 32766
@32766
D=A
@SP
A=M
M=D
@SP
M=M+1
// gt
@SP
AM=M-1
D=M
A=A-1
D=M-D
@GT_8_TRUE
D;JGT
@SP
A=M-1
M=0
@GT_8_END
0;JMP
(GT_8_TRUE)
@SP
A=M-1
M=-1
(GT_8_END)
// push constant 57
@57
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 31
@31
D=A
@SP
A=M
M=D
@SP
M=M+1
// push constant 53
@53
D=A
@SP
A=M
M=D
@SP
M=M+1
// add
@SP
M=M-1
A=M
D=M
A=A-1
M=D+M
// push constant 112
@112
D=A
@SP
A=M
M=D
@SP
M=M+1
// sub
@SP
M=M-1
A=M
D=M
A=A-1
M=M-D
// neg
@SP
A=M-1
M=-M
// and
@SP
M=M-1
A=M
D=M
A=A-1
M=D&M
// push constant 82
@82
D=A
@SP
A=M
M=D
@SP
M=M+1
// or
@SP
M=M-1
A=M
D=M
A=A-1
M=D|M
// not
@SP
A=M-1
M=!M
