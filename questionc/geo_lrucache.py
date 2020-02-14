import threading
import traceback
import json
import requests
from queue import Queue, Empty
from http.server import BaseHTTPRequestHandler, HTTPServer
from async_lrucache import AsyncLRUCache

class GeoLRUCache:
    def __init__(self, host, port, loadcb, timeoutseconds, sizelimit=None):
        self.closed = False
        self._async_cache = AsyncLRUCache(loadcb, timeoutseconds, sizelimit)
        self._peers = []
        self._send_queue = Queue()
        self._send_queue_thread = threading.Thread(target=send_queue_thread, args=(self,))
        self._receive_thread = threading.Thread(target=receive_thread, args=(self, host, port))
        self._send_queue_thread.start()
        self._receive_thread.start()

    def get(self, key):
        value = self._async_cache.get(key)
        self._send_queue.put(key)
        return value

    def add_peer(self, host, port):
        self._peers.append(Peer(f'http://{host}:{port}'))
    
    def close(self):
        self.closed = True
        self._send_queue_thread.join()
        self._receive_thread.join()

class Peer:
    def __init__(self, endpoint):
        """endpoint is an URL, to_json is an optional function
        that converts the {"key": key, "value": value} dict to a string
        (defaults to json.dumps).
        """
        self.endpoint = endpoint
    
    def send(self, key, value):
        try:
            data = json.dumps({"key": key, "value": value})
            r = requests.post(url=self.endpoint, data=data)
            r.close()
        except:
            print("couldn't update peer", self.endpoint)

def send_queue_thread(geocache: GeoLRUCache):
    while not geocache.closed:
        try:
            key = geocache._send_queue.get(timeout=1)
        except Empty:
            continue
        ok, value = geocache._async_cache.consult(key)
        if not ok:
            continue
        for peer in geocache._peers:
            peer.send(key, value)

def MakeServerClass(geocache: GeoLRUCache):
    class Server(BaseHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super(Server, self).__init__(*args, **kwargs)
        def log_message(self, format, *args):
            pass
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
    httpd.timeout = 1
    while not geocache.closed:
        httpd.handle_request()
    httpd.server_close()
