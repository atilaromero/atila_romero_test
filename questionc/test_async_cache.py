import unittest
import threading
import time
from async_cache import AsyncLRUCache

class AsyncLRUCacheTest(unittest.TestCase):
    def test_multiple_gets(self):
        count = 0
        def dummycb(key):
            nonlocal count
            count +=1
            time.sleep(0.1)
            return key
        cache = AsyncLRUCache(dummycb, 0.5, 3)
        cache.get(0)
        cache.get(0)
        cache.get(0)
        value = cache.get(0)
        self.assertEqual(count, 1)
        self.assertEqual(value, 0)

    def test_multiple_retrieves_different_keys(self):
        count = 0
        def dummycb(key):
            nonlocal count
            count +=1
            time.sleep(0.1)
            return key
        cache = AsyncLRUCache(dummycb, 0.5, 3)
        def th(cache: AsyncLRUCache, key):
            cache.get(key)
        t = {}
        for x in [1,2,3]:
            t[x] = threading.Thread(target=th, args=(cache, x))
            t[x].start()
        time.sleep(0.15)
        self.assertEqual(len(cache._lru._cache), 3)
        self.assertEqual(count, 3)

    def test_multiple_retrieves_same_keys(self):
        count = 0
        def dummycb(key):
            nonlocal count
            count +=1
            time.sleep(0.1)
            return key
        cache = AsyncLRUCache(dummycb, 0.5, 3)
        def th(cache: AsyncLRUCache, key):
            cache.get(key)
        t = {}
        for x in range(50):
            t[x] = threading.Thread(target=th, args=(cache, 1000000))
            t[x].start()
        time.sleep(0.15)
        for x in range(50):
            t[x] = threading.Thread(target=th, args=(cache, 1000000))
            t[x].start()
        self.assertEqual(len(cache._lru._cache), 1)
        self.assertEqual(count, 1)
        