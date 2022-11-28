import requests
from bs4 import BeautifulSoup
import pandas as pd

# GET request for scraping page
page = requests.get(
    "https://www.imdb.com/list/ls084908369/?sort=list_order,asc&st_dt=&mode=detail&page=1&ref_=ttls_vm_dtl"
)

url = "https://www.imdb.com/find?q="


# parse the HTML
soup = BeautifulSoup(page.content, "html.parser")

# find all div containers for movies
mList = soup.find_all("div", class_="lister-item-content")


movies_dict = {
    "title": [],
    "pRate": [],
    "genre": [],
    "starRate": [],
}

# returns text value if it exists
# otherwise it returns 'None'
def find_val(parent_soup, container, class_id):
    value_to_check = parent_soup.find(container, class_=class_id)

    if value_to_check != None:
        return value_to_check.text
    else:
        return "None"


# iterate through containers
for y, movie in enumerate(mList):
    # extract title
    movies_dict["title"].append(movie.find("h3", class_="lister-item-header").find("a").text)

    # extract parental rating
    movies_dict["pRate"].append(find_val(movie, "span", "certificate"))

    # extract genre
    movies_dict["genre"].append(find_val(movie, "span", "genre").replace("\n", ""))

    # extract star rating
    movies_dict["starRate"].append(find_val(movie, "span", "ipl-rating-star__rating"))


movies_df = pd.DataFrame.from_dict(movies_dict)

movies_df.to_csv("data/movies_data.csv")
print(movies_df.head())
