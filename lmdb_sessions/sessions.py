import cherrypy
import lmdb
import os
import pickle
import struct

from cherrypy.lib.sessions import Session


class LmdbSession(Session):
    """
    Implementation of an LMDB based backend for CherryPy sessions

    storage_path
        The folder where the LMDB database will be stored.
    """

    pickle_protocol = pickle.HIGHEST_PROTOCOL

    @classmethod
    def setup(cls, **kwargs):
        kwargs['storage_path'] = os.path.abspath(kwargs['storage_path'])
        cls.env = lmdb.open(kwargs['storage_path'])

        for k, v in kwargs.items():
            setattr(cls, k, v)

    def _exists(self):
        with self.env.begin() as txn:
            return txn.get(self.id.encode()) is not None

    def _load(self):
        with self.env.begin() as txn:
            data = txn.get(self.id.encode())

        if data is not None:
            return pickle.loads(data[4:])

    def _save(self, expiration_time):
        encoded_exp = struct.pack('I', int(expiration_time.timestamp()))
        data = pickle.dumps((self._data, expiration_time),
                            protocol=self.pickle_protocol)

        with self.env.begin(write=True) as txn:
            txn.put(self.id.encode(), encoded_exp + data)

    def _delete(self):
        with self.env.begin(write=True) as txn:
            txn.delete(self.id.encode())

    def acquire_lock(self):
        self.locked = True

    def release_lock(self):
        self.locked = False

    def clean_up(self):
        """
        Clean up expired sessions.

        We prefix the stored LMDB data with 4 bytes denoting the expiration
        time; on clean-up we iterate over all entries and use the prefix to
        delete expired ones.
        """
        now = struct.pack('I', int(self.now().timestamp()))

        with self.env.begin(write=True) as txn:
            cursor = txn.cursor()

            for key, value in cursor:
                if value[:4] <= now:
                    if self.debug:
                        cherrypy.log("Deleting session {}".format(key.decode()))
                    txn.delete(key)

    def __len__(self):
        """
        Return the number of active sessions.
        """
        with self.env.begin() as txn:
            return txn.stat()['entries']
