import os
from sip.schema import AppConfig, Page
from sip.constant import run_mode_environment_key


class App:

    def __init__(self, **modes) -> None:
        for key, val in modes.items():
            if not isinstance(val, AppConfig):
                raise ValueError(f"'{key}' must be instance of 'AppConfig'")
        self.modes: dict[str, AppConfig] = modes

    def add(self, page: Page) -> None: ...

    def build(self) -> None:
        run_mode: str | None = os.getenv(run_mode_environment_key)
        if run_mode is None:
            raise ValueError(f"'{run_mode_environment_key}' not set")
        if run_mode not in self.modes.keys():
            raise ValueError(f"'{run_mode}' not found in 'modes'")
