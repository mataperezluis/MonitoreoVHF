# vim:fileencoding=utf-8
"""setup script for ``reindent``, originally created by Tim Peters"""

import sys
from setuptools import setup


VERSION = '0.1.0'
ENTRY_POINTS = \
"""[console_scripts]
grabadorradio =grabador.__init__:main
"""


def main():
    """just wraps call to ``setup``"""
    setup(name='GrabadorRadio', version=VERSION,
        author="Luis Mata", author_email='mata.perez.luis@gmail.com',
        maintainer="Luis Mata", maintainer_email="mata.perez.luis@gmail.com",
        description='Graba el audio de las radiocomunicaciones',
        keywords=['GrabadorRadio'],
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
        packages=['grabador'], data_files=[('usr/share/GrabadorRadio', ['grabador/logo2.png', 'grabador/unet.png','grabador/ingresarRadio.ui','grabador/mainwindow.ui','grabador/usuarios.ui','grabador/acerca.ui']), ('/usr/share/applications', ['grabador/GrabadorRadio.desktop'])
                  ], 
        )
    return 0


def _get_long_description(fname='README.txt'):
    for line in open(fname, 'rb'):
        yield line


if __name__ == '__main__':
    sys.exit(main())
