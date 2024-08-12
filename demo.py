import streamlit as st
from sip.core import App, Page, Authentication, TracebackConfiguration


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


trace = TracebackConfiguration(
    disable=True,
    handler=error_page_handler,
)
app = App(
    app_name="Demo App",
    app_icon="D",
    version="0.0.0",
    traceback_handler=trace,
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

# st.write(st.query_params.get("page"))
