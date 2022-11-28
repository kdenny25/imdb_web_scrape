import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


def list_disney_releases(start, end):
    """Returns a Pandas Dataframe listing all entertainment releases from Disney.

    Attributes:
        start - start year
        end - end year

    Return:
        Dataframe:
            Columns - title, year, url
    """
    page_number = 1
    url = f'https://www.imdb.com/search/keyword/?keywords=disney&ref_=kw_ref_yr&sort=release_date,desc&mode=detail&page={str(page_number)}&release_date={start}%2C{end}'
    search_url = 'https://www.imdb.com/search/keyword/?keywords=disney&ref_=kw_nxt&mode=detail&'

    title_dict = {
        'title': [],
        'year': [],
        'url': []
    }

    def add_titles_to_dict():
        """ grabs title information and adds it to title_dict

        :return:
        appends itmes to title_dict
        """
        title_containers = soup.find_all("h3", class_="lister-item-header")
        for container in title_containers:
            title_dict['title'].append(container.find('a').text)
            title_dict['year'].append(container.find('span', class_='lister-item-year text-muted unbold').text)
            title_dict['url'].append(container.find('a', href=True)['href'])

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    next_page_exists = True

    while next_page_exists:
        add_titles_to_dict()

        try:
            # looks for next page link
            next_page_link = soup.find('a', class_='lister-page-next next-page', href=True)

            print(page_number)
            if next_page_link.text == 'Next »':
                page_number += 1
                new_url = f'https://www.imdb.com/search/keyword/?keywords=disney&ref_=kw_ref_yr&sort=release_date,desc&mode=detail&page={str(page_number)}&release_date={start}%2C{end}'
                page = requests.get(new_url)
                soup = BeautifulSoup(page.content, 'html.parser')
        except (AttributeError, NameError):
            next_page_exists = False

    titles_dataframe = pd.DataFrame(title_dict)
    return titles_dataframe

disney_releases = list_disney_releases('2015', '2022')
disney_releases.to_csv('./data/disney_releases.csv')
print(disney_releases)