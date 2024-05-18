import pytest
from src.view.view_utilities import filter_stratagems, sort_stratagems
from src.stratagem import Stratagem

@pytest.fixture
def stratagems():
    stratagems = {}
    strata = Stratagem("AC-8 Autocannon", "Weapon", "command", "icon_name")
    stratagems.update({1: strata})
    strata = Stratagem("Resupply", "Mission", "command", "icon_name")
    stratagems.update({2: strata})
    strata = Stratagem("Eagle Cluster Bomb", "Eagle", "command", "icon_name")
    stratagems.update({3: strata})
    strata = Stratagem("Reinforce", "Mission", "command", "icon_name")
    stratagems.update({4: strata})

    return stratagems

# Define the tests
def test_filter_stratagems(stratagems):
    filtered = filter_stratagems(stratagems, "re")
    assert len(filtered) == 2
    assert 2 in filtered
    assert 4 in filtered

    filtered = filter_stratagems(stratagems, "can")
    assert len(filtered) == 1
    assert 1 in filtered
    
    filtered = filter_stratagems(stratagems, "")
    assert len(filtered) == len(stratagems)

def test_sort_stratagems(stratagems):
    sorted_stratagems = sort_stratagems(stratagems)
    sorted_ids = list(sorted_stratagems.keys())

    # Expected order by category and then name
    expected_order = [3, 4, 2, 1]  # Defensive -> Offensive -> Offensive and Attack -> Counter Attack

    assert sorted_ids == expected_order