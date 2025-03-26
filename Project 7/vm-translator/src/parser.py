from enum import Enum
from typing import Optional, TextIO

class CommandType(Enum):
    ARITHMETIC = "C_ARITHMETIC"
    PUSH = "C_PUSH"
    POP = "C_POP"
    LABEL = "C_LABEL"
    GOTO = "C_GOTO"
    IF = "C_IF"
    FUNCTION = "C_FUNCTION"
    RETURN = "C_RETURN"
    CALL = "C_CALL"

class Parser:
    def __init__(self, file_path):
        self.file_path = file_path
        self.current_command = None
        self.current_line = 0
        with open(file_path, 'r') as file:
            self.commands = [line.strip() for line in file]
            self.commands = [cmd.split('//')[0].strip() for cmd in self.commands]
            self.commands = [cmd for cmd in self.commands if cmd]
    
    def has_more_commands(self):
        return self.current_line < len(self.commands)
    
    def advance(self):
        if self.has_more_commands():
            self.current_command = self.commands[self.current_line]
            self.current_line += 1
    
    def command_type(self):
        #returns command type
        first_word = self.current_command.split()[0]
        
        if first_word in ['add', 'sub', 'neg', 'eq', 'gt', 'lt', 'and', 'or', 'not']:
            return CommandType.ARITHMETIC
        elif first_word == 'push':
            return CommandType.PUSH
        elif first_word == 'pop':
            return CommandType.POP
        elif first_word == 'label':
            return CommandType.LABEL
        elif first_word == 'goto':
            return CommandType.GOTO
        elif first_word == 'if-goto':
            return CommandType.IF
        elif first_word == 'function':
            return CommandType.FUNCTION
        elif first_word == 'return':
            return CommandType.RETURN
        elif first_word == 'call':
            return CommandType.CALL
        else:
            raise ValueError(f"Unknown command type: {first_word}")

    def arg1(self):
        #returns first argument of command
        if self.command_type() == CommandType.ARITHMETIC:
            return self.current_command
        else:
            return self.current_command.split()[1]

    def arg2(self):
        #returns second argument
        command_type = self.command_type()
        if command_type in [CommandType.PUSH, CommandType.POP, CommandType.FUNCTION, CommandType.CALL]:
            return int(self.current_command.split()[2])
        else:
            raise ValueError(f"Command type {command_type} does not have arg2")