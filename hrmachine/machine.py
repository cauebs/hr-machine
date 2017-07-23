from enum import Enum
from typing import NamedTuple, Iterable, List, Dict, Union
import re


COMMENT_REGEX = re.compile(r'--.*$')
LABEL_REGEX = re.compile(r'^\s*([a-z]+[a-zA-Z\d]*):\s*$')
POINTER_REGEX = re.compile(r'^\[(\d+)\]$')


class Operation(Enum):
    INBOX = 'INBOX'
    OUTBOX = 'OUTBOX'
    COPYFROM = 'COPYFROM'
    COPYTO = 'COPYTO'
    ADD = 'ADD'
    SUB = 'SUB'
    BUMPUP = 'BUMPUP'
    BUMPDN = 'BUMPDN'
    JUMP = 'JUMP'
    JUMPZ = 'JUMPZ'
    JUMPN = 'JUMPN'

    def __str__(self) -> str:
        return self.name


class Instruction(NamedTuple):
    op: Operation
    arg: str
    line: int

    def __repr__(self) -> str:
        return f'{self.line}: {self.op} {self.arg}'


class Letter(Enum):
    (A, B, C, D, E, F, G, H, I, J, K, L, M, N, O,
     P, Q, R, S, T, U, V, W, X, Y, Z) = range(26)

    def __sub__(self, other: 'Letter') -> int:
        return self.value - other.value

    def __repr__(self) -> str:
        return self.name

    def from_string(char: str):
        value = ord(char.upper())
        return Letter(value - ord('A'))


Value = Union[int, Letter]


class Machine:
    head: Value
    registers: List[Value]
    inbox: List[Value]
    output: List[Value]

    def __init__(self, registers: Iterable[Value]) -> None:
        self.head = None
        self.registers = list(registers)

    def run(self, code: str, inbox: Iterable[Value],
            registers: Iterable[Value] = None) -> List[Value]:
        self.inbox = list(inbox)
        self.output = []

        if registers:
            self.registers = list(registers)

        instructions, labels = self._parse(code)
        return self._eval(instructions, labels)

    def run_file(self, file: str, inbox: Iterable[Value],
                 registers: Iterable[Value] = None) -> List[Value]:
        with open(file) as f:
            code = f.read()
        return self.run(code, inbox, registers)

    def _parse(self, code: str) -> List[Instruction]:
        instructions: List[Instruction] = []
        labels: Dict[str, int] = {}

        for i, line in enumerate(code.splitlines()):
            line = COMMENT_REGEX.sub('', line)
            if line.isspace() or not line:
                continue

            label_match = LABEL_REGEX.match(line)
            if label_match:
                label = label_match.group(1)
                labels[label] = len(instructions) - 1
                continue

            opname, *args = line.split()
            op = Operation(opname)
            arg = None if not args else args[0]
            instructions.append(Instruction(op, arg, i))

        return instructions, labels

    def _parse_pointer(self, arg: str) -> Value:
        pointer_match = POINTER_REGEX.match(arg)
        if pointer_match:
            index = pointer_match.group(1)
            return self.registers[int(index)]
        return arg

    def _eval(self, instructions: List[Instruction],
              labels: Dict[str, int]) -> List[Value]:
        current_line = 0
        while current_line < len(instructions):
            instruction = instructions[current_line]
            # print(instruction)
            op, arg, line = instruction

            if op == Operation.INBOX:
                if not self.inbox:
                    current_line = len(instructions)
                    break
                self.head = self.inbox.pop(0)

            elif op == Operation.OUTBOX:
                self.output.append(self.head)

            elif op == Operation.COPYFROM:
                arg = self._parse_pointer(arg)
                self.head = self.registers[int(arg)]

            elif op == Operation.COPYTO:
                arg = self._parse_pointer(arg)
                self.registers[int(arg)] = self.head

            elif op == Operation.ADD:
                arg = self._parse_pointer(arg)
                self.head += self.registers[int(arg)]

            elif op == Operation.SUB:
                arg = self._parse_pointer(arg)
                self.head -= self.registers[int(arg)]

            elif op == Operation.BUMPUP:
                arg = self._parse_pointer(arg)
                self.registers[int(arg)] += 1
                self.head = self.registers[int(arg)]

            elif op == Operation.BUMPDN:
                arg = self._parse_pointer(arg)
                self.registers[int(arg)] -= 1
                self.head = self.registers[int(arg)]

            elif op == Operation.JUMP:
                current_line = labels[arg]

            elif op == Operation.JUMPZ:
                if self.head == 0:
                    current_line = labels[arg]

            elif op == Operation.JUMPN:
                if self.head < 0:
                    current_line = labels[arg]

            else:
                raise SyntaxError(f'Invalid operation {repr(op)}')

            current_line += 1

        return self.output
