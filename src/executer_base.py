from abc import ABC, abstractmethod

class BaseExecutor(ABC):
  def __init__(self):
    pass

  def start(self):
    pass

  def stop(self):
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