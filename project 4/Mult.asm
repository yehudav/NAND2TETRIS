// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)



//-------------------------  initializing variables ----------------------------


    @R2                 //initializing R2 to 0

    M=0                 // R2 = 0

    @sum                // variable sum

    M=0                 // initialize sum = 0

    @i                  // initialize i = 0

    M=0

    @r0sign             // to checks if R0 > 0 and change it for loop and sum

    M=1

    @R0                 // set a variable with R0 value

    D=M

    @r0                 // the variable with R0 value

    M=D

//--------------------------  checks if R0 * R1 = 0 ----------------------------

    @R0                 // check if R0 or R1 = 0 - 0 * x = 0

    D=M

    @RESULT                // if R0 * R1 = 0 - go to end

    D;JEQ


//------------------------ use ABS(R0) to run the loop -------------------------

    @R0                 // if R0 > 0 start the loop

    D=M

    @LOOP               // jump to loop if R0 > 0

    D;JGT

    @r0sign             // if R0 <= 0 set the sign to 0 -> R0 < 0

    M=-M

    @r0                 // make r0 to - r0 for loop calculations

    M=-M

//------------------------------------------------------------------------------


(LOOP)                  // add R1 to sum R0 times

//---------------------- break loop - if i == R0 -------------------------------

    @i                  // if i = R0 break

    D=M                 // D = i

    @r0                 // r0 > 0 - assumption!!!!

    D=D-M               // D = i - R0

    @RESULT                // if D = 0 goto end - added R1 R0 times

    D;JEQ

//----------------------- for (i = 0 ; i < R0 ; i++) ---------------------------

    @R1                 // D = R1

    D=M

    @sum

    M=D+M               // sum += R1

    @i                  // i++

    M=M+1

    @LOOP

    0;JMP               // repeat the loop


//------------------------------------------------------------------------------

(RESULT)                // set R2 to be the sum

    @sum                // R1 * R0 value

    D=M                 // D = R1 * R0

    @R2                 // R2 = D

    M=D

    @r0sign             // if R0 < 0 then R2 = - R2

    D=M

    @END                // if R0 > 0 do not negate R2

    D;JGT

    @R2

    M=-M                // negate R2

(END)
