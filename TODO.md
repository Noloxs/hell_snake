# PyQt5 to PyQt6 Migration Checklist

This checklist outlines the necessary steps to migrate the Hell Snake application from PyQt5 to PyQt6.

1.  [ ] **Update Project Dependencies**
    1.1. [ ] Modify `requirements.txt`:
        1.1.1. [ ] Replace `PyQt5` with `PyQt6`.
        1.1.2. [ ] Replace `PyQt5-sip` with `PyQt6-sip` (if explicitly listed).
    1.2. [ ] Reinstall dependencies in the virtual environment:
        1.2.1. [ ] Clean the existing virtual environment (e.g., delete the `.venv` folder).
        1.2.2. [ ] Recreate the virtual environment.
        1.2.3. [ ] `pip install -r requirements.txt`

2.  [ ] **Update Import Statements**
    2.1. [ ] Globally replace `from PyQt5 import` with `from PyQt6 import`.
    2.2. [ ] Specifically, update imports for modules that have changed their location (e.g., `from PyQt5.QtGui import QAction` might become `from PyQt6.QtWidgets import QAction`).

3.  [ ] **Address API Changes**
    3.1. [ ] **Module Restructuring**: Many classes previously in `QtGui` or `QtCore` have moved to `QtWidgets`.
        3.1.1. [ ] Example: `QAction`, `QDesktopServices`, `QScreen` are now typically in `QtWidgets`.
    3.2. [ ] **Enum Value Changes**: Many enum values (e.g., `Qt.AlignRight`, `Qt.Checked`) are now directly accessible as `QtCore.Qt.AlignmentFlag.AlignRight` or `QtCore.Qt.CheckState.Checked`.
        3.2.1. [ ] Use `ruff` or similar tools to identify and fix these.
    3.3. [ ] **Property Access**: Methods like `size().width()`, `pos().x()` are now properties (`size.width`, `pos.x`).
        3.3.1. [ ] Update calls to `width()`, `height()`, `x()`, `y()` on `QSize`, `QPoint`, `QRect`, etc., to use property access.
    3.4. [ ] **`QApplication.instance()`**: Ensure correct usage, though often it remains similar.
    3.5. [ ] **`QPalette` and `QBrush`**: Review color handling, as there might be subtle changes in how colors are applied or retrieved.
    3.6. [ ] **`QPixmap` and `QIcon`**: Check constructors and methods for any breaking changes.
    3.7. [ ] **`QVariant` Removal**: PyQt6 largely removes the need for `QVariant`; Python native types are used directly.
        3.7.1. [ ] Review code that explicitly uses `QVariant` for data storage or retrieval.
    3.8. [ ] **Signal/Slot Syntax**: While PyQt5 supported the new style, ensure all connections use the modern `object.signal.connect(slot)` syntax.

5.  [ ] **Testing and Verification**
    5.1. [ ] Run all existing unit tests (`pytest`).
    5.2. [ ] Manually test all GUI functionalities to ensure correct behavior and visual appearance.
    5.3. [ ] Pay close attention to layout, widget sizing, and event handling.

6.  [ ] **Code Quality and Standards**
    6.1. [ ] Run `ruff format .` to reformat the code according to project standards.
    6.2. [ ] Run `ruff check .` to identify and fix any new linting issues introduced by the migration.

7.  [ ] **Documentation Update (if necessary)**
    7.1. [ ] Update any project documentation that refers to PyQt5 or specific PyQt5 behaviors.