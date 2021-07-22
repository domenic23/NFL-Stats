import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def fantasy_pros_scrape(URL):

    #scraping the URL
    r = requests.get(URL)
    stats = bs(r.content, features='lxml')
    
    #finding the table
    table = stats.find('table', {'class':'table table-bordered table-striped table-hover'}) #scrapes the table
    columns = table.find('thead').find_all('th')                                            #finds the column names
    column_names = [c.string for c in columns]                                              #puts the column names into a list

    #finds the players stats (each row of the column)
    table_rows = table.find('tbody').find_all('tr')
    l = []
    for tr in table_rows:
        td = tr.find_all('td')
        row = [str(tr.get_text()).strip() for tr in td]         
        l.append(row)

    df_list = []
    df = pd.DataFrame(l, columns=column_names)                                              #creates a DataFrame with all the stats we want and appends that DataFrame to a list of DataFrames
    df_list.append(df)
        
    result = pd.concat(df_list, ignore_index=True)                                          #concatenates the list of DataFrames into 1 large DataFrame and returns it

    #renaming the columns to add rushing in the names
    result.columns = ['Rank', 'Player', 'Cmp', 'Att', 'Cmp%', 'Yds', 'Y/A', 'TD', 'INT', 'SCK', 'R/Att', 'R/Yds', 'R/TD', 'FL', 'GP', 'FPTS', 'FPTS/G', 'OWN']
    result=result.set_index('Rank').drop(labels='OWN', axis=1)

    return result

### Quarterbacks ###

#2020 QB Stats in order of top fantasy performers (STD)
FprosQB_2020 = 'https://www.fantasypros.com/nfl/stats/qb.php'
QB_2020 = fantasy_pros_scrape(FprosQB_2020)

#2019 QB Stats in order of top fantasy performers (STD)
FprosQB_2019 = 'https://www.fantasypros.com/nfl/stats/qb.php?year=2019'
QB_2019 = fantasy_pros_scrape(FprosQB_2019)

#2018 QB Stats in order of top fantasy performers (STD)
FprosQB_2018 = 'https://www.fantasypros.com/nfl/stats/qb.php?year=2018'
QB_2018 = fantasy_pros_scrape(FprosQB_2018)

#2017 QB Stats in order of top fantasy performers (STD)
FprosQB_2017 = 'https://www.fantasypros.com/nfl/stats/qb.php?year=2017'
QB_2017 = fantasy_pros_scrape(FprosQB_2017)

#2016 QB Stats in order of top fantasy performer (STD)
FprosQB_2016 = 'https://www.fantasypros.com/nfl/stats/qb.php?year=2016'
QB_2016 = fantasy_pros_scrape(FprosQB_2016)
