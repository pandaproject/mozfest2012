from urlparse import urljoin

from lxml.html import fromstring
import requests

def scrape_year_page(url):
    if url not in scraped_urls:
        scraped_urls.append(url)
        response = requests.get(url)
    else:
        return None

    doc = fromstring(response.content)

    data = {}

    # Year
    data['year'] = doc.cssselect('h2')[0].text
    
    rows = doc.cssselect('table table tr')

    # Winners
    cells = rows[0].cssselect('td')
    data['male_winner'] = cells[1].text
    data['female_winner'] = cells[3].text

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
    data['weather'] = rows[6].cssselect('i')[0].text.strip() 

    return data

#BASE_URL = 'http://169.254.181.7/'
#EXAMPLE_PATH = '1977.asp.html'
#url = urljoin(BASE_URL, EXAMPLE_PATH)
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

field_names = ['year', 'male_winner', 'female_winner', 'registered_runners', 'finished_runners', 'start_temp', 'middle_temp', 'end_temp', 'wind_dir', 'wind_speed', 'hours_of_sunshine', 'weather']

with open('race_history.csv', 'w') as f:
    writer = csv.DictWriter(f, field_names)
    writer.writerow(dict(zip(field_names, field_names)))
    writer.writerows(output)
