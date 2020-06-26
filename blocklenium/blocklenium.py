import logging
import queue
import pyads

from ctypes import sizeof
from time import sleep

from blocklenium.selenium_worker import SeleniumWorker


logger = logging.getLogger(__name__)


class Blocklenium(object):
    def __init__(self, config):

        self.plc_start_flag = config['PLC_START_FLAG']

        self.queue = queue.Queue()

        self._t = SeleniumWorker(self.queue, config)

        self._plc = pyads.Connection(config['PLC_ID'], 851)

        self.callback = self._plc.notification(pyads.
                                               PLCTYPE_BOOL)(
                                                    self._callback)

        self.config = config

    def _callback(self, handle, name, timestamp, value):
        if value:
            logger.info('Queued flag to handle...')
            self.queue.put(True)

        logger.debug(
             'handle: {0} | name: {1} | timestamp: {2} | value: {3}'.format(
                handle, name, timestamp, value))

    def start(self):
        logger.info('Starting blocklenium...')

        self._plc.open()

        with self._plc:
            attr = pyads.NotificationAttrib(sizeof(pyads.PLCTYPE_BOOL))
            self._t.start()

            if self.config['DESK_LOGIN_REQUIRED']:
                try:
                    user = self._plc.read_by_name(
                        self.config['PLC_DESK_USER'],
                        pyads.PLCTYPE_STRING)
                    pwd = self._plc.read_by_name(
                        self.config['PLC_DESK_PW'],
                        pyads.PLCTYPE_STRING)

                    self._t.desk_username = user
                    self._t.desk_password = pwd
                except pyads.ADSError as e:
                    logging.error('''{0} or {1} not defined on PLC with 
                                  --login-required flag set.'''.format(
                        self.config['PLC_DESK_USER'],
                        self.config['PLC_DESK_PW']))
                    return

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
        logger.debug('Blocklenium terminated.')
