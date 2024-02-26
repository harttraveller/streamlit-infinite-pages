import streamlit as st
from typing import Any


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
