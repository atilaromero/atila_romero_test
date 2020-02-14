import unittest
from geo_lrucache import GeoLRUCache

class GeoLRUCacheTest(unittest.TestCase):
    def test_simple(self):
        def t1():
            cache1 = GeoLRUCache('localhost', 8000, )