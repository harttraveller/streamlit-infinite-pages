import sys
import toml
import subprocess
from pathlib import Path
from typing import Optional, Literal
from pydantic import BaseModel, Field, field_validator


path_home: Path = Path.home()
path_streamlit: Path = path_home / ".streamlit"
path_streamlit_config: Path = path_streamlit / "config.toml"
path_streamlit_credentials: Path = path_streamlit / "credentials.toml"


def skip_newsletter() -> None:
    """
    Normally when you start a streamlit app for the first time, it will prompt
    you for their email, to subscribe to their newsletter. This function checks
    if the Streamlit credentials file exists, and if not, creates it and writes
    an empty email field so it doesn't do that.
    """
    if not path_streamlit_credentials.exists():
        path_streamlit.mkdir(exist_ok=True)
        with open(path_streamlit_credentials, "w") as file:
            toml.dump({"general": {"email": ""}}, file)
        file.close()


def run(
    app: str | Path,
    host: str,
    port: int,
    browser: bool,
    execute: bool = False,
) -> list[str] | None:
    """
    Create a run command for a streamlit app.

    Notes:

    It uses `sys.executable` to ensure
    that the python executable with streamlit and this package installed is the
    one to run the app.

    Example:

    ```python
    import subprocess
    from sip import streamlit

    subprocess.run(streamlit.run(**parameters))
    ```
    """
    command = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
    ]
    if not execute:
        return command
    else:
        skip_newsletter()
        subprocess.run(command)


# * NOTE *
# Full config is not included in this version, as would take time and is of limited use.

"""
Source: https://docs.streamlit.io/library/advanced-features/configuration

You can run `streamlit config show` in an environment with streamlit
installed to see the source of the docstrings.

Additionally, some configuration options are hidden, and the docs can only
be found by running: `streamlit run --help`.

This file contains pydantic class for streamlit config file, which can be
modified and easily saved to the ~/.streamlit/config.toml location.

The default pydantic values are the default values from the docs, however
the 'create' function at the bottom only includes parameters I find useful,
along with defaults I prefer.

Comments are included inline describing the parameters, because some of them
are somewhat confusing. For instance, when 'showErrorDetails' is False,
that doesn't actually hide the error details for whatever reason, it just
reduces the amount of information available in the traceback - hence, why
a separate higher level configuration parameter has been added to manually
hide the traceback.

"""

# class StreamlitConfig(BaseModel):
#     """
#     global_disable_widget_state_duplication_warning (bool): --global.disableWidgetStateDuplicationWarning
#     By default, Streamlit displays a warning when a user sets both a widget default value
#     in the function defining the widget and a widget value via the widget's key in `st.session_state`.


#     """

#     global_disable_widget_state_duplication_warning: bool = Field(
#         default=False, alias="--global.disableWidgetStateDuplicationWarning"
#     )


# # ! ignored as 'global' is python keyword; adding attribute causes issues
# class GlobalConfig(BaseModel):
#     """
#     By default, Streamlit displays a warning when a user sets both a widget
#     default value in the function defining the widget and a widget value via
#     the widget's key in `st.session_state`.

#     If you'd like to turn off this warning, set this to True.

#     Default: false
#     disableWidgetStateDuplicationWarning = false

#     If True, will show a warning when you run a Streamlit-enabled script
#     via "python my_script.py".

#     Default: true
#     showWarningOnDirectExecution = true
#     """

#     # disableWatchDogWarning: bool = False # ! deprecated
#     disableWidgetStateDuplicationWarning: bool = False
#     showWarningOnDirectExecution: bool = True
#     # logLevel: str = "info" # ! hidden option: deprecated
#     unitTest: bool = False  # * hidden option: use `streamlit run --help`
#     suppressDeprecationWarnings: bool = (
#         False  # * hidden option: use `streamlit run --help`
#     )
#     # minCachedMessageSize: float # ! hidden option: ignored as I don't entirely understand yet
#     # maxCachedMessageAge: int # ! hidden option: ignored as I don't entirely understand yet
#     # storeCachedForwardMessagesInMemory: bool # ! hidden option: ignored as I don't entirely understand yet
#     # dataFrameSerialization: str # ! hidden option: deprecated


# class LoggerConfig(BaseModel):
#     """
#     Level of logging: 'error', 'warning', 'info', or 'debug'.

#     Default: 'info'
#     level = "info"

#     String format for logging messages. If logger.datetimeFormat is set,
#     logger messages will default to `%(asctime)s.%(msecs)03d %(message)s`. See
#     [Python's documentation](https://docs.python.org/2.6/library/logging.html#formatter-objects)
#     for available attributes.

#     Default: "%(asctime)s %(message)s"
#     messageFormat = "%(asctime)s %(message)s"
#     """

