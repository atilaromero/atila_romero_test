from atila_romero_geolrucache import GeoLRUCache
import sys

def loadcb(key):
    print('calculating square of', key)
    return key**2

def main(myport, peerport, timeoutseconds, cachesize=None):
    """
    For each line read from stdin, the program will calculate its square, or retrieve it from cache. It expects one number per line.
    It will also update the cache of a remote peer.
    If the value is taken from cache, it will not print the message 'calculating square of ...'
    """
    myport = int(myport)
    peerport = int(peerport)
    timeoutseconds = int(timeoutseconds)
    cache = GeoLRUCache('localhost', myport, loadcb, timeoutseconds, cachesize)
    cache.add_peer('localhost', peerport)
    try:
        for line in sys.stdin:
            line = line.strip()
            if line == "":
                continue
            try:
                key = float(line)
                value = cache.get(key)
                print(value)
            except:
                print('invalid number')
    except KeyboardInterrupt:
        cache.close()
    except:
        cache.close()
        raise
if __name__ == "__main__":
    try:
        myport, peerport, timeoutseconds, cachesize = [float(x) for x in sys.argv[1:]]
    except ValueError:
        print("This program requires 4 numbers as arguments:")
        print("myport, peerport, timeoutseconds, cachesize")
        print(main.__doc__)
        sys.exit(1)
    main(myport, peerport, timeoutseconds, cachesize)