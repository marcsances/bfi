# bfi: yet another Brainf### python interpreter

bfi is a quick and dirty python interpreter for the [Brainf### language](https://en.wikipedia.org/wiki/Brainfuck).

It loads the machine ram into a list of ints, each representing a register of the computer. The program is then loaded at the very beginning of the RAM, and a stack is loaded right after. After the stack, the data itself is loaded.

Upon initialization, the first instruction is loaded and processed and further on. Branching is solved with the stack.

This is a quick 1-hour implementation with a lot of "however's" on it, that might get fixed some day.

# usage

Store the program into a file (for example, the supplied helloworld.B). Then load it by calling:

 python bfi.py program.B
 
# debugging and stuff

You can call the program with the optional -d option to enable debug dumping. It prints the value of the registers and the content of the stack for each cycle.

| Register | Meaning                                               |
|----------|-------------------------------------------------------|
| pc       | Program Counter                                       |
| bsa      | Base Stack Address                                    |
| sp       | Stack Pointer                                         |
| bra      | Base Register (data) Address                          |
| rc       | Register Counter                                      |
| ci       | Current Instruction (value of data pointed by pc)     |
| cr       | Current Register    (value of data pointed by bra+rc) |
