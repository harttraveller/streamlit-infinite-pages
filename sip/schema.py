import streamlit as st
from pydantic import BaseModel
from typing import Optional, Any, Callable
from loguru import logger as log
from sip.utility import undefined_page_callable

class Page(BaseModel):
    # todo: finish docstring
    """
    _summary_

    Args:
        id (str): The unique page identifier.
        title (Optional[str]): The page title to display as Heading 1 on page. Defaults to None.
        main (Optional[Callable]): _description_. Defaults to 'undefined_page_callable'.
        main_args (Optional[list[Any]]): _description_. Defaults to empty list.
        main_kwargs (Optional[dict[str, Any]]): _description_. Defaults to empty dictionary.
        show (Optional[Callable]): _description_. Defaults to None.
        show_args (Optional[list[Any]]): _description_. Defaults to empty list.
        show_kwargs (Optional[dict[str, Any]]): _description_. Defaults to empty dictionary.
    """
    id: str
    title: Optional[str] = None
    main: Optional[Callable] = undefined_page_callable
    main_args: Optional[list[Any]] = list()
    main_kwargs: Optional[dict[str, Any]] = dict()
    show: Optional[Callable] = None
    show_args: Optional[list[Any]] = list()
    show_kwargs: Optional[dict[str, Any]] = dict()


    def __call__(self) -> Any:
        if self.title is not None:
            st.markdown(f"# {self.title}")
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