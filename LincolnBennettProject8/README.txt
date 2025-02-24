This program  takes a VM file (<filename.vm>) or a folder of VM files and creates a new assembly file (<filename.asm>) in the same directory as the input file, or inside the directory if the input was a filepath to a directory containing vm files.
Both absolute and relative file paths are accepted. The program does not handle invalid filepaths. Note that the output file will have the same filename as the input file but with a different extension.

Below is a command line command to run this program on a sample input. You should only ever modify the last argument "08/FunctionCalls/StaticsTest".

python run_project.py 08/FunctionCalls/StaticsTest

This will produce a new file "08/FunctionCalls/StaticsTest/StaticsTest.asm"

This program takes one argument, the filepath to the input file, including the filename of the input file.

The code for the program is found in src/project0.py

A runner script (run_project0.py) so that the program can be run directly from the repo. A sample inputs in the "07" folder are also included. 

**NOTE TO THE GRADER**
This program has been tested on Windows. I spoke with the professor after class and verified that my write function worked correctly.
A grader for my last assignment stated that on line 187 of the util.py file, the "\n" was causing issues, he was running Ubuntu. 
The professor gave me the points back, as we could not reproduce the error on machine. She told me to add a note in the README for future graders.


