from pathlib import Path


# Paths

path_assets: Path = Path(__file__).parent / ".assets"
path_default_theme: Path = path_assets / "default_theme.css"
path_default_logo: Path = path_assets / "default_logo.png"

# Variables

default_unauthorized_message: str = "You are not authorized to access this page."