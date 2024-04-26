from abc import ABC, abstractmethod

class BaseView(ABC):
  def __init__(self):
    pass

@abstractmethod
def add_executor_settings(self, executor):
    raise NotImplementedError

@abstractmethod
def update_macros(self):
    raise NotImplementedError

@abstractmethod
def update_armed(self):
    raise NotImplementedError

@abstractmethod
def show_change_macro_dialog(self, key):
    raise NotImplementedError

@abstractmethod
def update_current_loadout(self):
    raise NotImplementedError