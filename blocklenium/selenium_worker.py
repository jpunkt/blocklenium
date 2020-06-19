import configparser
import logging
import threading

from selenium import webdriver

logger = logging.getLogger(__name__)


class SeleniumWorker(threading.Thread):
    def __init__(self, queue, bookmarklet_path, chromedriver_path,
                 desk_url):
        threading.Thread.__init__(self)

        self.chromedriver_path = chromedriver_path
        self.desk_url = desk_url

        self.queue = queue

        self.chromedriver = None

        # Load javascript file
        # If the filename ends with '.url', read with config-parser
        if bookmarklet_path.endswith('.url'):
            # parse with config parser
            parser = configparser.ConfigParser()
            parser.read(bookmarklet_path)
            if 'InternetShortcut' in parser:
                self.js = parser['InternetShortcut']['URL']
            else:
                raise ValueError('Bookmarklet file must be a web link!')
        else:
            # TODO error handling
            with open(self.bookmarklet_path, "r") as f:
                # TODO read from web-url format
                self.js = f.read()

    def run(self):
        logger.debug('Thread running.')

        while True:
            q = self.queue.get()

            if q:
                logger.debug('Starting browser...')

                # Instantiate driver (opens browser)
                if self.chromedriver is None:
                    logger.debug('No browser running. Starting browser...')
                    self.chromedriver = webdriver.Chrome(
                                                    self.chromedriver_path)

                # Open a website
                logger.debug('Calling url')
                self.chromedriver.get(self.desk_url)

                if self.js is not None:
                    # Execute javascript
                    self.chromedriver.execute_script(self.js)
            else:
                logging.debug('Closing browser...')
                # Close browser
                if self.chromedriver is not None:
                    self.chromedriver.quit()

                break
