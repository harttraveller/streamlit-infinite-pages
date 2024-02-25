from pathlib import Path


# Paths

path_home: Path = Path.home()
path_streamlit: Path = path_home / ".streamlit"
path_streamlit_config: Path = path_streamlit / "config.toml"
path_assets: Path = Path(__file__).parent / ".assets"
path_default_theme: Path = path_assets / "default_theme.css"
path_default_logo: Path = path_assets / "default_logo.png"
