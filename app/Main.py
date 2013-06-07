import threading
import sys

import jsonParser
import locationsParser

# Set default encoding to UTF to avoid conflicts with symbols.
reload(sys)
sys.setdefaultencoding('utf-8')

soups = jsonParser.parse()

##### LOCATIONS ###################################################################
def locationCBFunc(formattedAddresses):
    print 'Formatted Addresses in thread: %s' % threading.current_thread().name
    print formattedAddresses

def locationsThread(callback):
    callback(locationsParser.parseLocations(soups))

thr = threading.Thread(target=locationsThread, name="locationThread", args=(locationCBFunc,)).start()