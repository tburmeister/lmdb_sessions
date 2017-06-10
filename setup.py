from distutils.core import setup

VERSION = '0.0.3'

setup(
    name='lmdb_sessions',
    version=VERSION,
    description='An LMDB based backend for CherryPy sessions',
    url='https://github.com/tburmeister/lmdb_sessions',
    author='Taylor Burmeister',
    author_email='burmeister.taylor@gmail.com',
    install_requires=['cherrypy >= 5.0.1', 'lmdb >= 0.92'],
    packages=['lmdb_sessions']
)
