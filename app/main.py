import os
import sys
sys.path.insert(0,os.path.dirname(os.path.dirname(__file__)))
import settings
from parsers import jsonparser as JsonParser
from parsers import contextparser as ContextParser
from naivebayesclassifier.naivebayesclassifier import NaiveBayesClassifier

WINDOWS = 'nt'
reload(sys)
sys.setdefaultencoding('utf-8') # Set default encoding to UTF to avoid conflicts with symbols.


soups = JsonParser.parseData(settings.CPK_DATA)
nbc = NaiveBayesClassifier(settings.APP_DATA_TRAINING)
contextMap = ContextParser.parseSoups( soups, nbc )

#  NOTE : contextMap may have repeats of similar texts, it needs to run through string comparison taking bests

# print contextMap

