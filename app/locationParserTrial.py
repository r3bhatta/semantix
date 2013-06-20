from bs4 import BeautifulSoup
import re


def parseSingleSoup(soup):
    if soup is not None:
        title = soup.title
        if title is not None and 'location' in str(title).lower():
            textArray = soup.findAll(text=True)
            ' remove any text of type scripts or just backslashes'
            
            noScriptsTextArray = []
            removeScriptTagsPattern = re.compile(r"[{}\[\]\*]")
            for text in textArray:
                if re.search(removeScriptTagsPattern, text) is None:
                    if len(re.sub(r'\s+', '', text)) > 0:
                        noScriptsTextArray.append(re.sub(r'\s+', ' ', text))

            for line in noScriptsTextArray:
                print line


def parseSingleSoupTrial2(soup):
    
    removeScriptTagsPattern = re.compile(r"[{}\[\]\*]")
    if soup is not None:
        pageTitle = soup.title
        if pageTitle is not None and 'location' in str(pageTitle).lower():
            divTagsCollection = soup.findAll('div')
            for divTag in divTagsCollection:
                divTagTextCollection = divTag.findAll(text=True)
                finalText = ""
                for text in divTagTextCollection:        
                    if len(re.sub(r'\s+', '', text)) > 0:
                        if re.search(removeScriptTagsPattern, text) is None:
                            finalText += str(re.sub(r'\s+', ' ', text))
                
                print finalText
                print "____________________________________"
                
                
def parseLocations(soups):
    for soup in soups:
        parseSingleSoupTrial2(soup)
