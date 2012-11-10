from urlparse import urljoin

from lxml.html import fromstring
import requests

def scrape_year_page(url):
    response = requests.get(url)

    doc = fromstring(response.content)

    data = {}

    # Year
    data['year'] = doc.cssselect('h2')[0].text
    
    # Registered runners
    cell = doc.cssselect('#registered')[0]
    data['registered_runners'] = int(cell.text.replace(',', ''))

    # Finished runners
    cell = doc.cssselect('#finished')[0]
    data['finished_runners'] = int(cell.text.replace(',', ''))

    # Wind
    cells = doc.cssselect('marquee')
    wind = cells[0].text

    if wind == 'calm':
        data['wind_dir'] = None
        data['wind_speed'] = 0
    else:  
        direction, speed = wind.split()

        data['wind_dir'] = direction
        data['wind_speed'] = int(speed)

    return data

BASE_URL = 'http://169.254.135.23/'
#EXAMPLE_PATH = '1977.asp.html'
#url = urljoin(BASE_URL, EXAMPLE_PATH)
#print scrape_year_page(url)

import csv

decades = [1960, 1970, 1980, 1990, 2000]
scraped_urls = []
output = []

for decade in decades:
    url = urljoin(BASE_URL, '%is.html' % decade)
    response = requests.get(url)

    if response.status_code != 200:
        continue

    doc = fromstring(response.content)

    year_links = doc.cssselect('tr b a')
    
    for year_link in year_links:
        path = year_link.attrib['href']
        year_url = urljoin(BASE_URL, path)

        if year_url not in scraped_urls:
            data = scrape_year_page(year_url)

            output.append(data)
            scraped_urls.append(year_url)

field_names = ['year', 'registered_runners', 'finished_runners', 'wind_dir', 'wind_speed']

with open('race_history.csv', 'w') as f:
    writer = csv.DictWriter(f, field_names)
    writer.writerow(dict(zip(field_names, field_names)))
    writer.writerows(output)
