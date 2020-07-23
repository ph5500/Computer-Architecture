"""CPU functionality."""

import sys


SP = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.branch_table = {
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b10100010: self.MUL,
            0b01000101: self.PUSH,
            0b01000110: self.POP,
        }
        
    def ram_read(self, mar):
        return self.ram[mar]
    
    def ram_write(self, mdr, mar):
        # mdr is the data being written
        self.ram[mar] = mdr

    def push_value(self, value):
        self.reg[SP] -= 1
        self.ram_write(value, self.reg[SP])
        
    def pop_value(self):
        value = self.ram_read(self.reg[SP])
        self.reg[SP] += 1
        return value
    
    
    
    
    
    
    
    def load(self, filename):
    
        """Load a program into memory."""

        address = 0
        
        
        

        
        # with open(filename) as f:
        #     for line in f:
                # try:
                #     v = int(line[0], 2)
                # except ValueError:
                #     continue
                # self.ram[address] = v
                # address += 1
                
                # line = line.split('#',  1)[0]
                
        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()
        
    def HLT(self, operand_a, operand_b):
        sys.exit()
    
    def LDI(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b
        self.pc += 3
        
    def PRN(self, operand_a, operand_b):
        print(self.reg[operand_a])
        self.pc += 2    
        
    def MUL(self, operand_a, operand_b):
        self.reg[operand_a] *= self.reg[operand_b]
        self.pc += 3
        
    def PUSH(self, operand_a, operand_b):
        self.push_value(self.reg[operand_a])
        self.pc += 2
        
    def POP(self, operand_a, operand_b):
        self.reg[operand_a] = self.pop_value()
        self.pc += 2
        
    
# 1, 2, 4, 8, 16, 32, 64, 128 etc.
    def run(self):
        """Run the CPU."""
        # HLT = 0b00000001
        # LDI = 0b10000010
        # PRN = 0b01000111
        # running = True
        
        while True:
            # need to read the memory address that's store in the register PC
            # store the result in the ir
            ir = self.ram_read(self.pc)
            # sets a specific register to a specified value
            operand_a = self.ram_read(self.pc +1)
            operand_b = self.ram_read(self.pc +2)
            
            # if ir == HLT:
            #     running = False
            # elif ir == LDI:
            #     self.reg[operand_a] = operand_b
            #     self.pc += 3
            # elif ir == PRN:
            #     print(self.reg[operand_a])
            #     self.pc += 2
            if ir in self.branch_table:
                self.branch_table[ir](operand_a, operand_b)
            else: 
                print(f'Unkown instruction {ir} at address {self.pc}')
                # stop the program by calling it in the run function
                # running = False
                sys.exit()
