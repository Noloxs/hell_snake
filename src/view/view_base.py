from abc import ABC, abstractmethod

class BaseView(ABC):
  def __init__(self):
    pass

@abstractmethod
def update_executor_settings(self, executor):
    raise NotImplementedError

@abstractmethod
def update_macros(self):
    raise NotImplementedError

@abstractmethod
def update_armed(self):
    raise NotImplementedError

@abstractmethod
def update_title_description(self, description):
    raise NotImplementedError

@abstractmethod
def show_change_macro_dialog(self, key):
    raise NotImplementedError

@abstractmethod
def update_current_loadout(self):
    raise NotImplementedError

@abstractmethod
def on_loadout_changed(self):
    raise NotImplementedError