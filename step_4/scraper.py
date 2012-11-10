#!/usr/bin/env python

from urlparse import urljoin

from lxml.html import fromstring
import requests

base_url = 'http://169.254.181.7/'

def scrape_year_page(url):
    response = requests.get(url)

    doc = fromstring(response.content)

    data = {}

    # Year
    data['year'] = doc.cssselect('h2')[0].text
    
    rows = doc.cssselect('table table tr')

    # Registered runners
    cells = rows[1].cssselect('td')
    data['registered_runners'] = int(cells[1].text.replace(',', ''))

    # Finished runners
    cells = rows[2].cssselect('td')
    data['finished_runners'] = int(cells[1].text.replace(',', ''))

    # Wind
    cells = rows[4].cssselect('td')
    wind = cells[1].text

    if wind == 'calm':
        data['wind_dir'] = None
        data['wind_speed'] = 0
    else:  
        direction, speed = wind.split()

        data['wind_dir'] = direction
        data['wind_speed'] = int(speed)

    return data

#EXAMPLE_PATH = '1977.asp.html'
#url = urljoin(base_url, EXAMPLE_PATH)
#print scrape_year_page(url)

import csv

decades = [1960, 1970, 1980, 1990, 2000]
scraped_urls = []
output = []

for decade in decades:
    url = urljoin(base_url, '%is.html' % decade)
    response = requests.get(url)

    if response.status_code != 200:
        continue

    doc = fromstring(response.content)

    year_links = doc.cssselect('tr b a')
    
    for year_link in year_links:
        path = year_link.attrib['href']
        year_url = urljoin(base_url, path)

        if year_url not in scraped_urls:
            data = scrape_year_page(year_url)

            output.append(data)
            scraped_urls.append(year_url)

field_names = ['year', 'registered_runners', 'finished_runners', 'wind_dir', 'wind_speed']

with open('race_history.csv', 'w') as f:
    writer = csv.DictWriter(f, field_names)
    writer.writerow(dict(zip(field_names, field_names)))
    writer.writerows(output)
