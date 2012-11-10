from urlparse import urljoin

from lxml.html import fromstring
import requests

def scrape_year_page(url):
    response = requests.get(url)

    doc = fromstring(response.content)

    data = {}

    # Year
    data['year'] = doc.cssselect('h2')[0].text
    
    return data

BASE_URL = 'http://169.254.181.7/'
EXAMPLE_PATH = '1977.asp.html'
url = urljoin(BASE_URL, EXAMPLE_PATH)
print scrape_year_page(url)


