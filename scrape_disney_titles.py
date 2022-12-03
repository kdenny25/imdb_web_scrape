import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd



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

def fill_release_details(file_path):
    driver = webdriver.Chrome('./driver/chromedriver')
    release_df = pd.read_csv(file_path, index_col='Unnamed: 0')

    new_columns = ['rating', 'num_ratings', 'popularity', 'metascore', 'type',
                   'length', 'rating', 'genre', 'release_date']

    release_df[new_columns] = 'Na'
    print(release_df)
    base_url = 'https://www.imdb.com'

    def if_element_exists(by, element):
        try:
            element_to_check = driver.find_element(by, element).text
        except NoSuchElementException:
            element_to_check = 'NaN'

        return element_to_check

    for idx, row in release_df.iterrows():
        #new_url = base_url + row['url']
        new_url = 'https://www.imdb.com/title/tt10298840/'
        driver.get(new_url)
        print(new_url)

        # Get Rating Value
        rating = if_element_exists('xpath',
                                       "//div[@data-testid='hero-rating-bar__aggregate-rating__score']/span[1]")
        rating = float(rating) if rating != 'NaN' else rating

        # Get number of ratings submitted.
        num_rating = if_element_exists('xpath',
                                        "//div[@data-testid='hero-rating-bar__aggregate-rating__score']/../div[3]")
        if num_rating != 'NaN':
            if 'K' in num_rating:
                num_rating = float(num_rating.replace('K', '')) * 1000
            else:
                num_rating = float(num_rating)

        # Get Popularity
        popularity = if_element_exists('xpath', "//div[@data-testid='hero-rating-bar__popularity__score']")
        popularity = int(popularity) if popularity != 'NaN' else popularity

        # Get metascore
        metascore = if_element_exists('xpath', "//span[@class='score-meta']")
        metascore = int(metascore) if metascore != 'NaN' else metascore

        release_date = if_element_exists('xpath', "//li[@data-testid='title-details-releasedate']/div/ul/li/a")

        if '(United States)' in release_date:
            release_date = release_date.replace(' (United States)', '')

        print(rating)
        print(num_rating)
        print(popularity)
        print(metascore)
        print(release_date)



fill_release_details('./data/disney_releases.csv')

# disney_releases = list_disney_releases('2015', '2022')
# disney_releases.to_csv('./data/disney_releases.csv')
# print(disney_releases)