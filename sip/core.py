import os
import streamlit as st
from sip.config.app import AppConfig
from sip.schema import Page
from sip import env, backend


class App:

    def __init__(self, **modes) -> None:
        run_mode: str | None = os.getenv(env.run_mode_environment_key)
        if run_mode is None:
            raise ValueError(f"'{env.run_mode_environment_key}' not set")
        if run_mode not in modes.keys():
            raise ValueError(f"'{run_mode}' not found in key word arguments")
        for key, val in modes.items():
            if not isinstance(val, AppConfig):
                raise ValueError(f"'{key}' must be instance of 'AppConfig'")
        self.config: AppConfig = modes[run_mode]
        self.pages: dict[str, Page] = dict()
        self.indexed_pages: list[str] = list()

    def add(self, page: Page) -> None:
        self.pages[page.id] = page
        if page.is_accessible:
            self.indexed_pages.append(page.id)

    def __set_page_config(self) -> None:
        st.set_page_config(
            page_title=self.config.app_name,
            page_icon=self.config.app_icon,
            layout=self.config.page_layout,
            initial_sidebar_state=self.config.initial_sidebar_state,
        )

    def __control_exception_traceback(self) -> None:
        if self.config.disable_traceback:
            backend.modify_exception_behavior(
                exception_handler=self.config.exception_handler
            )

    def __initialize_session_state(self) -> None:
        "initialize streamlit session state keys"
        backend.add_session_state_variables(data=env.required_session_state_keys)
        backend.add_session_state_variables(data=self.config.initial_session_state)

    def __apply_custom_css(self) -> None:
        css: str = backend.load_css(self.config.custom_css_path)
        backend.inject_css(css)

    def __apply_custom_js(self) -> None:
        js: str = backend.load_js(self.config.custom_js_path)
        backend.inject_js(js)

    def build(self) -> None:
        self.__set_page_config()
        self.__control_exception_traceback()
        self.__initialize_session_state()
        self.__apply_custom_css()
        self.__apply_custom_js()
