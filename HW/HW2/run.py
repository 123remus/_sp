#!/usr/bin/env python3
import sys
from lexer import lex
from voxast import parse
from codegen import generate_bytecode
from vm import execute

if len(sys.argv) < 2:
    print("Usage: python run.py <source_file.vox>")
    print("Examples:")
    print("  python run.py examples/basic.vox")
    print("  python run.py examples/simple.vox")
    sys.exit(1)

with open(sys.argv[1], 'r') as f:
    source = f.read()

print(f"Compiling {sys.argv[1]}...")

tokens = lex(source)
print(f"Lexical analysis: {len(tokens)} tokens")

program = parse(tokens)
print(f"Parsing: AST generated")

bytecode = generate_bytecode(program)
print(f"Code generation: {len(bytecode.main)} instructions, {len(bytecode.constants)} constants")

print("Running...")
execute(bytecode)
print("Done!")