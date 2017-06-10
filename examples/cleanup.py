import datetime
import cherrypy
import os

cherrypy.log = print

from lmdb_sessions.sessions import LmdbSession


if __name__ == '__main__':
    path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(path, '..', 'sessions')
    LmdbSession.setup(storage_path=path, debug=True)

    lmdbSession = None
    for i in range(10):
        lmdbSession = LmdbSession()
        lmdbSession._save(datetime.datetime.now())

    lmdbSession.clean_up()
