# Question C: GeoLRUCache
A Geo Distributed LRU (Least Recently Used) cache with time expiration

## How to run the sample program
It is an example application that uses the GeoLRUCache library

Using two shell prompts:

1.  On the first prompt:
    ```
    cd questionc/
    python3 main.py 8000 8001 10 20
    ```
    Arguments:
    1. 8000: port where the program listen for updates
    2. 8001: port of the peer, where to send updates to.
    3. 10: cache timeout in seconds
    4. 20: max size of the cache

    Type a number, press enter, repeat.

2. On the second prompt (mind the inverted port numbers)
    ```
    cd questionc/
    python3 main.py 8001 8000 10 20
    ```
    Type a number, press enter, repeat.

For each line read from stdin, the program will calculate its square, or retrieve it from cache. It expects one number per line.

It will also update the cache of the remote peer.

If the value is taken from cache, it will not print the message 'calculating square of ...'

## Using it as a library
In a shell prompt:
```
cd questionc/
python3 setup.py install --user
```

Then you can import the package in your programs like this:
```
#!/usr/bin/env python3
import time
from atila_romero_geolrucache import GeoLRUCache

def mycallback(x): 
    print('calling callback') 
    time.sleep(1) 
    return x * x 

cache = GeoLRUCache('localhost', 8000, mycallback, 10, 20)
cache.get(2) # prints 'calling callback'
cache.get(2) # does not print 'calling callback'
cache.add_peer('localhost', 8001)
# if you wish, open another terminal and start a peer using port 8001
cache.get(3)
# if the peer is up, it should receive the 3 9 key-value pair
```

## How it works
The design was divided into three parts:
- LRUCache

    It does not provide safety guards for concurrent
    access, so it only should be used in single thread programs.

- AsyncLRUCache

    It adds safety guards for concurrent access, using LRUCache as an internal cache. It uses locks to prevent race conditions.

- GeoLRUCache

    It uses the AsyncLRUCache as a inner cache and adds the funcionality of being able to send and receive updates.

    After initialization, use the add_peer function to set the peers that will receive updates when the cache changes.

    It starts two auxiliary threads: one for starting a http server to receive updates, and the other to send the updates according to a queue.


## Limitations
This solution works better for values that can be serialized in a small number of bytes because the key and the value are part of the update message. For values that put too much pressure on the network, an alternate solution should be used, for example sending only the key, and waiting for the peer to ask for the value if needed.

Another limitation that becomes important with big messages or with too many nodes is the need for a relay mechanism or a peer-to-peer solution that avoids direct communication between distant nodes if the message can be replicated by a nearer one.