#     level: str = "info"
#     messageFormat: str = "%(asctime)s %(message)s"
#     enableRich: bool = False  # * hidden option: use `streamlit run --help`

#     @field_validator("level")
#     def __validate_level(cls, level: str) -> str:
#         valid_level_options: set[str] = {"error", "warning", "info", "debug"}
#         if level not in valid_level_options:
#             raise ValueError(f"'level' must be one of {valid_level_options}")
#         return level


# class ClientConfig(BaseModel):
#     """
#     Controls whether uncaught app exceptions and deprecation warnings
#     are displayed in the browser. By default, this is set to True and
#     Streamlit displays app exceptions and associated tracebacks, and
#     deprecation warnings, in the browser.

#     If set to False, deprecation warnings and full exception messages
#     will print to the console only. Exceptions will still display in the
#     browser with a generic error message. For now, the exception type and
#     traceback show in the browser also, but they will be removed in the
#     future.

#     Default: true
#     showErrorDetails = true

#     Change the visibility of items in the toolbar, options menu,
#     and settings dialog (top right of the app).

#     Allowed values:
#     * "auto" : Show the developer options if the app is accessed through
#     localhost or through Streamlit Community Cloud as a developer.
#     Hide them otherwise.
#     * "developer" : Show the developer options.
#     * "viewer" : Hide the developer options.
#     * "minimal" : Show only options set externally (e.g. through
#     Streamlit Community Cloud) or through st.set_page_config.
#     If there are no options left, hide the menu.

#     Default: "auto"
#     toolbarMode = "auto"

#     Controls whether the default sidebar page navigation in a multi-page app is displayed.

#     Default: true
#     showSidebarNavigation = true

#     """

#     # caching: bool # ! hidden option: deprecated
#     # displayEnabled: bool # ! hidden option: deprecated
#     showErrorDetails: bool = True
#     toolbarMode: str = "auto"
#     showSidebarNavigation: bool = True

#     @field_validator("toolbarMode")
#     def __validate_toolbarMode(cls, toolbarMode: str) -> str:
#         valid_toolbarMode_options: set[str] = {"auto", "developer", "viewer", "minimal"}
#         if toolbarMode not in valid_toolbarMode_options:
#             raise ValueError(
#                 f"'toolbarMode' must be one of {valid_toolbarMode_options}"
#             )
#         return toolbarMode


# class RunnerConfig(BaseModel):
#     """
#     Allows you to type a variable or string by itself in a single line of
#     Python code to write it to the app.

#     Default: true
#     magicEnabled = true

#     Handle script rerun requests immediately, rather than waiting for script
#     execution to reach a yield point. This makes Streamlit much more
#     responsive to user interaction, but it can lead to race conditions in
#     apps that mutate session_state data outside of explicit session_state
#     assignment statements.

#     Default: true
#     fastReruns = true

#     Raise an exception after adding unserializable data to Session State.
#     Some execution environments may require serializing all data in Session
#     State, so it may be useful to detect incompatibility during development,
#     or when the execution environment will stop supporting it in the future.

#     Default: false
#     enforceSerializableSessionState = false

#     Adjust how certain 'options' widgets like radio, selectbox, and
#     multiselect coerce Enum members when the Enum class gets
#     re-defined during a script re-run.

#     Allowed values:
#     * "off": Disables Enum coercion.
#     * "nameOnly": Enum classes can be coerced if their member names match.
#     * "nameAndValue": Enum classes can be coerced if their member names AND
#     member values match.

#     Default: "nameOnly"
#     enumCoercion = "nameOnly"
#     """

#     magicEnabled: bool = True
#     # installTracer: bool # ! hidden option: deprecated
#     # fixMatplotlib: bool # ! hidden option: deprecated
#     """
#     Run the Python Garbage Collector after each
#     script execution. This can help avoid excess
#     memory use in Streamlit apps, but could
#     introduce delay in rerunning the app script
#     for high-memory-use applications.
#     """
#     postScriptGC: bool = False  # * hidden option: use `streamlit run --help`
#     """
#     Handle script rerun requests immediately,
#     rather than waiting for script execution to
#     reach a yield point. This makes Streamlit
#     much more responsive to user interaction,
#     but it can lead to race conditions in apps
#     that mutate session_state data outside of
#     explicit session_state assignment
#     statements.
#     """
#     fastReruns: bool = True
#     enforceSerializableSessionState: bool = False
#     enumCoercion: str = "nameOnly"

#     @field_validator("enumCoercion")
#     def __validate_enumCoercion(cls, enumCoercion: str) -> str:
#         valid_enumCoercion_options: set[str] = {"nameOnly", "off", "nameAndValue"}
#         if enumCoercion not in valid_enumCoercion_options:
#             raise ValueError(
#                 f"'enumCoercion' must be one of {valid_enumCoercion_options}"
#             )
#         return enumCoercion


