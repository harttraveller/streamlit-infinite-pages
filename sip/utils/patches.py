import toml
from pathlib import Path
from sip.constant import path_streamlit, path_streamlit_credentials


def skip_streamlit_newsletter_request() -> None:
    """
    Normally when you start a streamlit app for the first time, it will prompt
    you for their email, to subscribe to their newsletter. This function checks
    if the Streamlit credentials file exists, and if not, creates it and writes
    an empty email field so it doesn't do that.
    """
    if not path_streamlit_credentials.exists():
        path_streamlit.mkdir(exist_ok=True)
        with open(path_streamlit_credentials, "w") as file:
            toml.dump({"general": {"email": ""}}, file)
        file.close()
