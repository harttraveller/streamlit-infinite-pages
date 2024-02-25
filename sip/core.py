from pydantic.dataclasses import dataclass
from typing import Optional
from sip.schema import AppConfig, Page


@dataclass
class App:
    config: Optional[AppConfig] = None
    modes: Optional[dict[str, AppConfig]] = None

    def __post_init__(self) -> None:
        self.pages = list()

    def add(self, page: Page) -> None: ...

    def build(self) -> None: ...
