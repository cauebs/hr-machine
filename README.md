# HR-Machine

A simple interpreter for the [Human Resource Machine](http://store.steampowered.com/app/375820/Human_Resource_Machine/) instruction set. I highly recommend the game if you like to code.

---

## Usage

While playing the game, you can copy your solution to the clipboard and paste it in either other levels or outside the game.

![screenshot](images/copypaste.png?raw=true)

You can then edit the code in your favourite text editor and run it with the interpreter:

```python
>>> from hrmachine import Machine
>>> from hrmachine.utils import string_to_values

>>> machine = Machine(registers=[None])

>>> code = '''
... start:
... INBOX
... COPYTO 0
... INBOX
... ADD 0
... OUTBOX
... JUMP start'''

>>> inbox = [3, 1, 4, 1, 5, 9, 2, 6]
>>> outbox = machine.run(code, inbox)
>>> outbox
[4, 5, 14, 8]
```

The simple example above repeatedly takes two items from input and outputs their sum. For a more complex example, see the alphabetizer example at `examples/alphabetizer.hr` (or play the game :D)

---

## To do

+ turn it into a CLI tool
+ packaging
+ more examples
+ more tests
+ better exceptions