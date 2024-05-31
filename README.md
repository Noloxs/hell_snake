# Hell Snake

Welcome to Hell Snake, a Python program designed for managing and running stratagem macros for the game Hell Divers 2.

## Overview

Hell Snake simplifies the process of executing macros in the game Hell Divers 2, allowing players to automate calling stratagems within the game.

## Features
### Current

- **Macro Management**: Easily create and edit loadouts of your favorite stratagems tailored to your gameplay needs.
- **Customization**: Customize executors, delays macro triggers etc. to suit your playstyle and preferences.
- **Increased democracy**: Enhances your gameplay with at least 17% more democracy.

## Installation

To get started with Hell Snake, follow these steps:

1. Clone the repository to your local machine:

    ```
    git clone https://github.com/Noloxs/hell_snake.git
    ```

2. Navigate to the project directory:

    ```
    cd hell-snake
    ```

3. __Optional:__ run in python virtual environment using:
    
    ```
    python -m venv .venv
    ```

    and then activate it using:

    ```
    source .venv/bin/activate
    ```

4. Install the required dependencies:

    ```
    pip install -r requirements.txt
    ```

## Makefile usage (replaces other installation)

1. Initialize using
    ```
    make init
    ```
2. Run all QA using make
    ```
    make lint test
    ```
3. Run HellSnake
    ```
    make run
    ```

Look into the Makefile for the exact targets and what the do.

## Configuration

All the configuration options in hell snake is accessible through the interface it self.

__NB: Currently settings changes are not saved automatically. To save changes to key bindings, loadouts etc. Go to Files -> Settings -> Save settings__

### System settings
To configure hell snake to your needs go to **Files** -> **Settings** -> **Edit settings**

#### Key Bindings - Stratagem Bindings
Here you can change the keys used in hell divers to call down stratagems

__These should match your in game settings exactly__

#### Key Bindings - Global arm bindings
You can define a key which allows you to arm and disarm the macro execution. __This is default off__.

You can us any of the valid input keys and switch between the two supported modes:

- "**toggle**" Which toggles between armed and disarmed with each press
- "**push**" Which arms the macros while the key is pressed down and disarmed when released

#### Executor Settings
Change the selected executor to one of the supported emulators:

| Executor            | Windows | Linux | Mac OS | Notes                        |
|---------------------|---------|-------|--------|------------------------------|
| Pynput              | ?       | 🮱    | ?      |                              |
| pyautogui           | ?       | 🮱    | ?      |                              |
| Xdotool             | X       | 🮱    | X      |                              |
| Arduino passthrough | 🮱      | 🮱    | ?      | Requires additional hardware |
|

- 🮱 Confirmed to work
- X Not supported
- ? Unconfirmed


Each executor has their own settings to further customize them.
Common among most executors are the trigger delays and stratagem delays

**Trigger delay** Is the delay between holding the 'Open stratagem list' key and starting to activate the stratagems in milliseconds using:

__E.g.: 100ms delay with 30ms of jitter, meaning a delay between 100ms and 130ms__

You can also change the delay that is used between each stratagems key press in milliseconds using:

__E.g.: 30ms delay with 20ms of jitter, meaning a delay between 30ms and 50ms__

### Stratagem loadouts

Your loadouts can all be managed through the GUI going to **Loadouts** -> **Edit loadouts**

__The blue options are applied immediately, where as green are only applied after pressing the apply button (10)__

#### Loadout options
1) Add a new loadout to your configuration
2) Change which loadout is being edited
3) Rename the loadout
4) Delete the loadout from your configuration
5) Drag and drop to rearrange the macros
6) Click on a macro to select one for editing
7) Press to delete the selected macro from the loadout
8) Press to change stratagem assigned to the selected macro
9) Press to add a new macro key
10) Press to apply changes to current loadout

![Image of the edit loadouts menu](https://raw.githubusercontent.com/Noloxs/hell_snake/main/docs/edit_loadouts.png)

## Usage

1. Ensure that you have completed the 'Installation' section.
2. Configure Hell Snake to your preferences. See: 'Configuration'
3. Launch the Hell Snake program by running `python hell_snake.py` or `./hell_snake.py` if using venv.
4. Arm using the menu button or global key
5. Enjoy the enhanced gaming experience with Hell Divers 2!

## Contributing

Contributions to Hell Snake are welcome! If you have any ideas for new features, improvements, or bug fixes, feel free to open an issue or submit a pull request. 

## License

Hell Snake is licensed under the [GNU General Public License v3.0](LICENSE.md).

## Acknowledgements

- Special thanks to the developers of Hell Divers 2 for creating such an exciting game.
- Thank you to @nvigneux for creating and sharing the awesome stratagem icons. See his repository here: [Helldivers-2-Stratagems-icons-svg](https://github.com/nvigneux/Helldivers-2-Stratagems-icons-svg)
- Thanks to all contributors who have helped improve Hell Snake.

## Support

If you encounter any issues or have any questions, feel free to [open an issue](https://github.com/Noloxs/hell_snake/issues) on GitHub.

---

**Note:** This project is not affiliated with or endorsed by Hell Divers 2 or its developers. It is an independent project created for educational and entertainment purposes only.