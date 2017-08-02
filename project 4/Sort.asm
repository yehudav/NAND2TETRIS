//The program input will be at R14(starting address),R15(length of array).
//The program should sort the array starting at the address in R14 with length specified in R15.
//The sort is in descending order - the largest number at the head of the array.
//The array is allocated in the heap address 2048-16383.

//Bubble sort algorithm
//
//int tmp = 0;
//
//for (int i = 0; i < arraySize - 1; i++){
//
//    for (int j = 0; j < arraySize - i - 1; j++) {
//
//			if (array[j] < array[j + 1]) {
//                tmp = array[j];
//                array[j] = array[j + 1];
//                array[j + 1] = tmp;}}}


//------------------------------------------------------------------------------

	@R15
	D=M

	@arrayLength
	M=D-1

	D=M
	@END
	D;JEQ                   // if 1 == arrayLength goto END

	@R14
	D=M

	@arrayLength
	D=D+M

	@unsorted					// the last number address
	M=D

	@i                         // i = 0
    M=0



(LOOP)

	@i
    D=M

    @arrayLength
    D=D-M

    @END
    D;JEQ                       // if i == arrayLength goto END

	@R14						// reset j = 0
	D=M

	@j
	M=D


(NESTED_LOOP)


	@j							// current address
	D=M

	@unsorted					// current last unsorted address
	D=D-M

	@UPDATEI				    // current nested loop is finished
	D;JEQ


	@j							// check if array[j] < array[j+1]
	A=M
	D=M

	@j
	M=M+1

	@j
	A=M
	D=M-D

	@SWAP						// if  array[j] - array[j+1]  < 0 SWAP
	D;JGT


	@NESTED_LOOP				// repeat loop
	0;JMP



(SWAP)							// swap function

	@j 							// D = a
	M=M-1
	A=M
	D=M

	@tmp						// tmp = a
	M=D

	@j 							// D = b
	M=M+1
	A=M
	D=M

	@j							// a = D
	M=M-1
	A=M
	M=D

	@tmp						// b = tmp
	D=M
	@j
	M=M+1
	A=M
	M=D


	@NESTED_LOOP
	0;JMP

(UPDATEI)
    @i                         // i++
    M=M+1

    @LOOP
    0;JMP


(END)

