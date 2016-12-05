# bfi: yet another Brainf### python interpreter

bfi is a quick and dirty python interpreter for the [Brainf### language](https://en.wikipedia.org/wiki/Brainfuck).

It loads the machine ram into a list of ints, each representing a register of the computer. The program is then loaded at the very beginning of the RAM, and a stack is loaded right after. After the stack, the data itself is loaded.

Upon initialization, the first instruction is loaded and processed and further on. Branching is solved with the stack.

This is a quick 1-afternoon implementation with a lot of "however's" on it, which might get fixed some day.

# usage

Store the program into a file (for example, the supplied helloworld.B). Then load it by calling:
`
python bfi.py program.B`
 
By using -d you enable debug mode (see below).

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

Protip: open an additional terminal emulator, type tty to get the tty device file, then try this:

```
python bfi.py program.B -d 2>/dev/pts/3
```

where /dev/pts/3 is the device file for the additional terminal you opened.

This will run the program in the first terminal, and show debug information in the second terminal.

# what works?

Some working examples are included. Performance in this interpreter is not priority, my only aim with this small project was to understand the inner workings of the language and getting where to start to understanding better how VMs work.

A big hanoi.B extracted from [this website (thanks!)](http://www.clifford.at/bfcpu/bfcomp.html) is supplied for testing. It runs pretty slow (can take up to 2 minutes to show stuff on screen), but then it does work.

# other configuration

You can edit variables in constructor to adapt the scale of the computer. It's 8M RAM and 1K stack by default, which should be enough for the vast majority of the programs without an excessive resource abuse, but should you need more RAM or stack, just change self.RAMSIZE or self.STACKSIZE. Both are in number of words, so if you want 8M, change RAMSIZE to 8\*1024\*1024.
