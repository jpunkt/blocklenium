import logging
import queue
import pyads

from ctypes import sizeof
from time import sleep

from blocklenium.selenium_worker import SeleniumWorker


logger = logging.getLogger(__name__)


class Blocklenium(object):
    def __init__(self, plc_id, bookmarklet_path, chromedriver_path,
                 desk_url, plc_start_flag):

        self.plc_start_flag = plc_start_flag

        self.queue = queue.Queue()

        self._t = SeleniumWorker(self.queue, bookmarklet_path,
                                 chromedriver_path, desk_url)

        self._plc = pyads.Connection(plc_id, 851)

        self.callback = self._plc.notification(pyads.
                                               PLCTYPE_BOOL)(
                                                    self._callback)

    def _callback(self, handle, name, timestamp, value):
        if value:
            logger.info('Queued flag to handle...')
            self.queue.put(True)

        logger.debug(
             'handle: {0} | name: {1} | timestamp: {2} | value: {3}'.format(
                handle, name, timestamp, value))

    def start(self):
        logger.debug('Starting blocklenium...')

        self._plc.open()

        with self._plc:
            attr = pyads.NotificationAttrib(sizeof(pyads.PLCTYPE_BOOL))
            self._t.start()

            self._plc.add_device_notification(
                self.plc_start_flag, attr,
                self.callback)

            while True:
                sleep(10)

                try:
                    self._plc.read_state()
                except pyads.ADSError:
                    logger.info('PLC not running. Terminating...')

                    self.queue.put(False)
                    break

        self._t.join()
        logger.info('Blocklenium terminated.')
