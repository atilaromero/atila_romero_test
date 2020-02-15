import threading
import traceback
import json
import requests
from queue import Queue, Empty
from http.server import BaseHTTPRequestHandler, HTTPServer
from .async_lrucache import AsyncLRUCache

class GeoLRUCache:
    """GeoLRUCache is a Least Recently Used cache.
    It uses the AsyncLRUCache, which supports concurrent access, as a inner cache and adds the funcionality of being able to send and receive updates.

    After initialization, use the add_peer function to set the peers that will receive updates when the cache changes.

    It starts two auxiliary threads: one for starting a http server to receive updates, and the other to send the updates according to a queue.
    """
    def __init__(self, host, port, loadcb, timeoutseconds, sizelimit=None):
        """Parameters:
        host: the address that will be used to start the server
        port: the port number of the server receiveing incoming connections
        loadcb: callback function that accepts a key and returns a value
        timeoutseconds: cache timeout in seconds
        sizelimit: cache maximum size
        """
        self.closed = False
        self._async_cache = AsyncLRUCache(loadcb, timeoutseconds, sizelimit)
        self._peers = []
        self._send_queue = Queue()
        self._send_queue_thread = threading.Thread(target=send_queue_thread, args=(self,))
        self._receive_thread = threading.Thread(target=receive_thread, args=(self, host, port))
        self._send_queue_thread.start()
        self._receive_thread.start()

    def get(self, key):
        """If the value for this key is in cache and it is not expired, return the value and update the cache timestamp for this key.
        Otherwise, get the value from loadcb.
        Then, send the new access timestamp to the list of peers.
        """
        value = self._async_cache.get(key)
        self._send_queue.put(key)
        return value

    def add_peer(self, host, port):
        """Adds a peer to the list of peers.
        """
        self._peers.append(Peer(f'http://{host}:{port}'))
    
    def close(self):
        """It sets the closed boolean to True and waits for the two auxiliary threads to finish. 
        """
        self.closed = True
        self._send_queue_thread.join()
        self._receive_thread.join()

class Peer:
    """Represents another node that will receive updates"""
    def __init__(self, endpoint):
        """endpoint is an URL, to_json is an optional function
        that converts the {"key": key, "value": value} dict to a string
        (defaults to json.dumps).
        """
        self.endpoint = endpoint
    
    def send(self, key, value):
        """Send a key value pair to another node"""
        try:
            data = json.dumps({"key": key, "value": value})
            r = requests.post(url=self.endpoint, data=data)
            r.close()
        except:
            print("couldn't update peer", self.endpoint)

def send_queue_thread(geocache: GeoLRUCache):
    """When there are updates in the send_queue, send them to the peers.
    Stops when geocache.closed == True"""
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
    """Creates a new class type that has access to a GeoLRUCache object. Many instances of this class may access the GeoLRUCache object concurrently."""
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
    """Starts the http server to receive updates"""
    Server = MakeServerClass(geocache)
    httpd = HTTPServer((host, port), Server)
    httpd.timeout = 1
    while not geocache.closed:
        httpd.handle_request()
    httpd.server_close()

