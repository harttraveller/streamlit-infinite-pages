"""
Source: https://docs.streamlit.io/library/advanced-features/configuration

You can run `streamlit config show` in an environment with streamlit
installed to see the source of the docstrings.

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
from typing import Optional
from pydantic import BaseModel, field_validator


# ! ignored as 'global' is python keyword; adding attribute causes issues
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
    fastReruns: bool = True
    enforceSerializableSessionState: bool = False
    enumCoercion: str = "nameOnly"

    def __validate_enumCoercion(cls, enumCoercion: str) -> str:
        valid_enumCoercion_options: list[str] = {"nameOnly", "off", "nameAndValue"}
        if enumCoercion not in valid_enumCoercion_options:
            raise ValueError(
                f"'enumCoercion' must be one of {valid_enumCoercion_options}"
            )


class ServerConfig(BaseModel):
    folderWatchBlacklist: list = list()
    fileWatcherType: str = "auto"
    # cookieSecret # ! ignored as it is randomly generated
    headless: bool = False
    runOnSave: bool = True
    # address # ! ignored as I don't entirely understand it yet
    port: int = 8501
    baseUrlPath: str = ""
    enableCORS: bool = True
    enableXsrfProtection: bool = True
    maxUploadSize: int = 200
    maxMessageSize: int = 200
    enableWebsocketCompression: bool = False
    enableStaticServing: bool = False
    # sslCertfile # ! ignored for security reasons, see docstring
    # sslKeyFile # ! ignored for security reasons, see docstring

    def __validate_fileWatcherType(cls, fileWatcherType: str) -> str:
        valid_fileWatcherType_options: list[str] = {"auto", "watchdog", "poll", "none"}
        if fileWatcherType not in valid_fileWatcherType_options:
            raise ValueError(
                f"'fileWatcherType' must be one of {valid_fileWatcherType_options}"
            )


class BrowserConfig(BaseModel):
    serverAddress: str = "localhost"
    gatherUsageStates: bool = True
    serverPort: int = 8501


class MapboxConfig(BaseModel):
    token: str = ""


class DeprecationConfig(BaseModel):
    showPyplotGlobalUse: bool = True


class ThemeConfig(BaseModel):
    base: Optional[str] = None
    backgroundColor: Optional[str] = None
    secondaryBackgroundColor: Optional[str] = None
    textColor: Optional[str] = None
    font: Optional[str] = None

    def __validate_font(cls, font: str) -> str:
        valid_font_options: list[str] = {"sans serif", "serif", "monospace"}
        if font not in valid_font_options:
            raise ValueError(f"'font' must be one of {valid_font_options}")


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
