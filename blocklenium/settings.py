# The path to the Webdriver (for Chrome/Chromium)
CHROMEDRIVER_PATH = 'C:\\WebDriver\\bin\\chromedriver.exe'

# Tell the browser to ignore invalid/insecure https connections
BROWSER_INSECURE_CERTS = True

# The URL pointing to the Franka Control Webinterface (Desk)
DESK_URL = 'robot.franka.de'

# Expect a login page when calling Desk
DESK_LOGIN_REQUIRED = True

# The ADS Id of the PLC (defaults to localhost)
PLC_ID = '127.0.0.1.1.1'

# Boolean flag on the PLC, set TRUE to start the web browser
PLC_START_FLAG = 'GVL.bStartBlockly'

# Blocklenium sets this flag TRUE if it terminates due to an exception
PLC_ERROR_FLAG = 'GVL.bBlockleniumError'

# Blocklenium sets this to it's terminating error message
PLC_ERROR_MSG = 'GVL.sBlockleniumErrorMsg'

# Set the Username for Desk on the PLC
PLC_DESK_USER = 'GVL.sDeskUsername'

# Set the Password for Desk on the PLC
PLC_DESK_PW = 'GVL.sDeskPassword'
