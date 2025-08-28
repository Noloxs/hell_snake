
import os

class ResourceManager:
    _base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    @staticmethod
    def get_resource_path(*args):
        return os.path.join(ResourceManager._base_path, 'src', 'res', *args)

    @staticmethod
    def get_icon_path(icon_name):
        return ResourceManager.get_resource_path('icons', icon_name)

    @staticmethod
    def get_stratagem_icon_path(icon_name):
        return ResourceManager.get_resource_path('icons', 'stratagems', icon_name)

    @staticmethod
    def get_font_path(font_name):
        return ResourceManager.get_resource_path('fonts', font_name)

    @staticmethod
    def get_data_path(data_file_name):
        return ResourceManager.get_resource_path(data_file_name)
