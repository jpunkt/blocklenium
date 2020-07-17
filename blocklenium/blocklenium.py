import logging
import queue
import pyads

from ctypes import sizeof
from time import sleep

from blocklenium.selenium_worker import SeleniumWorker

logger = logging.getLogger(__name__)


class Blocklenium(object):
    def __init__(self, config):

        self.config = config

        self.is_error = False

        try:
            self._plc = pyads.Connection(config['PLC_ID'], 851)
        except pyads.ADSError as e:
            logger.exception(e)
            self.is_error = True
            exit(1)

        self.queue = queue.Queue()

        try:
            self._t = SeleniumWorker(self.queue, config)
        except ValueError as e:
            self.handle_error('Error during setup. Check the logs.', e)
            exit(1)

        self.callback = self._plc.notification(pyads.
                                               PLCTYPE_BOOL)(
            self._callback)

    def _callback(self, handle, name, timestamp, value):
        if value:
            logger.info(
                'Callback received True, queuing True for worker...')
            self.queue.put(True)
        else:
            logger.info(
                'Callback received False, queuing None for worker...')
            self.queue.put(None)

        logger.debug(
            'handle: {0} | name: {1} | timestamp: {2} | value: {3}'.
            format(handle, name, timestamp, value))

    def handle_error(self, message, error=None):
        self.is_error = True

        self.queue.put(False)
        self._t.join()

        self._plc.write_by_name(self.config['PLC_ERROR_FLAG'], True,
                                pyads.PLCTYPE_BOOL)
        self._plc.write_by_name(self.config['PLC_ERROR_MSG'], message,
                                pyads.PLCTYPE_STRING)

        logging.error(message)
        if error is not None:
            logging.error(error, exc_info=True)

        exit(1)

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
                    self.handle_error('''{0} or {1} not defined on PLC with 
                                  --login-required flag set.'''.format(
                        self.config['PLC_DESK_USER'],
                        self.config['PLC_DESK_PW']), e)
                    return

            self._plc.add_device_notification(
                self.config['PLC_START_FLAG'], attr,
                self.callback)

            while not self.is_error:
                sleep(10)

                try:
                    self._plc.read_state()
                except pyads.ADSError:
                    logger.info('PLC not running. Terminating...')

                    self.queue.put(False)
                    break

        self._t.join()
        logger.debug('Blocklenium terminated.')
        exit(0)
