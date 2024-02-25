import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from pathlib import Path
from typing import Any, Optional, Callable
from pydantic.dataclasses import dataclass
from pydantic import field_validator
from sip.constant import path_default_logo, path_default_theme
from sip.utils.defaults import default_unauthorized, default_undeveloped
from sip.utils.commands import make_app_start_command
from sip.utils.patches import skip_streamlit_newsletter_request


@dataclass
class AppConfig:
    app_name: str = "Streamlit Infinite Pages"  # ! unvalidated
    app_icon: str = "📚"  # * validated
    page_layout: str = "wide"  # * validated
    initial_sidebar_state: str = "expanded"  # * validated
    custom_logo: str | Path = path_default_logo  # * validated
    custom_css: Optional[str | Path] = path_default_theme  # * validated
    custom_js: Optional[str | Path] = None  # * validated
    initial_session_state: Optional[dict[str, Any]] = dict()
    authorization_function: Optional[Callable[[Optional[Any]], bool]] = None
    alpha_sort_pages: bool = False
    disable_traceback: bool = False
    custom_error_handler: Optional[Callable] = None

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

    def __post_init__(self) -> None: ...


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
    main: Optional[Callable[[Optional[Any]], None]] = None
    main_args: Optional[list[Any]] = list()
    main_kwargs: Optional[dict[str, Any]] = dict()
    authorizer: Optional[Callable[[Optional[Any]], bool]] = None
    authorizer_args: Optional[list[Any]] = list()
    authorizer_kwargs: Optional[dict[str, Any]] = dict()
    unauthorized: Optional[Callable[[Optional[Any]], None]] = default_unauthorized
    unauthorized_args: Optional[list[Any]] = list()
    unauthorized_kwargs: Optional[dict[str, Any]] = dict()
    undeveloped: Optional[Callable[[Optional[Any]], None]] = default_undeveloped
    undeveloped_args: Optional[list[Any]] = list()
    undeveloped_kwargs: Optional[dict[str, Any]] = dict()

    def __call__(self) -> Any:
        if self.title is not None:
            st.markdown(f"# {self.title}")
        if self.main is None:
            self.undeveloped(*self.undeveloped_args, **self.undeveloped_kwargs)
        else:
            if self.authorizer is None:
                self.main(*self.main_args, **self.main_kwargs)
            else:
                if self.authorizer(*self.authorizer_args, **self.authorizer_kwargs):
                    self.main(*self.main_args, **self.main_kwargs)
                else:
                    self.unauthorized(*self.unauthorized_args, **self.unauthorized_kwargs)
