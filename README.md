# bfi: yet another Brainf### python interpreter

bfi is a quick and dirty python interpreter for the [https://en.wikipedia.org/wiki/Brainfuck](Brainf### language).

It loads the machine ram into a list of ints, each representing a register of the computer. The program is then loaded at the very beginning of the RAM, and a stack is loaded right after. After the stack, the data itself is loaded.

Upon initialization, the first instruction is loaded and processed and further on. Branching is solved with the stack.

This is a quick 1-hour implementation with a lot of "however's" on it, that might get fixed some day.

# usage

Store the program into a file (for example, the supplied helloworld.B). Then load it by calling:

 python bfi.py program.B
 
# debugging and stuff

For now no debugging is supported, but you can modify the source and add self.dump() right before first instruction of method cycle() to keep control of the internal VM registers and the state of the stack.

| Register | Meaning                                               |
|----------|-------------------------------------------------------|
| pc       | Program Counter                                       |
| bsa      | Base Stack Address                                    |
| sp       | Stack Pointer                                         |
| bra      | Base Register (data) Address                          |
| rc       | Register Counter                                      |
| ci       | Current Instruction (value of data pointed by pc)     |
| cr       | Current Register    (value of data pointed by bra+rc) |
