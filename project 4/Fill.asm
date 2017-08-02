// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// for(i=0; i<256; i++){
//    for (j=0; j<32; j++){
//        RAM[adrs] = -1
//        adrs++
//    }
// }

    @SCREEN
    D=A
    @adrs
    M=D                         // adrs = screen's base adress
    @8192
    D=A
    @numberOfRegisters         // number of registers to fill
    M=D
    @i                         // i = 0
    M=0

(INPUT)

    @KBD
    D=M                         // input value

    @BLACK                      // if input > 0 go to black
    D;JGT

    @WHITE                      // if input = 0 go to white
    D;JEQ

(BLACK)
    @i
    D=M

    @numberOfRegisters
    D=D-M

    @INPUT
    D;JEQ                       // if i == numberOfRegisters goto INPUT


    @adrs
    A=M
    M=-1                       // fill the current register with black color

    @adrs
    M=M+1                      // go to the next one

    @i                         // increase the registers' counter by 1
    M=M+1

    @BLACK
    0;JMP


(WHITE)
    @i
    D=M

    @INPUT
    D;JLT                     // if i == 0 goto INPUT

    @adrs
    A=M
    M=0                       // fill the current register with white color

    @adrs
    M=M-1                     // go to the next register to white

    @i
    M=M-1                    // decrease the registers' counter by 1

    @WHITE
    0;JMP
