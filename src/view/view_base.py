from abc import ABC, abstractmethod

class BaseView(ABC):
  def __init__(self):
    pass

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

@abstractmethod
def update_executor_menu(self):
    raise NotImplementedError

@abstractmethod
def on_settings_changed(self):
    raise NotImplementedError

def get_settings_items(self):
    return []

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