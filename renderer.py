import os

class fg():
  def rgb(r, g, b): 
    if os.name == 'nt':
      return ""
    else:
      return f"\u001b[38;2;{r};{g};{b}m"


class bg():
  def rgb(r, g, b): 
    if os.name == 'nt':
      return ""
    else:
      return f"\u001b[48;2;{r};{g};{b}m"
