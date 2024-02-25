import os
import sys
import subprocess
from pathlib import Path
from typing import Optional
from sip.utils.st_config import skip_streamlit_newsletter_request
from sip.constant import run_mode_environment_key


def start(
    entry_script: str | Path,
    open_browser: bool = False,
    run_mode: Optional[str] = None,
    host_address: Optional[str] = None,
    host_port: Optional[int] = None,
) -> None:
    skip_streamlit_newsletter_request()
    entry_absolute = Path(entry_script).absolute()
    if not entry_absolute.exists():
        raise FileNotFoundError(str(entry_absolute))
    if run_mode is not None:
        os.environ[run_mode_environment_key] = run_mode
    command: list[str] = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(entry_absolute),
        f"--server.headless={str(not open_browser)}",
    ]
    if host_address is not None:
        command.append(
            f"--server.address={host_address}",
        )
    if host_port is not None:
        command.append(
            f"--server.port={str(host_port)}",
        )
    subprocess.run(command)
