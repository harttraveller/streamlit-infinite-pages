# Quickstart



```python
from sip import App, Page

app = App(
    dev=AppConfig(...)
    prod=AppConfig(...)
)

app.add(Page(
    ...
))


app.build()

```


```python

runner.start("entry.py", mode="dev")

```