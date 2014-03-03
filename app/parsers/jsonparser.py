from bs4 import BeautifulSoup
import quopri
import json
import re
import os, errno
import os.path
import collections
import crawler

def populateSoupData(soups, data, businessName):
    for line in data:
        loadedJson = json.loads(line)
        seqVal = loadedJson["sequence_number"]  
        body = loadedJson["body"]
        
        #decodedQP = quopri.decodestring(body)
        #soup = BeautifulSoup(decodedQP)

        soup = BeautifulSoup(body)
        
        # Used to have this, but maybe don't need it?
        #decodedQP = quopri.decodestring(body)
        #soup = BeautifulSoup(decodedQP)

        # get the title of the page from the body of the root page
        if seqVal == 0:
            businessName = str(soup.title).replace("<title>","").replace("</title>","")
        soups.append(soup)


def convertFileNameToUrl(filename):
    url = filename.encode('ascii', 'ignore')
    url = re.sub('_', '.', url)
    url = "http://" + url
    return url

# Input         - An input file that corresponds to a website
#               - for example cpk_com.txt
# Description   - Take in the input file and either get the cached version of the file or use the crawler and get its data
# Output        - A business type tuple that 
# Load the line and the value "body".
# Use the quopri module to decode the qp encoded value of each page.
def parseData(inputFilePath, fileName):
    soups = []
    businessName = ""
    business = collections.namedtuple("Business", ["soups", "name"])

    # If the file does not exist make it
    if os.path.isfile(inputFilePath) != True:
        print "Using the crawler @@@@@@@@@@@@@@@@@@@@@@@@@@@@"
        url = convertFileNameToUrl(fileName)
        jsonData = crawler.pullJsonEncodedHtml(url)
        with open(inputFilePath, 'w') as f:
            f.write(jsonData)
    
    # If the file does exist open it    
    with open(inputFilePath) as data:
        print "Not using the crawler ##############################"
        populateSoupData(soups, data, businessName)

    if businessName is None:
        businessName = "Not Found!"

    return business(soups, businessName)