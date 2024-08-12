import streamlit as st
from sip import App, Page


def zero_division_error() -> None:
    st.write(1 / 0)


def hidden_traceback(e: Exception) -> None:
    st.toast(":red[Error]")


app = App(
    name="Demo App",
    icon="🚀",
    traceback_handler=hidden_traceback,
)

app.add(Page(name="Error", main=zero_division_error))


app.run(index="Error")
