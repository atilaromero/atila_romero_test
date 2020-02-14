import unittest
import time
from lrucache import LRUCache, CacheData

class LRUCacheTest(unittest.TestCase):
    def test_get1(self):
        count = 0
        def dummyLoadCB(key):
            nonlocal count
            count += 1
            return {"mydata": key}
        cache = LRUCache(dummyLoadCB, 0.5)
        value = cache.get(0)
        self.assertEqual(value['mydata'], 0)
        self.assertEqual(count, 1)
        self.assertEqual(len(cache._cache), 1)
        self.assertEqual(cache._head.key, 0)
        self.assertEqual(cache._cache[0].prev, None)
        self.assertEqual(cache._cache[0].next, None)

    def test_get2(self):
        count = 0
        def dummyLoadCB(key):
            nonlocal count
            count += 1
            return {"mydata": key}
        cache = LRUCache(dummyLoadCB, 0.5)
        for x in range(2):
            value = cache.get(x)
            self.assertEqual(value['mydata'], x)
        self.assertEqual(len(cache._cache), 2)
        self.assertEqual(count, 2)
        self.assertEqual(cache._head.key, 1)
        self.assertEqual(cache._cache[1].prev, None)
        self.assertEqual(cache._cache[1].next.key, 0)
        self.assertEqual(cache._cache[0].prev.key, 1)
        self.assertEqual(cache._cache[0].next, None)

    def test_evict(self):
        count = 0
        def dummyLoadCB(key):
            nonlocal count
            count += 1
            return {"mydata": key}
        cache = LRUCache(dummyLoadCB, 0.5)
        for x in range(100):
            value = cache.get(x)
            self.assertEqual(value['mydata'], x)
        self.assertEqual(len(cache._cache), 100)
        self.assertEqual(count, 100)
        for x in range(100):
            self.assertEqual(cache.get(x)['mydata'], x)
        self.assertEqual(count, 100)
        self.assertEqual(cache._head.key, 99)
        self.assertEqual(cache._head.prev, None)
        self.assertEqual(cache._cache[0].next, None)
        self.assertEqual(cache._head.key, 99)
        cache._evict(49) # evict from 49 to 0, 50-99 are newer 
        self.assertEqual(count, 100)
        self.assertEqual(cache._head.key, 99)
        self.assertEqual(cache._tail.key, 50)
        self.assertEqual(len(cache._cache), 50)
        self.assertEqual(cache._cache[50].prev.key, 51)
        self.assertEqual(cache._cache[50].next, None)
        cache._evict(cache._head.key)
        self.assertEqual(len(cache._cache), 0)
        self.assertEqual(cache._head, None)
        self.assertEqual(cache._tail, None)

    def test_promote(self):
        count = 0
        def dummyLoadCB(key):
            nonlocal count
            count += 1
            return {"mydata": key}
        cache = LRUCache(dummyLoadCB, 0.5)
        for x in range(10):
            cache.get(x)
        cache._promote(cache._cache[5])
        self.assertEqual(cache._head.key, 5)
        self.assertEqual(cache._cache[5].prev, None)
        self.assertEqual(cache._cache[5].next.key, 9)
        self.assertEqual(cache._cache[9].prev.key, 5)
        self.assertEqual(cache._cache[9].next.key, 8)
        self.assertEqual(cache._cache[8].prev.key, 9)
        self.assertEqual(cache._cache[8].next.key, 7)
        self.assertEqual(cache._cache[7].prev.key, 8)
        self.assertEqual(cache._cache[7].next.key, 6)
        self.assertEqual(cache._cache[6].prev.key, 7)
        self.assertEqual(cache._cache[6].next.key, 4)
        self.assertEqual(cache._cache[4].prev.key, 6)
        self.assertEqual(cache._cache[4].next.key, 3)
        self.assertEqual(cache._cache[0].prev.key, 1)
        self.assertEqual(cache._cache[0].next, None)
        cache._promote(cache._cache[0])
        self.assertEqual(cache._cache[0].prev, None)
        self.assertEqual(cache._cache[0].next.key, 5)
        self.assertEqual(cache._cache[1].prev.key, 2)
        self.assertEqual(cache._cache[1].next, None)
        cache._promote(cache._cache[0])
        self.assertEqual(cache._cache[0].prev, None)
        self.assertEqual(cache._cache[0].next.key, 5)
        self.assertEqual(cache._cache[5].prev.key, 0)
        self.assertEqual(cache._cache[5].next.key, 9)
        cache._promote(cache._cache[5])
        self.assertEqual(cache._cache[5].prev, None)
        self.assertEqual(cache._cache[5].next.key, 0)
        self.assertEqual(cache._cache[0].prev.key, 5)
        self.assertEqual(cache._cache[0].next.key, 9)
        self.assertEqual(cache._cache[9].prev.key, 0)
        self.assertEqual(cache._cache[9].next.key, 8)

    def test_store_promote(self):
        count = 0
        def dummyLoadCB(key):
            nonlocal count
            count += 1
            return {"mydata": key}
        cache = LRUCache(dummyLoadCB, 0.5)
        cache._store(10, 10)
        self.assertEqual(cache._head.key, 10)
        self.assertEqual(cache._cache[10].prev, None)
        self.assertEqual(cache._cache[10].next, None)
        self.assertNotEqual(cache._cache[10].stamp, 0)
        prevStamp = cache._cache[10].stamp
        cache._promote(cache._cache[10])
        self.assertEqual(cache._head.key, 10)
        self.assertEqual(cache._cache[10].prev, None)
        self.assertEqual(cache._cache[10].next, None)
        self.assertGreater(cache._cache[10].stamp, prevStamp)

    def test_shrink(self):
        def dummyLoadCB(key):
            return {"mydata": key}
        cache = LRUCache(dummyLoadCB, 0.5)
        cache._shrink(10)
        self.assertEqual(len(cache._cache), 0)
        for x in range(10):
            cache.get(x)
        self.assertEqual(len(cache._cache), 10)
        cache._shrink(2)
        self.assertEqual(len(cache._cache), 2)
        self.assertEqual(cache._tail.key, 8)
        self.assertEqual(cache._tail.next, None)
        cache._shrink(0)
        self.assertEqual(len(cache._cache), 0)
        self.assertEqual(cache._head, None)
        self.assertEqual(cache._tail, None)

    def test_sizelimit(self):
        def dummyLoadCB(key):
            return {"mydata": key}
        cache = LRUCache(dummyLoadCB, 0.5, 2)
        for x in range(10):
            cache.get(x)
        self.assertEqual(len(cache._cache), 2)
        self.assertEqual(cache._tail.key, 8)
        self.assertEqual(cache._tail.next, None)
        
    def test_timeout(self):
        count = 0
        def dummyLoadCB(key):
            nonlocal count
            count += 1
            return {"mydata": key}
        cache = LRUCache(dummyLoadCB, 0.1, 2)
        for x in range(3):
            cache.get(x)
        self.assertEqual(count, 3)
        time.sleep(0.1)
        for x in range(3):
            cache.get(x)
        self.assertEqual(count, 6)
        time.sleep(0.05)
        cache.get(1)
        time.sleep(0.05)
        cache.get(1)
        time.sleep(0.05)
        cache.get(1)
        self.assertEqual(count, 6)
        for x in range(3):
            cache.get(x)
        self.assertEqual(count, 8)
        