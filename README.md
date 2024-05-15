# Hell Snake

Welcome to Hell Snake, a Python program designed for managing and running macros for the game Hell Divers 2.

## Overview

Hell Snake simplifies the process of executing macros in the game Hell Divers 2, allowing players to automate calling strategems within the game.

## Features
### Current

- **Macro Management**: Easily create, edit, and execute macros tailored to your gameplay needs.
- **Customization**: Customize macros to suit your playstyle and preferences.
- **Efficiency**: Enhance your gameplay efficiency by reducing manual input tasks.

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

## Configuration

To configure Hell Snake you need to create or modify a json file named: **settings.json** file located in the root of the project folder

__The easiest way to get started is using the: Dump settings option found in the menu under files. This will print out all the default options in the terminal__

### Change keyboard emulator
Change the value of __selectedExecutor__ to one of the supported emulators e.g. __pyautogui__, __pynput__ or __arduino__

```
"selectedExecutor": "pynput"
```

### Change strategem control keys

#### Trigger key
To change which keys are used to call in stratgems first start by setting the trigger key, this is the key that you hold down while activating your strategems

```
"triggerKey": "ctrl"
```

You can also change the delay that is used between holding the triggerKey and starting to activate the strategems in milliseconds using:

__E.g.: 100ms delay with 30ms of jitter, meaning a delay between 100ms and 130ms__

```
"triggerDelay": 100,
"triggerDelayJitter": 30
```

#### Command keys
The strategem keys are defined as an array in the order: UP, LEFT, DOWN, RIGHT

```
strategemKeys": [
    "w",
    "a",
    "s",
    "d"
  ]
```
You can also change the delay that is used between each strategems key press in milliseconds using:

__E.g.: 30ms delay with 20ms of jitter, meaning a delay between 30ms and 50ms__

```
"strategemKeyDelay": 30,
"strategemKeyDelayJitter": 20
```

### Strategem loadouts

Your loadouts can all be managed through the GUI going to **Loadouts** -> **Edit loadouts**

__The blue options are applied immediately, where as green are only applied after pressing the save button__

#### Loadout options
1) Add a new loadout to your configuration
2) Change which loadout is being edited
3) Rename the loadout
4) Delete the loadout from your configuration
5) Drag and drop to rearrange the macros
6) Click on a macro to select one for editing
7) Press to delete the selected macro from the loadout
8) Press to change strategem assigned to the selected macro
9) Press to add a new macro key
10) Press to apply changes to current loadout

![Image of the edit loadouts menu](https://raw.githubusercontent.com/Noloxs/hell_snake/main/docs/edit_loadouts.png)

### Global arming key
You can define a key which allows you to arm and disarm the macro execution. __This is default off__.
You can us any of the valid input keys and switch between the two supported modes:

- "**toggle**" Which toggles between armed and disarmed with each press
- "**push**" Which arms the macros while the key is pressed down and disarmed when released

```
"globalArmKey": "n",
"globalArmMode": "toggle"
```

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
- Thank you to @nvigneux for creating and sharing the awesome strategem icons. See his repository here: [Helldivers-2-Stratagems-icons-svg](https://github.com/nvigneux/Helldivers-2-Stratagems-icons-svg)
- Thanks to all contributors who have helped improve Hell Snake.

## Support

If you encounter any issues or have any questions, feel free to [open an issue](https://github.com/Noloxs/hell_snake/issues) on GitHub.

---

**Note:** This project is not affiliated with or endorsed by Hell Divers 2 or its developers. It is an independent project created for educational and entertainment purposes only.