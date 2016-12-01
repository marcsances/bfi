#!/usr/bin/env python

"""
bfi.py 0.1
Copyright (c) 2016, Marc Sances
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import sys
class BfVM(): 
    def __init__(self):
        self.RAMSIZE=8*1024*1024             # 8M ram
        self.STACKSIZE=1024                  # 1K stack

    def initram(self):
        self.ram=[0]*self.RAMSIZE

    def loadfile(self,file,address):
        with open(file) as f:
            program=list(f.read().replace("\n","")) + ["\n"]                                         # load program and append end flag
            self.ram=self.ram[:address] + program + self.ram[address+len(program):]
            return len(program)

    def dump(self):
        print "pc=" + str(self.pc) + ", bsa=" + str(self.bsa) + ", sp=" + str(self.sp) + ", bra=" + str(self.bra) + ", rc=" + \
         str(self.rc) + ", ci=" + str(self.ram[self.pc]) + ", cr=" + str(self.ram[self.bra+self.rc])
        self.printstack()
    
    def printstack(self):
        print "stack: " + str(self.ram[self.bsa:(self.bsa+self.sp)])

    def loadvm(self,init):
        self.initram()
        ps=self.loadfile(init,0)            # load init at address 0
        self.pc=0                           # set program counter to 0
        self.bsa=ps                         # set base stack address to end of init
        self.sp=0                           # set stack pointer to end of init
        self.bra=ps+self.STACKSIZE          # set base register address to end of init + stack
        self.rc=0                           # set register counter to 0
        while self.cycle():
            pass

    def ifc(self):
        """Instruction fetch cycle"""
        return self.ram[self.pc]

    def idx(self,ins):
        """Instruction decode and execution"""
        self.pc=self.pc+1                                             # increment program counter beforehand, so that it can be modified by ]
        if (ins=="+"):
            self.ram[self.bra+self.rc]=int(self.ram[self.bra+self.rc])+1   # increment
        elif (ins=="-"):
            self.ram[self.bra+self.rc]=int(self.ram[self.bra+self.rc])-1   # decrement
        elif (ins=="<"):
            self.rc=self.rc-1                                         # register left
        elif (ins==">"):
            self.rc=self.rc+1                                         # register right
        elif (ins==","):
            self.ram[self.bra+self.rc]=ord(sys.stdin.read(1))         # read
        elif (ins=="."):
            sys.stdout.write(unichr(self.ram[self.bra+self.rc]))      # write
        elif (ins=="["):     
            self.ram[self.bsa+self.sp]=self.pc-1                      # export context to stack
            self.sp=self.sp+1                                         # increment stack pointer
        elif (ins=="]"):                                              # loop end
            if (self.ram[self.bra+self.rc]!=0):                       # if condition is met
                self.sp=self.sp-1                                     # decrement stack pointer
                self.pc=int(self.ram[self.bsa+self.sp])               # recover context
        elif (ins=="\n"):
            return False
        else:
            pass                                                      # other token
        return True

    def cycle(self):
        """Emulates a BF CPU cycle"""
        self.dump()
        ins=self.ifc()
        return self.idx(ins)

if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("program")
    args=parser.parse_args()
    BfVM().loadvm(args.program)