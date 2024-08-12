import streamlit as st
from sip.base import App, Page


def test_page():
    st.write("Test Page")


app = App(
    name="Demo App",
    icon="D",
    version="0.0.0",
)

app.add(
    Page(name="test", renderer=test_page),
)

app.run(home="test")
