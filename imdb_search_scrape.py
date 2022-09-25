import requests
from bs4 import BeautifulSoup
import pandas as pd

# GET request for scraping page


url_base  = 'https://www.imdb.com/find?q='

df = pd.read_csv('./data/disney_plus_release_schedule.csv')
search_list = df[df['title']]


for i, title in enumerate(search_list):
    # GET request for search results
    page = requests.get(url_base + title)

    # parse HTML page to search for link
    soup = BeautifulSoup(page.content, 'html.parser')
    soup.fin('a', href=True)






# returns text value if it exists
# otherwise it returns 'None'
def find_val(parent_soup, container, class_id):
    value_to_check = parent_soup.find(container, class_=class_id)

    if value_to_check != None:
        return value_to_check.text
    else:
        return 'None'

