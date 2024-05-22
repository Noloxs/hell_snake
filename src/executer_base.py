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
  
  def attempt_auto_connect(self):
    pass