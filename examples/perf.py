import time
import os

from cherrypy.lib.sessions import FileSession
from lmdb_sessions.sessions import LmdbSession

if __name__ == '__main__':
    path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(path, '..', 'sessions')

    FileSession.setup(storage_path=path, clean_freq=0)
    fileSession = FileSession(storage_path=path)

    LmdbSession.setup(storage_path=path, clean_freq=0)
    lmdbSession = LmdbSession()

    fileSession.acquire_lock()
    start = time.time()
    for i in range(10000):
        fileSession.load()

    fileSession.release_lock()
    end = time.time()
    print('File load: {} seconds'.format(end - start))

    lmdbSession.acquire_lock()
    start = time.time()
    for i in range(10000):
        lmdbSession.load()

    lmdbSession.release_lock()
    end = time.time()
    print('LMDB load: {} seconds'.format(end - start))

    start = time.time()
    for i in range(10000):
        fileSession.acquire_lock()
        fileSession.save()
        fileSession.release_lock()

    end = time.time()
    print('File save: {} seconds'.format(end - start))

    start = time.time()
    for i in range(10000):
        lmdbSession.acquire_lock()
        lmdbSession.save()
        lmdbSession.release_lock()

    end = time.time()
    print('LMDB save: {} seconds'.format(end - start))
