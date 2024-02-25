from pathlib import Path
from typing import Any, Optional, Callable
from pydantic.dataclasses import dataclass
from pydantic import field_validator
from streamlit.commands.page_config import Layout, InitialSideBarState
from sip.env import path_default_logo, path_default_theme, required_session_state_keys
from sip.config.streamlit import (
    StreamlitConfig,
    LoggerConfig,
    ClientConfig,
    RunnerConfig,
    ServerConfig,
    BrowserConfig,
    UserInterfaceConfig,
    ThemeConfig,
)

# todo: add keyboard shortcut customization


@dataclass
class AppConfig:
    # main configuration parameters
    app_name: str = "Streamlit Infinite Pages"  # * no validation
    app_icon: str = "📚"
    page_layout: Layout = "wide"
    initial_sidebar_state: InitialSideBarState = "expanded"
    custom_logo: str | Path = path_default_logo
    custom_css: Optional[str | Path] = path_default_theme
    custom_js: Optional[str | Path] = None
    initial_session_state: dict[str, Any] = dict()
    authorization_function: Optional[Callable[[Optional[Any]], bool]] = None
    alpha_sort_pages: bool = False
    disable_error_traceback: bool = False
    custom_error_handler: Optional[Callable] = None
    # .streamlit/config.toml configuration parameters
    st_cfg_logger_level: str = "info"
    st_cfg_logger_enable_rich: bool = True
    st_cfg_client_show_error_details: bool = True
    st_cfg_client_toolbar_mode: str = "minimal"
    st_cfg_runner_magic_enabled: bool = False
    st_cfg_runner_post_script_garbage_collection: bool = False
    st_cfg_runner_fast_reruns: bool = True
    st_cfg_server_run_on_save: bool = True
    st_cfg_server_allow_run_on_save: bool = True
    st_cfg_server_address: str = "localhost"
    st_cfg_server_port: int = 8501
    st_cfg_server_enable_cors: bool = True
    st_cfg_server_enable_xsrf_protection: bool = True
    st_cfg_server_max_upload_size_mb: int = 200
    st_cfg_server_max_message_size_mb: int = 200
    st_cfg_browser_gather_usage_stats: bool = False
    st_cfg_ui_hide_top_bar: bool = True
    st_cfg_theme_base: str = "dark"
    st_cfg_theme_primary_color: str = ""
    st_cfg_theme_background_color: str = ""
    st_cfg_theme_secondary_background_color: str = ""
    st_cfg_theme_text_color: str = ""
    st_cfg_theme_font: str = ""

    def __make_streamlit_config(self) -> StreamlitConfig:
        return StreamlitConfig(
            logger=LoggerConfig(
                level=self.st_cfg_logger_level,
                enableRich=self.st_cfg_logger_enable_rich,
            ),
            client=ClientConfig(
                showErrorDetails=self.st_cfg_client_show_error_details,
                toolbarMode=self.st_cfg_client_toolbar_mode,
            ),
            runner=RunnerConfig(
                magicEnabled=self.st_cfg_runner_magic_enabled,
                postScriptGC=self.st_cfg_runner_post_script_garbage_collection,
                fastReruns=self.st_cfg_runner_fast_reruns,
            ),
            server=ServerConfig(
                runOnSave=self.st_cfg_server_run_on_save,
                allowRunOnSave=self.st_cfg_server_allow_run_on_save,
                address=self.st_cfg_server_address,
                port=self.st_cfg_server_port,
                enableCORS=self.st_cfg_server_enable_cors,
                enableXsrfProtection=self.st_cfg_server_enable_xsrf_protection,
                maxUploadSize=self.st_cfg_server_max_upload_size_mb,
                maxMessageSize=self.st_cfg_server_max_message_size_mb,
            ),
            browser=BrowserConfig(
                gatherUsageStats=self.st_cfg_browser_gather_usage_stats,
            ),
            ui=UserInterfaceConfig(
                hideTopBar=self.st_cfg_ui_hide_top_bar,
            ),
            theme=ThemeConfig(
                base=self.st_cfg_theme_base,
                primaryColor=self.st_cfg_theme_primary_color,
                backgroundColor=self.st_cfg_theme_background_color,
                textColor=self.st_cfg_theme_text_color,
                font=self.st_cfg_theme_font,
            ),
        )

    def __add_required_session_state_keys(self) -> None:
        for key in required_session_state_keys:
            self.initial_session_state[key] = None

    def __post_init__(self) -> None:
        self.streamlit_config = self.__make_streamlit_config()
        self.__add_required_session_state_keys()

    @field_validator("app_icon")
    def __validate_app_icon(cls, app_icon: str) -> str:
        if len(app_icon) > 1:
            raise ValueError("'app_icon' must be one character long")
        return app_icon

    # @field_validator("page_layout")
    # def __validate_page_layout(cls, page_layout: str) -> str:
    #     valid_page_layouts = {"wide", "centered"}
    #     if page_layout not in valid_page_layouts:
    #         raise ValueError(f"'page_layout' must be one of {valid_page_layouts}")
    #     return page_layout

    # @field_validator("initial_sidebar_state")
    # def __validate_initial_sidebar_state(cls, initial_sidebar_state: str) -> str:
    #     valid_initial_sidebar_states = {"expanded", "collapsed", "auto"}
    #     if initial_sidebar_state not in valid_initial_sidebar_states:
    #         raise ValueError(
    #             f"'initial_sidebar_state' must be one of {valid_initial_sidebar_states}"
    #         )
    #     return initial_sidebar_state

    @field_validator("custom_logo")
    def __validate_custom_logo(cls, custom_logo: str | Path) -> Path:
        custom_logo = Path(custom_logo)
        if not custom_logo.exists():
            raise FileNotFoundError(f"'custom_logo' not found at: {str(custom_logo)}")
        if not str(custom_logo).endswith(".png"):
            raise ValueError(f"'custom_logo' must be a .png file")
        return custom_logo

    @field_validator("custom_css")
    def __validate_custom_css(cls, custom_css: str | Path) -> Path:
        custom_css = Path(custom_css)
        if not custom_css.exists():
            raise FileNotFoundError(f"'custom_css' not found at: {str(custom_css)}")
        if not str(custom_css).endswith(".css"):
            raise ValueError(f"'custom_css' must be a .css file")
        return custom_css

    @field_validator("custom_js")
    def __validate_custom_js(cls, custom_js: str | Path) -> Path:
        custom_js = Path(custom_js)
        if not custom_js.exists():
            raise FileNotFoundError(f"'custom_js' not found at: {str(custom_js)}")
        if not str(custom_js).endswith(".js"):
            raise ValueError(f"'custom_js' must be a .js file")
        return custom_js
