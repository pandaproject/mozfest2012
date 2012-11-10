from urlparse import urljoin

from lxml.html import fromstring
import requests

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

    return data

BASE_URL = 'http://169.254.107.130/'
EXAMPLE_PATH = '1977.asp.html'
url = urljoin(BASE_URL, EXAMPLE_PATH)
print scrape_year_page(url)

