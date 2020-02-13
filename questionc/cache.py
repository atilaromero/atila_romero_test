import time

from collections import namedtuple
from typing import Dict

CacheData = namedtuple('CacheData', ['prev', 'next', 'value', 'stamp'])

class LRUCache:
    def __init__(self, loadcb, secondstimeout):
        self.loadcb = loadcb
        self.timeout = secondstimeout
        self.cache : Dict[CacheData] = {}
        self.head = None

    def get(self, key):
        if not key in self.cache:
            return self._refresh(key)
        cacheData : CacheData = self.cache[key]
        expired = ((time.time()-cacheData.stamp) > self.timeout)
        if expired:
            self._evict(cacheData)
            return self._refresh(key)
        self._promote(cacheData)
        return cacheData.value

    def _refresh(self, key):
        value = self.loadcb(key)
        cacheData = CacheData(None, None, value, time.time())
        self._promote(cacheData)
        return value

    def _promote(self, cacheData):
        if self.head is cacheData:
            return
        if cacheData.prev != None:
            prev : CacheData = cacheData.prev
            prev.next = cacheData.next
        if cacheData.next != None:
            next_ : CacheData = cacheData.next
            next_.prev = cacheData.prev
        cacheData.stamp = time.time()
        cacheData.prev = None
        cacheData.next = self.head
        self.head = cacheData

    def _evict(self, key):
        cacheData : CacheData = self.cache[key]
        del self.cache[key]

def resolve(domain):
    return "1.2.3.4"

g = LRUCache(resolve, 1)

x = g.get("x.com")