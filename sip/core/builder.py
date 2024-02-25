import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from pathlib import Path
from pydantic.dataclasses import dataclass
from typing import Optional, Any, Callable
from loguru import logger as log
from sip import constant
from sip.core.config import AppConfig
from sip.utils.defaults import default_unauthorized, default_undeveloped


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


@dataclass
class App:
    config: AppConfig

    def add(self, page: Page) -> None: ...

    def build(self) -> None: ...
