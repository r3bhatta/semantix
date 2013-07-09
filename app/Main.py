import sys
from parsers import JsonParser
from parsers import ContextParser

WINDOWS = 'nt'

# Set default encoding to UTF to avoid conflicts with symbols.
reload(sys)
sys.setdefaultencoding('utf-8')

soups = JsonParser.parse()

contextMap = ContextParser.parse(soups)

print contextMap