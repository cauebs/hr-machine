from typing import List
from hrmachine import Letter, Value


def string_to_values(string: str, zero_terminated=False) -> List[Value]:
    output = []
    for word in string.split():
        for char in word:
            if char.isalpha():
                output.append(Letter.from_string(char))
            elif char.isdigit():
                output.append(int(char))
            else:
                raise ValueError(f'Unsupported character {repr(char)}')

        if zero_terminated:
            output.append(0)

    return output
