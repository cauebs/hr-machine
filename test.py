from main import Machine


instructions = '''
a:
b:
    INBOX
    JUMPZ    e
    COPYTO   1
    INBOX
    JUMPZ    f
    COPYTO   0
    COPYFROM 9
    COPYTO   2
c:
    ADD      1
    COPYTO   2
    BUMPDN   0
    JUMPZ    d
    COPYFROM 2
    JUMP     c
d:
    COPYFROM 2
    OUTBOX
    JUMP     b
e:
    INBOX
    COPYFROM 9
f:
    OUTBOX
    JUMP     a
'''

m = Machine(n_registers=10)
m._registers[9] = 0
print(m.run(instructions, input_values=[3,1,4,1,5,9,2,6]))
