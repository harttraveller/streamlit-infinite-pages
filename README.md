# streamlit-infinite-pages

Streamlit app template with minimal theme, keyboard shortcuts, and support for an arbitrary number of pages.


## Features

### Future

- Stripe Integration
- AWS Cognito Integration
- Sentry Integration
- Custom pages (combinations of other pages)
    - Saving custom page state
        - Could do via cookies, but st cookies components create insecure iframes
        - Instead, create interface_state save functions that user can define