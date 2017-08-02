// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Divide.asm

// divides R13 and R14 and stores the result in R15.
// (R13, R14, R15 refer to RAM[13], RAM[14], and RAM[15], respectively.)
//The program input will be at R13,R14 while the result R13/R14 will be store at R15.
//The remainder should be discarded.
//You may assume both numbers are positive.
//The program should have a running time logarithmic with respect to the input.


	@R13
	D=M
	
	@divident					// number to divide
	M=D
	
	@quotient 					// output
	M=0
	
	@current_base 
	M=1
	
	@R14
	D=M
	
	@current_divisor			// number to divide by
	M=D 
	
	
	
(LOOP)
	
	@divident					// while divident >= divisor
	D=M 
	
	@R14
	D=D-M
	
	
	@END					
	D;JLT
	
	@divident					// if divident >= current_divisor
	D=M
	
	@current_divisor
	D=D-M 
	
	@X					
	D;JLT
	
	@current_divisor
	D=M 
	
	@divident					// divident -= current_divisor
	M=M-D 
	
	@current_base
	D=M
	
	@quotient					// quotient += current_base
	M=M+D
	
	@current_divisor			// current_divisor *= 2
	M=M<<
	
	@current_base				// current_base *= 2
	M=M<<
	
	
	@LOOP
	0;JMP
	
	
	
(X)
	@current_divisor			// current_divisor /= 2
	M=M>>
	
	@current_base				// current_base /= 2
	M=M>>
	
	@LOOP
	0;JMP
	
	
(END)


	@quotient
	D=M 

	@R15
	M=D
	
	
	
	
	
	
	