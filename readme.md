# Webscraping IMDB list

This is just a simple script to pull data of Disney movies between 2021 and 2022
from a pre-created list on IMDB.  

Originally I had a pre-created list of disney titles but for reproducibility 
scrape_disney_titles.py was created to generate the list of titles. In this 
file contains a function 'list_disney_releases' requiring the input of a range of years.
The result is a dataframe containing the Title, Year of Release and the IMDB url tail.

At the time of writing this script the dataset was missing full release dates
But, having additional information about the films could have a positive
impact on my analysis. To add more data a new script is born. This script
searches each title based from the list provided by Finder. I can now search
through each movie and extract more information.
