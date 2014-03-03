import urllib
import urlparse
from bs4 import BeautifulSoup
import json
import re

#import settings
#import os
#import sys
#sys.path.insert(0, '/path/to/application/app/folder')

#from semantix.app.trainer.businessname import fileNameFromURL

'''
This function opens a network object denoted by a URL and vists links 
within associated html. Any links identified will only further be explored
if the top level domain matches the original url argument. 

All extracted html from the links will be returned as a json encoded string
of the form:

json = [
	{
		"data" : "<str>",
		"sequence_number" : <integer>,
		"url" : <str>
	},
	...
]

@param url - a website url.

The url must be astirng will be modified to contain a preceeding "http://"
if it does not already contain it. There is no attempt to make a secure
connection.

Please make sure to do url validation in the calling function as this function
does not make any attempt to validate the url argument.
'''
def pullJsonEncodedHtml(url):
	if not isinstance(url, str):
		print "ERROR: crawler.pullJsonEncodedHtml called with non-string argument"
	
	if "http://" not in url:
		url = "http://" + url

	urls = [url]
	visited = [url]
	jsonData = []
	htmlText = ""
	current_level = 0

	try:
		htmlText = urllib.urlopen(urls[0]).read()
	except:
		print "ERROR: crawler.pullJsonEncodedHtml cannot open url argument " + urls[0]
		return None

	if htmlText is not "":
		htmlText = re.sub('\\s', '', htmlText)
		jsonData.append({
			"body" : htmlText,
			"sequence_number" : current_level,
			"url" : url
		})
		current_level = current_level + 1
	else:
		return None

	while len(urls) > 0:
		htmlText = ""
		newLevel = False
		
		try:
			htmlText = urllib.urlopen(urls[0]).read()
		except:
			print "ERROR: crawler.pullJsonEncodedHtml cannot open url argument " + urls[0]

		urls.pop(0)
		htmlSoup = BeautifulSoup(htmlText)

		for tag in htmlSoup.findAll('a', href=True):
			tag['href'] = urlparse.urljoin(url, tag['href'])
			if url in tag['href'] and tag['href'] not in visited:
				urls.append(tag['href'])
				visited.append(tag['href'])
				newLevel = True
				if htmlText is not "":
					htmlText = re.sub('\\s', '', htmlText)
					jsonData.append({
						"body" : htmlText,
						"sequence_number" : current_level,
						"url" : tag['href']
					})

		if newLevel:
			current_level = current_level + 1

	jsonStrData = ''
	for data in jsonData:
		jsonStrData = jsonStrData + json.dumps(data) + '\n'
	
	return jsonStrData
