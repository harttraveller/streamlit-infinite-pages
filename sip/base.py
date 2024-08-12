from __future__ import annotations

import sys
import streamlit as st
from pathlib import Path
from typing import Optional, Callable, Any
from pydantic import BaseModel
from dataclasses import dataclass
from . import constant


class Authentication(BaseModel):
    """
    key (str): The boolean authorization key for the streamlit session state,
    """

    key: str = "authenticated"
    handler: Callable[[], bool] = lambda: True


class Traceback(BaseModel):
    disable: bool = False
    handler: Callable[[Exception], None] = lambda exc: None


class Assets(BaseModel):
    logo: Path = constant.path_default_logo
    css: Path = constant.path_default_css
    js: Path = constant.path_default_js


class Page:
    id: str
    name: str
    main: Callable
    show: Callable


class App:
    def __init__(
        self,
        name: str,
        icon: str,
        version: str = str(),
        state: dict[str, Any] = dict(),
        assets: Assets = Assets(),
        traceback: Traceback = Traceback(),
        authentication: Authentication = Authentication(),
    ) -> None:
        # app config
        self.name = name
        self.icon = icon
        self.version = version
        self.state = state
        self.assets = assets
        self.traceback = traceback
        self.authentication = authentication

        # internal state
        self.pages: dict[str, Page] = dict()

        # app initialization
        self.__init_page_config()
        self.__init_traceback_control()
        self.__init_session_state()
        self.__init_custom_css()
        self.__init_custom_js()

    def __init_page_config(self) -> None:
        """
        - This needs to be called first, otherwise it wouldn't be split out.
        - The `layout` and `initial_sidebar_state` are currently constants
        to make UI dev easier, but this may be changed in the future.
        """
        st.set_page_config(
            page_title=self.name,
            page_icon=self.icon,
            layout=constant.app_layout,
            initial_sidebar_state=constant.app_initial_sidebar_state,
        )

    def __init_traceback_control(self) -> None:
        """
        This is a hotfix to control traceback.
        """
        st_exec_code_module = sys.modules["streamlit.runtime.scriptrunner.exec_code"]
        st_error_util_module = sys.modules["streamlit.error_util"]
        base_exception_handler = st_error_util_module.handle_uncaught_app_exception
        if self.traceback.disable:

            def custom_exception_handler_base_disabled(exception: Exception) -> None:
                self.traceback.handler(exception)

            st_exec_code_module.handle_uncaught_app_exception = custom_exception_handler_base_disabled  # type: ignore

        else:

            def custom_exception_handler_base_enabled(exception: Exception) -> None:
                self.traceback.handler(exception)
                base_exception_handler(exception)

            st_exec_code_module.handle_uncaught_app_exception = custom_exception_handler_base_enabled  # type: ignore

    def __init_session_state(self) -> None:
        """"""
        ...

    def __init_custom_css(self) -> None: ...

    def __init_custom_js(self) -> None: ...

    def add(self, page: Page) -> None:
        self.pages[page.id] = page

    def __check_auth(self) -> None:
        if not (self.authentication.key in st.session_state.keys()):
            st.session_state[self.authentication.key] = self.authentication.handler()
            st.rerun()
        elif not st.session_state[self.authentication.key]:
            st.session_state[self.authentication.key] = self.authentication.handler()
            st.rerun()

    def __render_app(self) -> None: ...

    def start(self) -> None:
        self.__check_auth()
        self.__render_app()
