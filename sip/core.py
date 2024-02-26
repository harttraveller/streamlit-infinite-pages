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
        self.pages[page.name] = page
        if page.is_accessible:
            self.indexed_pages.append(page.name)

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

    def __render_app(self) -> None:
        with st.sidebar:
            st.markdown("#")
            # arbitrary values, worked well enough
            logo_col, name_col, collapse_col = st.columns([1.8, 9, 2.5])
            with logo_col:
                backend.add_logo(
                    str(self.config.custom_logo_path),
                    link=self.config.custom_logo_link,
                    newtab=self.config.custom_logo_newtab,
                    top=self.config.custom_logo_css_params.top,
                    bottom=self.config.custom_logo_css_params.bottom,
                    left=self.config.custom_logo_css_params.left,
                    right=self.config.custom_logo_css_params.right,
                    height=self.config.custom_logo_css_params.height,
                    position=self.config.custom_logo_css_params.position,
                    classes=self.config.custom_logo_css_params.classes,
                )
            with name_col:
                st.markdown(
                    (
                        f"# {self.config.app_name} "
                        f":grey[{self.config.app_version if self.config.app_version is not None else ''}]"
                    )
                )
                if self.config.authentication_check is None:
                    auth_info_text = ":blue[Authorization Unnecessary]"
                else:
                    auth_info_text = backend.format_email(
                        st.session_state[env.state_key_user_email]
                    )
                st.markdown(auth_info_text)
            if self.config.alpha_sort_pages:
                self.indexed_pages = sorted(self.indexed_pages)
            selected_page = st.selectbox(
                label="quicksearch",
                options=self.indexed_pages,
                index=None,
                placeholder="Press Cmd+K to search pages...",
                key="quicksearch",
                label_visibility="collapsed",
            )
        page_name = None
        if selected_page is not None:
            backend.set_page(selected_page)
            page_name = backend.current_page()
        if page_name is not None:
            if page_name in self.pages.keys():
                print("Rendering Page")
                self.pages[page_name]()

    def build(self) -> None:
        self.__set_page_config()
        self.__control_exception_traceback()
        self.__initialize_session_state()
        self.__apply_custom_css()
        self.__apply_custom_js()
        # todo: this code sucks, needs to be refactored/rewritten
        if self.config.authentication_check is None:
            self.__render_app()
        else:
            auth_check_state = backend.collect_session_state_vars(
                self.config.authentication_check_keys
            )
            if self.config.authentication_check(**auth_check_state):
                auth_flow_state_info = backend.collect_session_state_vars(
                    self.config.not_authenticated_action_keys
                )
                if self.config.not_authenticated_action is not None:
                    self.config.not_authenticated_action(**auth_flow_state_info)
                else:
                    st.error(
                        "You are not authenticated, but no authentication flow is defined in this app."
                    )
