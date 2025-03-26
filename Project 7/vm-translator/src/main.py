import sys
import os
from parser import Parser, CommandType
from code_writer import CodeWriter

def translate_file(input_path, output_path, is_first=True):
    parser = Parser(input_path)
    
    code_writer = CodeWriter(output_path) if is_first else CodeWriter(output_path, append=True)

    while parser.has_more_commands():
        parser.advance()
        command_type = parser.command_type()
        
        if command_type == CommandType.ARITHMETIC:
            code_writer.write_arithmetic(parser.arg1())
        elif command_type in (CommandType.PUSH, CommandType.POP):
            code_writer.write_push_pop(command_type, parser.arg1(), parser.arg2())

    code_writer.close()

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_path>")
        sys.exit(1)

    input_path = sys.argv[1]
    
    # Handles both single file and directory inputs
    if os.path.isdir(input_path):
        output_path = os.path.join(input_path, os.path.basename(input_path) + ".asm")
        
        vm_files = [f for f in os.listdir(input_path) if f.endswith('.vm')]
        vm_files.sort()
        
        if not vm_files:
            print(f"Error: No .vm files found in directory {input_path}")
            sys.exit(1)
            
        # Process each .vm file in directory
        first_file = True
        for filename in vm_files:
            file_path = os.path.join(input_path, filename)
            translate_file(file_path, output_path, is_first=first_file)
            first_file = False
    else:
        # Process a single file
        if not input_path.endswith(".vm"):
            print("Error: Input file must have .vm extension")
            sys.exit(1)
        if not os.path.exists(input_path):
            print(f"Error: File {input_path} not found")
            sys.exit(1)
            
        output_path = input_path.replace(".vm", ".asm")
        translate_file(input_path, output_path)

if __name__ == "__main__":
    main()