import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from pathlib import Path
from pydantic import BaseModel, field_validator
from typing import Optional, Any, Callable
from loguru import logger as log
from sip import constant, utility

class Page(BaseModel):
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
    main: Optional[Callable[[Optional[Any]], None]] = utility.undefined_page_callable
    main_args: Optional[list[Any]] = list()
    main_kwargs: Optional[dict[str, Any]] = dict()
    show: Optional[Callable[[Optional[Any]], bool]] = None
    show_args: Optional[list[Any]] = list()
    show_kwargs: Optional[dict[str, Any]] = dict()
    unauthorized_message: str = constant.default_unauthorized_message

    def __call__(self) -> Any:
        if self.title is not None:
            st.markdown(f"# {self.title}")
        if self.show is None:
            self.main(*self.main_args, **self.main_kwargs)
        else:
            if self.show(*self.show_args, **self.show_kwargs):
                self.main(*self.main_args, **self.main_kwargs)
            else:
                st.error(self.unauthorized_message)

class App(BaseModel):
    app_name: str = "Streamlit Infinite Pages"
    app_icon: str = "📚"
    page_layout: str = "wide"
    initial_sidebar_state: str = "expanded"
    custom_logo: str | Path = constant.path_default_logo
    custom_css: Optional[str | Path] = constant.path_default_theme
    custom_js: Optional[str | Path] = None
    initial_session_state: Optional[dict[str, Any]] = dict()
    authorization_function: Optional[Callable[[Optional[Any]], bool]] = None
    alpha_sort_pages: bool = False

