import subprocess
import os

# Theme constants
THEME_AUTO = "auto"
THEME_LIGHT = "light"
THEME_DARK = "dark"


class Theme:
    """Color scheme definition."""

    def __init__(self, name, colors):
        self.name = name
        self.colors = colors

    def __getattr__(self, name):
        if name in self.__dict__.get('colors', {}):
            return self.colors[name]
        raise AttributeError(f"'{type(self).__name__}' has no color '{name}'")


# Light theme colors
LIGHT_THEME = Theme("light", {
    "window_bg": "#ffffff",
    "window_fg": "#000000",
    "menu_bg": "#f5f5f5",
    "menu_fg": "#000000",
    "menu_hover": "#e0e0e0",
    "list_bg": "#ffffff",
    "list_fg": "#000000",
    "list_hover": "#f0f0f0",
    "list_selected": "#e3f2fd",
    "input_bg": "#ffffff",
    "input_fg": "#000000",
    "input_border": "#cccccc",
    "button_bg": "#f0f0f0",
    "button_fg": "#000000",
    "button_hover": "#e0e0e0",
    "button_pressed": "#d0d0d0",
    "header_bg": "#e6e6e4",
    "header_fg": "#000000",
    "separator": "#cccccc",
    "armed_bar": "red",
    "disarmed_bar": "gray",
    "stratagem_bg": "#1f2832",
    "link": "#0066cc",
    "scrollbar_bg": "#f0f0f0",
    "scrollbar_handle": "#c0c0c0",
})

# Dark theme colors
DARK_THEME = Theme("dark", {
    "window_bg": "#1e1e1e",
    "window_fg": "#e0e0e0",
    "menu_bg": "#2d2d2d",
    "menu_fg": "#e0e0e0",
    "menu_hover": "#3d3d3d",
    "list_bg": "#252526",
    "list_fg": "#e0e0e0",
    "list_hover": "#2a2d2e",
    "list_selected": "#094771",
    "input_bg": "#3c3c3c",
    "input_fg": "#e0e0e0",
    "input_border": "#555555",
    "button_bg": "#3c3c3c",
    "button_fg": "#e0e0e0",
    "button_hover": "#4a4a4a",
    "button_pressed": "#555555",
    "header_bg": "#2d2d2d",
    "header_fg": "#e0e0e0",
    "separator": "#404040",
    "armed_bar": "#ff4444",
    "disarmed_bar": "#555555",
    "stratagem_bg": "#1f2832",
    "link": "#4da6ff",
    "scrollbar_bg": "#2d2d2d",
    "scrollbar_handle": "#555555",
})


def detect_system_theme():
    """
    Detect if the system is using dark mode.
    Returns 'dark' or 'light'.
    """
    # Method 1: Check GNOME/GTK settings via gsettings
    try:
        result = subprocess.run(
            ["gsettings", "get", "org.gnome.desktop.interface", "color-scheme"],
            capture_output=True, text=True, timeout=2
        )
        if "dark" in result.stdout.lower():
            return THEME_DARK
        elif "light" in result.stdout.lower() or "default" in result.stdout.lower():
            return THEME_LIGHT
    except (subprocess.SubprocessError, FileNotFoundError):
        pass

    # Method 2: Check GTK theme name
    try:
        result = subprocess.run(
            ["gsettings", "get", "org.gnome.desktop.interface", "gtk-theme"],
            capture_output=True, text=True, timeout=2
        )
        if "dark" in result.stdout.lower():
            return THEME_DARK
    except (subprocess.SubprocessError, FileNotFoundError):
        pass

    # Method 3: Check KDE Plasma settings
    try:
        kde_config = os.path.expanduser("~/.config/kdeglobals")
        if os.path.exists(kde_config):
            with open(kde_config) as f:
                content = f.read().lower()
                if "breezedark" in content or "dark" in content:
                    return THEME_DARK
    except (IOError, OSError):
        pass

    # Method 4: Check environment variable (some DEs set this)
    if os.environ.get("GTK_THEME", "").lower().endswith(":dark"):
        return THEME_DARK

    # Method 5: Check XDG portal (Flatpak/modern Linux)
    try:
        result = subprocess.run(
            ["dbus-send", "--session", "--print-reply", "--dest=org.freedesktop.portal.Desktop",
             "/org/freedesktop/portal/desktop", "org.freedesktop.portal.Settings.Read",
             "string:org.freedesktop.appearance", "string:color-scheme"],
            capture_output=True, text=True, timeout=2
        )
        # color-scheme: 0=no preference, 1=dark, 2=light
        if "uint32 1" in result.stdout:
            return THEME_DARK
    except (subprocess.SubprocessError, FileNotFoundError):
        pass

    # Default to light theme
    return THEME_LIGHT


def get_theme(theme_preference):
    """
    Get the theme based on user preference.
    theme_preference: 'auto', 'light', or 'dark'
    """
    if theme_preference == THEME_AUTO:
        system_theme = detect_system_theme()
        return DARK_THEME if system_theme == THEME_DARK else LIGHT_THEME
    elif theme_preference == THEME_DARK:
        return DARK_THEME
    else:
        return LIGHT_THEME


