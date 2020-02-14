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
    def __init__(self, loadcb, secondstimeout):
        self._loadcb = loadcb
        self._timeout = secondstimeout
        self._cache : Dict[CacheData] = {}
        self._head = None
        self._tail = None

    def get(self, key):
        if not key in self._cache:
            return self._refresh(key)
        cacheData : CacheData = self._cache[key]
        expired = ((time.time()-cacheData.stamp) > self._timeout)
        if expired:
            self._evict(cacheData)
            return self._refresh(key)
        self._promote(cacheData)
        return cacheData.value

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
        while not cacheData is None:
            del self._cache[cacheData.key]
            if not cacheData.prev is None:
                cacheData.prev.next = None
            cacheData.prev = None
            next_ = cacheData.next
            cacheData.next = None
            if self._head == cacheData:
                self._head = None
            if self._tail == cacheData:
                self._tail = None
            cacheData = next_



def resolve(domain):
    return "1.2.3.4"

g = LRUCache(resolve, 1)

x = g.get("x.com")