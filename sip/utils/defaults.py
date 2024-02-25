import streamlit as st


def default_unauthorized():
    st.error("You are not authorized to access this page.")


def default_undeveloped():
    st.error("This page has not yet been developed.")
