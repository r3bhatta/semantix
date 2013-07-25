from bs4 import BeautifulSoup
import quopri
import json
import os, errno
import collections

# Input         - 
# Description   - 
# Output        - 
# Load the line and the value "body".
 # Use the quopri module to decode the qp encoded value of each page.
def parseData(inputFile):
    soups = []
    businessName = ""
    business = collections.namedtuple("Business", ["soups", "name"])
    with open(inputFile) as data:
        for line in data:
            seqVal = json.loads(line)["sequence_number"]            
            body = json.loads(line)["body"]
            decodedQP = quopri.decodestring(body)
            soup = BeautifulSoup(decodedQP)

            if seqVal == 0:
                businessName = str(soup.title).replace("<title>","").replace("</title>","")

            soups.append(soup)

    if businessName is None:
        businessName = "Not Found!"

    return business(soups, businessName)
        
