import sys
import os
from src.project8 import main

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Incorrect Input")
        sys.exit(1)
    filename = sys.argv[1]
    filename = os.path.abspath(filename)
    main(filename, boot_strap_flag=True)
