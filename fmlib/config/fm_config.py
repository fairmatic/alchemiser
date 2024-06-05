from dynaconf import Dynaconf

class FMConfig:
    def __init__(self, config_file):
        self.settings = Dynaconf(
            settings_files=[config_file],
            environments=True,
            envvar_prefix="FM",
            env_switcher="FM_ENV"
        )

    def get(self):
        return self.settings