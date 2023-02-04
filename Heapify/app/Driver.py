"""
@author: Josiah Cherbony
@date: December 2022
This file will act as the driver for our heap class by making a heap with the
appropriate command line arguments and call its go method. Will handle improper
usage of command line arguments.
"""

from Heap import Heap
import sys

def main():
    """
    Act as the driver for our heap class by making a heap with the
    appropriate command line arguments and call its go method. Will handle improper
    usage of command line arguments.
    """

    # check that the appropriate number of command lines are entered
    if len(sys.argv) != 3:
        print("\nERROR! usage: python3 Driver.py <file> <label>\n")
        return

    # start the heap go function
    heap = Heap(sys.argv[1], sys.argv[2])

    # handle bad file input/input with empty path
    try:
        heap.go()
    except FileNotFoundError:
        print("\nERROR! File not found, please enter valid file or path.\n")
    except ValueError as error:
        print(error)

# call main function
if __name__ == '__main__':
    main()