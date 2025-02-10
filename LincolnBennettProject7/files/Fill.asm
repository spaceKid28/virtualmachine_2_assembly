// Screen and keyboard interaction program
// When any key is pressed, fills screen from start with black
// When no key is pressed, clears screen from end with white

@SCREEN     // Store SCREEN (which is 16384) into current, to keep track of what pixel we are on.
D=A
@current    // current represents what pixel we are on (we start on 16384)
M=D
    
@8192       // 512 pixels per line, 256 lines, 16 bits per pixel; 512 * 256 divided by 16 = 8196 RAM addresses
D=A         // we could possibly color
@total      // store this in variable "total"
M=D
    
(LOOP)
@KBD        // If no key is pressed (JEQ) jump to Clear Loop
D=M
@CLEAR      
D;JEQ
    
// Key is pressed
// below we will check whether or not we have filled the entire screen
@current    
D=M
@SCREEN     // Get screen base address
D=D-A       // Calculate how many words we've filled
@total
D=D-M       // Compare with total screen size
@LOOP       // If we've filled the whole screen, go back to check keyboard
D;JGE

// Here we color the pixel
@current    // Load current position
A=M         // Recall, current holds memory location, thus: set A = RAM[current]
M=-1        // Setting RAM[current] = -1
@current
M=M+1       // increment to next pixel
@LOOP       // JMP (no matter what) to the top of the LOOP statement
0;JMP

// this is the condition in which no key is pressed
(CLEAR)
@current       // Get current position
D=M             // We take our current address and subtract Screen value to get exactly how many pixels we have colored
@SCREEN
D=D-A           // This is the subtraction
@LOOP       // We jump, if D is less than or Equal (it should only ever be equal or greater) than zero. 
D;JLE      // this means the whole screen is white and we don't need to un color
    
@current
M=M-1       // Move back one pixel
A=M         // Set RAM[current] = 0; ie set to white
M=0
    
@LOOP
0;JMP
