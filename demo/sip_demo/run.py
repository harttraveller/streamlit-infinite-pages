from pathlib import Path
from sip import runner

app_script = Path(__file__).parent / "app.py"

runner.start(
    app_script,
    run_mode="prod",
    host_address="localhost",
    host_port=8501,
)
