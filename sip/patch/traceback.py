import sys
from typing import Callable


st_exec_code_module = sys.modules["streamlit.runtime.scriptrunner.exec_code"]
st_error_util_module = sys.modules["streamlit.error_util"]
base_exception_handler = st_error_util_module.handle_uncaught_app_exception


def null_handler(e: Exception) -> None:
    return None


def configure(
    disable: bool,
    handler: Callable[[Exception], None] = null_handler,
) -> None:
    if disable:

        def custom_exception_handler_base_disabled(exception: Exception) -> None:
            handler(exception)

        st_exec_code_module.handle_uncaught_app_exception = custom_exception_handler_base_disabled  # type: ignore

    else:

        def custom_exception_handler_base_enabled(exception: Exception) -> None:
            handler(exception)
            base_exception_handler(exception)

        st_exec_code_module.handle_uncaught_app_exception = custom_exception_handler_base_enabled  # type: ignore
