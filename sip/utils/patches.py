import toml
from pathlib import Path


def skip_streamlit_newsletter_request() -> None:
    """
    Normally when you start a streamlit app for the first time, it will prompt
    you for their email, to subscribe to their newsletter. This function checks
    if the Streamlit credentials file exists, and if not, creates it and writes
    an empty email field so it doesn't do that.
    """
    streamlit_config_directory: Path = Path.home() / ".streamlit"
    streamlit_credentials_file: Path = streamlit_config_directory / "credentials.toml"
    if not streamlit_credentials_file.exists():
        streamlit_config_directory.mkdir(exist_ok=True)
        with open(streamlit_credentials_file, "w") as file:
            toml.dump({"general": {"email": ""}}, file)
        file.close()
