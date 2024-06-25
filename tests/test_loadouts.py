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

def test_get_current_loadout_should_return_first_loadout_if_none_selected():
    mock_data = {
        "1": {"name": "Loadout 1", "macroKeys": {"1": "1"}},
        "2": {"name": "Loadout 2", "macroKeys": {"2": "2"}}
    }
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
        loadout_manager = LoadoutManager()

        assert loadout_manager.getCurrentLoadout() == "1"

def test_set_current_loadout_should_change_current_loadout():
    loadout_manager = LoadoutManager()
    loadout_manager.loadouts["2"] = Loadout("Loadout 2", {"2": "2"})
    loadout_manager.setCurrentLoadout("2")
    assert loadout_manager.getCurrentLoadout() == "2"

def test_set_current_loadout_should_not_change_current_loadout_if_invalid():
    mock_data = {
        "1": {"name": "Loadout 1", "macroKeys": {"1": "1"}},
        "2": {"name": "Loadout 2", "macroKeys": {"2": "2"}}
    }
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
        loadout_manager = LoadoutManager()
        loadout_manager.setCurrentLoadout("3")
        assert loadout_manager.getCurrentLoadout() == "1"

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
