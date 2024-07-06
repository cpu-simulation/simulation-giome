#! usr/bin/python
from abc import ABC, abstractmethod
from .errors import PrBaseException
from dataclasses import dataclass
import ctypes



ram_ex=[{"address": 0XFE, "value": 0X12},
        {"address": 0XFF, "value": 0X13},
        ]



class RAM:
    def __init__(self,ram) -> None:
        self.ram=ram
        self.ram.append({"address": 0x13, "value": "XOR"})
        self.ram.append({"address": 0x15, "value": "LSH"})
        self.ram.append({"address": 0x17, "value": "RSH"})
        self.ram.append({"address": 0x19, "value": "CMP"})
        self.ram.append({"address": 0x0000, "value": "AND"})
        self.ram.append({"address": 0x8000, "value": "ANDI"})
        self.ram.append({"address": 0x1000, "value": "ADD"})
        self.ram.append({"address": 0x9000, "value": "ADDI"})
        self.ram.append({"address": 0x2000, "value": "LDA"})
        self.ram.append({"address": 0xA000, "value": "LDAI"})
        self.ram.append({"address": 0x3000, "value": "STA"})
        self.ram.append({"address": 0xB000, "value": "STAI"})
        self.ram.append({"address": 0x4000, "value": "BUN"})
        self.ram.append({"address": 0xC000, "value": "BUNI"})
        self.ram.append({"address": 0x5000, "value": "BSA"})
        self.ram.append({"address": 0xD000, "value": "BSAI"})
        self.ram.append({"address": 0x6000, "value": "ISZ"})
        self.ram.append({"address": 0xE000, "value": "ISZI"})
        self.ram.append({"address": 0x7800, "value": "CLA"})
        self.ram.append({"address": 0x7400, "value": "CLE"})
        self.ram.append({"address": 0x7200, "value": "CMA"})
        self.ram.append({"address": 0x7100, "value": "CME"})
        self.ram.append({"address": 0x7080, "value": "CIR"})
        self.ram.append({"address": 0x7040, "value": "CIL"})
        self.ram.append({"address": 0x7020, "value": "INC"})
        self.ram.append({"address": 0x7010, "value": "SPA"})
        self.ram.append({"address": 0x7008, "value": "SNA"})
        self.ram.append({"address": 0x7004, "value": "SZA"})
        self.ram.append({"address": 0x7002, "value": "SZE"})
        self.ram.append({"address": 0x7001, "value": "HLT"})
        self.ram.append({"address": 0xF800, "value": "INP"})
        self.ram.append({"address": 0xF400, "value": "OUT"})
        self.ram.append({"address": 0xF200, "value": "SKI"})
        self.ram.append({"address": 0xF100, "value": "SKO"})
        self.ram.append({"address": 0xF080, "value": "ION"})
        self.ram.append({"address": 0xF040, "value": "IOF"})

        


    def cla(self,address):
        for i in self.ram:
            if i["address"]==address:
                i["value"]=0
        return self.ram
    def load(self):
        return self.ram
    


class BaseMemory(ABC,RAM):

    def bulk_write(self, data: list[dict]) -> None:
        for elemnt in data:
            if elemnt["address"]:
                self.write(elemnt)
    
    @property
    def bulk_read(self) -> list[dict]:
        return self.ram

    def write(self, data: dict) -> None:
        found = False
        for i in self.ram:
            if (i["address"] == data["address"]):
                self.cla(data["address"])
                i["value"] = data["value"]
                found = True
                break
        if not found:
            self.ram.append(data)
    
    def read(self, address) -> dict:
        for i in self.ram:
            if i["address"] == address:
                return i
        return None





class BaseRegister(BaseMemory):
    def __init__(self, ram) -> None:
        super().__init__(ram)
        self.registers = {"PC": None, "TC": None, "AR": None, "AC": None, "DR": None, "E":None}

    def set_PC(self,address):
        self.registers["PC"]=address
    
    def set_TC(self, value):
        self.registers["TC"] = value
    
    def set_AR(self, address):
        self.registers["AR"] = address
    
    def set_AC(self, value):
        self.registers["AC"] = value
    
    def set_DR(self, value):
        self.registers["DR"] = value
    def set_E(self,value):
        self.registers["E"]=value
    
    def write_register(self, data: dict) -> None:
        for key, value in data.items():
            if key in self.registers:
                self.registers[key] = value

    def read_all_registers(self) -> dict:
        return self.registers
    def read_register(self,name_register) -> dict:
        return self.registers[name_register]
        

    
