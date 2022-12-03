# Webscraping IMDB list

This is just a simple script to pull data of Disney movies between 2021 and 2022
from a pre-created list on IMDB. 

Originally I had a pre-created list of disney titles but for reproducibility 
scrape_disney_titles.py was created to generate the list of titles. In this 
file contains a function 'list_disney_releases' requiring the input of a range of years.
The result is a dataframe containing the Title, Year of Release and the IMDB url tail.

Now I have a function that can grab a few additional details about a movie. Most of these 
are performance measures in addition to the release date. At this point I have identified a
few challenges. 

1. It is not easy to determine separate movies from tv series as they are not categorized as such. 
   * I may be able to categorize them myself from the search titles.
2. Acquiring the Motion Picture Rating is not always in the same spot
3. 