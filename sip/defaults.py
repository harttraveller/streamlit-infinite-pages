import streamlit as st


def default_not_accessible(*args, **kwargs) -> None:
    st.error("This page is not currently accessible.")


def default_not_developed(*args, **kwargs) -> None:
    st.error("This page has not yet been developed.")


def default_exception_handler(e: Exception, *args, **kwargs) -> None:
    st.toast(":red[Internal Server Error]")
