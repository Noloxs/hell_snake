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
    return []
  
  def get_settings_items(self):
    return []
  
  @abstractmethod
  def prepare(self):
    raise NotImplementedError

class MenuItem():
  def __init__(self, title, icon, callback, menu_type):
    self.title = title
    self.icon = icon
    self.callback = callback
    self.menu_type = menu_type
    self.children = []

class SettingsItem():
  def __init__(self, title, default_value, key, value_type):
    self.title = title
    self.default_value = default_value
    self.key = key
    self.value_type = value_type