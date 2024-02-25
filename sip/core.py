from sip.schema import AppConfig, Page


class App:
    def __init__(self, **modes) -> None:
        for key, val in modes.items():
            if not isinstance(val, AppConfig):
                raise ValueError(f"'{key}' must be instance of 'AppConfig'")
        self.modes = modes

    def add(self, page: Page) -> None: ...

    def build(self) -> None: ...
