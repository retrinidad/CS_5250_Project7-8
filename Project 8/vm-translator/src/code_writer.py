from parser import CommandType
import os

class CodeWriter:
    def __init__(self, output_path, append=False, is_sys_init=False):
        self.file = open(output_path, 'a' if append else 'w')
        self.file_name = ""
        self.label_counter = 0
        self.current_function = "OS"
        self.return_counter = 0

        if not append and is_sys_init:
            self.write_init()

    def set_file_name(self, file_name: str):
        self.file_name = file_name

    def write_init(self):
        self.file.write("// Bootstrap code\n")

        self.file.write("@256\n")
        self.file.write("D=A\n")
        self.file.write("@SP\n")
        self.file.write("M=D\n")
    
        self.write_function("OS", 0)
        self.write_call("Sys.init", 0)

    def write_label(self, label):
        # assembly for label
        full_label = f"{self.current_function}${label}" if self.current_function else label
        self.file.write(f"// label {label}\n")
        self.file.write(f"({full_label})\n")
    
    def write_goto(self, label):
        # assembly for goto
        full_label = f"{self.current_function}${label}" if self.current_function else label
        self.file.write(f"// goto {label}\n")
        self.file.write(f"@{full_label}\n")
        self.file.write("0;JMP\n")

    def write_if(self, label):
        # assembly for if-goto
        full_label = f"{self.current_function}${label}" if self.current_function else label
        self.file.write(f"// if-goto {label}\n")

        self.file.write("@SP\n")
        self.file.write("AM=M-1\n")
        self.file.write("D=M\n")
        self.file.write(f"@{full_label}\n")
        self.file.write("D;JNE\n")

    def write_function(self, function_name, n_vars):
        # assembly for function
        self.current_function = function_name
        self.file.write(f"// function {function_name} {n_vars}\n")
        self.file.write(f"({function_name})\n")
        
        for _ in range(int(n_vars)):
            self.file.write("@0\n")
            self.file.write("D=A\n")
            self._push_d_to_stack()

    def write_call(self, function_name, n_args):
        # assembly for call
        return_label = f"{self.current_function}$ret.{self.return_counter}"
        self.return_counter += 1
        
        self.file.write(f"// call {function_name} {n_args}\n")
        
        self.file.write(f"@{return_label}\n")
        self.file.write("D=A\n")
        self._push_d_to_stack()
        
        for segment in ["LCL", "ARG", "THIS", "THAT"]:
            self.file.write(f"@{segment}\n")
            self.file.write("D=M\n")
            self._push_d_to_stack()
        
        self.file.write("@SP\n")
        self.file.write("D=M\n")
        self.file.write("@5\n")
        self.file.write("D=D-A\n")
        self.file.write(f"@{n_args}\n")
        self.file.write("D=D-A\n")
        self.file.write("@ARG\n")
        self.file.write("M=D\n")
    
        self.file.write("@SP\n")
        self.file.write("D=M\n")
        self.file.write("@LCL\n")
        self.file.write("M=D\n")
    
        self.file.write(f"@{function_name}\n")
        self.file.write("0;JMP\n")
    
        self.file.write(f"({return_label})\n")

    def write_return(self):
        # assembly for return
        self.file.write("// return\n")
    
        self.file.write("@LCL\n")
        self.file.write("D=M\n")
        self.file.write("@R13\n")
        self.file.write("M=D\n")
    
        self.file.write("@5\n")
        self.file.write("D=A\n")
        self.file.write("@R13\n")
        self.file.write("A=M-D\n")
        self.file.write("D=M\n")
        self.file.write("@R14\n")
        self.file.write("M=D\n")
    
        self.file.write("@SP\n")
        self.file.write("AM=M-1\n")
        self.file.write("D=M\n")
        self.file.write("@ARG\n")
        self.file.write("A=M\n")
        self.file.write("M=D\n")
    
        self.file.write("@ARG\n")
        self.file.write("D=M+1\n")
        self.file.write("@SP\n")
        self.file.write("M=D\n")
    
        self.file.write("@R13\n")
        self.file.write("AM=M-1\n")
        self.file.write("D=M\n")
        self.file.write("@THAT\n")
        self.file.write("M=D\n")
    
        self.file.write("@R13\n")
        self.file.write("AM=M-1\n")
        self.file.write("D=M\n")
        self.file.write("@THIS\n")
        self.file.write("M=D\n")
    
        self.file.write("@R13\n")
        self.file.write("AM=M-1\n")
        self.file.write("D=M\n")
        self.file.write("@ARG\n")
        self.file.write("M=D\n")
    
        self.file.write("@R13\n")
        self.file.write("AM=M-1\n")
        self.file.write("D=M\n")
        self.file.write("@LCL\n")
        self.file.write("M=D\n")
    
        self.file.write("@R14\n")
        self.file.write("A=M\n")
        self.file.write("0;JMP\n")

    def _push_d_to_stack(self):
        # push D register to stack
        self.file.write("@SP\n")
        self.file.write("A=M\n")
        self.file.write("M=D\n")
        self.file.write("@SP\n")
        self.file.write("M=M+1\n")

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
        if segment == "static":
            self.file.write(f"// pop static {index}\n")
            self.file.write("@SP\n")
            self.file.write("AM=M-1\n")
            self.file.write("D=M\n")
            self.file.write(f"@{self.file_name}.{index}\n")
            self.file.write("M=D\n")
            return
        
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
        if segment == "static":
            self.file.write(f"// push static {index}\n")
            self.file.write(f"@{self.file_name}.{index}\n")
            self.file.write("D=M\n")
            self._push_d_to_stack()
            return 
        
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
