
class Stratagem:
  def __init__(self, name, category, command, icon_name):
    self.name = name
    self.category = category
    self.command = command
    if icon_name == "":
      self.icon_name = "Placeholder.svg"
    else:
      self.icon_name = icon_name
  
  def prepare(self, controller):
    self.commandArray=[]
    for input in self.command:
      key = controller.get_settings_manager().stratagemKeys[input]
      self.commandArray.append(controller.get_executor().parse_macro_key(key))