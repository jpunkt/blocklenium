import logging
import sys

import click

from blocklenium import settings
from blocklenium.blocklenium import Blocklenium

logger = logging.getLogger('blocklenium.main')


if __name__ == '__main__':
    print('Please use the click entry-point.')
    pass





@click.command()
@click.option('--plc_id', default=settings.PLC_ID, show_default=True,
              help='ADS Id of PLC')
@click.option('--plc_flag', 'plc_start_flag',
              default=settings.PLC_START_FLAG, show_default=True,
              help='PLC variable name of flag to start browser (BOOL)')
@click.option('--plc_errorflag', 'plc_error_flag',
              default=settings.PLC_ERROR_FLAG, show_default=True,
              help='PLC variable name of flag set TRUE if an error occurs.'
              )
@click.option('--plc_errormsg', 'plc_error_msg',
              default=settings.PLC_ERROR_MSG, show_default=True,
              help='PLC variable name to hold error messages')
@click.option('--webdriver', 'chromedriver_path',
              default=settings.CHROMEDRIVER_PATH, show_default=True,
              type=click.Path(exists=True, file_okay=True, dir_okay=False),
              help='Path to selenium webdriver for chrome')
@click.option('--insecure-con', 'browser_insecure_certs', is_flag=True,
              help='Suppress warning for insecure site certificates')
@click.option('--login-required', 'desk_login_required', is_flag=True,
              help='''Target URL requires a login. Requires the login 
                   credentials to be set to the appropriate variables in 
                   the PLC (see below for default values)''')
@click.option('--plc-desk-user', 'plc_desk_user', show_default=True,
              default=settings.PLC_DESK_USER,
              help='''Change the PLC variable which stores the username for
                   the target URL''')
@click.option('--plc-desk-password', 'plc_desk_pw',
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
         plc_error_flag,
         plc_error_msg,
         chromedriver_path,
         browser_insecure_certs,
         desk_login_required,
         plc_desk_user,
         plc_desk_pw,
         bookmarklet_path,
         desk_url):
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    logger.info('Initializing blocklenium...')

    # Build config dictionary from passed arguments
    config = {key.upper(): value for key, value in locals().items()}

    if logger.level == logging.DEBUG:
        for k in config.keys():
            logger.debug('config[{0}]={1}'.format(k, config[k]))

    blknm = Blocklenium(config)

    blknm.start()
