This program is an Assembler for the Hack Computer: takes a filename (<filename>.in) and creates a new hack file (<filename>.hack) in the same directory as the input file. Both absolute and relative file paths are accepted. The program does not handle invalid filepaths. Note that the output file will have the same filename as the input file but with a different extension.

Below is a command line command to run this program on a sample input. You should only ever modify the last argument "files/RectL.asm".

python run_project6.py files/RectL.asm

This will produce a new file "files/RectL.hack"

This program takes one argument, the filepath to the input file, including the filename of the input file. To run this program from the command line, ensure that the input file has an extension of *.asm

The code for the program is found in src/project0.py

A runner script (run_project0.py) so that the program can be run directly from the repo. A sample inputs in the "files" folder are also included. 
