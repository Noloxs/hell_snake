import sys
from views import Overview, SettingsView,FilterDialog
from macro_executer import MacroExecuter
from model import Model
    
class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.executer = MacroExecuter(self.model)

    def open_settings_window(self):
        settings_view = SettingsView(self)
        settings_view.mainloop()

    def change_theme(self, theme):
        self.model.set_setting("theme", theme)
        self.view.update_label(f"Theme changed to {theme}")
    
    def save_macros(self, macros):
        self.model.macros = macros
        self.view.update_macros()

    def toggle_armed(self):
        self.model.armed = not self.model.armed
        for key, strategem in self.model.macros.items():
            strategem.prepare_strategem()
        self.view.update_armed()
        self.executer.arm(self.model.armed)
    
    def show_change_macro_dialog(self, key):
        dialog = FilterDialog(self, key)
        dialog.mainloop()

    def change_macro_binding(self, key, strategemId):
        self.model.change_macro_binding(key, strategemId)
        self.view.update_macros()
    
    def change_active_loadout(self, loadoutId):
        self.model.set_active_loadout(loadoutId)
        self.view.update_current_loadout()
        self.view.update_macros()
    
    def exit(self):
        sys.exit(0)