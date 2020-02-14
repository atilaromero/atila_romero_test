import unittest
import threading
import time
from geo_lrucache import GeoLRUCache

class GeoLRUCacheTest(unittest.TestCase):
    def test_simple(self):
        count = 0
        def dummycb(key):
            nonlocal count
            count += 1
            return key
        cache1 = GeoLRUCache('localhost', 8001, dummycb, 1, 3)
        cache1.get(10)
        cache1.close()
        self.assertEqual(len(cache1._async_cache._lru._cache), 1)

    def test_two(self):
        count = 0
        def dummycb(key):
            nonlocal count
            count += 1
            return key
        cache1 = GeoLRUCache('localhost', 8001, dummycb, 1, 3)
        cache2 = GeoLRUCache('localhost', 8002, dummycb, 1, 3)
        cache1.get(10)
        self.assertEqual(len(cache1._async_cache._lru._cache), 1)
        def t1f(cache2):
            cache2.add_peer('localhost', 8001)
            cache2.get(10)
            cache2.get(20)
            while not cache2._send_queue.empty():
                time.sleep(0.1)
        t1 = threading.Thread(target=t1f, args=(cache2,))
        t1.start()
        t1.join()
        cache2.close()
        cache1.close()
        self.assertEqual(len(cache1._async_cache._lru._cache), 2)

    def test_send_receive(self):
        count = 0
        def dummycb(key):
            nonlocal count
            count += 1
            return key
        cache1 = GeoLRUCache('localhost', 8001, dummycb, 10, 10)
        cache2 = GeoLRUCache('localhost', 8002, dummycb, 10, 10)
        cache1.add_peer('localhost', 8002)
        cache2.add_peer('localhost', 8001)
        self.assertEqual(len(cache1._async_cache._lru._cache), 0)
        self.assertEqual(len(cache1._async_cache._lru._cache), 0)
        def t1f(cache2):
            for x in range(10):
                cache2.get(x)
            while not cache2._send_queue.empty():
                time.sleep(0.1)
        t1 = threading.Thread(target=t1f, args=(cache1,))
        t1.start()
        t1.join()
        cache2.close()
        cache1.close()
        self.assertEqual(len(cache1._async_cache._lru._cache), 10)

    def test_mutual(self):
        count = 0
        def dummycb(key):
            nonlocal count
            count += 1
            return key
        cache1 = GeoLRUCache('localhost', 8001, dummycb, 10, 100)
        cache2 = GeoLRUCache('localhost', 8002, dummycb, 10, 100)
        cache1.add_peer('localhost', 8002)
        cache2.add_peer('localhost', 8001)
        self.assertEqual(len(cache1._async_cache._lru._cache), 0)
        self.assertEqual(len(cache1._async_cache._lru._cache), 0)

        for x in range(10):
            cache1.get(x)
        while not cache1._send_queue.empty():
            time.sleep(0.1)
        self.assertEqual(len(cache1._async_cache._lru._cache), 10)
        self.assertEqual(len(cache2._async_cache._lru._cache), 10)
        self.assertEqual(count, 10)

        for x in range(20):
            cache2.get(x)
        while not cache2._send_queue.empty():
            time.sleep(0.1)
        self.assertEqual(len(cache1._async_cache._lru._cache), 20)
        self.assertEqual(len(cache2._async_cache._lru._cache), 20)
        self.assertEqual(count, 20)

        for x in range(30):
            cache1.get(x)
        while not cache1._send_queue.empty():
            time.sleep(0.1)
        self.assertEqual(len(cache1._async_cache._lru._cache), 30)
        self.assertEqual(len(cache2._async_cache._lru._cache), 30)
        self.assertEqual(count, 30)

        cache2.close()
        cache1.close()
        self.assertEqual(len(cache1._async_cache._lru._cache), 30)
        self.assertEqual(len(cache2._async_cache._lru._cache), 30)
