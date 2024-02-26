import sys
import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
from typing import Any, Callable
from PIL import Image
from PIL.Image import Image as ImageObject
from sip import env


def add_session_state_variables(data: dict[str, Any] | set[str]) -> None:
    if isinstance(data, set):
        for key in data:
            if key not in st.session_state.keys():
                st.session_state[key] = None
    elif isinstance(data, dict):
        for key, val in data.items():
            if key not in st.session_state.keys():
                st.session_state[key] = val
    else:
        raise ValueError("invalid type passed to 'data' parameter")


def load_png(path: str | Path) -> ImageObject:
    return Image.open(path)


def load_css(path: str | Path | None) -> str:
    if path is None:
        return "<style>\n</style>"
    elif env.key_custom_css not in st.session_state.keys():
        with open(path) as file:
            css = file.read()
        file.close()
        st.session_state[env.key_custom_css] = f"<style>\n{css}\n</style>"
    return st.session_state[env.key_custom_css]


def inject_css(css: str) -> None:
    st.markdown(css, unsafe_allow_html=True)


def load_js(path: str | Path | None) -> str:
    if path is None:
        return f"<script>\n</script>"
    elif env.key_custom_js not in st.session_state.keys():
        with open(path) as file:
            js = file.read()
        file.close()
        st.session_state[env.key_custom_js] = f"<script>\n{js}\n</script>"
    return st.session_state[env.key_custom_js]


def inject_js(js: str) -> None:
    components.html(js, height=0, width=0)


def modify_exception_behavior(exception_handler: Callable[[Exception], None]) -> None:
    script_runner = sys.modules["streamlit.runtime.scriptrunner.script_runner"]
    script_runner.handle_uncaught_app_exception = exception_handler  # type:ignore
