'''
try:
    from mercurial import demandimport; demandimport.enable()
except ImportError:
    import sys
    sys.stderr.write("abort: couldn't find mercurial libraries in [%s]\n" %
    				' '.join(sys.path))
    sys.stderr.write("(check your install and PYTHONPATH)\n")
    sys.exit(-1)
'''

import os
from os import listdir
import sys
import collections
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import settings
from parsers import jsonparser as JsonParser
from parsers import contextparser as ContextParser
from parsers import businesstypeparser as BusinessTypeParser
from naivebayesclassifier.naivebayesclassifier import NaiveBayesClassifier
import stringsimilarity

WINDOWS = 'nt'
reload(sys)
sys.setdefaultencoding('utf-8')     # Set default encoding to UTF to avoid conflicts with symbols.

# Parse a single business, identified by input file.
def parseBusiness(inputFile):
    soups = JsonParser.parseData(inputFile)
    nbc = NaiveBayesClassifier(os.path.join(settings.APP_DATA_TRAINING, 'general'), settings.APP_DATA_COMMON_WORDS)
    return ContextParser.parseSoups(soups, nbc)
    # NOTE: contextMap may have repeats of similar texts, it needs to run through string comparison
    # taking bests.

# Parse a single business file to identify its business type.
def parseBusinessType(inputFile):
    nbc = NaiveBayesClassifier(os.path.join(settings.APP_DATA_TRAINING, 'businesses'),settings.APP_DATA_COMMON_WORDS)
    # Our data files are .txt files for now.
    if inputFile.endswith('.txt'):
        jsonParsedTuple = JsonParser.parseData(inputFile, True)
        businessTuple = collections.namedtuple('Business', ['name', 'file', 'type'])

        businessTuple.name = jsonParsedTuple.name
        businessTuple.file = inputFile
        businessTuple.type = BusinessTypeParser.parse(inputFile, jsonParsedTuple.soups, nbc)
        return businessTuple

# Filter and prune menu items.
def pruneMenuItems(inputFile):
    business = parseBusiness(inputFile)
    filteredMenuItems = []
    for label, menuItems in business.items():
        if label.label == 'menu' and label.probability >= 0.6:
            for item in menuItems:
                if len(item.split()) <= 5:
                    filteredMenuItems.append(item)
    filteredMenuItems = list(set(filteredMenuItems))
    for item in filteredMenuItems:
        print item

#business = parseBusinessType(os.path.join(settings.APP_DATA_HTML, 'partymixnyc_com.txt'))
#print (business.file, business.type.label, business.type.probability)

#business = parseBusiness(os.path.join(settings.APP_DATA_HTML, "alexandregallery_com.txt"))
nbc = NaiveBayesClassifier(os.path.join(settings.APP_DATA_TRAINING, 'general'), settings.APP_DATA_COMMON_WORDS)
nbc.demo();
'''
for key in business:
    print "-----------------------------------------------------------------"
    print key
'''

'''
results = []
for businessFile in listdir(settings.APP_DATA_HTML):
    business = parseBusinessType(os.path.join(settings.APP_DATA_HTML, businessFile))
    
    if business:
        print (business.file, business.type.label, business.type.probability)
        results.append((business.file, business.type.label, business.type.probability))


print "______________________________________________________________________"
print results


pruneMenuItems(os.path.join(settings.APP_DATA_HTML, 'cpk_com.txt'))
print stringsimilarity.compute('word is one', 'word is two')

results = []
for businessFile in listdir(settings.APP_DATA_HTML):
    business = parseBusinessType(os.path.join(settings.APP_DATA_HTML, businessFile))
    print (business.file, business.type.label, business.type.probability)
    if business:
        results.append((business.file, business.type.label, business.type.probability))
'''
