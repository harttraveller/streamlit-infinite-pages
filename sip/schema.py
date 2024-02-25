import streamlit as st
from pydantic import BaseModel
from typing import Optional, Any, Callable
from loguru import logger as log
from sip.utility import default_page_callable

class Page(BaseModel):
    title: Optional[str] = None
    main: Optional[Callable] = default_page_callable
    main_args: Optional[list[Any]] = list()
    main_kwargs: Optional[dict[str, Any]] = dict()
    show: Optional[Callable] = None
    show_args: Optional[list[Any]] = list()
    show_kwargs: Optional[dict[str, Any]] = dict()


    # todo: remove page name, make title optional check
    def __call__(self) -> Any:
        if self.title:
            st.markdown(f"# {self.name}")
        if self.show is None:
            log.info(
                f"[{st.session_state['email']}] render page, non-restricted: {self.name}"
            )
            return self.main(*self.main_args, **self.main_kwargs)
        else:
            if self.show():
                log.info(
                    f"[{st.session_state['email']}] render page, restricted: {self.name}"
                )
                return self.main(*self.main_args, **self.main_kwargs)
            else:
                log.error(
                    f"[{st.session_state['email']}] unauthorized user attempted to access page: {self.name}"
                )
                st.error("**Error: You do not have authorization to access this page.**")