# class ServerConfig(BaseModel):
#     """
#     List of folders that should not be watched for changes. This
#     impacts both "Run on Save" and @st.cache.

#     Relative paths will be taken as relative to the current working directory.

#     Example: ['/home/user1/env', 'relative/path/to/folder']

#     Default: []
#     folderWatchBlacklist = []

#     Change the type of file watcher used by Streamlit, or turn it off
#     completely.

#     Allowed values:
#     * "auto" : Streamlit will attempt to use the watchdog module, and
#     falls back to polling if watchdog is not available.
#     * "watchdog" : Force Streamlit to use the watchdog module.
#     * "poll" : Force Streamlit to always use polling.
#     * "none" : Streamlit will not watch files.

#     Default: "auto"
#     fileWatcherType = "auto"

#     Symmetric key used to produce signed cookies. If deploying on multiple replicas, this should
#     be set to the same value across all replicas to ensure they all share the same secret.

#     Default: randomly generated secret key.
#     cookieSecret = "e79cb7b97e33473aa8bd6ba07479d8deeb428defd6a4dbe8a674d6d046f78507"

#     If false, will attempt to open a browser window on start.

#     Default: false unless (1) we are on a Linux box where DISPLAY is unset, or
#     (2) we are running in the Streamlit Atom plugin.
#     headless = false

#     Automatically rerun script when the file is modified on disk.

#     Default: false
#     runOnSave = false

#     The address where the server will listen for client and browser
#     connections. Use this if you want to bind the server to a specific address.
#     If set, the server will only be accessible from this address, and not from
#     any aliases (like localhost).

#     Default: (unset)
#     address =

#     The port where the server will listen for browser connections.

#     Default: 8501
#     port = 8501

#     The base path for the URL where Streamlit should be served from.

#     Default: ""
#     baseUrlPath = ""

#     Enables support for Cross-Origin Resource Sharing (CORS) protection, for added security.

#     Due to conflicts between CORS and XSRF, if `server.enableXsrfProtection` is on and
#     `server.enableCORS` is off at the same time, we will prioritize `server.enableXsrfProtection`.

#     Default: true
#     enableCORS = true

#     Enables support for Cross-Site Request Forgery (XSRF) protection, for added security.

#     Due to conflicts between CORS and XSRF, if `server.enableXsrfProtection` is on and
#     `server.enableCORS` is off at the same time, we will prioritize `server.enableXsrfProtection`.

#     Default: true
#     enableXsrfProtection = true

#     Max size, in megabytes, for files uploaded with the file_uploader.

#     Default: 200
#     maxUploadSize = 200

#     Max size, in megabytes, of messages that can be sent via the WebSocket connection.

#     Default: 200
#     maxMessageSize = 200

#     Enables support for websocket compression.

#     Default: false
#     enableWebsocketCompression = false

#     Enable serving files from a `static` directory in the running app's directory.

#     Default: false
#     enableStaticServing = false

#     Server certificate file for connecting via HTTPS.
#     Must be set at the same time as "server.sslKeyFile".

#     ['DO NOT USE THIS OPTION IN A PRODUCTION ENVIRONMENT. It has not gone through security audits or performance tests. For the production environment, we recommend performing SSL termination by the load balancer or the reverse proxy.']
#     sslCertFile =

#     Cryptographic key file for connecting via HTTPS.
#     Must be set at the same time as "server.sslCertFile".

#     ['DO NOT USE THIS OPTION IN A PRODUCTION ENVIRONMENT. It has not gone through security audits or performance tests. For the production environment, we recommend performing SSL termination by the load balancer or the reverse proxy.']
#     sslKeyFile =
#     """

#     folderWatchBlacklist: list = list()
#     fileWatcherType: str = "auto"
#     # cookieSecret # ! ignored as it is randomly generated
#     headless: bool = False
#     runOnSave: bool = True
#     allowRunOnSave: bool = True
#     address: str = (
#         "localhost"  # ? not clear what the difference between this and browser option is
#     )
#     port: int = (
#         8501  # ? not clear what the difference between this and browser option is
#     )
#     # scriptHealthCheckEnabled: bool # ! hidden option: experimental
#     baseUrlPath: str = ""
#     enableCORS: bool = True
#     enableXsrfProtection: bool = True
#     maxUploadSize: int = 200
#     maxMessageSize: int = 200
#     # enableArrowTruncation: bool # ! hidden option, don't entirely understand
#     enableWebsocketCompression: bool = False
#     enableStaticServing: bool = False
#     # sslCertfile # ! ignored for security reasons, see docstring
#     # sslKeyFile # ! ignored for security reasons, see docstring

