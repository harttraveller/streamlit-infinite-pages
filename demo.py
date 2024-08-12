import streamlit as st
from sip import App, Page
from loguru import logger


def home_page() -> None:
    st.markdown("# Home")


# * should return true if authenticated, else false
# * you can store use information in the session state
def authentication_handler() -> None:
    super_secret_password = "qwerty"
    password_input = st.text_input(label="Enter password:", type="password")
    if password_input:
        if password_input == super_secret_password:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.toast("Incorrect password")
            st.session_state["authenticated"] = False


app = App(
    name="Demo App",
    icon="🚀",
    authentication_handler=authentication_handler,
)

app.add(Page(name="Home", renderer=home_page))

app.run(index="Home")
