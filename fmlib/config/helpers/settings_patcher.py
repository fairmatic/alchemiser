from unittest.mock import patch


class SettingsPatcher:
    """
    A context manager that patches the dynaconf lazy settings dictionary with the given key values
    NOTE: We are having to double patch instead of using with mock.patch because when the test is complete the
    mock.patch contextmanager tries to unpatch and call dict.clear, but dynaconf lazy settings dictionary object does
    not have a implementation for `clear` function hence it fails.
    """

    def __init__(self, settings, **kwargs):
        self.settings = settings
        self.patch_dict = kwargs
        self.old_patch_dict = {}

    def __enter__(self):
        self.patcher = patch.dict(self.settings, self.patch_dict)
        self.patcher.start()

    def get_old_values(self):
        for key in self.patch_dict:
            self.old_patch_dict[key] = self.settings[key]

    def __exit__(self, *args):
        self.patcher = patch.dict(self.settings, self.old_patch_dict)
        self.patcher.start()
