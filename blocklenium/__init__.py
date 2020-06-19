from .main import main

from blocklenium import settings


__version__ = '0.0.1'


def read_defaultconfig():
    return {key: value for key, value in vars(settings).items()
            if key.isupper()}
