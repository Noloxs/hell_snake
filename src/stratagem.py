class Stratagem:
  def __init__(self, name, category, command, icon_name):
    self.name = name
    self.category = category
    self.command = command
    self.icon_name = icon_name
  
  def prepare_stratagem(self, model, executer):
    self.commandArray=[]
    for input in self.command:
      key = model.settings.stratagemKeys[input]
      self.commandArray.append(executer.parse_macro_key(key))