"""
Source: https://docs.streamlit.io/library/advanced-features/configuration

This file contains pydantic class for streamlit config file, which can be
modified and easily saved to the ~/.streamlit/config.toml location.

The default pydantic values are the default values from the docs, however
the 'create' function at the bottom only includes parameters I find useful,
along with defaults I prefer.

Comments are included inline describing the parameters, because some of them
are somewhat confusing. For instance, when 'showErrorDetails' is False,
that doesn't actually hide the error details for whatever reason, it just
reduces the amount of information available in the traceback - hence, why
a separate higher level configuration parameter has been added to manually
hide the traceback.

"""

import toml
from pathlib import Path
from pydantic import BaseModel, field_validator


# global config is ignored as 'global' is python keyword, so adding
# as attribute introduces problems, and alias didn't seem to work
class GlobalConfig(BaseModel):
    disableWidgetStateDuplicationWarning: bool = False
    showWarningOnDirectExecution: bool = True


class LoggerConfig(BaseModel):
    level: str = "info"
    messageFormat: str = "%(asctime)s %(message)s"


class ClientConfig(BaseModel):
    showErrorDetails: bool = True
    toolbarMode: str = "auto"
    showSidebarNavigation: bool = True

    @field_validator("toolbarMode")
    def __validate_toolbarMode(cls, toolbarMode: str) -> str:
        valid_toolbarMode_options: list[str] = {"auto", "developer", "viewer", "minimal"}
        if toolbarMode not in valid_toolbarMode_options:
            raise ValueError(f"'toolbarMode' must be one of {valid_toolbarMode_options}")


class RunnerConfig(BaseModel):
    magicEnabled: bool = True


class ServerConfig(BaseModel): ...


class BrowserConfig(BaseModel): ...


class MapboxConfig(BaseModel): ...


class DeprecationConfig(BaseModel): ...


class ThemeConfig(BaseModel): ...


class StreamlitConfig(BaseModel):
    logger: LoggerConfig
    client: ClientConfig
    runner: RunnerConfig
    server: ServerConfig
    browser: BrowserConfig
    mapbox: MapboxConfig
    deprecation: DeprecationConfig
    theme: ThemeConfig


def create(): ...
