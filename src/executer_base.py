from abc import ABC, abstractmethod

class BaseExecutor(ABC):
  def __init__(self):
    pass

  @abstractmethod
  def on_macro_triggered(self):
    raise NotImplementedError
  
  @abstractmethod
  def parse_macro_key(self, key):
    raise NotImplementedError
  
  def get_menu_items(self):
    pass
  
  def get_settings_items(self):
    return []

class MenuItem():
  def __init__(self, title, icon, callback):
    self.title = title
    self.icon = icon
    self.callback = callback
    self.children = {}

class SettingsItem():
  def __init__(self, title, key, value_type):
    self.title = title
    self.key = key
    self.value_type = value_type