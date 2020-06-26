import logging
import sys

import click

from blocklenium import settings
from blocklenium.blocklenium import Blocklenium

logger = logging.getLogger('blocklenium.main')


@click.command()
@click.option('--plc_id', default=settings.PLC_ID, show_default=True,
              help='ADS Id of PLC')
@click.option('--plc_flag', 'plc_start_flag',
              default=settings.PLC_START_FLAG, show_default=True,
              help='PLC variable name of flag to start browser (BOOL)')
@click.option('--webdriver', 'chromedriver_path',
              default=settings.CHROMEDRIVER_PATH, show_default=True,
              type=click.Path(exists=True, file_okay=True, dir_okay=False),
              help='Path to selenium webdriver for chrome')
@click.option('--insecure-con', 'chromedriver_insecure', is_flag=True,
              help='Suppress warning for insecure site certificates')
@click.option('--login-required', 'chromedriver_login', is_flag=True,
              help='''Target URL requires a login. Requires the login 
                   credentials to be set to the appropriate variables in 
                   the PLC (see below for default values)''')
@click.option('--plc-desk-user', 'plc_desk_username', show_default=True,
              default=settings.PLC_DESK_USER,
              help='''Change the PLC variable which stores the username for
                   the target URL''')
@click.option('--plc-desk-password', 'plc_desk_password',
              show_default=True,
              default=settings.PLC_DESK_PW,
              help='''Change the PLC variable which stores the password for
                   the target URL''')
@click.option('-b', '--bookmarklet', 'bookmarklet_path',
              required=True,
              type=click.Path(exists=True, file_okay=True, dir_okay=False),
              help='Path to bookmarklet javascript code')
@click.option('-u', '--url', 'desk_url',
              required=True,
              help='URL to run bookmarklet on')
def main(plc_id,
         plc_start_flag,
         chromedriver_path,
         chromedriver_insecure,
         chromedriver_login,
         plc_desk_username,
         plc_desk_password,
         bookmarklet_path,
         desk_url):
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    logger.debug('Initializing...')

    config = dict()
    config['PLC_ID'] = plc_id
    config['PLC_START_FLAG'] = plc_start_flag
    config['PLC_DESK_USER'] = plc_desk_username
    config['PLC_DESK_PW'] = plc_desk_password
    config['CHROMEDRIVER_PATH'] = chromedriver_path
    config['BROWSER_INSECURE_CERTS'] = chromedriver_insecure
    config['BOOKMARKLET_PATH'] = bookmarklet_path
    config['DESK_LOGIN_REQUIRED'] = chromedriver_login
    config['DESK_URL'] = desk_url

    if logger.level == logging.DEBUG:
        for k in config.keys():
            logger.debug('config[{0}]={1}'.format(k, config[k]))

    blknm = Blocklenium(config)

    blknm.start()


if __name__ == '__main__':
    print('Please use the click entry-point.')
    pass
