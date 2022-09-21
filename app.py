import requests
from bs4 import BeautifulSoup

# GET request for scraping page
page = requests.get\
    ('https://www.imdb.com/list/ls084908369/?sort=list_order,asc&st_dt=&mode=detail&page=1&ref_=ttls_vm_dtl')

# parse the HTML
soup = BeautifulSoup(page.content, 'html.parser')

# find all div containers for movies
mList = soup.find_all('div', class_='lister-item-content')

titles = []
pRate = []
# iterate through containers
for movie in mList:
    titles.append(movie.find('h3', class_='lister-item-header').find('a').text)

    # check for missing values and append the parental rating
    pRate_val = movie.find('span', class_='certificate')
    if pRate_val != None:
        pRate.append(movie.find('span', class_='certificate').text)
    else:
        pRate.append('None')

print(titles)
print(pRate)