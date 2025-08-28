# feat: Centralize Resource Path Management

This feature refactors how the application handles paths to resources like icons, fonts, and data files. Currently, paths are constructed using string concatenation, which is brittle and error-prone. The goal is to create a centralized utility for managing resource paths, making the code cleaner, more robust, and easier to maintain.

---

## User Story
**As a** developer,
**I want to** centralize the way resource paths are generated,
**so that** I can reduce code duplication, improve maintainability, and prevent path-related errors.

---

## Scope
### In Scope
- Creating a new `resource_manager.py` utility for handling resource paths.
- Refactoring all existing code that manually constructs resource paths to use the new utility.
- Adding comprehensive unit tests for the new `ResourceManager`.
- Removing old, redundant path constants from `constants.py`.

### Out of Scope
- Adding new resources (icons, fonts, etc.).
- Changing the location of any existing resources.
- Modifying the resources themselves.

---

## Dependencies and Risks
- **Dependency:** The implementation will rely on Python's built-in `os` or `pathlib` modules for platform-independent path construction.
- **Risk:** A missed or incorrect refactoring of a resource path could lead to `FileNotFoundError` exceptions at runtime. This risk is mitigated by running the full test suite and performing manual UI checks.

---

## Relevant Files
*   `constants.py`
*   `src/model.py`
*   `src/executor/executer_base_serial.py`
*   `src/view/pyqt5/main.py`
*   `src/view/pyqt5/filter_dialog.py`
*   `src/view/pyqt5/edit_config_dialog.py`
*   `src/view/pyqt5/edit_loadout_dialog.py`
*   `tests/test_stratagems_list.py`
*   `src/utilities/resource_manager.py` (created)
*   `tests/test_resource_manager.py` (created)

---

## Implementation Plan
- [x] **Create a new `resource_manager.py` utility file.**
  - [x] This file will be located at `src/utilities/resource_manager.py`.
  - [x] It will contain functions to get paths for different resource types (e.g., icons, fonts, data).
  - [x] The functions will use `os.path.join` or `pathlib` to construct platform-independent paths.
- [x] **Add tests for the new `resource_manager.py`.**
  - [x] Create a new test file `tests/test_resource_manager.py`.
  - [x] Add tests to verify that the path generation functions work as expected.
  - [x] Run `pytest` to ensure the new tests pass.
- [x] **Refactor existing code to use the new `ResourceManager`.**
  - [x] Identify all places in the codebase where resource paths are manually constructed.
  - [x] Replace manual path construction with calls to the new utility functions.
  - [x] This will likely affect files in `src/view/`, `src/model.py`, and `hell_snake.py`.
- [x] **Update `constants.py`**
  - [x] Remove the old path constants that are now replaced by the `ResourceManager`.
  - [x] Keep base path constants that the `ResourceManager` itself will use.
- [x] **Run the full test suite.**
  - [x] Execute `pytest` from the project root.
  - [x] Ensure all existing and new tests pass to verify the refactoring did not break anything.

---

## Acceptance Criteria
- A centralized `ResourceManager` provides a single interface for obtaining resource paths.
- All parts of the application that previously constructed resource paths now use the `ResourceManager`.
- The application successfully loads and displays all visual resources (icons, fonts) at runtime.
- The application successfully loads data resources (e.g., `stratagems.json`).
- All existing and new unit tests pass successfully.
- The application runs without any `FileNotFoundError` or other path-related errors.
