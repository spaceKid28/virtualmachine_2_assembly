import sys
import os
from src.project7 import main

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python run_project.py <filename>")
        sys.exit(1)
    filename = sys.argv[1]
    filename = os.path.abspath(filename)
    print(filename)
    main(filename)
# this is my terminal command: python run_project.py 07/StackArithmetic/SimpleAdd/SimpleAdd.vm
# this is my terminal command: python run_project.py 07/StackArithmetic/StackTest/StackTest.vm