from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static, Label, ListView, ListItem, Select

class MainScreen(App):
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("s", "save_settings", "Save Settings"),
        ("l", "save_loadouts", "Save Loadouts"),
        ("e", "edit_config", "Edit Config"),
        ("a", "toggle_armed", "Arm/Disarm"),
        ("t", "edit_loadouts", "Edit Loadouts"),
    ]

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            with Horizontal(id="header-container"):
                yield Static(id="armed-icon")
                with Vertical(id="title-container"):
                    yield Label(id="loadout-name")
                    yield Static(id="title-line")
                    yield Label(id="loadout-description")
            yield Static(id="armed-bar")
            yield Select([], id="loadout-select", prompt="Select Loadout")
            yield ListView(id="macro-list")
        yield Footer()

    def on_mount(self) -> None:
        self.update_armed()
        self.update_current_loadout()
        self.update_macros()
        self.update_loadout_menu_items()

    def action_save_settings(self) -> None:
        self.controller.get_settings_manager().saveToFile()

    def action_save_loadouts(self) -> None:
        self.controller.get_loadouts_manager().saveToFile()

    def action_edit_config(self) -> None:
        # Placeholder for editing config
        pass

    def action_toggle_armed(self) -> None:
        self.controller.toggle_armed()
        self.update_armed()

    def action_edit_loadouts(self) -> None:
        # Placeholder for editing loadouts
        pass

    def on_select_changed(self, event: Select.Changed) -> None:
        if event.select.id == "loadout-select":
            self.controller.set_active_loadout(event.value)
            self.update_current_loadout()
            self.update_macros()

    def update_loadout_menu_items(self):
        loadout_select = self.query_one("#loadout-select", Select)
        loadouts = []
        for loadoutId, loadout in self.controller.get_loadouts_manager().loadouts.items():
            loadouts.append((loadout.name, loadoutId))
        loadout_select.set_options(loadouts)
        loadout_select.value = self.controller.get_active_loadout_id()

    def update_macros(self):
        macro_list = self.query_one("#macro-list", ListView)
        macro_list.clear()
        for key, value in self.controller.getAllMacros():
            macro_list.append(ListItem(Label(f"{key}: {value.name}")))

    def update_armed(self):
        if self.controller.is_armed():
            self.query_one("#armed-icon").update("X")  # Placeholder
            self.query_one("#armed-bar").styles.background = "red"
        else:
            self.query_one("#armed-icon").update("O")  # Placeholder
            self.query_one("#armed-bar").styles.background = "gray"

    def update_current_loadout(self):
        current_loadout = self.controller.get_active_loadout()
        if current_loadout:
            self.query_one("#loadout-name").update(current_loadout.name.upper())
            self.update_title_description(current_loadout.name.upper())
        else:
            self.query_one("#loadout-name").update("")
            self.update_title_description(None)

    def update_title_description(self, description):
        title_line = self.query_one("#title-line")
        loadout_description = self.query_one("#loadout-description")
        if description:
            title_line.styles.visibility = "visible"
            loadout_description.update(description)
            loadout_description.styles.visibility = "visible"
        else:
            title_line.styles.visibility = "hidden"
            loadout_description.styles.visibility = "hidden"