class ALU(BaseRegister,BaseMemory):
    def __init__(self, ram):
        super().__init__(ram)


    def plus(self,num1,num2):
        return int(num1)+int(num2)
                 

    
    def OR(self,num1, num2):
        #inputs shuold be in the form of binary
        num1=int(num1)
        num2=int(num2)
        result = num1 | num2
        return bin(result)[2:]
        
    
    def NOT(self,num1):
    # Perform bitwise NOT and limit the result to 4 bits (for example)
        num1=int(num1)
        result = ~num1 & 0b1111
        return bin(result)
    
    def AND(self,num1,num2):
        num1=int(num1)
        num2=int(num2)
        result = num1 & num2
        return bin(result)[2:]
    
    
    def circular_left_shift(self,value, shift, bit_size=16):
        """Perform circular left shift on a value."""
        mask = (1 << bit_size) - 1
        shift %= bit_size
        return ((value << shift) & mask) | (value >> (bit_size - shift))
    
    def circular_right_shift(self,value, shift, bit_size=16):
        """Perform circular right shift on a value."""
        mask = (1 << bit_size) - 1
        shift %= bit_size
        return ((value >> shift) & mask) | (value << (bit_size - shift) & mask)
    
    def compare(self,num1,num2):
        num1=int(num1,2)
        num2=int(num2,2)
        if num1>num2:
            return num1
        elif num2>num1:
            return num2
        else:
            return num2


