import threading
import sys
import os
import jsonParser
import MenuParser
import LocationsParser
import json

WINDOWS = 'nt'

# Set default encoding to UTF to avoid conflicts with symbols.
reload(sys)
sys.setdefaultencoding('utf-8')

soups = jsonParser.parse()

##### LOCATIONS #####
def locationCallback(allSoupsAddresses):
    print 'Formatted addresses in thread: %s' % threading.current_thread().name
    
    for address in allSoupsAddresses:
        if os.name == WINDOWS:
            print(address.encode('cp1252'))            
        else:
            print address
    
def locationsThread(callback):
    callback(LocationsParser.parse(soups))

def locations():
    return json.dumps(LocationsParser.parse(soups))

##### Menu #####
def menuCallback(formattedAddresses):  
    print 'Menu items in thread: %s' % threading.current_thread().name

def menuThread(callback):
	callback(MenuParser.parse(soups))

def menu():
    return json.dumps(MenuParser.parse(soups))
    
##### Threads #####################################################################
threading.Thread(target=locationsThread, name="Location Thread", args=(locationCallback,)).start()
threading.Thread(target=menuThread, name="Menu Thread", args=(menuCallback,)).start()
