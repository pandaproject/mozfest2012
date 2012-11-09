#!/usr/bin/env python

from urlparse import urljoin

from lxml.html import fromstring
import requests

base_url = 'http://localhost:8000/'
first_path = '2000s.html'
scraped_paths = []

def get_page_doc(path):
    if path not in scraped_paths:
        scraped_paths.append(path)
        response = requests.get(urljoin(base_url, path))
        return fromstring(response.content)
    else:
        return None

def scrape_decade_doc(doc):
    year_links = doc.cssselect('tr b a')
    
    for year_link in year_links:
        path = year_link.attrib['href']
       
        year_doc = get_page_doc(path)

        if year_doc is not None:
            scrape_year_doc(year_doc)

    decade_links = doc.cssselect('td[colspan="4"] a')

    for decade_link in decade_links:
        path = decade_link.attrib['href']

        decade_doc = get_page_doc(path)

        if decade_doc is not None:
            scrape_decade_doc(decade_doc)

def scrape_year_doc(doc):
    print doc.cssselect('h2')[0].text

response = requests.get(urljoin(base_url, first_path))
doc = fromstring(response.content)
scrape_decade_doc(doc)

outline ="""
request page

for page in pages:
        for row in list:
                get detail page
                    
                            get field 1 by id
                                    get field 2 position relative to field 1
                                            get field 3 and split into 4 and 5
                                                    store detail url
                                                        
                                                        save to csv
                                                        save to panda?
                                                        """
