import datetime
import cherrypy

cherrypy.log = print

from lmdb_sessions.sessions import LmdbSession


if __name__ == '__main__':
    LmdbSession.setup(storage_path='examples/sessions/lmdb', debug=True)

    lmdbSession = None
    for i in range(10):
        lmdbSession = LmdbSession(storage_path='examples/sessions/lmdb')
        lmdbSession._save(datetime.datetime.now())

    lmdbSession.clean_up()
