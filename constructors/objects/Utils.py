import textwrap
from constructors import lexer as lexer
from constructors import parser as parser

def indent(text, amount, ch=' '):
  return textwrap.indent(text, amount * ch)

class ClearObject(object):
  def __init__(self):
    self.exec_code = ""
  def transpile(self):
    self.exec_code = self.exec_code + "os.system('cls' if os.name == 'nt' else 'clear')\n"
    return self.exec_code

class RevealObject(object):
  def __init__(self):
    self.exec_code = ""
  def transpile(self, value, indents):
    self.exec_code = self.exec_code + "print(" + value + ")" + "\n"
    for i in range(indents):
      self.exec_code = "\t" + self.exec_code
    return self.exec_code

class VarObject(object):
  def __init__(self):
    self.exec_code = ""
  def transpile(self, name, operator, value, indents):
    self.exec_code = self.exec_code + name + " " + operator + " " + value + "\n"
    for i in range(indents):
      self.exec_code = "\t" + self.exec_code
    return self.exec_code

class SleepObject(object):
  def __init__(self):
    self.exec_code = ""
  def transpile(self, value, indents):
    self.exec_code = self.exec_code + "import time\ntime.sleep("+ str(value) +")\n"
    for i in range(indents):
      self.exec_code = "\t" + self.exec_code
    return self.exec_code

class InitObject(object):
  def __init__(self):
    self.exec_code = ""
  def transpile(self, name, indents):
    with open(name+'.slice', 'r') as lang_data:
      lang_code = lang_data.read()

    lex = lexer.Lexer(lang_code)
    tkns = lex.tokenize()
    parse = parser.Parser(tkns)
    data = parse.parse()
    self.exec_code = self.exec_code + "# MODULE import "+name+".slice\n"
    self.exec_code = self.exec_code + data + "# END import\n\n"

    return self.exec_code

class RepeatObject(object):
  def __init__(self):
    self.exec_code = ""
  def transpile(self, value, indents):
    self.exec_code = self.exec_code + "for i in range("+value+"):\n"
    for i in range(indents):
      self.exec_code = "\t" + self.exec_code
    return self.exec_code

class RENDObject(object):
  def __init__(self):
    self.exec_code = ""
  def transpile(self, indents):
    return self.exec_code

class DEFINEObject(object):
  def __init__(self):
    self.exec_code = ""
  def transpile(self, value, indents):
    self.exec_code = self.exec_code + """def """+value+"""():\n"""
    for i in range(indents):
        self.exec_code = "\t" + self.exec_code
    return self.exec_code

class DEFINEENDObject(object):
  def __init__(self):
    self.exec_code = ""
  def transpile(self, indents):
    self.exec_code = self.exec_code + "\n"
    for i in range(indents):
      self.exec_code = "\t" + self.exec_code
    return self.exec_code

class DEFINECALLObject(object):
  def __init__(self):
    self.exec_code = ""
  def transpile(self, value, indents):
    self.exec_code = self.exec_code + value + "()\n"
    for i in range(indents):
      self.exec_code = "\t" + self.exec_code
    return self.exec_code

class CommentObject(object):
  def __init__(self):
    self.exec_code = ""
  def transpile(self, value, indents):
    value = value[1:]
    end_quote = len(value)-1
    value = value[:end_quote]
    self.exec_code = self.exec_code +"# "+ value + "\n"
    for i in range(indents):
      self.exec_code = "\t" + self.exec_code
    return self.exec_code
