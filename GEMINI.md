# Gemini Code Assistant Documentation

This document provides an overview of the Hell Snake project for the Gemini code assistant.

## Project Overview

Hell Snake is a Python application designed to assist players of the game Helldivers 2 by simplifying the process of calling in stratagems. It features a graphical user interface (GUI) built with PyQt5 and 
supports various methods for sending inputs to the game, including keyboard/mouse simulation and integration with hardware devices like Arduino and Raspberry Pi Pico.

The project follows a Model-View-Controller (MVC) architectural pattern to separate concerns and enhance maintainability.

## Key Components

### `hell_snake.py`

This is the main entry entry point of the application. It initializes the necessary components and starts the application.

### `src/`

This directory contains the core source code of the application, organized into the following subdirectories:

-   **`controller.py`**: The central controller that connects the model, view, and input execution components. It handles user interactions and orchestrates the application's logic.
-   **`model.py`**: Manages the application's data, including user settings, stratagem loadouts, and the list of available stratagems.
-   **`view/`**: Contains the GUI implementation. The primary view is built using PyQt5, located in the `src/view/pyqt5/` directory.
-   **`executor/`**: This directory contains different "executor" modules, each responsible for a specific method of sending inputs to the game. This modular design allows for easy extension to support new 
input methods.
-   **`res/`**: Contains application resources such as icons, fonts, and the `stratagems.json` file, which defines the available stratagems and their properties.

### `tests/`

This directory contains the test suite for the application, written using the `pytest` framework.

### `requirements.txt`

This file lists all the Python dependencies required to run the application.

## Development and Collaboration Guidelines

**IMPORTANT**: For all development and collaboration processes, including setting up your environment, making changes, committing, creating and reviewing pull requests, and general developer workflow, always refer to the comprehensive [AI Development Guide](AI-GUIDE.md).

## Feature Development Workflow

When a new feature is requested or needs to be implemented, the AI agent must consult the [AI Development Guide](AI-GUIDE.md) for the following processes:

-   **Defining a New Feature**: Refer to Section 6 of the [AI Development Guide](AI-GUIDE.md) to understand how to gather requirements, ask clarifying questions, and create a detailed feature description document.
-   **Breaking Down a Feature into Tasks**: Refer to Section 7 of the [AI Development Guide](AI-GUIDE.md) to learn how to break down a defined feature into high-level tasks and detailed subtasks, and how to document them in a TODO file.

## Sub-Projects

### Arduino Passthrough

The `arduino_passthrough/` directory contains Arduino sketches (`.ino` files) that enable an Arduino board to act as a USB HID (Human Interface Device) for sending keyboard and mouse inputs to the computer. 
These sketches are designed to work with the `executer_arduino.py` module in the main Hell Snake application, allowing for hardware-based input execution.

To use:
1.  Open the `.ino` file in the Arduino IDE.
2.  Select the correct board and port.
3.  Upload the sketch to your Arduino board.
4.  Ensure the Hell Snake application is configured to use the Arduino executor.

### Pico Passthrough

The `pico_passthrough/` directory contains MicroPython code for Raspberry Pi Pico boards. This code configures the Pico to function as a USB HID, similar to the Arduino, for sending inputs to the game. It 
integrates with the `executer_pico.py` module in the Hell Snake application.

To use:
1.  Ensure your Raspberry Pi Pico is running MicroPython firmware.
2.  Copy the contents of the `pico_passthrough/` directory to the root of your Pico's filesystem.
3.  Ensure the Hell Snake application is configured to use the Pico executor.

### Build and CI

-   **`Makefile`**: Contains commands for building, testing, and cleaning the project.
-   **`.github/workflows/run_test.yml`**: Defines the GitHub Actions workflow for running tests automatically.
