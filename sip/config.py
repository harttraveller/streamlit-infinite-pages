import streamlit as st
from pathlib import Path
from typing import Any, Optional, Callable
from pydantic.dataclasses import dataclass
from pydantic import field_validator
from sip.defaults import default_unauthorized, default_undeveloped
from sip.constant import path_default_logo, path_default_theme


@dataclass
class PageConfig:
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


@dataclass
class AppConfig:
    app_name: str = "Streamlit Infinite Pages"  # ! unvalidated
    app_icon: str = "📚"  # * validated
    page_layout: str = "wide"  # * validated
    initial_sidebar_state: str = "expanded"  # * validated
    custom_logo: str | Path = path_default_logo
    custom_css: Optional[str | Path] = path_default_theme
    custom_js: Optional[str | Path] = None
    initial_session_state: Optional[dict[str, Any]] = dict()
    authorization_function: Optional[Callable[[Optional[Any]], bool]] = None
    alpha_sort_pages: bool = False
    disable_traceback: bool = False

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

    def __post_init__(self) -> None: ...