class BaseCore(BaseMemory):

    memory: BaseMemory = ...
    registers: BaseRegister = ... 
    alu: ALU = ...


    def __init__(self, ram):
        self.memory = BaseMemory(ram)
        self.registers = BaseRegister(ram)
        self.alu = ALU(ram)
        self.instruction_set = {
            "RSH":0x17,
            "CMP":0x19,
            "LSH":0x15,
            "XOR":0x13,
            "AND": 0x0,      # Example opcode for AND
            "ANDI": 0x8,     # Example opcode for ANDI
            "ADD": 0x1,      # Example opcode for ADD
            "ADDI": 0x9,     # Example opcode for ADDI
            "LDA": 0x2,      # Example opcode for LDA
            "LDAI": 0xA,     # Example opcode for LDAI
            "STA": 0x3,      # Example opcode for STA
            "STAI": 0xB,     # Example opcode for STAI
            "BUN": 0x4,      # Example opcode for BUN
            "BUNI": 0xC,     # Example opcode for BUNI
            "BSA": 0x5,      # Example opcode for BSA
            "BSAI": 0xD,     # Example opcode for BSAI
            "ISZ": 0x6,      # Example opcode for ISZ
            "ISZI": 0xE,     # Example opcode for ISZI
            "CLA": 0x7800,   # Opcode for CLA
            "CLE": 0x7400,   # Opcode for CLE
            "CMA": 0x7200,   # Opcode for CMA
            "CME": 0x7100,   # Opcode for CME
            "CIR": 0x7080,   # Opcode for CIR
            "CIL": 0x7040,   # Opcode for CIL
            "INC": 0x7020,   # Opcode for INC
            "SPA": 0x7010,   # Opcode for SPA
            "SNA": 0x7008,   # Opcode for SNA
            "SZA": 0x7004,   # Opcode for SZA
            "SZE": 0x7002,   # Opcode for SZE
            "HLT": 0x7001,   # Opcode for HLT
            "INP": 0xF800,   # Opcode for INP
            "OUT": 0xF400,   # Opcode for OUT
            "SKI": 0xF200,   # Opcode for SKI
            "SKO": 0xF100,   # Opcode for SKO
            "ION": 0xF080,   # Opcode for ION
            "IOF": 0xF040    # Opcode for IOF
        }

    def compile(self, instructions: list[str]) -> None:
        """
        Compile instructions into machine code and save them in memory.
        """

        self.saved_instructions=[]
        for instruction in instructions:
            list_operands=instruction.split()
            saved_address=[]
            x=""
            for elemnt in list_operands:
                
                if "0X" not in elemnt.upper():
                    x=self.instruction_set.get(elemnt.upper())
                else:
                    saved_address.append(int(elemnt,16))
            
            
            self.saved_instructions.append({"operand":x,"address":saved_address})
        

    def execute_instruction(self) -> None:
        """
        Execute saved instructions.
        """
        # For demonstration purposes, this method will be simplified
        self.registers.set_PC(0x0)  # Starting address
        while True:

            pc_value = self.registers.read_register("PC")

            if pc_value >= len(self.saved_instructions):
                break
            instruction = self.saved_instructions[pc_value]
            #what the code should do
            opcode=instruction["operand"]
            for name, code in self.instruction_set.items():
                if code == opcode:
                    opcode = name
                    break
            #entery address
            operands=instruction["address"]
            if opcode[-1]!="I":
                if instruction is None:
                    break

                if opcode == "LDA":
                    self.registers.set_AR(operands[0])
                    self.registers.set_DR(self.memory.read(self.registers.read_register("AR"))["value"])
                    self.registers.set_AC(self.registers.read_register("DR"))
            
                elif opcode == "STA":
                    self.memory.write({"address": operands, "value": self.registers.read_register("AC")})
                elif opcode == "ADD":
                    self.registers.set_AR(operands[0])
                    self.registers.set_DR(self.memory.read(self.registers.read_register("AR"))["value"])
                    self.registers.set_AC(self.alu.plus(self.registers.read_register("AC"),self.registers.read_register("DR")))
                elif opcode ==  "AND":
                    self.registers.set_AR(operands)
                    self.registers.set_DR(self.memory.read(self.registers.read_register("AR"))["value"])
                    self.registers.set_AC(self.alu.AND(self.registers.read_register("AC"),self.registers.read_register("DR")))
                elif opcode ==  "OR":
                    self.registers.set_AR(operands)
                    self.registers.set_DR(self.memory.read(self.registers.read_register("AR"))["value"])
                    self.registers.set_AC(self.alu.OR(self.registers.read_register("AC"),self.registers.read_register("DR")))
                elif opcode ==  "NOT":
                    self.registers.set_AR(operands)
                    self.registers.set_DR(self.memory.read(self.registers.read_register("AR"))["value"])
                    self.registers.set_AC(self.alu.NOT(self.registers.read_register("DR")))
                elif opcode ==  "XOR":
                    self.registers.set_AR(operands)
                    self.registers.set_DR(self.memory.read(self.registers.read_register("AR"))["value"])
                    self.registers.set_AC(self.alu.XOR(self.registers.read_register("DR"),self.registers.read_register("AC")))
                elif opcode ==  "LSH":
                    self.registers.set_AC(self.alu.left_shifting(operands, operands[1]))
                elif opcode ==  "RSH":
                    self.registers.set_AC(self.alu.right_shifting(operands, operands[1]))
                elif opcode ==  "CMP":
                    self.registers.set_AC(self.alu.compare(operands, operands[1]))
                elif opcode == "CLA":
                    self.registers.set_AC(None)
                elif opcode =="CLE":
                    self.registers.set_E(None)
                elif opcode =="CMA":
                    self.registers.set_AC(self.alu.NOT(self.registers.read_register("AC")))
                elif opcode =="CME":
                    self.registers.set_E(self.alu.NOT(self.registers.read_register("E")))
                elif opcode =="CIR":
                    self.registers.set_AC(self.alu.circular_right_shift(value=self.registers.read_register("AC"),shift=self.registers.read_register("E")))
                elif opcode =="CIL":
                    self.registers.set_AC(self.alu.circular_left_shift(value=self.registers.read_register("AC"),shift=self.registers.read_register("E")))
                elif opcode =="INC":
                    self.registers.set_AC(self.alu.plus(self.registers.read_register("AC"),1))
                elif opcode =="OUT":
                    self.registers.read_register("AC")
                elif opcode =="BUN":
                    self.registers.set_PC(operands[0])
                    continue
                elif opcode =="BSA":
                    current_pc = self.registers.read_register("PC")
                    self.memory.write({"address": operands[0], "value": current_pc + 1})
                    self.registers.set_PC(operands[0] + 1)
                    continue
                elif opcode == "ISZ":
                    self.registers.set_DR(self.memory.read(self.registers.read_register("AR"))["value"])
                    self.registers.set_DR(self.registers.read_register("DR")+1)
                    self.memory.write({"address":self.registers.read_register("AR"),"value":self.registers.read_register("DR")})
                    if self.registers.read_register("DR")==0:
                        self.registers.set_PC(self.registers.read_register("PC")+1)
                else:
                    raise ValueError(f"Unknown opcode: {opcode}")
            else:
                #indirect instructions
                effective_address=self.memory.read(operands)["value"]
                if instruction is None:
                    break

                if opcode == "LDAI":

                    self.registers.set_AR(effective_address)
                    self.registers.set_DR(self.memory.read(self.registers.read_register("AR"))["value"])
                    self.registers.set_AC(self.registers.read_register("DR"))
            
                elif opcode == "STAI":
                    self.memory.write({"address": effective_address, "value": self.registers.read_register("AC")})
                elif opcode == "ADDI":
                    self.registers.set_AR(effective_address)
                    self.registers.set_DR(self.memory.read(self.registers.read_register("AR"))["value"])
                    self.registers.set_AC(self.alu.plus(self.registers.read_register("AC"),self.registers.read_register("DR")))
                elif opcode ==  "ANDI":
                    self.registers.set_AR(effective_address)
                    self.registers.set_DR(self.memory.read(self.registers.read_register("AR"))["value"])
                    self.registers.set_AC(self.alu.AND(self.registers.read_register("AC"),self.registers.read_register("DR")))
                elif opcode ==  "ORI":
                    self.registers.set_AR(effective_address)
                    self.registers.set_DR(self.memory.read(self.registers.read_register("AR"))["value"])
                    self.registers.set_AC(self.alu.OR(self.registers.read_register("AC"),self.registers.read_register("DR")))
                elif opcode ==  "NOTI":
                    self.registers.set_AR(effective_address)
                    self.registers.set_DR(self.memory.read(self.registers.read_register("AR"))["value"])
                    self.registers.set_AC(self.alu.NOT(self.registers.read_register("DR")))
                elif opcode ==  "XORI":
                    self.registers.set_AR(effective_address)
                    self.registers.set_DR(self.memory.read(self.registers.read_register("AR"))["value"])
                    self.registers.set_AC(self.alu.XOR(self.registers.read_register("DR"),self.registers.read_register("AC")))
                elif opcode == "BUNI":
                    self.registers.set_PC(effective_address)
                elif opcode =="BSAI":
                    current_pc = self.registers.read_register("PC")
                    self.memory.write({"address": effective_address, "value": current_pc + 1})
                    self.registers.set_PC(effective_address + 1)
                elif opcode =="ISZI":
                    self.registers.set_DR(self.memory.read(self.registers.read_register("AR"))["value"])
                    self.registers.set_DR(self.registers.read_register("DR")+1)
                    self.memory.write({"address":self.registers.read_register("AR"),"value":self.registers.read_register("DR")})
                    if self.registers.read_register("DR")==0:
                        self.registers.set_PC(self.registers.read_register("PC")+1)
                
                else:
                    raise ValueError(f"Unknown opcode: {opcode}")
            self.registers.set_PC(pc_value + 1)
            



#example use of reading from ram
"""ram_1=RAM(ram_ex)
x=BaseMemory(ram_1.load())
out=x.read(0XFE)
print(out)"""

#example use of writing in to the ram
"""ram_1=RAM(ram_ex)
x=BaseMemory(ram_1.load())
x.write({"address": 0XFE, "value": 0X11})
print(ram_1.load())"""

#example use of bulk writing in to the ram
"""ram_1=RAM(ram_ex)
x=BaseMemory(ram_1.load())
x.bulk_write([{"address": 0XFE, "value": 0X12}, {"address": 0XFF, "value": 0X13} ])
print(ram_1.load())"""

#example for writing in registers
"""base_memory = BaseMemory(ram_ex)
base_register = BaseRegister()
base_register.write_re({"PC":0x13,"TC":0x7,"AR":0x17})
print(base_register.read())"""

#example for compile
"""core_1 =BaseCore(ram_ex)
core_1.compile(["LDAI 0XFE","ADDI 0XFF"])
core_1.execute_instruction()"""