#!/usr/bin/env python

"""
bfi.py 0.2
Copyright (c) 2016, Marc Sances
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import sys,re
class BfVM(): 
    def __init__(self,debug):
        self.RAMSIZE=8*1024*1024             # 8M ram
        self.STACKSIZE=1024                  # 1K stack
        self.DEBUG=debug

    def initram(self):
        self.ram=[0]*self.RAMSIZE

    def loadfile(self,file,address):
        with open(file) as f:
            program=list(re.sub('[^<>,.+\-\[\]]', '', f.read())) + ["\n"]                                         # load program and append end flag
            self.ram=self.ram[:address] + program + self.ram[address+len(program):]
            return len(program)

    def dump(self):
        sys.stderr.write("pc=" + str(self.pc) + ", bsa=" + str(self.bsa) + ", sp=" + str(self.sp) + ", bra=" + str(self.bra) + ", rc=" + \
         str(self.rc) + ", ci=" + str(self.ram[self.pc]) + ", cr=" + str(self.ram[self.bra+self.rc]) + "\n") 
        self.printstack()
    
    def printstack(self):
        sys.stderr.write("stack: " + str(self.ram[self.bsa:(self.bsa+self.sp)]) + "\n")

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
            c=sys.stdin.read(1)
            if c=='':
                sys.exit(0)
            self.ram[self.bra+self.rc]=ord(c) if len(c)>0 else 0      # read
        elif (ins=="."):
            sys.stdout.write(unichr(self.ram[self.bra+self.rc]))      # write
        elif (ins=="["):     
            if (self.ram[self.bra+self.rc]!=0):
                self.ram[self.bsa+self.sp]=self.pc-1                  # export context to stack
                self.sp=self.sp+1                                     # increment stack pointer
            else:
                self.skiploop()
        elif (ins=="]"):                                              # loop end
            self.sp=self.sp-1                                     # decrement stack pointer
            if (self.ram[self.bra+self.rc]!=0):                       # if condition is not met
                self.pc=int(self.ram[self.bsa+self.sp])               # recover context
        elif (ins=="\n"):
            return False
        else:
            pass                                                      # other token
        return True

    def _s(self):
        if (self.ram[self.pc]=="["):
            r=1                                                       # add one recursion level
        elif (self.ram[self.pc]=="]"):
            r=-1                                                      # remove one recursion level
        else:
            r=0                                                       # depth is untouched
        self.pc=self.pc+1                                             # skip to next instruction
        return r

    def skiploop(self):
        depth=1
        while (depth>0 and not self.ram[self.pc]=="\n"):
            depth=depth+self._s()

    def cycle(self):
        """Emulates a BF CPU cycle"""
        if (self.DEBUG):
            self.dump()
        ins=self.ifc()
        return self.idx(ins)

if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("program")
    parser.add_argument("-d",dest="debug",action="store_true")
    args=parser.parse_args()
    BfVM(args.debug).loadvm(args.program)
