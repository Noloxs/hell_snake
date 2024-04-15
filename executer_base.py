from abc import ABC, abstractmethod

class BaseExecutor(ABC):
  def __init__(self):
    pass

  @abstractmethod
  def on_macro_triggered(self):
    raise NotImplementedError

  @abstractmethod
  def add_settings(self, overview):
    pass