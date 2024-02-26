import os
import streamlit as st
from streamlit.commands.page_config import Layout
from streamlit.delta_generator import DeltaGenerator
from typing import Any, Optional, Callable
from pydantic.dataclasses import dataclass
from sip.config.app import AppConfig
from sip.defaults import default_undeveloped, default_unauthorized
from sip import env, backend


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
