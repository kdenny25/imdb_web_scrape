import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# GET request for scraping page


url_base  = 'https://www.imdb.com/find?q='

df = pd.read_csv('./data/disney_plus_release_schedule.csv')
search_list = df['title']

# takes list of movies and formats them to be
# easily read by imdb's search
def cleanSearch(list):
    newList = []
    for i in list:
        new_text = re.sub("[\(\[].*?[\)\]]", "", i)
        new_text = new_text.replace(" ", "+")
        newList.append(new_text)
    return newList

clean_search = cleanSearch(search_list)

page = requests.get(url_base + clean_search[1])

soup = BeautifulSoup(page.content, 'html.parser')

for i, title in enumerate(clean_search):
    # GET request for search results
    #page = requests.get(url_base + title)
    print(title)
    # parse HTML page to search for link
    #soup = BeautifulSoup(page.content, 'html.parser')
    #soup.fin('a', href=True)





# returns text value if it exists
# otherwise it returns 'None'
def find_val(parent_soup, container, class_id):
    value_to_check = parent_soup.find(container, class_=class_id)

    if value_to_check != None:
        return value_to_check.text
    else:
        return 'None'

