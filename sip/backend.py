import sys
import base64
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


def collect_session_state_vars(session_state_keys: list[str]) -> dict[str, Any]:
    "session state variables may change, so this needs to be dynamically generated"
    return {key: st.session_state[key] for key in session_state_keys}


def load_css(path: str | Path | None) -> str:
    if path is None:
        return "<style>\n</style>"
    elif env.state_key_custom_css not in st.session_state.keys():
        with open(path) as file:
            css = file.read()
        file.close()
        st.session_state[env.state_key_custom_css] = f"<style>\n{css}\n</style>"
    return st.session_state[env.state_key_custom_css]


def inject_css(css: str) -> None:
    st.markdown(css, unsafe_allow_html=True)


def load_js(path: str | Path | None) -> str:
    if path is None:
        return f"<script>\n</script>"
    elif env.state_key_custom_js not in st.session_state.keys():
        with open(path) as file:
            js = file.read()
        file.close()
        st.session_state[env.state_key_custom_js] = f"<script>\n{js}\n</script>"
    return st.session_state[env.state_key_custom_js]


def inject_js(js: str) -> None:
    components.html(js, height=0, width=0)


def modify_exception_behavior(exception_handler: Callable[[Exception], None]) -> None:
    script_runner = sys.modules["streamlit.runtime.scriptrunner.script_runner"]
    script_runner.handle_uncaught_app_exception = exception_handler  # type:ignore


def load_png(path: str | Path) -> ImageObject:
    return Image.open(path)


@st.cache_data
def base64_of_bin(path: str | Path) -> str:
    with open(path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def add_logo(
    path: str,
    link: str,
    top: str,
    bottom: str,
    left: str,
    right: str,
    height: str,
    position: str,
    newtab: bool,
    classes: list[str],
) -> None:
    "Add a logo to streamlit sidebar."
    target = "_blank" if newtab else "_self"
    markup = (
        "<a href='%s' target='%s'><img src='data:image/png;base64,%s' style='z-index: 10; position: %s; top: %s; bottom: %s; left: %s; right: %s; height: %s;' class='%s'/></a>"
        % (
            link,
            target,
            base64_of_bin(path),
            position,
            top,
            bottom,
            left,
            right,
            height,
            " ".join([c for c in classes]),
        )
    )
    st.markdown(
        markup,
        unsafe_allow_html=True,
    )


def format_email(email: str) -> str:
    if "@" in email:
        informal_username, domain = email.split("@")
        return f"**:green[{informal_username}:green[@]:green[{domain}]]**"
    else:
        return f"**:red[Not Logged In]**"


def current_page() -> str | None:
    """
    get current page from url query params

    note that this is done otherwise anytime the selectbox is cleared,
    or the page is reloaded, the page will revert to the default
    """
    query_params = {
        key: val[0] for key, val in st.experimental_get_query_params().items()
    }
    if not len(query_params):
        return None
    elif env.key_page_id not in query_params.keys():
        return None
    else:
        return query_params[env.key_page_id]


def set_page(page_id: str) -> None:
    st.experimental_set_query_params(**{env.key_page_id: page_id})


def reset_page() -> None:
    st.experimental_set_query_params(**dict())
