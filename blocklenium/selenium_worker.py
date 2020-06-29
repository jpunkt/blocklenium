import configparser
import logging
import threading
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver

logger = logging.getLogger(__name__)


class SeleniumWorker(threading.Thread):
    def __init__(self, queue, config):
        threading.Thread.__init__(self)

        self.chromedriver_path = config['CHROMEDRIVER_PATH']
        self.desk_url = config['DESK_URL']
        self.login_required = config['DESK_LOGIN_REQUIRED']

        self.queue = queue

        self.chromedriver = None

        # Set options for chromedriver
        self.chromecaps = webdriver.DesiredCapabilities.CHROME.copy()
        # Accept insecure connections
        self.chromecaps['acceptInsecureCerts'] = \
            config['BROWSER_INSECURE_CERTS']

        # Load javascript file
        # If the filename ends with '.url', read with config-parser
        bookmarklet_path = config['BOOKMARKLET_PATH']
        if bookmarklet_path.endswith('.url'):
            # parse with config parser
            parser = configparser.ConfigParser()
            parser.read(bookmarklet_path)
            if 'InternetShortcut' in parser:
                self.js = parser['InternetShortcut']['URL']
            else:
                raise ValueError('Bookmarklet file must be a web link!')
        else:
            with open(bookmarklet_path, "r") as f:
                self.js = f.read()

    def run(self):
        logger.debug('Thread running.')

        while True:
            q = self.queue.get()

            if q:
                logger.info('Starting browser...')

                # Instantiate driver (opens browser)
                if self.chromedriver is None:
                    logger.debug('No browser running. Starting browser...')
                    self.chromedriver = webdriver.Chrome(
                                    self.chromedriver_path,
                                    desired_capabilities=self.chromecaps)

                # Open a website
                logger.debug('Calling url')
                self.chromedriver.get(self.desk_url)

                # Log in if needed
                if self.login_required:
                    self.desk_login()

                # Execute JavaScript
                if self.js is not None:
                    logger.info('Executing JavaScript...')
                    # Execute javascript
                    self.chromedriver.execute_script(self.js)
            else:
                logger.info('Closing browser...')
                # Close browser
                if self.chromedriver is not None:
                    self.chromedriver.quit()

                break

    def desk_login(self):
        logger.info('attempting login to desk...')
        # the user-input fields have weird ids, so we need to select
        # them by searching for ids containing 'Username' or 'Password'
        userfields = self.chromedriver.find_elements_by_css_selector(
            "input[id*='Username']")
        pwdfields = self.chromedriver.find_elements_by_css_selector(
            "input[id*='Password']")

        if (len(userfields) > 0) and (len(pwdfields > 0)):
            userfields[0].send_keys(self.desk_username)
            pwdfields[0].send_keys(self.desk_password)

            loginbtn = self.chromedriver.find_element_by_xpath(
                "//button[@type='submit']")
            loginbtn.click()

            # Wait for the new page to be fully loaded
            WebDriverWait(self.chromedriver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME,
                                                "timeline-header"))
            )
        else:
            logger.info(
                'Expected Login page but found no login fields. Ignored')
