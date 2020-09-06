import os
import sys
import sys
import argparse
import click
import parser as p
import renderer
from constructors import lexer as lexer
from constructors import parser as p

from alive_progress import alive_bar, config_handler

config_handler.set_global(spinner="classic")
current_path=os.getcwd()
parser = argparse.ArgumentParser(description='tarex.py')
parser.add_argument('-i', '--input', help='The file that you want to convert', required=True, type=str)
parser.add_argument('-o', '--output', help='The output folder name', required=False, type=str)
args = parser.parse_args()
if (args.output == None) == True:
    output = os.path.join(current_path, (os.path.splitext(args.input)[0]+'.py'))
    fname = args.input
else:
    output = os.path.join(current_path, (os.path.splitext(args.output)[0]+''))
    fname = args.input

print()
if fname.endswith(".slice"):
  print(renderer.fg.rgb(0, 136, 255)+"[Info] "+renderer.fg.rgb(255, 255, 255)+"Converting script...")
  with alive_bar(6, bar="classic2") as bar:
    with open(fname, "r") as lang_data:
      lang_code = lang_data.read()
    bar()

    lex = lexer.Lexer(lang_code)
    bar()
    tkns = lex.tokenize()
    bar()
    parse = p.Parser(tkns)
    bar()
    data = parse.parse()
    bar()

    with open(output, "w+") as lang_data:
      lang_code = lang_data.write(data)
    bar()
    

else:
  print(renderer.fg.rgb(255, 20, 0)+"[Err.] "+renderer.fg.rgb(255, 255, 255)+"This script only works on .slice files.")
