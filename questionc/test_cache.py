import unittest
from cache import LRUCache


class QuestionC(unittest.TestCase):
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
        cache._evict(49) # evict from 49 to 0, 50-99 are newer 
        self.assertEqual(count, 100)
        self.assertEqual(len(cache._cache), 50)



