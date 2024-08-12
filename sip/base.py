from __future__ import annotations

import sys
import base64
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
from typing import Optional, Callable, Any, Self
from pydantic import BaseModel, model_validator
from dataclasses import dataclass
from . import constant

# ! utility functions


@st.cache_data
def _load_css(path: Path) -> str:
    with open(path) as file:
        css = file.read()
    file.close()
    return f"<style>\n{css}</style>"


@st.cache_data
def _load_js(path: Path) -> str:
    with open(path) as file:
        js = file.read()
    file.close()
    return f"<script>\n{js}</script>"


@st.cache_data
def _load_logo(path: Path) -> str:
    """Load logo as base64"""
    with open(path, "rb") as file:
        data = file.read()
    return base64.b64encode(data).decode()


# ! page model


class Page(BaseModel):
    name: str
    renderer: Callable[[], None]
    authorizer: Callable[[], bool] = lambda: True

    @property
    def id(self) -> str:
        return self.name

    # @property
    # def id(self) -> str:
    #     return "".join([c.lower() if c.isalnum() else "_" for c in self.name.lower()])


# ! configuration models


class Authentication(BaseModel):
    """
    key (str): The boolean authorization key for the streamlit session state,
    """

    key: str = "authenticated"
    handler: Callable[[], bool] = lambda: True


class Traceback(BaseModel):
    disable: bool = False
    handler: Callable[[Exception], None] = lambda exc: None


class Logo(BaseModel):
    path: Path = constant.path_default_logo
    top: str = "0.3rem"
    bottom: str = "auto"
    left: str = "0.2rem"
    right: str = "auto"
    height: str = "30px"
    position: str = "absolute"
    classes: list[str] = ["logo"]

    @model_validator(mode="after")
    def __exists(self) -> Self:
        if not self.path.exists():
            raise FileNotFoundError(str(self.path))
        return self


class Assets(BaseModel):
    js: Path = constant.path_default_js
    css: Path = constant.path_default_css

    @model_validator(mode="after")
    def __exists(self) -> Self:
        for path in [self.css, self.js]:
            if not path.exists():
                raise FileNotFoundError(str(path))
        return self


class State(BaseModel):
    keys: set[str] = set()
    pairs: dict[str, Any] = dict()


# ! main app class


class App:
    def __init__(
        self,
        name: str,
        icon: str,
        logo: Logo = Logo(),
        version: str = str(),
        state: State = State(),
        traceback: Traceback = Traceback(),
        authentication: Authentication = Authentication(),
    ) -> None:
        # app config
        self.name = name
        self.icon = icon
        self.logo = logo
        self.version = version
        self.state = state
        self.traceback = traceback
        self.authentication = authentication
        # todo: make customizable
        self.assets = Assets()

        # internal state
        self.pages: dict[str, Page] = dict()

        # app initialization
        self.__init_page_config()
        self.__init_traceback_control()
        self.__init_session_state()
        self.__inject_css()
        self.__inject_js()

    # ! these run before app is built
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
        if not self.authentication.key in st.session_state:
            st.session_state[self.authentication.key] = False
        for key in self.state.keys:
            if not (key in st.session_state.keys()):
                st.session_state[key] = None
        for key, val in self.state.pairs.items():
            if not (key in st.session_state.keys()):
                st.session_state[key] = val

    def __inject_css(self) -> None:
        st.markdown(_load_css(self.assets.css), unsafe_allow_html=True)

    def __inject_js(self) -> None:
        components.html(_load_js(self.assets.js), height=0, width=0)

    def __authenticate(self) -> None:
        if not st.session_state[self.authentication.key]:
            st.session_state[self.authentication.key] = self.authentication.handler()
            st.rerun()

    # ! this stage allows the user to add pages

    def add(self, page: Page) -> None:
        if page.authorizer():
            self.pages[page.name] = page

    # ! utilities when actually building app

    def __add_logo(self) -> None:
        markup = (
            "<img src='data:image/png;base64,%s' style='z-index: 10; position: %s; top: %s; bottom: %s; left: %s; right: %s; height: %s;' class='%s'/>"
            % (
                _load_logo(self.logo.path),
                self.logo.position,
                self.logo.top,
                self.logo.bottom,
                self.logo.left,
                self.logo.right,
                self.logo.height,
                " ".join([c for c in self.logo.classes]),
            )
        )
        st.markdown(
            markup,
            unsafe_allow_html=True,
        )

    def __render_page(self, name: str) -> None:
        if self.pages[name].authorizer():
            self.pages[name].renderer()
        else:
            st.error("Unauthorized")

    @property
    def url_page(self) -> str:
        return ""  # todo

    def set_url_page(self, id: str) -> None: ...

    # ! function to build app given config, and successful authorization

    def run(self, home: str) -> None:
        """
        Args:
            home (str): id of home/index page to start on
        """
        # double check authenticated, probably redundant, may remove later
        if not st.session_state[self.authentication.key]:
            self.__authenticate()
        else:
            with st.sidebar:
                # arbitrary values, worked well enough
                logo_col, name_col, collapse_col = st.columns([1.8, 9, 2.5])
                with logo_col:
                    self.__add_logo()
                with name_col:
                    st.markdown(f"# {self.name} :grey[{self.version}]")
                selected_page = st.selectbox(
                    label="quicksearch",
                    options=list(self.pages.keys()),
                    index=None,
                    placeholder="Press Cmd+K to search pages...",
                    key="quicksearch",
                    label_visibility="collapsed",
                )
            target_page = None
            # if not (selected_page is None)
            #     self.set_url_page(selected_page)
            #     target_page = selected_page
            # else:
            #     target_page = self.url_page
            # self.__render_page(target_page)
