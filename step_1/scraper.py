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

    return data

EXAMPLE_PATH = '1977.asp.html'
url = urljoin(base_url, EXAMPLE_PATH)
print scrape_year_page(url)


