import lmdb
import os
import pickle

from cherrypy.lib.sessions import Session


class LmdbSession(Session):
    """
    Implementation of an LMDB based backend for CherryPy sessions

    storage_path
        The folder where the LMDB database will be stored.
    """

    pickle_protocol = pickle.HIGHEST_PROTOCOL

    def __init__(self, id=None, **kwargs):
        kwargs['storage_path'] = os.path.abspath(kwargs['storage_path'])

        self.env = lmdb.open(kwargs['storage_path'], max_dbs=2)
        self.exp_db = self.env.open_db('expiration'.encode(), dupsort=True)

        Session.__init__(self, id=id, **kwargs)

    def __del__(self):
        self.env.close()

    @classmethod
    def setup(cls, **kwargs):
        kwargs['storage_path'] = os.path.abspath(kwargs['storage_path'])

        for k, v in kwargs.items():
            setattr(cls, k, v)

    def _exists(self):
        with self.env.begin() as txn:
            return txn.get(self.id.encode()) is not None

    def _load(self):
        with self.env.begin() as txn:
            data = txn.get(self.id.encode())

        if data is not None:
            return pickle.loads(data)

    def _save(self, expiration_time):
        encoded_id = self.id.encode()

        with self.env.begin(write=True) as txn:
            data = pickle.dumps((self._data, expiration_time),
                                protocol=self.pickle_protocol)

            if txn.put(encoded_id, data, overwrite=False):
                # new entry; add to expiration database
                exp = expiration_time.timestamp()
                bucket = exp - (exp % 60)
                txn.put(str(bucket).encode(), encoded_id, db=self.exp_db)
            else:
                # existing entry; overwrite without adding to expiration db
                txn.put(encoded_id, data, overwrite=True)

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

        On creation, we store each session id in an LMDB entry keyed on the 60
        minute bucket of the expiration time. On clean-up, we retrieve these
        entries and iterate over the stored session ids.
        """
        now = self.now().timestamp()
        bucket = now - (now % 60)
        key = str(bucket).encode()

        with self.env.begin(write=True) as txn:
            cursor = txn.cursor(self.exp_db)
            data = cursor.get(key)

            if data is None:
                return

            for key, value in cursor:
                txn.delete(value)

    def __len__(self):
        """
        Return the number of active sessions.
        """
        with self.env.begin() as txn:
            return txn.stat()['entries']
