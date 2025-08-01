from src.controller import Controller
from src.view.view_base import BaseView
from src.view.textual.main import MainScreen

import threading

class TextualView(BaseView):
    def __init__(self, controller: Controller):
        super().__init__()
        self.app = MainScreen(controller)

    def show_interface(self):
        self.app.run()

    def _call_app(self, method, *args, **kwargs):
        if self.app._running:
            if self.app._thread_id == threading.get_ident():
                method(*args, **kwargs)
            else:
                self.app.call_from_thread(method, *args, **kwargs)

    def update_macros(self):
        self._call_app(self.app.update_macros)

    def update_current_loadout(self):
        self._call_app(self.app.update_current_loadout)

    def update_armed(self):
        self._call_app(self.app.update_armed)

    def update_title_description(self, description):
        self._call_app(self.app.update_title_description, description)

    def on_loadout_changed(self):
        self._call_app(self.app.update_loadout_menu_items)

    def update_executor_menu(self):
        pass

    def on_settings_changed(self):
        pass

    def confirm_save_loadouts(self) -> bool:
        return False

    def get_settings_items(self):
        return []

    def on_exit(self):
        pass
