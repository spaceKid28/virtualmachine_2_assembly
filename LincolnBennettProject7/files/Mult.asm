@2     // RAM[2] will hold the product of RAM[0] and RAM[1], therefore we set it to zero
M=0     
@0	// Load RAM[0] into D
D=M
@END	// if RAM[0] is 0, JUMP to the END, which is infinite loop in our progrma
D;JEQ
@1     // Load RAM[1] into D
D=M     
@END    // If R1 is 0, go to END, which holds the infinite loop in our program
D;JEQ   
@3     // set RAM[3] to RAM[1]. This will count the number of times we are going to add RAM[0]
M=D
(LOOP)
@0 // Load RAM[0] into D (recall we will add it to RAM[2] exactly RAM[1] times
D=M
@2 // Add RAM[0] into RAM[2]
M=D+M
@3 // Now we need to decrement the counter
M=M-1
D=M //Store our counter to run if statement
@LOOP //if our counter is above 0, then we countinue to run the loop
D;JGT
(END) // infinite loop at the end of our program
@END
0;JMP    
