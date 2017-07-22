from enum import Enum
from typing import NamedTuple, List, Dict, Union
import re


COMMENT_REGEX = re.compile(r'#.*$')
LABEL_REGEX = re.compile(r'^\s*([a-z]+[a-zA-Z\d]*):\s*$')
POINTER_REGEX = re.compile(r'^\[(\d+)\]$')


class Instruction(NamedTuple):
    line: int
    op: str
    arg: str = None


class Number(int):
    pass


class Letter(Enum):
    (A, B, C, D, E, F, G, H, I, J, K, L, M, N, O,
     P, Q, R, S, T, U, V, W, X, Y, Z) = range(26)

    def __sub__(self, other: 'Letter'):
        return self.value - other.value

    def __repr__(self):
        return self.name


Value = Union[Number, Letter]


class Machine:
    def __init__(self, registers: List[Value]) -> None:
        self._head = None
        self._labels: Dict[str, int] = {}
        self._registers = registers  # maybe copying would be good

    def run(self, code: str, input_values: List[Value]) -> List[Value]:
        self._input = input_values
        self._output: List[Value] = []
        return self._eval(self._parse(code))

    def run_file(self, file: str, input_values: List[Value]) -> List[Value]:
        with open(file) as f:
            code = f.read()
        return self.run(code, input_values)

    def _parse(self, code: str) -> List[Instruction]:
        instructions: List[Instruction] = []
        for i, line in enumerate(code.splitlines()):
            line = COMMENT_REGEX.sub('', line)
            if line.isspace() or not line:
                continue

            label_match = LABEL_REGEX.match(line)
            if label_match:
                label = label_match.group(1)
                self._labels[label] = len(instructions) - 1
                continue

            tokens = line.split()
            if 0 < len(tokens) <= 2:
                instructions.append(Instruction(i, *tokens))
            else:
                raise SyntaxError(f'Invalid line:\n{line}')

        return instructions

    def _eval(self, instructions: List[Instruction]) -> List:
        self._current_line = 0
        while 0 <= self._current_line < len(instructions):
            instruction = instructions[self._current_line]
            self.__getattribute__('_' + instruction.op)(instruction.arg)
            self._current_line += 1

        return self._output

    def _parse_pointer(self, arg):
        pointer_match = POINTER_REGEX.match(arg)
        if pointer_match:
            index = pointer_match.group(1)
            return self._registers[int(index)]
        return arg

    def _INBOX(self, arg):
        if not self._input:
            self._current_line = -2
            return
        self._head = self._input.pop(0)

    def _OUTBOX(self, arg):
        self._output.append(self._head)

    def _COPYFROM(self, arg):
        arg = self._parse_pointer(arg)
        self._head = self._registers[int(arg)]

    def _COPYTO(self, arg):
        arg = self._parse_pointer(arg)
        self._registers[int(arg)] = self._head

    def _ADD(self, arg):
        arg = self._parse_pointer(arg)
        self._head += self._registers[int(arg)]

    def _SUB(self, arg):
        arg = self._parse_pointer(arg)
        self._head -= self._registers[int(arg)]

    def _BUMPUP(self, arg):
        arg = self._parse_pointer(arg)
        self._registers[int(arg)] += 1
        self._head = self._registers[int(arg)]

    def _BUMPDN(self, arg):
        arg = self._parse_pointer(arg)
        self._registers[int(arg)] -= 1
        self._head = self._registers[int(arg)]

    def _JUMP(self, arg):
        self._current_line = self._labels[arg]

    def _JUMPZ(self, arg):
        if self._head == 0:
            self._current_line = self._labels[arg]

    def _JUMPN(self, arg):
        if self._head < 0:
            self._current_line = self._labels[arg]
