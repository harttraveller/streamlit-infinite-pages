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
        self.cfg: AppConfig = modes[run_mode]

    def add(self, page: Page) -> None: ...

    def __set_page_config(self) -> None:
        st.set_page_config(
            page_title=self.cfg.app_name,
            page_icon=self.cfg.app_icon,
            layout=self.cfg.page_layout,
            initial_sidebar_state=self.cfg.initial_sidebar_state,
        )

    def __initialize_session_state(self) -> None:
        "initialize streamlit session state keys"
        backend.add_session_state_variables(data=env.required_session_state_keys)
        backend.add_session_state_variables(data=self.cfg.initial_session_state)

    def __apply_custom_css(self) -> None:
        css: str = backend.load_css(self.cfg.custom_css_path)
        backend.inject_css(css)

    def __apply_custom_js(self) -> None:
        js: str = backend.load_js(self.cfg.custom_js_path)
        backend.inject_js(js)

    def build(self) -> None:
        self.__set_page_config()
        self.__initialize_session_state()
