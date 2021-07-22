import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def renaming_columns(df, URL):

    #renaming the columns for QBs
    if re.search('qb', URL):
        df.columns = ['Rank', 'Player', 'Comp', 'Att', 'Comp%', 'Yds', 'Y/A', 'PassTD', 'INT', 'SCK', 'RushAtt', 'RushYds', 'RushTD', 'FL', 'GP', 'FPTS', 'FPTS/G', 'OWN']
        df=df.set_index('Rank').drop(labels='OWN', axis=1)

    #renaming the columns for RBs
    elif re.search('rb', URL):
        df.columns = ['Rank', 'Player', 'RushAtt', 'RushYds', 'Y/A', 'LG', '20+', 'RushTD', 'Rec', 'TGT', 'RecYds', 'Y/R', 'RecTD', 'FL', 'GP', 'FPTS', 'FPTS/G', 'OWN']
        df=df.set_index('Rank').drop(labels=['OWN', '20+'], axis=1)

    #renaming the columns for WRs
    elif re.search('wr', URL):
        df.columns = ['Rank', 'Player', 'Rec', 'TGT', 'RecYds', 'Y/R', 'LG', '20+', 'RecTD', 'RushAtt', 'RushYds', 'RushTD', 'FL', 'GP', 'FPTS', 'FPTS/G', 'OWN']
        df=df.set_index('Rank').drop(labels=['OWN', '20+'], axis=1)
    
    #renaming the columns for TEs
    elif re.search('te', URL):
        df.columns = ['Rank', 'Player', 'Rec', 'TGT', 'RecYds', 'Y/R', 'LG', '20+', 'RecTD', 'RushAtt', 'RushYds', 'RushTD', 'FL', 'GP', 'FPTS', 'FPTS/G', 'OWN']
        df=df.set_index('Rank').drop(labels=['OWN', '20+', 'RushAtt', 'RushYds', 'RushTD'], axis=1)

    #renaming the columns for Ks
    elif re.search('k', URL):
        df.columns = ['Rank', 'Player', 'FG', 'FGA', 'PCT(%)', 'LG', '1-19', '20-29', '30-39', '40-49', '50+', 'XPT', 'XPA', 'GP', 'FPTS', 'FPTS/G', 'OWN']
        df=df.set_index('Rank').drop(labels=['OWN'], axis=1)

    return df

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

    df = pd.DataFrame(l, columns=column_names)                                              #creates a DataFrame with all the stats we want and appends that DataFrame to a list of DataFrames
    df = renaming_columns(df, URL)                                                            #renames the columns in the DataFrame

    return df

# All positions in order of top fantasy performers in each respective scoring rules (Standard or Points Per Reception(PPR))
### Quarterbacks ###

# Standard Scoring
QB_STD_2020 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/qb.php?year=2020&scoring=Standard')
QB_STD_2019 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/qb.php?year=2019&scoring=Standard')
QB_STD_2018 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/qb.php?year=2018&scoring=Standard')
QB_STD_2017 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/qb.php?year=2017&scoring=Standard')
QB_STD_2016 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/qb.php?year=2016&scoring=Standard')

### Running Backs ### 

# Standard Scoring
RB_STD_2020 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/rb.php?year=2020&scoring=Standard')
RB_STD_2019 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/rb.php?year=2019&scoring=Standard')
RB_STD_2018 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/rb.php?year=2018&scoring=Standard')
RB_STD_2017 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/rb.php?year=2017&scoring=Standard')
RB_STD_2016 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/rb.php?year=2016&scoring=Standard')

#PPR Scoring
RB_PPR_2020 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/rb.php?year=2020&scoring=PPR')
RB_PPR_2019 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/rb.php?year=2019&scoring=PPR')
RB_PPR_2018 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/rb.php?year=2018&scoring=PPR')
RB_PPR_2017 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/rb.php?year=2017&scoring=PPR')
RB_PPR_2016 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/rb.php?year=2016&scoring=PPR')

### Wide Receivers ###

# Standard Scoring
WR_STD_2020 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/wr.php?year=2020&scoring=Standard')
WR_STD_2019 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/wr.php?year=2019&scoring=Standard')
WR_STD_2018 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/wr.php?year=2018&scoring=Standard')
WR_STD_2017 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/wr.php?year=2017&scoring=Standard')
WR_STD_2016 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/wr.php?year=2016&scoring=Standard')

#PPR Scoring
WR_PPR_2020 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/wr.php?year=2020&scoring=PPR')
WR_PPR_2019 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/wr.php?year=2019&scoring=PPR')
WR_PPR_2018 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/wr.php?year=2018&scoring=PPR')
WR_PPR_2017 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/wr.php?year=2017&scoring=PPR')
WR_PPR_2016 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/wr.php?year=2016&scoring=PPR')

### Tight Ends ###

#Standard Scoring
TE_STD_2020 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/te.php?year=2020&scoring=Standard')
TE_STD_2019 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/te.php?year=2019&scoring=Standard')
TE_STD_2018 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/te.php?year=2018&scoring=Standard')
TE_STD_2017 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/te.php?year=2017&scoring=Standard')
TE_STD_2016 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/te.php?year=2016&scoring=Standard')

#PPR Scoring
TE_PPR_2020 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/te.php?year=2020&scoring=PPR')
TE_PPR_2019 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/te.php?year=2019&scoring=PPR')
TE_PPR_2018 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/te.php?year=2018&scoring=PPR')
TE_PPR_2017 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/te.php?year=2017&scoring=PPR')
TE_PPR_2016 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/te.php?year=2016&scoring=PPR')

### Kickers ###

#Standard Scoring
K_STD_2020 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/k.php?year=2020&scoring=Standard')
K_STD_2019 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/k.php?year=2019&scoring=Standard')
K_STD_2018 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/k.php?year=2018&scoring=Standard')
K_STD_2017 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/k.php?year=2017&scoring=Standard')
K_STD_2016 = fantasy_pros_scrape('https://www.fantasypros.com/nfl/stats/k.php?year=2016&scoring=Standard')

#example graphs
QB_2020['Cmp'] = QB_2020['Cmp'].astype('int')
QB_2020['Yds'] = QB_2020['Yds'].str.replace(',', '').astype('int')
plot1 = QB_2020.head(10).plot(x='Player', y='Cmp', kind='bar')
plot2 = QB_2020.head(10).plot(x='Player', y='Yds', kind='bar')
