import re
import threading
import time


# A map that contains all classification types as keys, with their respective values as a list of text 
contextMap = {}
# The most common script tags
scriptTags = re.compile(r"[{}\[\]\*>=]")


# Input         -   soup        : A soup that 
#                   contextMap  : 
# Description   -   Iterates through the single soup looking for text and calling the classifier, classifying the text into the map

def parseSingleSoup(soup, nbc):
    textList = []
    
    if soup is not None:
        tags = soup.findAll()

        for tag in tags:
            tagText = tag.findAll(text=True, recursive=False)                                                # get one level of text depth
            finalText = ''
            for text in tagText:        
                text = re.sub('[.!;+_|]', '', text.strip())
                if len(re.sub(r'\s+', '', text)) > 0 and re.search(scriptTags, text) is None:                # if this actually contains text AND do not take characters with script chars in it
                        #print "text  is a" + re.sub(r'\s+', '', text.strip()) + "b"
                        #print "length is " + str(len(re.sub(r'\s+', '', text)))
                        finalText += str(re.sub(r'\s+',' ', text))            

            if finalText:
                
                # Clean up the string.
                finalText = ' '.join(finalText.split())

                # Classify the string.
                data = nbc.classify(finalText)

                # Push the classified text into the context Map
                if data in contextMap:
                    contextMap[data].append(finalText)
                else:
                    contextMap[data] = [finalText]

# Input         - soups     : A list of soups that Beautiful soup is capable of parsing
#               - nbc       : A trained naive bayes classifier
# Description   - 
# Output        - A map that contains all classification types as keys, with their respective values as a list of text 

def parseSoups(soups, nbc):
    
    
    threads = []
    start_time = time.time()
    for soup in soups:
        parseSingleSoup(soup, nbc)        
        #t = threading.Thread(target=parseSingleSoup, args = (soup,nbc))
        #threads.append(t)
        #t.start()

    # Wait for all of them to finish
    #[x.join() for x in threads]

    print "Classification took " + str((time.time() - start_time))  + " seconds"

    #for key,value in contextMap.items():
    #    print key
    #    print value
    return contextMap
