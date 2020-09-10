# vim:fileencoding=utf-8
"""setup script for ``reindent``, originally created by Tim Peters"""

import sys
from setuptools import setup


VERSION = '0.1.0'
ENTRY_POINTS = \
"""[console_scripts]
MonitoreoRadio =Monitoreo.__init__:main
"""


def main():
    """just wraps call to ``setup``"""
    setup(name='MonitoreoRadio', version=VERSION,
        author="Luis Mata", author_email='mata.perez.luis@gmail.com',
        maintainer="Luis Mata", maintainer_email="mata.perez.luis@gmail.com",
        description='Permite Consultar la informacion de las radiocomunicaciones',
        keywords=['MonitoreoRadio'],
        entry_points=ENTRY_POINTS,
        classifiers=[
            "Development Status :: 6 - Mature",
            "Environment :: GUI",
            "Intended Audience :: Developers",
            "License :: GPL",
            "Natural Language :: Español",
            "Programming Language :: Python",
            "Topic :: Software Development :: Quality Assurance",
            ],
        long_description=''.join([l for l in _get_long_description()]),
        platforms=['all'], license="GPL",
        packages=['Monitoreo'], data_files=[('usr/share/MonitoreoRadio', ['Monitoreo/logo2.png', 'Monitoreo/Play-Normal-icon.png','Monitoreo/monitoreo.ui']), ('/usr/share/applications', ['Monitoreo/monitorradio.desktop'])
                  ], 
        )
    return 0


def _get_long_description(fname='README.txt'):
    for line in open(fname, 'rb'):
        yield line


if __name__ == '__main__':
    sys.exit(main())
