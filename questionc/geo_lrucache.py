import threading
import traceback
import json
import requests
from queue import Queue
from http.server import BaseHTTPRequestHandler, HTTPServer
from async_lrucache import AsyncLRUCache

class GeoLRUCache:
    def __init__(self, host, port, loadcb, timeoutseconds, sizelimit=None):
        self._async_cache = AsyncLRUCache(loadcb, timeoutseconds, sizelimit)
        self._send_queue = Queue()
        self._send_queue_thread = threading.Thread(target=send_queue_thread, args=(self,))
        self.peers = []
        self._receive_thread = threading.Thread(target=receive_thread, args=(self, host, port))
        self._send_queue_thread.start()
        self._receive_thread.start()

    def get(self, key):
        value = self._async_cache.get(key)
        self._send_queue.put(key)
        return value

class Peer:
    def __init__(self, endpoint):
        """endpoint is an URL, to_json is an optional function
        that converts the {"key": key, "value": value} dict to a string
        (defaults to json.dumps).
        """
        self.endpoint = endpoint
    
    def send(self, key, value):
        data = json.dumps({"key": key, "value": value})
        r = requests.post(url=self.endpoint, data=data)
        r.close()

def send_queue_thread(geocache: GeoLRUCache):
    while not geocache._send_queue is None:
        key = geocache._send_queue.get()
        ok, value = geocache._async_cache.consult(key)
        if not ok:
            continue
        for peer in geocache.peers:
            peer.send(key, value)

def MakeServerClass(geocache: GeoLRUCache):
    class Server(BaseHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super(Server, self).__init__(*args, **kwargs)
        def geocache(self):
            return geocache
        def do_POST(self):
            try:
                length = int(self.headers.get('content-length'))
                data = self.rfile.read(length)
                data = json.loads(data)
                key = data["key"]
                value = data["value"]
                self.geocache()._async_cache.inject(key, value)
                self.send_response(204)
            except:
                print(traceback.format_exc())
                self.send_response(504)
            self.end_headers()
    return Server
    
def receive_thread(geocache: GeoLRUCache, host: str, port: int):
    Server = MakeServerClass(geocache)
    httpd = HTTPServer((host, port), Server)
    httpd.serve_forever()
