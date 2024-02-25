from pathlib import Path


# Paths

path_home: Path = Path.home()
path_streamlit: Path = path_home / ".streamlit"
path_streamlit_config: Path = path_streamlit / "config.toml"
path_streamlit_credentials: Path = path_streamlit / "credentials.toml"
path_assets: Path = Path(__file__).parent / ".assets"
path_default_theme: Path = path_assets / "default_theme.css"
path_default_logo: Path = path_assets / "default_logo.png"


# Variables

run_mode_environment_key: str = "SIP_RUN_MODE"
required_session_state_keys: set[str] = {
    "custom_css",
    "custom_js",
}
