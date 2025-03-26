from parser import CommandType
import os

class CodeWriter:
    def __init__(self, output_path, append=False):
        self.file = open(output_path, 'a' if append else 'w')
        self.file_name = os.path.basename(output_path).replace('.asm', '')
        if not append:
            self.file.write("@256\n")
            self.file.write("D=A\n")
            self.file.write("@SP\n")
            self.file.write("M=D\n")
        self.label_counter = 0

    def write_arithmetic(self, command):
        if command in ['add', 'sub', 'and', 'or']:
            self._write_binary_operation(command)
        elif command in ['neg', 'not']:
            self._write_unary_operation(command)
        elif command in ['eq', 'gt', 'lt']:
            self._write_comparison(command)

    def write_push_pop(self, command_type: CommandType, segment, index):
        if command_type == CommandType.PUSH:
            if segment == "constant":
                self._write_push_constant(index)
            else:
                self._write_push(segment, index)
        elif command_type == CommandType.POP:
            self._write_pop(segment, index)

    def close(self):
        self.file.close()

    def _write_push_constant(self, value):
        #Push constant to stack
        self.file.write(f"// push constant {value}\n")
        self.file.write(f"@{value}\n")
        self.file.write("D=A\n")
        self.file.write("@SP\n")
        self.file.write("A=M\n")
        self.file.write("M=D\n")
        self.file.write("@SP\n")
        self.file.write("M=M+1\n")

    def _write_binary_operation(self, command):
        self.file.write(f"// {command}\n")
        self.file.write("@SP\n")
        self.file.write("M=M-1\n")
        self.file.write("A=M\n")
        self.file.write("D=M\n")
        self.file.write("A=A-1\n")
        if command == "add":
            self.file.write("M=D+M\n")
        elif command == "sub":
            self.file.write("M=M-D\n")
        elif command == "and":
            self.file.write("M=D&M\n")
        elif command == "or":
            self.file.write("M=D|M\n")

    def _write_unary_operation(self, command):
        self.file.write(f"// {command}\n")
        self.file.write("@SP\n")
        self.file.write("A=M-1\n")
        if command == "neg":
            self.file.write("M=-M\n")
        elif command == "not":
            self.file.write("M=!M\n")

    def _write_comparison(self, command):
        label = f"{command.upper()}_{self.label_counter}"
        self.label_counter += 1
        
        self.file.write(f"// {command}\n")
        self.file.write("@SP\n")
        self.file.write("AM=M-1\n")
        self.file.write("D=M\n")
        self.file.write("A=A-1\n")
        self.file.write("D=M-D\n")
        self.file.write(f"@{label}_TRUE\n")
        
        if command == "eq":
            self.file.write("D;JEQ\n")
        elif command == "gt":
            self.file.write("D;JGT\n")
        elif command == "lt":
            self.file.write("D;JLT\n")
            
        self.file.write("@SP\n")
        self.file.write("A=M-1\n")
        self.file.write("M=0\n")
        self.file.write(f"@{label}_END\n")
        self.file.write("0;JMP\n")
        self.file.write(f"({label}_TRUE)\n")
        self.file.write("@SP\n")
        self.file.write("A=M-1\n")
        self.file.write("M=-1\n")
        self.file.write(f"({label}_END)\n")

    def _write_pop(self, segment, index):
        if segment == "local":
            base = "LCL"
        elif segment == "argument":
            base = "ARG"
        elif segment == "this":
            base = "THIS"
        elif segment == "that":
            base = "THAT"
        elif segment == "pointer":
            base = "R" + str(3 + int(index))
        elif segment == "temp":
            base = "R" + str(5 + int(index))
        elif segment == "static":
            base = self.file_name + "." + str(index)

        self.file.write(f"// pop {segment} {index}\n")
    
        if segment in ["local", "argument", "this", "that"]:
            # Calculates target address to store in R13
            self.file.write(f"@{base}\n")
            self.file.write("D=M\n")
            self.file.write(f"@{index}\n")
            self.file.write("D=D+A\n")
            self.file.write("@R13\n")
            self.file.write("M=D\n")
            # Obtains value from stack and stores at target
            self.file.write("@SP\n")
            self.file.write("AM=M-1\n")
            self.file.write("D=M\n")
            self.file.write("@R13\n")
            self.file.write("A=M\n")
            self.file.write("M=D\n")
        elif segment in ["pointer", "temp"]:
            # Pops value from stack
            self.file.write("@SP\n")
            self.file.write("AM=M-1\n")
            self.file.write("D=M\n")
            # Stores in target register
            self.file.write(f"@{base}\n")
            self.file.write("M=D\n")
        elif segment == "static":
            # Pops value from stack
            self.file.write("@SP\n")
            self.file.write("AM=M-1\n")
            self.file.write("D=M\n")
            # Store in static variable
            self.file.write(f"@{base}\n")
            self.file.write("M=D\n")

    def _write_push(self, segment, index):
        if segment == "local":
            base = "LCL"
        elif segment == "argument":
            base = "ARG"
        elif segment == "this":
            base = "THIS"
        elif segment == "that":
            base = "THAT"
        elif segment == "pointer":
            base = str(3 + int(index))
        elif segment == "temp":
            base = str(5 + int(index))
        elif segment == "static":
            base = self.file_name + "." + str(index)

        self.file.write(f"// push {segment} {index}\n")
    
        if segment in ["local", "argument", "this", "that"]:
            self.file.write(f"@{base}\n") 
            self.file.write("D=M\n")
            self.file.write(f"@{index}\n")
            self.file.write("A=D+A\n")
            self.file.write("D=M\n")
        elif segment in ["pointer", "temp"]:
            self.file.write(f"@{base}\n")
            self.file.write("D=M\n")
        elif segment == "static":
            self.file.write(f"@{base}\n")
            self.file.write("D=M\n")
        
        self.file.write("@SP\n")
        self.file.write("A=M\n")
        self.file.write("M=D\n")
        self.file.write("@SP\n")
        self.file.write("M=M+1\n")
