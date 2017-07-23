from hrmachine import Machine, Letter
from hrmachine.utils import string_to_values


def test_string_to_values():
    expected = [Letter.P, Letter.Y, Letter.T, Letter.H, Letter.O, Letter.N]
    assert string_to_values('python') == expected

    expected = [Letter.L, Letter.I, Letter.N, Letter.U, Letter.X, 0]
    assert string_to_values('linux', zero_terminated=True) == expected

    expected = [8, 0, Letter.B, Letter.I, Letter.T, 0]
    assert string_to_values('8 bit', zero_terminated=True) == expected


def test_alphabetizer():
    registers = [None] * 25
    registers[23] = 0
    registers[24] = 10

    machine = Machine(registers)

    inbox = string_to_values('cauebs python', zero_terminated=True)
    outbox = machine.run_file('examples/alphabetizer.hr', inbox)
    assert outbox == string_to_values('cauebs')

    inbox = string_to_values('human resource', zero_terminated=True)
    outbox = machine.run_file('examples/alphabetizer.hr',
                              inbox, registers=registers)
    assert outbox == string_to_values('human')

    inbox = string_to_values('mypy pytest', zero_terminated=True)
    outbox = machine.run_file('examples/alphabetizer.hr',
                              inbox, registers=registers)
    assert outbox == string_to_values('mypy')


if __name__ == '__main__':
    test_alphabetizer()
