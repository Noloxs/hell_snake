import pytest

from src.classes.settings import Settings

# Mocking and other utilities
from unittest.mock import patch, mock_open
import json
from src import constants

class TestSettings:
    def test_singleton_instance_should_be_identical_when_requested_multiple_times(self):
        instance1 = Settings.getInstance()
        instance2 = Settings.getInstance()
        assert instance1 is instance2

    @patch("builtins.open", mock_open())
    def test_initial_configuration_should_have_default_values_when_created(self):
        with patch("builtins.open", mock_open()) as mock_file:
            mock_open.side_effect = OSError

            # obtain instance, which should resort to defaults despite the error
            settings = Settings.getInstance()
        
        # Verify that the default values are set despite file error
        assert settings.triggerKey == "ctrl"
        assert settings.triggerDelay == 100
            
    @patch("builtins.open", new_callable=mock_open, read_data='{"triggerKey": "shift", "triggerDelay": 50}')
    def test_configuration_should_change_when_loaded_from_file(self, mock_file):
        settings = Settings.getInstance()
        # settings.loadFromFile()
        assert settings.triggerKey == "shift"
        assert settings.triggerDelay == 50


    @patch("builtins.open", mock_open())
    def test_should_save_correct_settings_to_file_when_modified(self):
        settings = Settings.getInstance()
        settings.triggerKey = 'alt'
        settings.triggerDelay = 200
        
        settings.saveToFile()

        # Ensure file is saved
        mock_file = open(constants.SETTINGS_PATH, "w")
        # Load the JSON written to the file to verify selected values
        written_data = json.loads(mock_file.write.call_args[0][0])

        # Verify specific values are accurately written to the file
        assert written_data["triggerKey"] == "alt"
        assert written_data["triggerDelay"] == 200

    def teardown_method(self, method):
        # Reset the singleton instance for isolated tests
        Settings._instance = None
