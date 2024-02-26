from sip.core import App, AppConfig, Page
from .page import home, test, broken


dev_config: AppConfig = AppConfig(disable_traceback=False)
prod_config: AppConfig = AppConfig(disable_traceback=True)

app = App(dev=dev_config, prod=prod_config)

app.add(
    Page(
        id="home",
        name="Home Page",
        render_main=home.render,
    )
)

app.add(
    Page(
        id="test",
        name="Test Page",
        render_main=test.render,
    )
)

app.add(
    Page(
        id="broken",
        name="Broken Page (Zero Division Error)",
        render_blocked=broken.render,
    )
)

app.build()
