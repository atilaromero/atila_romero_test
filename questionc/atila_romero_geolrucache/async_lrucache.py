from threading import Lock, Event
from queue import Queue
from .lrucache import LRUCache


class AsyncLRUCache:
    """AsyncLRUCache is a Least Recently Used cache.
    It adds safety guards for concurrent access, using LRUCache as an internal cache. It uses locks to prevent race conditions.
    """
    def __init__(self, loadcb, timeoutseconds, sizelimit=None):
        """Parameters:
        loadcb: callback function that accepts a key and returns a value
        timeoutseconds: cache timeout in seconds
        sizelimit: cache maximum size
        """
        self._loadcb = loadcb
        self._lruLock = Lock() # lock for inner synchronous lock _lru
        self._retrievingLock = Lock() # lock for _retrieving Events dict 
        self._retrieving = {}
        self._lru = LRUCache(None, timeoutseconds, sizelimit)

    def get(self, key):
        """get replicates the behaviour of LRUCache.get, but adding locks.
        In case of a cache miss, _retrieve will be called and it will call loadcb.
        Since the loadcb callback may block, it is kept outside the lock.
        """
        if not self._lru.has(key):
            self._retrieve(key)
        with self._lruLock:
            cacheData = self._lru._cache[key]
            self._lru._promote(cacheData)
            value = cacheData.value
        return value

    def consult(self, key):
        """Does not update anything. return (bool, value), where bool indicates if the key is in the cache"""
        with self._lruLock:
            if not self._lru.has(key):
                return (False, None)
            cacheData = self._lru._cache[key]
            value = cacheData.value
            return (True, value)
    
    def inject(self, key, value):
        """Inject just adds the key value pair to the inner cache, setting the locks first. If a retrieve operation is already going on, it will reupdate the value, as we have no way to cancel the loadcb callback"""
        with self._lruLock:
            with self._retrievingLock:
                self._lru._store(key, value)

    def _retrieve(self, key):
        """Retrieve value for key using the _loadcb callback.
        It uses events to avoid duplicate calls to _loadcb.
        It doesn't return anything, at the end, value should be in cache.
        The inner cache is only blocked when we have the value.
        """
        ev = None
        with self._retrievingLock:
            if key in self._retrieving: #someone else is retrieving
                ev : Event = self._retrieving[key]
            else: # we are the first
                self._retrieving[key] = Event()
        if not ev is None: #someone else is retrieving
            ev.wait()
            return
        # we are the first
        value = self._loadcb(key)
        with self._lruLock:
            with self._retrievingLock:
                self._lru._store(key, value)
                self._retrieving[key].set()
                del self._retrieving[key]
        return
