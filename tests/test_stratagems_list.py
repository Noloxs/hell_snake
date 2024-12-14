import pytest
import constants
import json
from collections import defaultdict

@pytest.fixture
def stratagems():
    """Load stratagems from a JSON file and return a dictionary of Stratagem objects."""
    with open(constants.RESOURCE_PATH+"stratagems.json") as json_file:
        stratagems = json.load(json_file)

    return stratagems

def test_unique_stratagem_icons(stratagems):
    icon_names = [item['icon_name'] for item in stratagems.values() if 'icon_name' in item and item['icon_name'].strip()]
    # Check if the length of the list matches the length of the set (unique values)
    assert len(icon_names) == len(set(icon_names)), "Duplicate icon names found"

def test_unique_stratagem_icons(stratagems):
    # Dictionary to track occurrences of command arrays
    command_occurrences = defaultdict(list)
    
    # Populate the occurrences dictionary with indices of duplicates
    for key, item in stratagems.items():
        if 'command' in item:
            command_tuple = tuple(item['command'])
            command_occurrences[command_tuple].append(key)
    
    # Find duplicates
    duplicates = {cmd: keys for cmd, keys in command_occurrences.items() if len(keys) > 1}
    
    # If duplicates exist, raise an assertion error and print them
    if duplicates:
        duplicate_info = "\n".join(
            f"Command {cmd} appears in entries {keys}" for cmd, keys in duplicates.items()
        )
        pytest.fail(f"Duplicate command arrays found:\n{duplicate_info}")
