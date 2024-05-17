import pytest
from src.view.view_utilities import filter_strategems, sort_strategems
from src.strategem import Strategem

@pytest.fixture
def strategems():
    strategems = {}
    strate = Strategem("AC-8 Autocannon", "Weapon", "command", "icon_name")
    strategems.update({1: strate})
    strate = Strategem("Resupply", "Mission", "command", "icon_name")
    strategems.update({2: strate})
    strate = Strategem("Eagle Cluster Bomb", "Eagle", "command", "icon_name")
    strategems.update({3: strate})
    strate = Strategem("Reinforce", "Mission", "command", "icon_name")
    strategems.update({4: strate})

    return strategems

# Define the tests
def test_filter_strategems(strategems):
    filtered = filter_strategems(strategems, "re")
    assert len(filtered) == 2
    assert 2 in filtered
    assert 4 in filtered

    filtered = filter_strategems(strategems, "can")
    assert len(filtered) == 1
    assert 1 in filtered
    
    filtered = filter_strategems(strategems, "")
    assert len(filtered) == len(strategems)

def test_sort_strategems(strategems):
    sorted_strategems = sort_strategems(strategems)
    sorted_ids = list(sorted_strategems.keys())

    # Expected order by category and then name
    expected_order = [3, 4, 2, 1]  # Defensive -> Offensive -> Offensive and Attack -> Counter Attack

    assert sorted_ids == expected_order