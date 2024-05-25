import pytest

from src.classes.settings import Settings

# Mocking and other utilities
from unittest.mock import patch, mock_open, MagicMock
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
        assert settings.triggerKey == "shift"
        assert settings.triggerDelay == 50

    @patch("builtins.open", new_callable=mock_open, read_data='{"stratagemKeys": ["w", "a", "s", "d"], "strategemKeyDelay": 50, "strategemKeyDelayJitter": 20}')
    @patch("src.classes.settings.Settings.migrate_1_to_2", new_callable=MagicMock)
    def test_configuration_should_be_migrated_when_version_is_old(self, mock_migrate_method, mock_file):
        settings = Settings.getInstance()
        # Confirm that migrate_1_to_2 was called once.
        mock_migrate_method.assert_called_once()


    @patch("builtins.open", new_callable=mock_open, read_data='{"stratagemKeys": ["w", "a", "s", "d"], "strategemKeyDelay": 50, "strategemKeyDelayJitter": 20}')
    def test_configuration_should_have_certain_updates_if_migrated_to_version_2(self, mock_file):
        settings = Settings.getInstance()

        # Assert that the settings has been upgraded to version 2
        assert hasattr(settings, 'version')
        assert settings.version == 2

        # Assert that a misspelled version of stratagemKey* has been updated does not exist
        assert hasattr(settings, 'stratagemKeys')
        assert settings.strategemKeys  == "unknown"
        assert hasattr(settings, 'stratagemKeyDelay')
        assert settings.strategemKeyDelay == "unknown"
        assert hasattr(settings, 'stratagemKeyDelayJitter')
        assert settings.strategemKeyDelayJitter == "unknown"

    @patch("builtins.open", mock_open())
    def test_should_save_correct_version(self):
        """
        This test verifies that the 'version' key is correctly saved to the
        settings file with the value of 2. This is crucial for ensuring that
        the settings are being saved with the requisite version information,
        which might be used for future migrations or compatibility checks.
        """

        # Get a singleton instance of Settings
        settings = Settings.getInstance()
        
        # Trigger the save to file operation
        settings.saveToFile()

        # Simulate the file opening in write mode as per the settings path
        mock_file = open(constants.SETTINGS_PATH, "w")
        # Parse the JSON data written to the simulated file
        written_data = json.loads(mock_file.write.call_args[0][0])

        assert written_data["version"] == 2

    @patch("builtins.open", new_callable=mock_open, read_data='{"triggerKey": "shift", "triggerDelay": 50}')
    def test_unknown_property_should_be_stored_when_created(self, mock_file):
        settings = Settings.getInstance()
        settings.testProp = "ctrl"
        assert settings.testProp == "ctrl"

    @patch("builtins.open", mock_open())
    def test_should_save_correct_settings_to_file_when_modified(self):
        settings = Settings.getInstance()
        settings.triggerKey = 'alt'
        settings.triggerDelay = 200
        settings.testProp = "test"
        
        settings.saveToFile()

        # Ensure file is saved
        mock_file = open(constants.SETTINGS_PATH, "w")
        # Load the JSON written to the file to verify selected values
        written_data = json.loads(mock_file.write.call_args[0][0])

        # Verify specific values are accurately written to the file
        assert written_data["triggerKey"] == "alt"
        assert written_data["triggerDelay"] == 200
        assert written_data["testProp"] == "test"

    def teardown_method(self, method):
        # Reset the singleton instance for isolated tests
        Settings._instance = None
