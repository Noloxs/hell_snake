from src.settings import Settings


class Stratagem:
  def __init__(self, name, category, command, icon_name):
    self.name = name
    self.category = category
    self.command = command
    if icon_name == "":
      self.icon_name = "Placeholder.svg"
    else:
      self.icon_name = icon_name
  
  def prepare_stratagem(self, executer):
    self.commandArray=[]
    for input in self.command:
      key = Settings.getInstance().stratagemKeys[input]
      self.commandArray.append(executer.parse_macro_key(key))