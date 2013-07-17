from bs4 import BeautifulSoup
import quopri
import json
import os, errno

def parseData(inputFile):
    soups = []
    with open(inputFile) as data:
        for line in data:
            # Load the line and the value 'body'.
            body = json.loads(line)['body']
            # Use the quopri module to decode the qp encoded value of each page.
            decodedQP = quopri.decodestring(body)
            soups.append(BeautifulSoup(decodedQP))
    
    return soups
  
def parseFirstPage(inputFile):
	with open(inputFile) as data:
		for line in data:
			if json.loads(line)['sequence_number'] == 0:
				body = json.loads(line)['body']
				decodedQP = quopri.decodestring(body)
				return BeautifulSoup(decodedQP)
	raise Exception('Bad input file, cannot find first page.')
