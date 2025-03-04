Insider the GardnerChess folder, there are four .jack files. This is sufficent to run the program.

Gardner Chess is mostly the same as regular chess, except that the board is 5x5. Note that the game requires User Input. 

The board is Zero Indexed. The first number is the row number. The second number is the column number. Top Left square is 0,0 Bottom Right square is 4,4

    0   1   2   3   4
0
1
2
3
4

Input Must be Formatted EXACTLY as follows: piece oldx oldy - newx newy
For Example: P11-12 moves a Pawn from square 1,1 to 1,2. (the hypen is required). The mappings of the Character to Piece can be found on the screen of the game. Note that input is case-sensitive

After the first player presses enter, the board should updated, and the second player can then make their move immediately.

The game is not sophisticated enough to check for legal vs illegal moves. For example, if you move a Queen from 2,2 to 4,2
there must already by a Queen in 2,2 and 2,2 to 4,2 must be a legal move (there must not be a piece inbetween the two squares).
