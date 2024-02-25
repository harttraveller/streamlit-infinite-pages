import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from pathlib import Path
from typing import Any, Optional, Callable
from pydantic.dataclasses import dataclass
from pydantic import field_validator
from sip.constant import path_default_logo, path_default_theme
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


def default_unauthorized(*args, **kwargs) -> None:
    st.error("You are not authorized to access this page.")


def default_undeveloped(*args, **kwargs) -> None:
    st.error("This page has not yet been developed.")


@dataclass
class AppConfig:
    # main configuration parameters
    app_name: str = "Streamlit Infinite Pages"  # * no validation
    app_icon: str = "📚"  # * validated
    page_layout: str = "wide"  # * validated
    initial_sidebar_state: str = "expanded"  # * validated
    custom_logo: str | Path = path_default_logo  # * validated
    custom_css: Optional[str | Path] = path_default_theme  # * validated
    custom_js: Optional[str | Path] = None  # * validated
    initial_session_state: Optional[dict[str, Any]] = dict()
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

    def __post_init__(self) -> None:
        self.streamlit_config = self.__make_streamlit_config()

    @field_validator("app_icon")
    def __validate_app_icon(cls, app_icon: str) -> str:
        if len(app_icon) > 1:
            raise ValueError("'app_icon' must be one character long")
        return app_icon

    @field_validator("page_layout")
    def __validate_page_layout(cls, page_layout: str) -> str:
        valid_page_layouts = {"wide", "centered"}
        if page_layout not in valid_page_layouts:
            raise ValueError(f"'page_layout' must be one of {valid_page_layouts}")
        return page_layout

    @field_validator("initial_sidebar_state")
    def __validate_initial_sidebar_state(cls, initial_sidebar_state: str) -> str:
        valid_initial_sidebar_states = {"expanded", "collapsed", "auto"}
        if initial_sidebar_state not in valid_initial_sidebar_states:
            raise ValueError(
                f"'initial_sidebar_state' must be one of {valid_initial_sidebar_states}"
            )
        return initial_sidebar_state

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


@dataclass
class Page:
    # todo: finish docstring
    """
    _summary_

    Args:
        id (str): The unique page identifier.
        title (Optional[str]): The page title to display as Heading 1 on page. Defaults to None.
        main (Optional[Callable]): _description_. Defaults to 'undefined_page_callable'.
        main_args (Optional[list[Any]]): _description_. Defaults to empty list.
        main_kwargs (Optional[dict[str, Any]]): _description_. Defaults to empty dictionary.
        show (Optional[Callable]): _description_. Defaults to None.
        show_args (Optional[list[Any]]): _description_. Defaults to empty list.
        show_kwargs (Optional[dict[str, Any]]): _description_. Defaults to empty dictionary.
    """
    id: str
    title: Optional[str] = None
    main: Callable[[Optional[Any]], None] = default_undeveloped
    main_args: list[Any] = list()
    main_kwargs: dict[str, Any] = dict()
    authorizer: Optional[Callable[[Optional[Any]], bool]] = None
    authorizer_args: list[Any] = list()
    authorizer_kwargs: dict[str, Any] = dict()
    unauthorized: Callable[[Optional[Any]], None] = default_unauthorized
    unauthorized_args: list[Any] = list()
    unauthorized_kwargs: dict[str, Any] = dict()

    def __call__(self) -> Any:
        if self.title is not None:
            st.markdown(f"# {self.title}")
        if self.authorizer is None:
            self.main(*self.main_args, **self.main_kwargs)
        else:
            if self.authorizer(*self.authorizer_args, **self.authorizer_kwargs):
                self.main(*self.main_args, **self.main_kwargs)
            else:
                self.unauthorized(*self.unauthorized_args, **self.unauthorized_kwargs)
