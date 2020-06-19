import logging
import sys

import click

from blocklenium.blocklenium import Blocklenium
from blocklenium.settings import CHROMEDRIVER_PATH, DESK_URL, PLC_ID, \
    PLC_START_FLAG, BOOKMARKLET_PATH

logger = logging.getLogger('blocklenium.main')


@click.command()
@click.option('--plc_id', default=PLC_ID, show_default=True,
              help='ADS Id of PLC')
@click.option('--plc_flag', 'plc_start_flag',
              default=PLC_START_FLAG, show_default=True,
              help='PLC variable name of flag to start browser (BOOL)')
@click.option('--webdriver', 'chromedriver_path',
              default=CHROMEDRIVER_PATH, show_default=True,
              type=click.Path(exists=True, file_okay=True, dir_okay=False),
              help='Path to selenium webdriver for chrome')
@click.option('-b', '--bookmarklet', 'bookmarklet_path',
              required=True,
              type=click.Path(exists=True, file_okay=True, dir_okay=False),
              help='Path to bookmarklet javascript code')
@click.option('-u', '--url', 'desk_url',
              required=True,
              help='URL to run bookmarklet on')
def main(plc_id, plc_start_flag, chromedriver_path, bookmarklet_path,
         desk_url):
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

    logger.debug('Initializing...')
    blknm = Blocklenium(plc_id, bookmarklet_path, chromedriver_path,
                        desk_url, plc_start_flag)

    blknm.start()


if __name__ == '__main__':
    main(PLC_ID, BOOKMARKLET_PATH, CHROMEDRIVER_PATH,
         DESK_URL, PLC_START_FLAG)
