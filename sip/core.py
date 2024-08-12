import sys
import streamlit as st
from typing import Optional, Callable
from dataclasses import dataclass
from streamlit.commands.page_config import Layout, InitialSideBarState


@dataclass
class Page:
    name: str
    renderer: Callable[[], None]
    authorizer: Callable[[], bool] = lambda: True


class App:
    def __init__(
        self,
        app_name: str,
        app_icon: str,
        page_layout: Layout = "wide",
        initial_sidebar_state: InitialSideBarState = "auto",
        initial_session_state: dict = dict(),
        authentication_handler: Callable[[], bool] = lambda: True,
        traceback_handler: Optional[Callable[[Exception], None]] = None,
    ) -> None:
        # app config
        self.app_name = app_name
        self.app_icon = app_icon
        self.page_layout: Layout = page_layout
        self.initial_sidebar_state: InitialSideBarState = initial_sidebar_state
        self.initial_session_state = initial_session_state
        self.traceback_handler = traceback_handler
        self.authentication_handler = authentication_handler

        self.pages: dict[str, Page] = dict()
        self.auth_state_key = "_authenticated_"

        # app initialization
        self.__init_page_config()
        self.__init_traceback_control()
        self.__init_session_state()

    def __init_page_config(self) -> None:
        """
        - This needs to be called first, otherwise it wouldn't be split out.
        - The `layout` and `initial_sidebar_state` are currently constants
        to make UI dev easier, but this may be changed in the future.
        """
        st.set_page_config(
            page_title=self.app_name,
            page_icon=self.app_icon,
            layout=self.page_layout,
            initial_sidebar_state=self.initial_sidebar_state,
        )

    def __init_traceback_control(self) -> None:
        """
        This is a hotfix to control traceback.
        """
        if not (self.traceback_handler is None):
            st_exec = sys.modules["streamlit.runtime.scriptrunner.exec_code"]
            st_exec.handle_uncaught_app_exception = self.traceback_handler  # type: ignore

    def __init_session_state(self) -> None:
        if not (self.auth_state_key in st.session_state):
            st.session_state[self.auth_state_key] = False
        for key, val in self.initial_session_state.items():
            if not (key in st.session_state.keys()):
                st.session_state[key] = val

    def __authenticate(self) -> None:
        if not st.session_state[self.auth_state_key]:
            st.session_state[self.auth_state_key] = self.authentication_handler()
            st.rerun()

    def add(self, page: Page | list[Page]) -> None:
        if isinstance(page, list):
            for p in page:
                self.add(p)
        else:
            if page.authorizer():
                self.pages[page.name] = page

    def run(self, index: str) -> None:
        self.__authenticate()
        with st.sidebar:
            selected_page = st.selectbox(
                label="quicksearch",
                options=list(self.pages.keys()),
                index=None,
                placeholder="Go to page...",
                key="quicksearch",
                label_visibility="collapsed",
            )
        target_page = index
        if selected_page:
            st.query_params["page"] = selected_page
            target_page = selected_page
        else:
            url_page = st.query_params.get("page")
            if url_page:
                target_page = url_page
        if target_page in self.pages.keys():
            self.pages[target_page].renderer()
        else:
            st.error("Page does not exist, or user is unauthorized.")
