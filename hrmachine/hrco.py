#!/usr/bin/env python3

import re
import subprocess
from sys import argv


COMMENT_REGEX = re.compile(r'#.*$', re.MULTILINE)
BLANK_LINE_REGEX = re.compile(r'^\s*', re.MULTILINE)
LABEL_REGEX = re.compile(r'.+:\s*', re.MULTILINE)

with open(argv[1]) as f:
    code = f.read()

code = COMMENT_REGEX.sub('', code)
code = BLANK_LINE_REGEX.sub('', code)
instructions = LABEL_REGEX.sub('', code)

subprocess.run(['xclip', '-selection', 'clipboard'],
               input=code, encoding='utf-8')

print(f'Copied {len(instructions.splitlines())} instruction to clipboard!')
