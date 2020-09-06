
from constructors.objects.Utils import *
from constructors import lexer as lexer
from constructors import parser as parser
import renderer

class Parser(object):
  def __init__(self, tokens):
    self.tokens = tokens
    self.token_index = 0
    self.transpiled_code = ""
    self.indents = 0 # This would be the global variable
  def parse(self):
    line = 0
    count=0
    while self.token_index < len(self.tokens):
      count += 1
      token_type = self.tokens[self.token_index][0]        
      token_value = self.tokens[self.token_index][1]
      # commands
      if token_type == "IDENTIFIER" and token_value == "VAR":
        self.parse_variables(self.tokens[self.token_index: len(self.tokens)])
      elif token_type == "COMMENT":
        self.token_index += 1
      elif token_type == "IDENTIFIER" and token_value == "OUTPUT":
        self.parse_print(self.tokens[self.token_index: len(self.tokens)])
      elif token_type == "IDENTIFIER" and token_value == "CLEAR":
        self.parse_clear(self.tokens[self.token_index: len(self.tokens)])
      elif token_type == "IDENTIFIER" and token_value == "PAUSE":
        self.parse_pause(self.tokens[self.token_index: len(self.tokens)])
      elif token_type == "IDENTIFIER" and token_value == "END_REPEAT":
        self.parse_repeat_end(self.tokens[self.token_index: len(self.tokens)])
      elif token_type == "IDENTIFIER" and token_value == "REPEAT":
        self.parse_repeat(self.tokens[self.token_index: len(self.tokens)])
      elif token_type == "IDENTIFIER" and token_value == "LOAD":
        self.parse_init(self.tokens[self.token_index: len(self.tokens)])
      elif token_type == "IDENTIFIER" and token_value == "FUNCTION":
        self.parse_function(self.tokens[self.token_index: len(self.tokens)])
      elif token_type == "IDENTIFIER" and token_value == "END_FUNCTION":
        self.parse_function_end(self.tokens[self.token_index: len(self.tokens)])
      elif token_type == "IDENTIFIER" and token_value == "CALL":
        self.parse_function_call(self.tokens[self.token_index: len(self.tokens)])
      elif token_type == "COMMENT":
        self.token_index += 1
      else:
        print(renderer.fg.rgb(255, 20, 20)+"\nError: No such command called \""+token_value+"\"\nAll commands must be in uppercase.\n\n")
        exit(2)
        
    
    return "import os\n"+self.transpiled_code
      #end commands

  def run(self):
    exec(self.transpiled_code)
        

  def parse_variables(self, tkns):
    tokens_checked = 0
    name = ''
    operator = ''
    value = ''
    start_val = 0
    for token in range(start_val, len(tkns)):
      token_type = tkns[tokens_checked][0]
      token_value = tkns[tokens_checked][1]
      #print(token_value)
      #print(token_type)
      #print(token)
      if token_type == "STATEMENT_END":
        break
      elif token == 1 and token_type == "IDENTIFIER":
        name = token_value
        print(renderer.fg.rgb(0, 136, 255)+"[Info] "+renderer.fg.rgb(255, 255, 255)+"Parsing variable '"+str(name)+"'...")
      elif token == 1 and token_type != "IDENTIFIER":
        raise ValueError("ERR: Invalid Variable Name: " + token_value)
        quit()
      elif token == 2 and token_type == "VAR_CREATION" and token_value == "-=-":
        operator = "="
      elif token == 2 and token_type == "OPERATOR" and token_value != "-=-":
        operator = token_value
      elif token == 2 and token_type not in ['VAR_CREATION', 'OPERATOR']:
        raise SyntaxError("Unidentified Operator")
        quit()
      elif token == 3 and token_type in ['IDENTIFIER', 'STRING', 'INTEGER', 'BOOL']:
        value = token_value
      elif token == 3 and token_type not in ['IDENTIFIER', 'STRING', 'INTEGER', "BOOL"]:
        raise SyntaxError("Invalid Syntax: " + token_value)
        quit()
      elif token > 3 and token_type in ['OPERATOR', 'IDENTIFIER', 'STRING', 'INTEGER', 'BOOL']:
        value = value + " " + token_value
      elif token > 3 and token_type not in ['OPERATOR', 'IDENTIFIER', 'STRING', 'INTEGER', "BOOL"]:
        raise SyntaxError("Invalid Syntax: "  + token_value)
        quit()
      tokens_checked += 1
    varObj = VarObject()
    self.transpiled_code = self.transpiled_code + varObj.transpile(name, operator, value, self.indents)
    self.token_index += tokens_checked + 1

  def parse_print(self, tkns):
    tokens_checked = 0
    value = ""
    for token in range(0, len(tkns)):
      token_type = tkns[tokens_checked][0]
      token_value = tkns[tokens_checked][1]
      if token_type == "STATEMENT_END":
        break
      elif token == 1 and token_type in ["IDENTIFIER", "STRING", "INTEGER"]:
        value = token_value
      elif token == 1 and token_type not in ["IDENTIFIER", "STRING", "INTEGER"]:
        raise SyntaxError("Invalid Reveal Value: " + token_value)
      elif token > 1 and token_type in ["IDENTIFIER", "STRING", "INTEGER", "OPERATOR"]:
        value = value + token_value
      elif token > 1 and token_type in ["IDENTIFIER", "STRING", "INTEGER", "OPERATOR"]:
        raise SyntaxError("Invalid Reveal Value: " + token_value)
      tokens_checked += 1
    revealObj = RevealObject()
    self.transpiled_code = self.transpiled_code + revealObj.transpile(value, self.indents)
    self.token_index = self.token_index + tokens_checked + 1

  def parse_pause(self, tkns):
    tokens_checked = 0
    value = ""
    for token in range(0, len(tkns)):
      token_type = tkns[tokens_checked][0]
      token_value = tkns[tokens_checked][1]
      if token_type == "STATEMENT_END":
        break
      elif token == 1 and token_type in ["IDENTIFIER", "STRING", "INTEGER"]:
        value = token_value
      elif token == 1 and token_type not in ["IDENTIFIER", "STRING", "INTEGER"]:
        raise SyntaxError("Invalid Reveal Value: " + token_value)
      elif token > 1 and token_type in ["IDENTIFIER", "STRING", "INTEGER", "OPERATOR"]:
        value = value + token_value
      elif token > 1 and token_type in ["IDENTIFIER", "STRING", "INTEGER", "OPERATOR"]:
        raise SyntaxError("Invalid Reveal Value: " + token_value)
      tokens_checked += 1
    revealObj = SleepObject()
    self.transpiled_code = self.transpiled_code + revealObj.transpile(value, self.indents)
    self.token_index = self.token_index + tokens_checked + 1

  def parse_repeat(self, tkns):
    tokens_checked = 0
    value = ""
    for token in range(0, len(tkns)):
      token_type = tkns[tokens_checked][0]
      token_value = tkns[tokens_checked][1]
      if token_type == "STATEMENT_END":
        break
      elif token == 1 and token_type in ["IDENTIFIER", "STRING", "INTEGER"]:
        value = token_value
      elif token == 1 and token_type not in ["IDENTIFIER", "STRING", "INTEGER"]:
        raise SyntaxError("Invalid Reveal Value: " + token_value)
      elif token > 1 and token_type in ["IDENTIFIER", "STRING", "INTEGER", "OPERATOR"]:
        value = value + token_value
      elif token > 1 and token_type in ["IDENTIFIER", "STRING", "INTEGER", "OPERATOR"]:
        raise SyntaxError("Invalid Reveal Value: " + token_value)
      tokens_checked += 1
    revealObj = RepeatObject()
    self.transpiled_code = self.transpiled_code + revealObj.transpile(value, self.indents)
    self.indents += 1 #So, here you would indents once more

    self.token_index = self.token_index + tokens_checked + 1 

  def parse_clear(self, tkns):
    tokens_checked = 1
    clearObj = ClearObject()
    self.transpiled_code = self.transpiled_code + clearObj.transpile()
    self.token_index = self.token_index + tokens_checked + 1
  
  def parse_repeat_end(self, tkns):
    tokens_checked = 1
    clearObj = RENDObject()
    self.transpiled_code = self.transpiled_code + clearObj.transpile(self.indents)
    self.token_index = self.token_index + tokens_checked + 1
    self.indents -= 1

  def parse_init(self, tkns):
    tokens_checked = 0
    name = ''
    start_val = 0
    for token in range(start_val, len(tkns)):
      token_type = tkns[tokens_checked][0]
      token_value = tkns[tokens_checked][1]
      #print(token_value)
      #print(token_type)
      #print(token)
      if token_type == "STATEMENT_END":
        break
      elif token == 1 and token_type == "IDENTIFIER":
        name = token_value
        print(renderer.fg.rgb(0, 136, 255)+"[Info] "+renderer.fg.rgb(255, 255, 255)+"Inserting module '"+str(name)+"'...")
      tokens_checked += 1
    initObject = InitObject()
    self.transpiled_code = self.transpiled_code + initObject.transpile(name, self.indents)
    self.token_index += tokens_checked + 1

  def parse_comments(self, tkns):
    tokens_checked = 0
    name = ""
    start_val = 0
    for token in range(start_val, len(tkns)):
      token_type = tkns[tokens_checked][0]
      token_value = tkns[tokens_checked][1]
      #print(token_value)
      #print(token_type)
      #print(token)
      if token_type == "STATEMENT_END":
        break
      elif token == 1 and token_type == "STRING":
        name = token_value
      tokens_checked += 1
    print(renderer.fg.rgb(0, 136, 255)+"[Info] "+renderer.fg.rgb(255, 255, 255)+"Ignored line due to comment...")
    initObject = CommentObject()
    self.transpiled_code = self.transpiled_code + initObject.transpile(name, self.indents)
    self.token_index += tokens_checked + 1


  def parse_function(self, tkns):
    tokens_checked = 0
    value = ""
    for token in range(0, len(tkns)):
      token_type = tkns[tokens_checked][0]
      token_value = tkns[tokens_checked][1]
      if token_type == "STATEMENT_END":
        break
      elif token == 1 and token_type == "IDENTIFIER":
        name = token_value
        print(renderer.fg.rgb(0, 136, 255)+"[Info] "+renderer.fg.rgb(255, 255, 255)+"Parsing function '"+str(name)+"'...")   
      elif token == 1 and token_type != "IDENTIFIER":
        raise ValueError("")   
      tokens_checked += 1
    revealObj = DEFINEObject()
    self.transpiled_code = self.transpiled_code + revealObj.transpile(name, self.indents)
    self.indents += 1
    self.token_index = self.token_index + tokens_checked + 1 

  def parse_function_end(self, tkns):
    tokens_checked = 0
    value = ""
    for token in range(0, len(tkns)):
      token_type = tkns[tokens_checked][0]
      token_value = tkns[tokens_checked][1]
      if token_type == "STATEMENT_END":
        break
      tokens_checked += 1
    revealObj = DEFINEENDObject()
    self.indents -= 1
    self.transpiled_code = self.transpiled_code + revealObj.transpile(self.indents)
    self.token_index = self.token_index + tokens_checked + 1 

  def parse_function_call(self, tkns):
    tokens_checked = 0
    name = ""
    for token in range(0, len(tkns)):
      token_type = tkns[tokens_checked][0]
      token_value = tkns[tokens_checked][1]
      if token_type == "STATEMENT_END":
        break
      elif token == 1 and token_type == "IDENTIFIER":
        name = token_value
      tokens_checked += 1
    revealObj = DEFINECALLObject()
    self.transpiled_code = self.transpiled_code + revealObj.transpile(name, self.indents)
    self.token_index = self.token_index + tokens_checked + 1 
