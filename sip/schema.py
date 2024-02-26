import os
import streamlit as st
from streamlit.commands.page_config import Layout
from streamlit.delta_generator import DeltaGenerator
from typing import Any, Optional, Callable
from pydantic import BaseModel
from sip.config.app import AppConfig
from sip.utils.defaults import (
    default_render_main,
    default_render_blocked,
    default_access_check,
)
from sip import env, backend


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
    name: str
    render_main: Callable[..., None] = default_render_main
    render_main_keys: list[str] = list()
    access_check: Callable[..., bool] = default_access_check
    access_check_keys: list[str] = list()
    render_blocked: Callable[..., None] = default_render_blocked
    render_blocked_keys: list[str] = list()

    @property
    def render_main_kwargs(self) -> dict[str, Any]:
        return backend.collect_session_state_vars(self.render_main_keys)

    @property
    def access_check_kwargs(self) -> dict[str, Any]:
        return backend.collect_session_state_vars(self.access_check_keys)

    @property
    def render_blocked_kwargs(self) -> dict[str, Any]:
        return backend.collect_session_state_vars(self.render_blocked_keys)

    @property
    def is_accessible(self) -> bool:
        return self.access_check(**self.access_check_kwargs)

    def __call__(self) -> Any:
        if self.name is not None:
            st.markdown(f"# {self.name}")
        if self.is_accessible:
            self.render_main(**self.render_main_kwargs)
        else:
            self.render_blocked(**self.render_blocked_kwargs)
