import re
import renderer
class Lexer(object):
  def __init__(self, code):
    self.source = code
  def tokenize(self):
    source_index = 0
    tokens = []
    source_code = self.source.split()
    while source_index < len(source_code):
      chip = source_code[source_index]
      if chip in ['==', "/", "+=", "-=", "-", "+", "*", "<", ">", "<=", ">=", "!=", "or", "and", "in", "not", "="]:
        tokens.append(["OPERATOR", chip])
      elif chip == "(":
        tokens.append(["CASE", "("])
      elif chip == ",":
        tokens.append(["SEPERATOR", ","])
      elif chip == ");":
        tokens.append(["CASE", ")"])
        tokens.append(["SEPERATOR", ","])
      elif chip[0] == "?": #Oh, you did it wrong. Here, I'll fix it
        strt = '""'
        comment_full = f"{chip[ 1: ]}"
        while True:
          source_index += 1
          current = source_code[source_index]
          if current[-1] == "?":
            comment_full = "\n" + current[ : -1] + " " +  strt
            tokens.append(["COMMENT", comment_full])
            break
          else:
            comment_full = comment_full + current + " "
      elif re.match("[a-z]", chip.lower()):
        if chip[-1] == ";" and chip[0] != '"':
          if len(chip) != 2:
            tokens.append(["IDENTIFIER", chip[ : -1]])
          else:
            tokens.append(["IDENTIFIER", chip[0]])
          tokens.append(["STATEMENT_END", ";"])
        else:
          tokens.append(["IDENTIFIER", chip])
      elif chip[0] in ['"', "'"] and chip[-1] == chip[0] or chip[-2] == chip[0]:
        if chip[-1] == ";":
          tokens.append(["STRING", chip[ :-1]])
          tokens.append(["STATEMENT_END", ";"])
        else:
          tokens.append(["STRING", chip])

      elif chip[0] in ['"', "'", "'''"]:
          tr = chip[0]
          while True:
            source_index += 1
            chip = chip + f" {source_code[source_index]}"
            if chip[-1] == tr or chip[-2] == tr:
              if chip[-1] == ";":
                tokens.append(["STRING", chip[ : -1]])
                tokens.append(["STATEMENT_END", ";"])
              else:
                tokens.append(["STRING", chip])
              break
            else:
              continue
      elif re.match('[0-9]', chip) or re.match('[0-9]', chip):
        if chip[-1] == ";":
          if len(chip) != 2:
            tokens.append(["INTEGER", chip[ : -1]])
          else:
            tokens.append(["INTEGER", chip[0]])
          tokens.append(["STATEMENT_END", ";"])
        else:
          tokens.append(["INTEGER", chip])
      source_index += 1
    return tokens

