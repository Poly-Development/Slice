import os
import sys
import argparse
import parser as p
import renderer
from constructors import lexer as lexer
from constructors import parser as p

current_path=os.getcwd()
parser = argparse.ArgumentParser(description='tarex.py')
parser.add_argument('-r', '--run', help='The script that you want to run', required=True, type=str)
args = parser.parse_args()

fname = args.run
print()
if fname.endswith(".slice"):
  print(renderer.fg.rgb(0, 136, 255)+"[Info] "+renderer.fg.rgb(255, 255, 255)+"Converting script...")

  with open(fname, "r") as lang_data:
    lang_code = lang_data.read()

  lex = lexer.Lexer(lang_code)
  tkns = lex.tokenize()
  parse = p.Parser(tkns)
  data = parse.parse()
  parse.run()
    

else:
  print(renderer.fg.rgb(255, 20, 0)+"[Err.] "+renderer.fg.rgb(255, 255, 255)+"This script only works on .slice files.")
