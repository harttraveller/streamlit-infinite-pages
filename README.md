# streamlit-infinite-pages

Streamlit wrapper to make creating multi page apps easier.

## Install

```sh
pip install streamlit-infinite-pages
```

## Features

- [x] Simpler multi-page apps
- [x] Control traceback
    - Fix security issue with base streamlit that leaks code/traceback into app
- [x] Customizable authentication flow
- [x] Per page authorization/access control
- [ ] Add simple branding/metadata integration
- [ ] Keyboard shortcuts
- [ ] Custom CSS / JS
- [ ] Add various stateful elements


## Tutorial

### One simple app

```python
import streamlit as st
from sip import App, Page

def home_page() -> None:
    st.markdown("# Home")


app = App(
    name="Demo App",
    icon="🚀",
)

app.add(Page(name="Home", main=home_page))

# `index` is the default page
app.run(index="Home")
```

### Multi page app

```python
import streamlit as st
from sip import App, Page

def home_page() -> None:
    st.markdown("# Home")

def other_page() -> None:
    st.markdown("# Other page")

app = App(
    name="Demo App",
    icon="🚀",
)

app.add(Page(name="Home", main=home_page))

app.add(Page(name="Other", main=other_page))

# alternatively, you can add pages as a list
# app.add(
#     [
#         Page(name="Home", main=home_page),
#         Page(name="Other", main=other_page),
#     ],
# )

app.run(index="Home")
```

### Control output traceback

This app will show the default traceback.

```python
import streamlit as st
from sip import App, Page

def zero_division_error() -> None:
    st.write(1 / 0)

app = App(
    name="Demo App",
    icon="🚀",
)

app.add(Page(name="Error", main=zero_division_error))

app.run(index="Error")
```

And this one will hide it. You can substitute whatever handler logic you want in here.

```python
import streamlit as st
from sip import App, Page

def zero_division_error() -> None:
    st.write(1 / 0)

def hidden_traceback(e: Exception) -> None:
    st.toast(":red[Error]")

app = App(
    name="Demo App",
    icon="🚀",
    traceback_handler=hidden_traceback,
)

app.add(Page(name="Error", main=zero_division_error))

app.run(index="Error")
```



### Add authentication flow

You can replace the authentication handler with whatever function you want, integrating cognito, auth0, keycloak, etc. You'll can store the token and user in the session state if need be.

```python
import streamlit as st
from sip import App, Page

def home_page() -> None:
    st.markdown("# Home")

# should return true if authentication succeeded, false if failed
# otherwise if no input submitted none
def authentication_handler() -> bool | None:
    super_secret_password = "qwerty"
    password_input = st.text_input(label="Enter password:", type="password")
    if password_input:
        return password_input == super_secret_password
    else:
        return None

app = App(
    name="Demo App",
    icon="🚀",
    auth_handler=authentication_handler,
)

app.add(Page(name="Home", main=home_page))

app.run(index="Home")
```

### Per page authorization

Of course, the actual authentication should be more secure. You could probably replace the `admin_only_check` function with user groups after a JWT is validated or something.

```python
import streamlit as st
from sip import App, Page

users = {
    "alice": {
        "password": "ilikebob",
        "access": "basic",
    },
    "bob": {
        "password": "bobrocks",
        "access": "admin",
    },
}

def home_page() -> None:
    st.markdown("# Home")

def admin_only_page() -> None:
    st.markdown("This page is only accessible to admins.")

def admin_only_check() -> bool:
    return st.session_state["access"] == "admin"

# should return true if authentication succeeded, false if failed
# otherwise if no input submitted none
def authentication_handler() -> bool | None:
    username_input = st.text_input(label="Enter username:")
    password_input = st.text_input(label="Enter password:", type="password")
    if username_input and password_input:
        if not (username_input in users.keys()):
            return False
        else:
            if password_input == users[username_input]["password"]:
                st.session_state["user"] = username_input
                st.session_state["access"] = users[username_input]["access"]
                return True
            else:
                return False
    else:
        return None


app = App(
    name="Demo App",
    icon="🚀",
    auth_handler=authentication_handler,
    initial_session_state={"access": None},
)

app.add(
    Page(name="Home", main=home_page),
)

app.add(
    Page(
        name="only for admins",
        main=admin_only_page,
        accessible=admin_only_check,
    )
)

app.run(index="Home")
```

