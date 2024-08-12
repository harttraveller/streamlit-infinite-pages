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
- [x] Per page authorization
- [ ] Add branding
- [ ] Keyboard shortcuts
- [ ] Custom CSS / JS
- [ ] Add various stateful elements


## Tutorial

### Extremely simple app

```python
from sip import App, Page
```





<!--
Streamlit app template with minimal theme, keyboard shortcuts, and support for an arbitrary number of pages.


## Features

### Future

- Stripe Integration
- AWS Cognito Integration
- Sentry Integration
- Custom pages (combinations of other pages)
    - Saving custom page state
        - Could do via cookies, but st cookies components create insecure iframes
        - Instead, create interface_state save functions that user can define -->