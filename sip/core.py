import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from pathlib import Path
from pydantic.dataclasses import dataclass
from typing import Optional, Any, Callable
from loguru import logger as log
from sip import constant
from sip.config import AppConfig, PageConfig


@dataclass
class App:
    config: AppConfig

    def __post_init__(self) -> None: ...

    def add(self, page: PageConfig) -> None: ...
