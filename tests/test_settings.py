from src.settings import SettingsManager

# Mocking and other utilities
import json
import constants
from unittest.mock import patch, mock_open, MagicMock

@patch("builtins.open", mock_open())
def test_initial_configuration_should_have_default_values_when_created():
    with patch("builtins.open", mock_open()):
        mock_open.side_effect = OSError

        # obtain instance, which should resort to defaults despite the error
        settings = SettingsManager()
    
    # Verify that the default values are set despite file error
    assert settings.triggerKey == "ctrl"
    assert settings.selectedExecutor == constants.EXECUTOR_PYNPUT
        
@patch("builtins.open", new_callable=mock_open, read_data='{"triggerKey": "shift", "globalArmKey": "n"}')
def test_configuration_should_change_when_loaded_from_file(mock_file):
    settings = SettingsManager()
    assert settings.triggerKey == "shift"
    assert settings.globalArmKey == "n"

@patch("builtins.open", new_callable=mock_open, read_data='{"version":1, "stratagemKeys": ["w", "a", "s", "d"], "strategemKeyDelay": 50, "strategemKeyDelayJitter": 20}')
@patch("src.settings.SettingsManager.migrate_1_to_2", new_callable=MagicMock)
def test_configuration_should_be_migrated_when_version_is_1(mock_migrate_method, mock_file):
    _ = SettingsManager()
    # Confirm that migrate_1_to_2 was called once.
    mock_migrate_method.assert_called_once()

@patch("builtins.open", new_callable=mock_open, read_data='{"stratagemKeys": ["w", "a", "s", "d"], "strategemKeyDelay": 50, "strategemKeyDelayJitter": 20}')
@patch("src.settings.SettingsManager.migrate_2_to_3", new_callable=MagicMock)
def test_configuration_should_be_migrated_when_version_is_2(mock_migrate_method, mock_file):
    SettingsManager()
    # Confirm that migrate_2_to_3 was called once.
    mock_migrate_method.assert_called_once()

@patch("builtins.open", new_callable=mock_open, read_data='{"stratagemKeys": ["w", "a", "s", "d"], "strategemKeyDelay": 50, "strategemKeyDelayJitter": 20}')
def test_configuration_should_have_certain_updates_if_migrated_to_version_2(mock_file):
    settings = SettingsManager()

    # Assert that the settings has been upgraded to version 2
    assert hasattr(settings, 'version')
    assert settings.version == 4

    # Assert that a misspelled version of stratagemKey* has been updated does not exist
    assert hasattr(settings, 'stratagemKeys')
    assert not hasattr(settings, 'strategemKeys')
    assert not hasattr(settings, 'strategemKeyDelay')
    assert not hasattr(settings, 'strategemKeyDelayJitter')

@patch("builtins.open", mock_open())
def test_should_save_correct_version():
    """
    This test verifies that the 'version' key is correctly saved to the
    settings file with the value of 2. This is crucial for ensuring that
    the settings are being saved with the requisite version information,
    which might be used for future migrations or compatibility checks.
    """

    # Get a singleton instance of Settings
    settings = SettingsManager()
    
    # Trigger the save to file operation
    settings.saveToFile()

    # Simulate the file opening in write mode as per the settings path
    mock_file = open(constants.SETTINGS_PATH, "w")
    # Parse the JSON data written to the simulated file
    written_data = json.loads(mock_file.write.call_args[0][0])

    assert written_data["version"] == 4

@patch("builtins.open", new_callable=mock_open, read_data='{"triggerKey": "shift", "triggerDelay": 50}')
def test_unknown_property_should_be_stored_when_created(mock_file):
    settings = SettingsManager()
    settings.testProp = "ctrl"
    assert settings.testProp == "ctrl"

@patch("builtins.open", mock_open())
def test_should_save_correct_settings_to_file_when_modified():
    settings = SettingsManager()
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
