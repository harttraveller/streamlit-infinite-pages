from importlib import metadata
from .__meta__ import __name__, __package__, __module__, __version__
from .core import App, Page

__streamlit_version: str = metadata.version("streamlit")
__compatible_streamlit_versions: set[str] = {
    "1.37.1",
}

if __streamlit_version not in __compatible_streamlit_versions:

    class IncompatibleStreamlitVersionError(Exception): ...

    raise IncompatibleStreamlitVersionError(
        (
            "Due to some patches introduced to control traceback, "
            "it is uncertain whether streamlit versions outside of the "
            f"supported versions will work. Your version is {__streamlit_version}.\n"
            f"Please change to one of the following versions: {__compatible_streamlit_versions}"
        )
    )
