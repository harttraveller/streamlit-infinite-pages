import streamlit as st
from sip.core import App, Page


def other_page():
    st.write("Other Page")


def home_page():
    st.write("Home Page")


def error_page():
    st.write(1 / 0)


def error_page_handler(e):
    st.toast(":red[Server Error]")


def hidden_page():
    st.write("This shouldn't be visible.")


app = App(
    app_name="Demo App",
    app_icon="D",
    traceback_handler=error_page_handler,
)

app.add(
    [
        Page(name="Home", renderer=home_page),
        Page(name="Other", renderer=other_page),
        Page(name="Error", renderer=error_page),
        Page(name="Hidden", renderer=hidden_page, authorizer=lambda: False),
    ]
)

app.run(index="Home")
