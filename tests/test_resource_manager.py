import os
import pytest
from src.utilities.resource_manager import ResourceManager

class TestResourceManager:
    def test_get_resource_path(self):
        path = ResourceManager.get_resource_path("test_file.txt")
        expected_path_part = os.path.join("src", "res", "test_file.txt")
        assert expected_path_part in path
        assert os.path.exists(os.path.dirname(path)) # Check if the base path exists

    def test_get_icon_path(self):
        path = ResourceManager.get_icon_path("test_icon.png")
        expected_path_part = os.path.join("src", "res", "icons", "test_icon.png")
        assert expected_path_part in path

    def test_get_stratagem_icon_path(self):
        path = ResourceManager.get_stratagem_icon_path("test_stratagem.svg")
        expected_path_part = os.path.join("src", "res", "icons", "stratagems", "test_stratagem.svg")
        assert expected_path_part in path

    def test_get_font_path(self):
        path = ResourceManager.get_font_path("test_font.ttf")
        expected_path_part = os.path.join("src", "res", "fonts", "test_font.ttf")
        assert expected_path_part in path

    def test_get_data_path(self):
        path = ResourceManager.get_data_path("stratagems.json")
        expected_path_part = os.path.join("src", "res", "stratagems.json")
        assert expected_path_part in path

    def test_absolute_path_resolution(self):
        # This test ensures that the paths are absolute and correctly resolved
        path = ResourceManager.get_resource_path("some_file.txt")
        assert os.path.isabs(path)
        # Verify that the path starts with the project root
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        assert path.startswith(project_root)
