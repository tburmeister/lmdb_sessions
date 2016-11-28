import time

from cherrypy.lib.sessions import FileSession
from lmdb_sessions.sessions import LmdbSession

if __name__ == '__main__':
    FileSession.setup(storage_path='examples/sessions/file', clean_freq=0)
    fileSession = FileSession(storage_path='examples/sessions/file')

    LmdbSession.setup(storage_path='examples/sessions/lmdb', clean_freq=0)
    lmdbSession = LmdbSession(storage_path='examples/sessions/lmdb')

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
