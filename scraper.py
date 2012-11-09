#!/usr/bin/env python

from urlparse import urljoin

from lxml.html import fromstring
import requests

base_url = 'http://localhost:8000/'
first_path = '2000s.html'
scraped_urls = []
output = []

def scrape_decade_page(url):
    if url not in scraped_urls:
        scraped_urls.append(url)
        response = requests.get(url)
    else:
        return None

    doc = fromstring(response.content)

    year_links = doc.cssselect('tr b a')
    
    for year_link in year_links:
        path = year_link.attrib['href']
        year_url = urljoin(base_url, path)
        data = scrape_year_page(year_url)

        output.append(data)

    decade_links = doc.cssselect('td[colspan="4"] a')

    for decade_link in decade_links:
        path = decade_link.attrib['href']
        decade_url = urljoin(base_url, path)
        scrape_decade_page(decade_url)

def scrape_year_page(url):
    if url not in scraped_urls:
        scraped_urls.append(url)
        response = requests.get(url)
    else:
        return None

    doc = fromstring(response.content)

    data = {}

    data['year'] = doc.cssselect('h2')[0].text
    
    rows = doc.cssselect('table table tr')

    # Winners
    cells = rows[0].cssselect('td')
    data['male_winner'] = rows[1].text
    data['female_winner'] = rows[3].text

    # Registered runners
    cells = rows[1].cssselect('td')
    data['registered_runners'] = int(cells[1].text.replace(',', ''))

    # Finished runners
    cells = rows[2].cssselect('td')
    data['finished_runners'] = int(cells[1].text.replace(',', ''))

    # Temps
    temp_items = rows[3].cssselect('li')
    data['start_temp'] = int(temp_items[0].text.split()[-1])
    data['middle_temp'] = int(temp_items[1].text.split()[-1])
    data['end_temp'] = int(temp_items[2].text.split()[-1])

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

    # Sunshine
    cells = rows[5].cssselect('td')
    data['hours_of_sunshine'] = cells[1].text

    # Weather description
    data['weather'] = rows[6].cssselect('i')[0].text 

    return data

first_url = urljoin(base_url, first_path)
scrape_decade_page(first_url)

print output
