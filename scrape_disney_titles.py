import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
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

    title_dict = {
        'title': [],
        'url': [],
        'certificate': [],
        'runtime': [],
        'genre': []
    }

    def add_titles_to_dict():
        """ grabs title information and adds it to title_dict

        :return:
        appends itmes to title_dict
        """

        def does_element_exist(container, class_name):
            """ checks if element exists in imdb lister item"""
            try:
                value = container.find('span', class_=class_name).text
            except (AttributeError, NameError):
                value = 'Na'
            return value


        title_containers = soup.find_all('div', class_='lister-item-content')
        for container in title_containers:
            # gather data for title and url
            header_container= container.find('h3', class_='lister-item-header')
            title_dict['title'].append(header_container.find('a').text)

            title_dict['url'].append(header_container.find('a', href=True)['href'])

            # the following aren't always available and need conditional functions to work
            title_dict['certificate'].append(does_element_exist(container, 'certificate'))
            title_dict['runtime'].append(does_element_exist(container, 'runtime'))
            title_dict['genre'].append(does_element_exist(container, 'genre').strip())



        # title_containers = soup.find_all("h3", class_="lister-item-header")
        # for container in title_containers:
        #     title_dict['title'].append(container.find('a').text)
        #     title_dict['year'].append(container.find('span', class_='lister-item-year text-muted unbold').text)
        #     title_dict['url'].append(container.find('a', href=True)['href'])

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
    """ Cycles through urls from the csv file created using disney releases.
    Returns a combined dataframe with Rating, number of ratings, popularity score,
    metascore and the release date.

    :param file_path:
    :return: DataFrame
        title
        url
        certificate
        runtime
        genre
        rating
        num_ratings
        popularity
        metascore
        release_date
    """
    options = Options()
    # this function does not work when headless = True
    options.headless = False
    driver = webdriver.Chrome('./driver/chromedriver', options=options)
    release_df = pd.read_csv(file_path, index_col='Unnamed: 0')

    temp_dict = {
        'rating': [],
        'num_ratings': [],
        'popularity': [],
        'metascore': [],
        'release_date': []
    }

    #release_df[new_columns] = 'Na'
    print(release_df)
    base_url = 'https://www.imdb.com'

    def if_element_exists(by, element):
        try:
            element_to_check = driver.find_element(by, element).text
        except NoSuchElementException:
            element_to_check = 'NaN'

        return element_to_check

    for idx, row in release_df.iterrows():
        new_url = base_url + row['url']
        #new_url = 'https://www.imdb.com/title/tt10298840/'
        driver.get(new_url)
        print(new_url)

        # Get Rating Value
        rating_val = if_element_exists('xpath',
                                       "//div[@data-testid='hero-rating-bar__aggregate-rating__score']/span[1]")
        rating_val = float(rating_val) if rating_val != 'NaN' else rating_val

        # Get number of ratings submitted.
        num_rating_val = if_element_exists('xpath',
                                        "//div[@data-testid='hero-rating-bar__aggregate-rating__score']/../div[3]")
        if num_rating_val != 'NaN':
            if 'K' in num_rating_val:
                num_rating_val = float(num_rating_val.replace('K', '')) * 1000
            else:
                num_rating_val = float(num_rating_val)

        # Get Popularity
        popularity_val = if_element_exists('xpath', "//div[@data-testid='hero-rating-bar__popularity__score']")
        #popularity_val = int(popularity_val) if popularity_val != 'NaN' else popularity_val

        # Get metascore
        metascore_val = if_element_exists('xpath', "//span[@class='score-meta']")
        metascore_val = int(metascore_val) if metascore_val != 'NaN' else metascore_val

        release_date_val = if_element_exists('xpath', "//li[@data-testid='title-details-releasedate']/div/ul/li/a")

        country = re.findall("\(.*?\)", release_date_val)
        if len(country) > 0:
            release_date_val = release_date_val.replace(country[0], '').strip()

        print(rating_val)
        print(num_rating_val)
        print(popularity_val)
        print(metascore_val)
        print(release_date_val)

        temp_dict['rating'].append(rating_val)
        temp_dict['num_ratings'].append(num_rating_val)
        temp_dict['popularity'].append(popularity_val)
        temp_dict['metascore'].append(metascore_val)
        temp_dict['release_date'].append(release_date_val)

    temp_df = pd.DataFrame(temp_dict)
    new_df = pd.concat([release_df, temp_df], axis=1)

    return new_df




fill_details = fill_release_details('./data/disney_releases.csv')
fill_details.to_csv('./data/disney_release_data.csv')

# disney_releases = list_disney_releases('2015', '2022')
# disney_releases.to_csv('./data/disney_releases.csv')
# print(disney_releases)