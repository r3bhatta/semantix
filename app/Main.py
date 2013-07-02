import threading
import sys
import os
import jsonParser
import locationsParser 

# Set default encoding to UTF to avoid conflicts with symbols.
reload(sys)
sys.setdefaultencoding('utf-8')
WINDOWS = 'nt'

soups = jsonParser.parse()

##### LOCATIONS ###################################################################################
def locationCallBack(allSoupsAddresses):
    print 'Formatted Addresses in thread: %s' % threading.current_thread().name
    
    for singleSoupAddresses in allSoupsAddresses:
        for address in singleSoupAddresses:
            
            if os.name == WINDOWS:
                print(address.encode('cp1252'))            
            else:
                print address
    
def locationsThread(callback):
    callback(locationsParser.parseLocations(soups))

thr = threading.Thread(target=locationsThread, name="locationThread", args=(locationCallBack,)).start()

