import streamlit as st
from sip.core import App, AppConfig, Page
from sip_demo.page import home, test, broken


dev_config: AppConfig = AppConfig(disable_traceback=False)
prod_config: AppConfig = AppConfig(disable_traceback=True)

cfg = dev_config.make_streamlit_config()


app = App(dev=dev_config, prod=prod_config)


app.add(
    Page(
        name="Home Page",
        render_main=home.render,
    )
)

app.add(
    Page(
        name="Test Page",
        render_main=test.render,
    )
)

app.add(
    Page(
        name="Broken Page",
        render_main=broken.render,
    )
)

app.build()
