import time

from collections import namedtuple
from typing import Dict

class CacheData:
    def __init__(self, prev, next_, key, value, stamp):
        self.prev = prev
        self.next = next_
        self.key = key
        self.value = value
        self.stamp = stamp

class LRUCache:
    def __init__(self, loadcb, timeoutseconds, sizelimit=None):
        self._loadcb = loadcb
        self.timeout = timeoutseconds
        self.sizelimit = sizelimit
        self._cache : Dict[CacheData] = {}
        self._head = None
        self._tail = None

    def get(self, key):
        if not self.has(key):
            return self._refresh(key)
        cacheData : CacheData = self._cache[key]
        self._promote(cacheData)
        return cacheData.value

    def has(self, key):
        if not key in self._cache:
            return False
        cacheData : CacheData = self._cache[key]
        expired = ((time.time()-cacheData.stamp) > self.timeout)
        if expired:
            self._evict(cacheData)
            return False
        return True

    def _refresh(self, key):
        """Refresh (or retrieve for the first time) cached value for corresponding key using the loadcb.
        """
        value = self._loadcb(key)
        self._store(key, value)
        return value
    
    def _store(self, key, value):
        """Update the key in cache with the given value"""
        cacheData = CacheData(None, None, key, value, time.time())
        self._cache[key] = cacheData
        self._promote(cacheData)
        if not self.sizelimit is None:
            self._shrink(self.sizelimit)

    def _promote(self, cacheData : CacheData):
        """Move cacheData to the top"""
        if self._head is cacheData:
            cacheData.stamp = time.time()
            return
        if cacheData.prev != None:
            prev = cacheData.prev
            prev.next = cacheData.next
        if cacheData.next != None:
            next_ : CacheData = cacheData.next
            next_.prev = cacheData.prev
        if self._tail == cacheData:
            self._tail = cacheData.prev
        if self._tail is None:
            self._tail = cacheData
        cacheData.stamp = time.time()
        cacheData.prev = None
        cacheData.next = self._head
        if cacheData.next != None:
            cacheData.next.prev = cacheData
        self._head = cacheData

    def _evict(self, key):
        """Remove cache[key] and all its descendants from cache.
            Deleting the circular references makes things easier for the GIL
        """
        cacheData : CacheData = self._cache[key]
        if self._head == cacheData:
            self._head = None
        self._tail = cacheData.prev
        while not cacheData is None:
            del self._cache[cacheData.key]
            if not cacheData.prev is None:
                cacheData.prev.next = None
            cacheData.prev = None
            next_ = cacheData.next
            cacheData.next = None
            cacheData = next_

    def _shrink(self, size):
        """shrink the oldest items in cache until it has the specified size
        """
        while len(self._cache) > size:
            self._evict(self._tail.key)
