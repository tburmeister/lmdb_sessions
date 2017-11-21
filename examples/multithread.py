import os

from lmdb_sessions.sessions import LmdbSession
from threading import Thread


def worker(num):
    print('Worker {} starting'.format(num))
    lmdb_session = LmdbSession()

    for i in range(10000):
        lmdb_session.acquire_lock()
        lmdb_session.load()
        lmdb_session.save()
        lmdb_session.release_lock()

    print('Worker {} done'.format(num))


if __name__ == '__main__':
    path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(path, '..', 'sessions')
    LmdbSession.setup(storage_path=path, clean_freq=0)

    threads = []
    for i in range(5):
        t = Thread(target=worker, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
