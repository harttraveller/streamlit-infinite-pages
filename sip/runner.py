import sys
import toml
import subprocess
from pathlib import Path
from typing import Any
from pydantic import BaseModel, model_validator, field_validator


def skip() -> None:
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


class Command(BaseModel):
    app: str

    @model_validator(mode="before")
    def __prevalidate(self, data: Any) -> Any: ...

    def build(self) -> list[str]:
        """
        The output streamlit CLI command to start the app with the associated parameters.
        """
        return [
            sys.executable,
            "-m",
            "streamlit",
            "run",
        ]


def start(command: Command) -> None:
    subprocess.run(str(command))