#     @field_validator("fileWatcherType")
#     def __validate_fileWatcherType(cls, fileWatcherType: str) -> str:
#         valid_fileWatcherType_options: set[str] = {"auto", "watchdog", "poll", "none"}
#         if fileWatcherType not in valid_fileWatcherType_options:
#             raise ValueError(
#                 f"'fileWatcherType' must be one of {valid_fileWatcherType_options}"
#             )
#         return fileWatcherType


# class BrowserConfig(BaseModel):
#     """
#     Internet address where users should point their browsers in order to
#     connect to the app. Can be IP address or DNS name and path.

#     This is used to:
#     - Set the correct URL for CORS and XSRF protection purposes.
#     - Show the URL on the terminal
#     - Open the browser

#     Default: "localhost"
#     serverAddress = "localhost"

#     Whether to send usage statistics to Streamlit.

#     Default: true
#     gatherUsageStats = true

#     Port where users should point their browsers in order to connect to the
#     app.

#     This is used to:
#     - Set the correct URL for CORS and XSRF protection purposes.
#     - Show the URL on the terminal
#     - Open the browser

#     Default: whatever value is set in server.port.
#     serverPort = 8501
#     """

#     serverAddress: str = (
#         "localhost"  # ? not clear what the difference between this and server option is
#     )
#     gatherUsageStats: bool = True
#     serverPort: int = (
#         8501  # ? not clear what the difference between this and server option is
#     )
#     # ? possible answer: this determines where the browser opens? Or is duplicate param?


# class UserInterfaceConfig(BaseModel):  # * hidden option: use `streamlit run --help`
#     hideTopBar: bool = False
#     # hideSidebarNav: bool # ! deprecated


# # ! ignored, the parent package doesn't support 'magic' feature anyways
# # class MagicConfig(BaseModel): # * hidden option: use `streamlit run --help`
# #     displayRootDocString: bool
# #     displayLastExprIfNoSemicolon: bool


# class MapboxConfig(BaseModel):
#     """
#     Configure Streamlit to use a custom Mapbox
#     token for elements like st.pydeck_chart and st.map.
#     To get a token for yourself, create an account at
#     https://mapbox.com. It's free (for moderate usage levels)!

#     Default: ""
#     token = ""
#     """

#     token: str = ""


# class DeprecationConfig(BaseModel):
#     """
#     Set to false to disable the deprecation warning for using the global pyplot instance.

#     Default: true
#     showPyplotGlobalUse = true
#     """

#     # showfileuploaderEncoding: bool # ! hidden: deprecated
#     # showImageFormat: bool # ! hidden: deprecated
#     showPyplotGlobalUse: bool = True


# class ThemeConfig(BaseModel):
#     """
#     The preset Streamlit theme that your custom theme inherits from.
#     One of "light" or "dark".
#     base =

#     Primary accent color for interactive elements.
#     primaryColor =

#     Background color for the main content area.
#     backgroundColor =

#     Background color used for the sidebar and most interactive widgets.
#     secondaryBackgroundColor =

#     Color used for almost all text.
#     textColor =

#     Font family for all text in the app, except code blocks. One of "sans serif",
#     "serif", or "monospace".
#     font =
#     """

#     base: Optional[str] = None
#     primaryColor: Optional[str] = None  # * hidden option: use `streamlit run --help`
#     backgroundColor: Optional[str] = None
#     secondaryBackgroundColor: Optional[str] = None
#     textColor: Optional[str] = None
#     font: Optional[str] = None

#     @field_validator("font")
#     def __validate_font(cls, font: str) -> str:
#         valid_font_options: set[str] = {"sans serif", "serif", "monospace"}
#         if font not in valid_font_options:
#             raise ValueError(f"'font' must be one of {valid_font_options}")
#         return font


# class StreamlitConfig(BaseModel):
#     logger: LoggerConfig = LoggerConfig()
#     client: ClientConfig = ClientConfig()
#     runner: RunnerConfig = RunnerConfig()
#     server: ServerConfig = ServerConfig()
#     browser: BrowserConfig = BrowserConfig()
#     ui: UserInterfaceConfig = UserInterfaceConfig()
#     mapbox: MapboxConfig = MapboxConfig()
#     deprecation: DeprecationConfig = DeprecationConfig()
#     theme: ThemeConfig = ThemeConfig()

#     def save(
#         self, path: str | Path = path_streamlit_config, overwrite: bool = False
#     ) -> None:
#         if isinstance(path, str):
#             path = Path(path)
#         if path.exists() and not overwrite:
#             raise FileExistsError(str(path))
#         with open(path, "w") as file:
#             toml.dump(self.model_dump(), file)
#         file.close()
