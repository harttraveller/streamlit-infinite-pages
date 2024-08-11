from importlib import metadata
from .__meta__ import __name__, __package__, __module__, __version__

streamlit_version: str = metadata.version("streamlit")
compatible_streamlit_versions: set[str] = {
    "1.37.1",
}


class IncompatibleStreamlitVersionError(Exception): ...


if streamlit_version not in compatible_streamlit_versions:
    raise IncompatibleStreamlitVersionError(
        (
            "Due to some patches introduced to control traceback, "
            "it is uncertain whether streamlit versions outside of the "
            f"supported versions will work. Your version is {streamlit_version}.\n"
            f"Please change to one of the following versions: {compatible_streamlit_versions}"
        )
    )
