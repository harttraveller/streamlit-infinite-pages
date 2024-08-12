import sys
import streamlit as st
from typing import Optional, Callable
from dataclasses import dataclass
from streamlit.commands.page_config import Layout, InitialSideBarState


@dataclass
class Page:
    name: str
    main: Callable[[], None]
    accessible: Callable[[], bool] = lambda: True


class App:
    def __init__(
        self,
        name: str,
        icon: str,
        page_layout: Layout = "wide",
        initial_sidebar_state: InitialSideBarState = "auto",
        initial_session_state: dict = dict(),
        auth_handler: Callable[[], bool | None] = lambda: True,
        auth_key: str = "authenticated",
        traceback_handler: Optional[Callable[[Exception], None]] = None,
    ) -> None:
        # app config
        self.app_name = name
        self.app_icon = icon
        self.page_layout: Layout = page_layout
        self.initial_sidebar_state: InitialSideBarState = initial_sidebar_state
        self.initial_session_state = initial_session_state
        self.traceback_handler = traceback_handler
        self.auth_handler = auth_handler
        self.auth_key = auth_key

        self.pages: dict[str, Page] = dict()

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
        if not (self.auth_key in st.session_state):
            st.session_state[self.auth_key] = False
        for key, val in self.initial_session_state.items():
            if not (key in st.session_state.keys()):
                st.session_state[key] = val

    def add(self, page: Page | list[Page]) -> None:
        if isinstance(page, list):
            for p in page:
                self.add(p)
        else:
            self.pages[page.name] = page

    def __authenticate(self) -> None:
        auth_result = self.auth_handler()
        if not (auth_result is None):
            st.session_state[self.auth_key] = auth_result
            if st.session_state[self.auth_key]:
                st.rerun()
            else:
                st.toast(":red[Authentication Failed]")

    def run(self, index: str) -> None:
        if not st.session_state[self.auth_key]:
            self.__authenticate()
        else:
            accessible_pages = [
                page.name for page in self.pages.values() if page.accessible()
            ]
            with st.sidebar:
                selected_page = st.selectbox(
                    label="quicksearch",
                    options=accessible_pages,
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
                if self.pages[target_page].accessible():
                    self.pages[target_page].main()
                else:
                    st.error("Page does not exist, or user is unauthorized.")
            else:
                st.error("Page does not exist, or user is unauthorized.")
