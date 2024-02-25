import os
import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from typing import Any, Optional, Callable
from pydantic.dataclasses import dataclass
from sip.config.app import AppConfig
from sip.constant import run_mode_environment_key


def default_unauthorized(*args, **kwargs) -> None:
    st.error("You are not authorized to access this page.")


def default_undeveloped(*args, **kwargs) -> None:
    st.error("This page has not yet been developed.")


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


class App:

    def __init__(self, **modes) -> None:
        for key, val in modes.items():
            if not isinstance(val, AppConfig):
                raise ValueError(f"'{key}' must be instance of 'AppConfig'")
        self.modes: dict[str, AppConfig] = modes

    def add(self, page: Page) -> None: ...

    def build(self) -> None:
        run_mode: str | None = os.getenv(run_mode_environment_key)
        if run_mode is None:
            raise ValueError(f"'{run_mode_environment_key}' not set")
        if run_mode not in self.modes.keys():
            raise ValueError(f"'{run_mode}' not found in 'modes'")
