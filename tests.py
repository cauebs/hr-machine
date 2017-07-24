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


def test_digit_exploder():
    registers = [None] * 12
    registers[9] = 0
    registers[10] = 10
    registers[11] = 100

    machine = Machine(registers)

    outbox = machine.run_file('examples/digit-exploder.hr',
                              inbox=[9, 809, 838, 66])
    assert outbox == [9, 8, 0, 9, 8, 3, 8, 6, 6]

    outbox = machine.run_file('examples/digit-exploder.hr',
                              inbox=[819, 14, 544, 92],
                              registers=registers)
    assert outbox == [8, 1, 9, 1, 4, 5, 4, 4, 9, 2]

    outbox = machine.run_file('examples/digit-exploder.hr',
                              inbox=[638, 504, 5, 21, 33],
                              registers=registers)
    assert outbox == [6, 3, 8, 5, 0, 4, 5, 2, 1, 3, 3]


def test_vowel_incinerator():
    registers = [None] * 10
    registers[0:5] = string_to_values('aeiou')
    registers[5] = 0

    machine = Machine(registers)
    outbox = machine.run_file('examples/vowel-incinerator.hr',
                              inbox=string_to_values('AOJEQOQDJTNJQEBNEJCJ'))
    assert outbox == string_to_values('JQQDJTNJQBNJCJ')


def test_string_reverse():
    registers = [None] * 15
    registers[14] = 0

    machine = Machine(registers)

    inbox = string_to_values('cauebs python', zero_terminated=True)
    outbox = machine.run_file('examples/string-reverse.hr', inbox)
    assert outbox == string_to_values('sbeuacnohtyp')

    inbox = string_to_values('human resource', zero_terminated=True)
    outbox = machine.run_file('examples/string-reverse.hr',
                              inbox, registers=registers)
    assert outbox == string_to_values('namuhecruoser')

    inbox = string_to_values('mypy pytest', zero_terminated=True)
    outbox = machine.run_file('examples/string-reverse.hr',
                              inbox, registers=registers)
    assert outbox == string_to_values('ypymtsetyp')


if __name__ == '__main__':
    test_alphabetizer()
