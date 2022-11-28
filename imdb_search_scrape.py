import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# GET request for scraping page

URL_BASE = "https://www.imdb.com"
URL_SRCH_BASE = "https://www.imdb.com/find?q="

df = pd.read_csv("./data/disney_plus_release_schedule.csv")
search_list = df["title"]

# takes list of movies and formats them to be
# easily read by imdb's search
def cleanSearch(list):
    newList = []
    for i in list:
        new_text = re.sub("[\(\[].*?[\)\]]", "", i)
        new_text = new_text.replace(" ", "+")
        newList.append(new_text)
    return newList


# clean the search list
clean_search = cleanSearch(search_list)

page = requests.get(URL_SRCH_BASE + clean_search[1])
soup = BeautifulSoup(page.content, "html.parser")

# pulls a list of all titles from the search
srch_titles = soup.find("table", class_="findList").find_all("a", href=True)

for x in srch_titles:
    srch_link = URL_BASE + srch_titles[x]["href"]
    trgt_page = requests.get(srch_link)
    trgt_soup = BeautifulSoup(trgt_page.content, "html.parser")
    

print(srch_titles[0])

# for i, title in enumerate(clean_search):
# GET request for search results
# page = requests.get(url_base + title)
# print(title)
# parse HTML page to search for link
# soup = BeautifulSoup(page.content, 'html.parser')
# soup.find('a', href=True)


# returns text value if it exists
# otherwise it returns 'None'
def find_val(parent_soup, container, class_id):
    value_to_check = parent_soup.find(container, class_=class_id)

    if value_to_check == None:
        return "None"
    else:
        return value_to_check.text
