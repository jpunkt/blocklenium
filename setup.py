import re
import ast

from setuptools import setup


_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('blocklenium/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))
    setup(
        name='blocklenium',
        version=version,
        description='pyADS bridge for selenium-controlled browser',
        url='https://github.com/jpunkt/blocklenium.git',
        license='MIT',
        author='Johannes Payr',
        author_email='johannes.payr@mci.edu',
        platforms='any',

        packages=[
            'blocklenium'
        ],

        install_requires=[
            'selenium',
            'pyads',
            'click'
        ],

        entry_points='''
            [console_scripts]
            blocklenium=blocklenium:main
        '''

    )