def generate_stylesheet(theme):
    """Generate a Qt stylesheet for the given theme."""
    return f"""
        /* Main window */
        QMainWindow, QDialog {{
            background-color: {theme.colors['window_bg']};
            color: {theme.colors['window_fg']};
        }}

        QWidget {{
            background-color: {theme.colors['window_bg']};
            color: {theme.colors['window_fg']};
        }}

        /* Menu bar */
        QMenuBar {{
            background-color: {theme.colors['menu_bg']};
            color: {theme.colors['menu_fg']};
            border-bottom: 1px solid {theme.colors['separator']};
        }}

        QMenuBar::item {{
            background-color: transparent;
            padding: 4px 8px;
        }}

        QMenuBar::item:selected {{
            background-color: {theme.colors['menu_hover']};
        }}

        /* Menus */
        QMenu {{
            background-color: {theme.colors['menu_bg']};
            color: {theme.colors['menu_fg']};
            border: 1px solid {theme.colors['separator']};
        }}

        QMenu::item {{
            padding: 5px 20px;
        }}

        QMenu::item:selected {{
            background-color: {theme.colors['menu_hover']};
        }}

        QMenu::separator {{
            height: 1px;
            background-color: {theme.colors['separator']};
            margin: 4px 0px;
        }}

        /* List widgets */
        QListWidget {{
            background-color: {theme.colors['list_bg']};
            color: {theme.colors['list_fg']};
            border: none;
        }}

        QListWidget::item {{
            background-color: transparent;
        }}

        QListWidget::item:hover {{
            background-color: {theme.colors['list_hover']};
        }}

        QListWidget::item:selected {{
            background-color: {theme.colors['list_selected']};
        }}

        /* Labels */
        QLabel {{
            color: {theme.colors['window_fg']};
            background-color: transparent;
        }}

        /* Buttons */
        QPushButton {{
            background-color: {theme.colors['button_bg']};
            color: {theme.colors['button_fg']};
            border: 1px solid {theme.colors['input_border']};
            padding: 5px 10px;
            border-radius: 3px;
        }}

        QPushButton:hover {{
            background-color: {theme.colors['button_hover']};
        }}

        QPushButton:pressed {{
            background-color: {theme.colors['button_pressed']};
        }}

        /* Line edits */
        QLineEdit {{
            background-color: {theme.colors['input_bg']};
            color: {theme.colors['input_fg']};
            border: 1px solid {theme.colors['input_border']};
            padding: 4px;
            border-radius: 3px;
        }}

        QLineEdit:focus {{
            border: 1px solid {theme.colors['link']};
        }}

        /* Spin boxes */
        QSpinBox {{
            background-color: {theme.colors['input_bg']};
            color: {theme.colors['input_fg']};
            border: 1px solid {theme.colors['input_border']};
            padding: 4px;
        }}

        /* Combo boxes */
        QComboBox {{
            background-color: {theme.colors['input_bg']};
            color: {theme.colors['input_fg']};
            border: 1px solid {theme.colors['input_border']};
            padding: 4px;
            border-radius: 3px;
        }}

        QComboBox::drop-down {{
            border: none;
        }}

        QComboBox QAbstractItemView {{
            background-color: {theme.colors['menu_bg']};
            color: {theme.colors['menu_fg']};
            selection-background-color: {theme.colors['menu_hover']};
        }}

        /* Tab widgets */
        QTabWidget::pane {{
            border: 1px solid {theme.colors['separator']};
            background-color: {theme.colors['window_bg']};
        }}

        QTabBar::tab {{
            background-color: {theme.colors['button_bg']};
            color: {theme.colors['button_fg']};
            padding: 8px 16px;
            border: 1px solid {theme.colors['separator']};
            border-bottom: none;
        }}

        QTabBar::tab:selected {{
            background-color: {theme.colors['window_bg']};
        }}

        QTabBar::tab:hover:!selected {{
            background-color: {theme.colors['button_hover']};
        }}

        /* Scroll bars */
        QScrollBar:vertical {{
            background-color: {theme.colors['scrollbar_bg']};
            width: 12px;
        }}

        QScrollBar::handle:vertical {{
            background-color: {theme.colors['scrollbar_handle']};
            min-height: 20px;
            border-radius: 4px;
            margin: 2px;
        }}

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}

        QScrollBar:horizontal {{
            background-color: {theme.colors['scrollbar_bg']};
            height: 12px;
        }}

        QScrollBar::handle:horizontal {{
            background-color: {theme.colors['scrollbar_handle']};
            min-width: 20px;
            border-radius: 4px;
            margin: 2px;
        }}

        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}

        /* Frames */
        QFrame[frameShape="4"] {{ /* HLine */
            color: {theme.colors['separator']};
            background-color: {theme.colors['separator']};
        }}

        /* Message boxes */
        QMessageBox {{
            background-color: {theme.colors['window_bg']};
            color: {theme.colors['window_fg']};
        }}
    """


class ThemeManager:
    """Manages application theming."""

    _instance = None
    _theme = None
    _app = None

    @classmethod
    def initialize(cls, app, settings_manager):
        """Initialize the theme manager with the QApplication instance."""
        cls._app = app
        cls._settings = settings_manager
        cls.apply_theme()

    @classmethod
    def get_current_theme(cls):
        """Get the currently active theme."""
        if cls._theme is None:
            preference = getattr(cls._settings, 'theme', THEME_AUTO) if cls._settings else THEME_AUTO
            cls._theme = get_theme(preference)
        return cls._theme

    @classmethod
    def apply_theme(cls):
        """Apply the theme based on settings."""
        if cls._app is None:
            return

        preference = getattr(cls._settings, 'theme', THEME_AUTO) if cls._settings else THEME_AUTO
        cls._theme = get_theme(preference)
        stylesheet = generate_stylesheet(cls._theme)
        cls._app.setStyleSheet(stylesheet)

    @classmethod
    def set_theme(cls, theme_preference):
        """Set and apply a new theme preference."""
        if cls._settings:
            cls._settings.theme = theme_preference
        cls.apply_theme()

    @classmethod
    def is_dark_mode(cls):
        """Check if currently in dark mode."""
        theme = cls.get_current_theme()
        return theme.name == "dark"
