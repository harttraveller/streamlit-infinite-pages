import sys
import subprocess
from pathlib import Path
from typing import Optional
from pathlib import Path


def make_app_start_command(
    app: str | Path,
    host: str,
    port: int,
    browser: bool,
    global_development_mode: bool,
    suppress_deprecation_warnings: bool,
    enable_rich: bool,
    show_error_details: bool,
    tool_bar_mode: str,
    run_on_save: bool,
    allow_run_on_save: bool,
    enable_cors: bool = True,
    enable_xsrf_protection: bool = True,
    ui_hide_top_bar: bool = True,
    theme_base: str = "dark",
    theme_primary_color: str = "#4b77ff",
    theme_background_color: str = "black",
    theme_secondary_background_color: str = "#191e29",
) -> list[str]:
    # todo: adjust options for dev/prod mode
    return [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        app,
        f"--global.developmentMode={str(global_development_mode)}",
        f"--global.suppressDeprecationWarnings={str(suppress_deprecation_warnings)}",
        f"--logger.enableRich={str(enable_rich)}",
        f"--client.showErrorDetails={str(show_error_details)}",
        f"--client.toolbarMode={str(tool_bar_mode)}",
        "--runner.magicEnabled=False",
        f"--server.headless={str(not browser)}",
        f"--server.runOnSave={str(run_on_save)}",
        f"--server.allowRunOnSave={str(allow_run_on_save)}",
        f"--server.enableCORS={str(enable_cors)}",
        f"--server.enableXsrfProtection={str(enable_xsrf_protection)}",
        "--browser.gatherUsageStats=False",
        f"--theme.base={str(theme_base)}",
        f"--theme.primaryColor={str(theme_primary_color)}",
        f"--ui.hideTopBar={str(ui_hide_top_bar)}",
        f"--server.address={host}",
        f"--server.port={str(port)}",
        f"--theme.backgroundColor={str(theme_background_color)}",
        f"--theme.secondaryBackgroundColor={str(theme_secondary_background_color)}",
    ]


def start(entry_script: str | Path, mode: Optional[str]) -> None: ...
