# LmdbSessions: An LMDB Based Backend for CherryPy Sessions

LmdbSessions is an almost drag-and-drop substitute for CherryPy's built-in file
backed sessions, but with much better performance, e.g. 6x faster reads and 3x
faster writes.

## Installation

Installation should be as easy as:

```
$ pip install lmdb_sessions
```

To install from source:

```
$ cd /path/to/lmdb_sessions && pip install . --upgrade
```

## Usage

The script `server.py` in the `examples` directory demonstrates how to setup
LmdbSessions on a CherryPy server and use it to show a user how many times
they have visited the site.

To use, you first need to import the `LmdbSession` class:

```
from lmdb_sessions.sessions import LmdbSession
```

Then you have to configure your server to use `LmdbSession` based sessions:

```
cherrypy.config.update({
	'tools.sessions.on': True,
	'tools.sessions.storage_class': LmdbSession,
	'tools.sessions.storage_path': '/path/to/sessions/directory')
})
```

After that, usage should be exactly the same as any other CherryPy sessions
backend, i.e. totally transparent.

## Performance

You can compare the performance of LmdbSessions vs. CherryPy's built-in file
based sessions yourself by running `examples/perf.py`. On my MacBook Pro,
LmdbSessions performs reads roughly 6x faster and writes roughly 3x faster.

## Backend Size

By Default, the LMDB session backend has a maximum size of 10MB; if you
exceed this limit, new sessions will raise exceptions. You can increase
the size limit of the backing store by adding the following config option:

```
cherrypy.config.update({
    'tools.sessions.map_size': map_size
})
```

Where `map_size` is the maximum size in bytes.
