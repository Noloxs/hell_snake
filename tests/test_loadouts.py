import pytest
from unittest.mock import patch, mock_open, MagicMock
import json
from src.loadouts import LoadoutManager, Loadout
import constants

@pytest.fixture(autouse=True, scope="function")
def reset_loadout_manager_instance():
    yield
    LoadoutManager._instance = None  # This ensures the instance is reset after each test

def test_load_from_file_should_populate_loadouts_when_file_exists():
    mock_data = {
        "1": {"name": "Loadout 1", "macroKeys": {"1": "1"}},
        "2": {"name": "Loadout 2", "macroKeys": {"2": "2"}}
    }
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
        loadout_manager = LoadoutManager()
        assert len(loadout_manager.loadouts) == 2
        assert loadout_manager.loadouts["1"].name == "Loadout 1"
        assert loadout_manager.loadouts["2"].name == "Loadout 2"

def test_load_from_file_should_not_change_loadouts_when_file_does_not_exist():
    with patch("builtins.open", side_effect=OSError):
        loadout_manager = LoadoutManager()
        assert len(loadout_manager.loadouts) == 1

def test_save_to_file_should_write_correct_data():
    loadout_manager = LoadoutManager()
    loadout_manager.loadouts["1"] = Loadout("Loadout 1", {"1": "1"})
    loadout_manager.loadouts["2"] = Loadout("Loadout 2", {"2": "2"})

    with patch("builtins.open", mock_open()) as mock_file:
        loadout_manager.saveToFile()

    mock_file.assert_called_once_with(constants.LOADOUTS_PATH, "w")
    handle = mock_file()
    handle.write.assert_called_once()
    written_data = json.loads(handle.write.call_args[0][0])
    assert written_data["1"]["name"] == "Loadout 1"
    assert written_data["2"]["name"] == "Loadout 2"

def test_export_to_json_should_write_correct_data():
    loadout_manager = LoadoutManager()
    loadout_manager.loadouts["1"] = Loadout("Loadout 1", {"1": "1"})
    loadout_manager.loadouts["2"] = Loadout("Loadout 2", {"2": "2"})

    mock_file_path = "/tmp/exported_loadouts.json"
    with patch("builtins.open", mock_open()) as mock_file:
        loadout_manager.exportLoadoutsToJson(mock_file_path)

    mock_file.assert_called_once_with(mock_file_path, "w")
    handle = mock_file()
    written_data = json.loads(handle.write.call_args[0][0])
    assert written_data["1"]["name"] == "Loadout 1"
    assert written_data["2"]["name"] == "Loadout 2"

def test_attach_change_listener_should_add_callback_to_observers():
    loadout_manager = LoadoutManager()
    callback = MagicMock()
    loadout_manager.attach_change_listener(callback)
    assert callback in loadout_manager._observers

def test_detach_change_listener_should_remove_callback_from_observers():
    loadout_manager = LoadoutManager()
    callback = MagicMock()
    loadout_manager.attach_change_listener(callback)
    loadout_manager.detach_change_listener(callback)
    assert callback not in loadout_manager._observers

def test_notify_change_should_call_all_callbacks():
    loadout_manager = LoadoutManager()
    callback1 = MagicMock()
    callback2 = MagicMock()
    loadout_manager.attach_change_listener(callback1)
    loadout_manager.attach_change_listener(callback2)
    loadout_manager.notify_change()
    callback1.assert_called_once()
    callback2.assert_called_once()

def test_import_from_json_should_replace_loadouts_on_valid_file():
    mock_data = {
        "3": {"name": "Imported Loadout 3", "macroKeys": {"3": "3"}},
        "4": {"name": "Imported Loadout 4", "macroKeys": {"4": "4"}}
    }
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
        loadout_manager = LoadoutManager()
        # Ensure initial loadouts are present
        assert len(loadout_manager.loadouts) > 0
        
        result = loadout_manager.importLoadoutsFromJson("/tmp/imported_loadouts.json")
        assert result is True
        assert len(loadout_manager.loadouts) == 2
        assert loadout_manager.loadouts["3"].name == "Imported Loadout 3"
        assert loadout_manager.loadouts["4"].name == "Imported Loadout 4"

def test_import_from_json_should_return_false_on_invalid_json():
    with patch("builtins.open", mock_open(read_data="invalid json")):
        loadout_manager = LoadoutManager()
        initial_loadouts_count = len(loadout_manager.loadouts)
        result = loadout_manager.importLoadoutsFromJson("/tmp/invalid.json")
        assert result is False
        assert len(loadout_manager.loadouts) == initial_loadouts_count # Loadouts should not change

def test_import_from_json_should_return_false_on_invalid_data_structure():
    mock_data = {
        "3": "not a dict",
        "4": {"name": "Imported Loadout 4", "macroKeys": {"4": "4"}}
    }
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
        loadout_manager = LoadoutManager()
        initial_loadouts_count = len(loadout_manager.loadouts)
        result = loadout_manager.importLoadoutsFromJson("/tmp/invalid_structure.json")
        assert result is False
        assert len(loadout_manager.loadouts) == initial_loadouts_count # Loadouts should not change
