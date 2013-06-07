from bs4 import BeautifulSoup
from address import AddressParser, Address
import jsonParser
import re
import quopri
import json
import os, errno
import requests

addresses = []

def unique_list(l):
    ulist = []
    [ulist.append(x) for x in l if x not in ulist]
    return ulist

def locationCheck(tag):
    for key in dict(tag.attrs):
        if key.find('location') != -1:
            return True
        if type(tag[key]) is unicode:
            if str(tag[key]).find('location') != -1:
                return True
        else:
            if any('location' in s for s in tag[key]):
                return True
    return False

def parseSingleSoup(soup):
    title = soup.title

    if title is not None and 'location' in str(title):
        r = re.compile(r'location', re.IGNORECASE)          
        locationTags = soup.find_all(locationCheck)

        if locationTags:
            addressParser = AddressParser()
              
            for locationTag in locationTags:
                if str(locationTag.name) != 'script':
                    locationSoup = BeautifulSoup(str(locationTag))
                    # Extract the text value from all the tags.
                    allText = locationSoup.find_all(text = True)
                    index = 0
                    for text in allText:
                        'Remove script tags if they got through'
                        removeScriptTagsPattern = re.compile(r"[{}\[\]]")

                        if re.search(removeScriptTagsPattern, text) is None:
                            cleanText = text
                            
                            address = None
                            try:
                                parsedAdress = addressParser.parse_address(cleanText).full_address()
                                'If the address parser did not break this code, it means that it passed the parsing'
                                'Retain the old string, as the address parser parses it funny, but we use its validation'
                                index += 1
                                siblingIndex = index + 1
                                maxSiblingSearchDepth = 4
                                siblingSearchDepth = 0

                                while (siblingSearchDepth < maxSiblingSearchDepth):
                                    siblingText = str(allText[siblingIndex])

                                    if re.sub(r'\s+', '', siblingText) != re.sub(r'\s+', '', cleanText):
                                        cleanText += " " + siblingText
                                    # Found 3 > numbers in a row, hopefully it's a postal code.
                                    if len(re.findall(r"\D(\d[0-9]{3,})\D", ' ' + siblingText + ' ')) > 0:
                                        break;

                                    siblingIndex += 1
                                    siblingSearchDepth += 1

                                if cleanText not in addresses:

                                    'Remove duplicate and make all white spaces look nice'
                                    cleanText = ' '.join(unique_list(cleanText.split(" ")))
                                    cleanText = re.sub(r'\s+', ' ', cleanText)
                                    addresses.append(cleanText)
                                    
                            except:
                                pass
def parseLocations(soups):
    for soup in soups:
        parseSingleSoup(soup)
    return addresses