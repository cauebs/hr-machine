from typing import NamedTuple
import re


class Instruction(NamedTuple):
    op: str
    arg: str = None


class Machine:
    def __init__(self, n_registers=8):
        self._head = None
        self._registers = [None] * n_registers
        self._labels = {}

    def run(self, code, input_values=[]):
        self._labels = {}
        self.input = input_values
        self.output = []
        return self._eval(self._parse(code))

    def run_file(self, filename, input_values=[]):
        with open(filename) as f:
            code = f.read()
        return self.run(code, input_values)

    def _parse(self, code):
        raw_instructions = code.strip().splitlines()
        instructions = []

        label_regex = re.compile(r'^\s*([a-z])+:\s*$')
        for i, line in enumerate(raw_instructions):
            label_match = label_regex.match(line)
            if label_match:
                label = label_match.group(1)
                self._labels[label] = i
                instructions.append(Instruction('LABEL', label))
                continue

            tokens = line.split()

            if 0 < len(tokens) <= 2:
                instructions.append(Instruction(*tokens))
            else:
                raise SyntaxError(f'Invalid line:\n{line}')

        return instructions

    def _eval(self, instructions):
        operations = {
            'INBOX': self._inbox,
            'OUTBOX': self._outbox,
            'COPYFROM': self._copyfrom,
            'COPYTO': self._copyto,
            'ADD': self._add,
            'SUB': self._sub,
            'BUMPUP': self._bumpup,
            'BUMPDN': self._bumpdn,
            'JUMP': self._jump,
            'JUMPZ': self._jumpz,
            'JUMPN': self._jumpn,
            'LABEL': self._label
        }

        self._current_line = 0
        while 0 <= self._current_line < len(instructions):
            instruction = instructions[self._current_line]
            operations[instruction.op](instruction.arg)
            self._current_line += 1

        return self.output

    def _inbox(self, arg):
        if not self.input:
            self._current_line = -2
            return
        self._head = self.input.pop(0)

    def _outbox(self, arg):
        self.output.append(self._head)

    def _copyfrom(self, arg):
        self._head = self._registers[int(arg)]

    def _copyto(self, arg):
        self._registers[int(arg)] = self._head

    def _add(self, arg):
        self._head += self._registers[int(arg)]

    def _sub(self, arg):
        self._head -= self._registers[int(arg)]

    def _bumpup(self, arg):
        self._registers[int(arg)] += 1
        self._head = self._registers[int(arg)]

    def _bumpdn(self, arg):
        self._registers[int(arg)] -= 1
        self._head = self._registers[int(arg)]

    def _jump(self, arg):
        self._current_line = self._labels[arg]

    def _jumpz(self, arg):
        if self._head == 0:
            self._current_line = self._labels[arg]

    def _jumpn(self, arg):
        if self.head < 0:
            self._current_line = self._labels[arg]

    def _label(self, arg):
        pass
