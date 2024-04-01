class Strategem:
  def __init__(self, name, category, command, icon_name):
    self.name = name
    self.category = category
    self.command = command
    self.icon_name = icon_name
  
  def prepare_strategem(self):
    from config import strategemKeys
    self.commandString = ""
    self.commandArray=[]
    for input in self.command:
      self.commandString += strategemKeys[input]
      self.commandArray.append(strategemKeys[input])