from bs4 import BeautifulSoup
import re
import jsonParser

def parse(soups):
    menuItems = []

    for soup in soups:
        newMenuItems = parseSingleSoup(soup)
        if not menuItems:
            menuItems = newMenuItems
        else:
            if newMenuItems:
                menuItems += newMenuItems

    return menuItems

def parseSingleSoup(soup):
    title = soup.title
    if title is not None and 'menu' in str(title).lower():
        attrs = ['title', 'name', 'salad', 'salads']

        def getMenuTags(tag):
            for key in dict(tag.attrs):
                for attr in attrs:
                    if key.find(attr) != -1:
                        return True
                    if type(tag[key]) is unicode:
                        if str(tag[key]).find(attr) != -1:
                            return True
                    else:
                        if any(attr in t for t in tag[key]):
                            return True

        menuTags = soup.find_all(getMenuTags)
        menuItems = []

        for tag in menuTags:
            for key in tag.attrs:
                '''
                if 'Salads' in tag[key]:
                    print 'Salads'
                '''
                if 'name' in tag[key]:
                    menuItems.append(tag.get_text())

        return menuItems

