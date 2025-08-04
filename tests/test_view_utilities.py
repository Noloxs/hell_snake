import pytest
from src.view.view_utilities import filter_stratagems, sort_stratagems
from src.stratagem import Stratagem

@pytest.fixture
def stratagems():
    stratagems = {}
    strata = Stratagem("AC-8 Autocannon", "Weapon", "command", "")
    stratagems.update({1: strata})
    strata = Stratagem("Resupply", "Mission", "command", "icon_name")
    stratagems.update({2: strata})
    strata = Stratagem("Eagle Cluster Bomb", "Eagle", "command", "icon_name")
    stratagems.update({3: strata})
    strata = Stratagem("Reinforce", "Mission", "command", "icon_name")
    stratagems.update({4: strata})
    strata = Stratagem("StA-X3 W.A.S.P. Launcher", "Weapon", "command", "")
    stratagems.update({5: strata})
    strata = Stratagem("GL-21 Grenade Launcher", "Weapon", "command", "")
    stratagems.update({6: strata})

    return stratagems

# Define the tests
def test_filter_stratagems(stratagems):
    filtered = filter_stratagems(stratagems, "re")
    assert len(filtered) == 3
    assert 2 in filtered
    assert 4 in filtered
    assert 6 in filtered

    filtered = filter_stratagems(stratagems, "can")
    assert len(filtered) == 1
    assert 1 in filtered
    
    filtered = filter_stratagems(stratagems, "")
    assert len(filtered) == len(stratagems)

def test_sort_stratagems(stratagems):
    sorted_stratagems = sort_stratagems(stratagems)
    sorted_ids = list(sorted_stratagems.keys())

    # Expected order by category and then name
    expected_order = [3, 4, 2, 1, 6, 5]  # Defensive -> Offensive -> Offensive and Attack -> Counter Attack

    assert sorted_ids == expected_order

def test_stratagem_placeholder_icon(stratagems):
    assert stratagems.get(1).icon_name == "Placeholder.svg"
    assert stratagems.get(2).icon_name == "icon_name"

def test_filter_stratagems_special_characters(stratagems):
    filtered = filter_stratagems(stratagems, "wasp")
    assert len(filtered) == 1
    assert 5 in filtered

    filtered = filter_stratagems(stratagems, "gl-")
    assert len(filtered) == 1
    assert 6 in filtered
    assert 3 not in filtered
