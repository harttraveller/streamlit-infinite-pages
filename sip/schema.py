import os
import streamlit as st
from streamlit.commands.page_config import Layout
from streamlit.delta_generator import DeltaGenerator
from typing import Any, Optional, Callable
from pydantic.dataclasses import dataclass
from sip.config.app import AppConfig
from sip.defaults import (
    default_not_developed,
    default_not_accessible,
    default_visibility_check,
)
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
    name: Optional[str] = None
    main: Callable[..., None] = default_not_developed
    main_kwargs: list[str] = list()
    show: Callable[..., bool] = default_visibility_check
    show_kwargs: list[str] = list()
    blocked: Callable[..., None] = default_not_accessible
    blocked_kwargs: list[str] = list()

    @staticmethod
    def __collect_session_state_vars(session_state_keys: list[str]) -> dict[str, Any]:
        return {key: st.session_state[key] for key in session_state_keys}

    def __call__(self) -> Any:
        if self.name is not None:
            st.markdown(f"# {self.name}")
        if self.show is None:
            self.main(**Page.__collect_session_state_vars(self.main_kwargs))
        else:
            if self.show(**Page.__collect_session_state_vars(self.show_kwargs)):
                self.main(**Page.__collect_session_state_vars(self.main_kwargs))
            else:
                self.blocked(**Page.__collect_session_state_vars(self.blocked_kwargs))
