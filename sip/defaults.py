import streamlit as st


def default_unauthorized(*args, **kwargs) -> None:
    st.error("You are not authorized to access this page.")


def default_undeveloped(*args, **kwargs) -> None:
    st.error("This page has not yet been developed.")


def default_exception_handler(e: Exception, *args, **kwargs) -> None:
    st.toast(":red[Internal Server Error]")
