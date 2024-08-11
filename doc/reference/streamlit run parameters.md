```sh
streamlit run --help
Usage: streamlit run [OPTIONS] TARGET [ARGS]...

  Run a Python script, piping stderr to Streamlit.

  The script can be local or it can be an url. In the latter case, Streamlit
  will download the script to a temporary file and runs this file.

Options:
  --global.disableWidgetStateDuplicationWarning BOOLEAN
                                  By default, Streamlit displays a warning
                                  when a user sets both a widget default value
                                  in the function defining the widget and a
                                  widget value via the widget's key in
                                  `st.session_state`.

                                  If you'd like to turn off this warning, set
                                  this to True.  [env var: STREAMLIT_GLOBAL_DI
                                  SABLE_WIDGET_STATE_DUPLICATION_WARNING]
  --global.showWarningOnDirectExecution BOOLEAN
                                  If True, will show a warning when you run a
                                  Streamlit-enabled script via "python
                                  my_script.py".  [env var: STREAMLIT_GLOBAL_S
                                  HOW_WARNING_ON_DIRECT_EXECUTION]
  --global.developmentMode BOOLEAN
                                  Are we in development mode.

                                  This option defaults to True if and only if
                                  Streamlit wasn't installed normally.  [env
                                  var: STREAMLIT_GLOBAL_DEVELOPMENT_MODE]
  --global.e2eTest BOOLEAN        Are we in an e2e (playwright) test? Set
                                  automatically when our e2e tests are
                                  running.  [env var:
                                  STREAMLIT_GLOBAL_E2E_TEST]
  --global.unitTest BOOLEAN       Are we in a unit test?  [env var:
                                  STREAMLIT_GLOBAL_UNIT_TEST]
  --global.appTest BOOLEAN        Are we in an app test? Set automatically
                                  when the AppTest framework is running  [env
                                  var: STREAMLIT_GLOBAL_APP_TEST]
  --global.suppressDeprecationWarnings BOOLEAN
                                  Hide deprecation warnings in the streamlit
                                  app.  [env var: STREAMLIT_GLOBAL_SUPPRESS_DE
                                  PRECATION_WARNINGS]
  --global.minCachedMessageSize FLOAT
                                  Only cache ForwardMsgs that are greater than
                                  or equal to this minimum.  [env var:
                                  STREAMLIT_GLOBAL_MIN_CACHED_MESSAGE_SIZE]
  --global.maxCachedMessageAge INTEGER
                                  Expire cached ForwardMsgs whose age is
                                  greater than this value. A message's age is
                                  defined by how many times its script has
                                  finished running since the message has been
                                  accessed.  [env var:
                                  STREAMLIT_GLOBAL_MAX_CACHED_MESSAGE_AGE]
  --global.storeCachedForwardMessagesInMemory BOOLEAN
                                  If True, store cached ForwardMsgs in backend
                                  memory. This is an internal flag to validate
                                  a potential removal of the in-memory forward
                                  message cache.  [env var: STREAMLIT_GLOBAL_S
                                  TORE_CACHED_FORWARD_MESSAGES_IN_MEMORY]
  --logger.level TEXT             Level of logging: 'error', 'warning',
                                  'info', or 'debug'.

                                  Default: 'info'  [env var:
                                  STREAMLIT_LOGGER_LEVEL]
  --logger.messageFormat TEXT     String format for logging messages. If
                                  logger.datetimeFormat is set, logger
                                  messages will default to
                                  `%(asctime)s.%(msecs)03d %(message)s`. See
                                  [Python's documentation](https://docs.python
                                  .org/2.6/library/logging.html#formatter-
                                  objects) for available attributes.

                                  Default: "%(asctime)s %(message)s"  [env
                                  var: STREAMLIT_LOGGER_MESSAGE_FORMAT]
  --logger.enableRich BOOLEAN     Controls whether uncaught app exceptions are
                                  logged via the rich library.

                                  If True and if rich is installed, exception
                                  tracebacks will be logged with syntax
                                  highlighting and formatting. Rich tracebacks
                                  are easier to read and show more code than
                                  standard Python tracebacks.

                                  If set to False, the default Python
                                  traceback formatting will be used.  [env
                                  var: STREAMLIT_LOGGER_ENABLE_RICH]
  --client.showErrorDetails BOOLEAN
                                  Controls whether uncaught app exceptions and
                                  deprecation warnings are displayed in the
                                  browser. By default, this is set to True and
                                  Streamlit displays app exceptions and
                                  associated tracebacks, and deprecation
                                  warnings, in the browser.

                                  If set to False, deprecation warnings and
                                  full exception messages will print to the
                                  console only. Exceptions will still display
                                  in the browser with a generic error message.
                                  For now, the exception type and traceback
                                  show in the browser also, but they will be
                                  removed in the future.  [env var:
                                  STREAMLIT_CLIENT_SHOW_ERROR_DETAILS]
  --client.toolbarMode TEXT       Change the visibility of items in the
                                  toolbar, options menu, and settings dialog
                                  (top right of the app).

                                  Allowed values: * "auto"      : Show the
                                  developer options if the app is accessed
                                  through                 localhost or through
                                  Streamlit Community Cloud as a developer.
                                  Hide them otherwise. * "developer" : Show
                                  the developer options. * "viewer"    : Hide
                                  the developer options. * "minimal"   : Show
                                  only options set externally (e.g. through
                                  Streamlit Community Cloud) or through
                                  st.set_page_config.                 If there
                                  are no options left, hide the menu.  [env
                                  var: STREAMLIT_CLIENT_TOOLBAR_MODE]
  --client.showSidebarNavigation BOOLEAN
                                  Controls whether to display the default
                                  sidebar page navigation in a multi-page app.
                                  This only applies when app's pages are
                                  defined by the `pages/` directory.  [env
                                  var:
                                  STREAMLIT_CLIENT_SHOW_SIDEBAR_NAVIGATION]
  --runner.magicEnabled BOOLEAN   Allows you to type a variable or string by
                                  itself in a single line of Python code to
                                  write it to the app.  [env var:
                                  STREAMLIT_RUNNER_MAGIC_ENABLED]
  --runner.postScriptGC BOOLEAN   Run the Python Garbage Collector after each
                                  script execution. This can help avoid excess
                                  memory use in Streamlit apps, but could
                                  introduce delay in rerunning the app script
                                  for high-memory-use applications.  [env var:
                                  STREAMLIT_RUNNER_POST_SCRIPT_GC]
  --runner.fastReruns BOOLEAN     Handle script rerun requests immediately,
                                  rather than waiting for script execution to
                                  reach a yield point. This makes Streamlit
                                  much more responsive to user interaction,
                                  but it can lead to race conditions in apps
                                  that mutate session_state data outside of
                                  explicit session_state assignment
                                  statements.  [env var:
                                  STREAMLIT_RUNNER_FAST_RERUNS]
  --runner.enforceSerializableSessionState BOOLEAN
                                  Raise an exception after adding
                                  unserializable data to Session State. Some
                                  execution environments may require
                                  serializing all data in Session State, so it
                                  may be useful to detect incompatibility
                                  during development, or when the execution
                                  environment will stop supporting it in the
                                  future.  [env var: STREAMLIT_RUNNER_ENFORCE_
                                  SERIALIZABLE_SESSION_STATE]
  --runner.enumCoercion TEXT      Adjust how certain 'options' widgets like
                                  radio, selectbox, and multiselect coerce
                                  Enum members when the Enum class gets re-
                                  defined during a script re-run.

                                  Allowed values: * "off": Disables Enum
                                  coercion. * "nameOnly": Enum classes can be
                                  coerced if their member names match. *
                                  "nameAndValue": Enum classes can be coerced
                                  if their member names AND   member values
                                  match.  [env var:
                                  STREAMLIT_RUNNER_ENUM_COERCION]
  --server.folderWatchBlacklist TEXT
                                  List of folders that should not be watched
                                  for changes.

                                  Relative paths will be taken as relative to
                                  the current working directory.

                                  Example: ['/home/user1/env',
                                  'relative/path/to/folder']  [env var:
                                  STREAMLIT_SERVER_FOLDER_WATCH_BLACKLIST]
  --server.fileWatcherType TEXT   Change the type of file watcher used by
                                  Streamlit, or turn it off completely.

                                  Allowed values: * "auto"     : Streamlit
                                  will attempt to use the watchdog module, and
                                  falls back to polling if watchdog is not
                                  available. * "watchdog" : Force Streamlit to
                                  use the watchdog module. * "poll"     :
                                  Force Streamlit to always use polling. *
                                  "none"     : Streamlit will not watch files.
                                  [env var:
                                  STREAMLIT_SERVER_FILE_WATCHER_TYPE]
  --server.headless BOOLEAN       If false, will attempt to open a browser
                                  window on start.

                                  Default: false unless (1) we are on a Linux
                                  box where DISPLAY is unset, or (2) we are
                                  running in the Streamlit Atom plugin.  [env
                                  var: STREAMLIT_SERVER_HEADLESS]
  --server.runOnSave BOOLEAN      Automatically rerun script when the file is
                                  modified on disk.  [env var:
                                  STREAMLIT_SERVER_RUN_ON_SAVE]
  --server.allowRunOnSave BOOLEAN
                                  Allows users to automatically rerun when app
                                  is updated.  [env var:
                                  STREAMLIT_SERVER_ALLOW_RUN_ON_SAVE]
  --server.address TEXT           The address where the server will listen for
                                  client and browser connections. Use this if
                                  you want to bind the server to a specific
                                  address. If set, the server will only be
                                  accessible from this address, and not from
                                  any aliases (like localhost).

                                  Default: (unset)  [env var:
                                  STREAMLIT_SERVER_ADDRESS]
  --server.port INTEGER           The port where the server will listen for
                                  browser connections.

                                  Don't use port 3000 which is reserved for
                                  internal development.  [env var:
                                  STREAMLIT_SERVER_PORT]
  --server.scriptHealthCheckEnabled BOOLEAN
                                  Flag for enabling the script health check
                                  endpoint. It's used for checking if a script
                                  loads successfully. On success, the endpoint
                                  will return a 200 HTTP status code. On
                                  failure, the endpoint will return a 503 HTTP
                                  status code.

                                  Note: This is an experimental Streamlit
                                  internal API. The API is subject to change
                                  anytime so this should be used at your own
                                  risk  [env var: STREAMLIT_SERVER_SCRIPT_HEAL
                                  TH_CHECK_ENABLED]
  --server.baseUrlPath TEXT       The base path for the URL where Streamlit
                                  should be served from.  [env var:
                                  STREAMLIT_SERVER_BASE_URL_PATH]
  --server.enableCORS BOOLEAN     Enables support for Cross-Origin Resource
                                  Sharing (CORS) protection, for added
                                  security.

                                  Due to conflicts between CORS and XSRF, if
                                  `server.enableXsrfProtection` is on and
                                  `server.enableCORS` is off at the same time,
                                  we will prioritize
                                  `server.enableXsrfProtection`.  [env var:
                                  STREAMLIT_SERVER_ENABLE_CORS]
  --server.enableXsrfProtection BOOLEAN
                                  Enables support for Cross-Site Request
                                  Forgery (XSRF) protection, for added
                                  security.

                                  Due to conflicts between CORS and XSRF, if
                                  `server.enableXsrfProtection` is on and
                                  `server.enableCORS` is off at the same time,
                                  we will prioritize
                                  `server.enableXsrfProtection`.  [env var:
                                  STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION]
  --server.maxUploadSize INTEGER  Max size, in megabytes, for files uploaded
                                  with the file_uploader.  [env var:
                                  STREAMLIT_SERVER_MAX_UPLOAD_SIZE]
  --server.maxMessageSize INTEGER
                                  Max size, in megabytes, of messages that can
                                  be sent via the WebSocket connection.  [env
                                  var: STREAMLIT_SERVER_MAX_MESSAGE_SIZE]
  --server.enableArrowTruncation BOOLEAN
                                  Enable automatically truncating all data
                                  structures that get serialized into Arrow
                                  (e.g. DataFrames) to ensure that the size is
                                  under `server.maxMessageSize`.  [env var:
                                  STREAMLIT_SERVER_ENABLE_ARROW_TRUNCATION]
  --server.enableWebsocketCompression BOOLEAN
                                  Enables support for websocket compression.
                                  [env var: STREAMLIT_SERVER_ENABLE_WEBSOCKET_
                                  COMPRESSION]
  --server.enableStaticServing BOOLEAN
                                  Enable serving files from a `static`
                                  directory in the running app's directory.
                                  [env var:
                                  STREAMLIT_SERVER_ENABLE_STATIC_SERVING]
  --browser.serverAddress TEXT    Internet address where users should point
                                  their browsers in order to connect to the
                                  app. Can be IP address or DNS name and path.

                                  This is used to: - Set the correct URL for
                                  CORS and XSRF protection purposes. - Show
                                  the URL on the terminal - Open the browser
                                  [env var: STREAMLIT_BROWSER_SERVER_ADDRESS]
  --browser.gatherUsageStats BOOLEAN
                                  Whether to send usage statistics to
                                  Streamlit.  [env var:
                                  STREAMLIT_BROWSER_GATHER_USAGE_STATS]
  --browser.serverPort INTEGER    Port where users should point their browsers
                                  in order to connect to the app.

                                  This is used to: - Set the correct URL for
                                  XSRF protection purposes. - Show the URL on
                                  the terminal (part of `streamlit run`). -
                                  Open the browser automatically (part of
                                  `streamlit run`).

                                  This option is for advanced use cases. To
                                  change the port of your app, use
                                  `server.Port` instead. Don't use port 3000
                                  which is reserved for internal development.

                                  Default: whatever value is set in
                                  server.port.  [env var:
                                  STREAMLIT_BROWSER_SERVER_PORT]
  --server.sslCertFile TEXT       Server certificate file for connecting via
                                  HTTPS. Must be set at the same time as
                                  "server.sslKeyFile".

                                  ['DO NOT USE THIS OPTION IN A PRODUCTION
                                  ENVIRONMENT. It has not gone through
                                  security audits or performance tests. For
                                  the production environment, we recommend
                                  performing SSL termination by the load
                                  balancer or the reverse proxy.']  [env var:
                                  STREAMLIT_SERVER_SSL_CERT_FILE]
  --server.sslKeyFile TEXT        Cryptographic key file for connecting via
                                  HTTPS. Must be set at the same time as
                                  "server.sslCertFile".

                                  ['DO NOT USE THIS OPTION IN A PRODUCTION
                                  ENVIRONMENT. It has not gone through
                                  security audits or performance tests. For
                                  the production environment, we recommend
                                  performing SSL termination by the load
                                  balancer or the reverse proxy.']  [env var:
                                  STREAMLIT_SERVER_SSL_KEY_FILE]
  --ui.hideTopBar BOOLEAN         Flag to hide most of the UI elements found
                                  at the top of a Streamlit app.

                                  NOTE: This does *not* hide the main menu in
                                  the top-right of an app.  [env var:
                                  STREAMLIT_UI_HIDE_TOP_BAR]
  --magic.displayRootDocString BOOLEAN
                                  Streamlit's "magic" parser typically skips
                                  strings that appear to be docstrings. When
                                  this flag is set to True, Streamlit will
                                  instead display the root-level docstring in
                                  the app, just like any other magic string.
                                  This is useful for things like notebooks.
                                  [env var:
                                  STREAMLIT_MAGIC_DISPLAY_ROOT_DOC_STRING]
  --magic.displayLastExprIfNoSemicolon BOOLEAN
                                  Make Streamlit's "magic" parser always
                                  display the last expression in the root file
                                  if it has no semicolon at the end. This
                                  matches the behavior of Jupyter notebooks,
                                  for example.  [env var: STREAMLIT_MAGIC_DISP
                                  LAY_LAST_EXPR_IF_NO_SEMICOLON]
  --theme.base TEXT               The preset Streamlit theme that your custom
                                  theme inherits from. One of "light" or
                                  "dark".  [env var: STREAMLIT_THEME_BASE]
  --theme.primaryColor TEXT       Primary accent color for interactive
                                  elements.  [env var:
                                  STREAMLIT_THEME_PRIMARY_COLOR]
  --theme.backgroundColor TEXT    Background color for the main content area.
                                  [env var: STREAMLIT_THEME_BACKGROUND_COLOR]
  --theme.secondaryBackgroundColor TEXT
                                  Background color used for the sidebar and
                                  most interactive widgets.  [env var:
                                  STREAMLIT_THEME_SECONDARY_BACKGROUND_COLOR]
  --theme.textColor TEXT          Color used for almost all text.  [env var:
                                  STREAMLIT_THEME_TEXT_COLOR]
  --theme.font TEXT               Font family for all text in the app, except
                                  code blocks. One of "sans serif", "serif",
                                  or "monospace".  [env var:
                                  STREAMLIT_THEME_FONT]
  --help                          Show this message and exit.
```