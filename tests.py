from hrmachine import Machine, Number
from hrmachine.utils import string_to_letters


registers = [None] * 25
registers[23] = Number(0)
registers[24] = Number(10)

word_a = string_to_letters('cauebs')
word_b = string_to_letters('python')
inbox = word_a + [0] + word_b + [0]
print(inbox)

outbox = Machine(registers).run_file('examples/alphabetizer.hr', inbox)
print(outbox)
