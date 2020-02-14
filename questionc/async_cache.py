from threading import Lock, Event
from cache import LRUCache


class AsyncLRUCache:
    def __init__(self, loadcb, secondstimeout, sizelimit=None):
        self._loadcb = loadcb
        self._lruLock = Lock() # lock for inner synchronous lock _lru
        self._retrievingLock = Lock() # lock for _retrieving Events dict 
        self._retrieving = {}
        self._lru = LRUCache(None, secondstimeout, sizelimit)

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
            return cacheData.value
    
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
