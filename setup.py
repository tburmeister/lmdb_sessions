from distutils.core import setup

VERSION = '0.0.1'

setup(
    name='lmdb_sessions',
    version=VERSION,
    description='An LMDB based backend for CherryPy sessions',
    url='https://github.com/tburmeister/lmdb_sessions',
    author='Taylor Burmeister',
    install_requires=['cherrypy >= 5.0.1', 'lmdb >= 0.92'],
    packages=['lmdb_sessions']
)
