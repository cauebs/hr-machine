from typing import List
from hrmachine import Letter, Number


def string_to_letters(string: str, zero_terminated=True) -> List[Letter]:
    output = []
    for character in string:
        if character.isalpha():
            output.append(Letter.__getattr__(character.upper()))
        elif character.isdigit():
            output.append(Number(character))
        else:
            raise ValueError('String contains unsupported characters')

    return output
