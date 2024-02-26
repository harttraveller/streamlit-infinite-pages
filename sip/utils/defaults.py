import streamlit as st


def default_render_blocked(**kwargs) -> None:
    st.error("This page is not currently accessible.")


def default_render_main(**kwargs) -> None:
    st.error("This page has not yet been developed.")


def default_access_check(**kwargs) -> bool:
    return True


def default_exception_handler(e: Exception, *args, **kwargs) -> None:
    st.toast(":red[Internal Server Error]")
