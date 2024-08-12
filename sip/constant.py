from pathlib import Path
from streamlit.commands.page_config import Layout, InitialSideBarState

app_layout: Layout = "wide"
app_initial_sidebar_state: InitialSideBarState = "auto"

path_static = Path(__file__).parent / ".static"
path_default_css = path_static / "default.css"
path_default_js = path_static / "default.js"
path_default_logo = path_static / "default.png"
