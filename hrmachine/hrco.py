#!/usr/bin/env python3

import re
import subprocess
from sys import argv


with open(argv[1]) as f:
    code = f.read()

comment_regex = re.compile(r'#.*$', re.MULTILINE)
blank_line_regex = re.compile(r'^\s*', re.MULTILINE)
label_regex = re.compile(r'.+:\s*', re.MULTILINE)

code = comment_regex.sub('', code)
code = blank_line_regex.sub('', code)
instructions = label_regex.sub('', code)

subprocess.run(['xclip', '-selection', 'clipboard'],
               input=code, encoding='utf-8')

print(f'Copied {len(instructions.splitlines())} instruction to clipboard!')
