import cherrypy
import os

from lmdb_sessions.sessions import LmdbSession


class Server(object):

    @cherrypy.expose()
    def index(self):
        count = cherrypy.session.get('count', 0) + 1
        cherrypy.session['count'] = count
        return "You have visited {} times".format(count)


if __name__ == '__main__':
    path = os.path.abspath(os.path.dirname(__file__))

    cherrypy.config.update({
        'server.socket_host': '0.0.0.0',
        'server.socket_port': 8081,
        'tools.sessions.on': True,
        'tools.sessions.storage_class': LmdbSession,
        'tools.sessions.storage_path': os.path.join(path, '..', 'sessions')
    })

    cherrypy.tree.mount(Server(), '/')
    cherrypy.engine.start()
    cherrypy.engine.block()
