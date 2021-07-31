import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import hvplot.pandas

all_QB = []
all_RB_STD = []
all_RB_PPR = []
all_WR_STD = []
all_WR_PPR = []
all_TE_STD = []
all_TE_PPR = []
all_K = []

def to_numeric(df):
    for column in df.columns:
        if column != 'Player':
            df[column]=df[column].str.replace(',', '').astype('float')
    return df

def renaming_columns(df, URL):
    global all_QB
    global all_RB_STD
    global all_RB_PPR
    global all_WR_STD
    global all_WR_PPR
    global all_TE_STD
    global all_TE_PPR
    global all_K

    #adding the year to each Dataframe for uses later
    for i in range(2020,2015,-1):
            if re.search(str(i), URL):
                df['Year'] = str(i)
    
    #renaming the columns for QBs
    if re.search('qb', URL):
        df.columns = ['Rank', 'Player', 'Comp', 'Att', 'Comp%', 'Yds', 'Y/A', 'PassTD', 'INT', 'SCK', 'RushAtt', 'RushYds', 'RushTD', 'FL', 'GP', 'FPTS', 'FPTS/G', 'OWN', 'Year']
        df=df.set_index('Rank').drop(labels='OWN', axis=1)
        df=to_numeric(df)
        all_QB.append(df)

    #renaming the columns for RBs
    elif re.search('rb', URL):
        df.columns = ['Rank', 'Player', 'RushAtt', 'RushYds', 'Y/A', 'LG', '20+', 'RushTD', 'Rec', 'TGT', 'RecYds', 'Y/R', 'RecTD', 'FL', 'GP', 'FPTS', 'FPTS/G', 'OWN', 'Year']
        df=df.set_index('Rank').drop(labels=['OWN', '20+'], axis=1)
        df=to_numeric(df)
        if re.search('Standard', URL):
            all_RB_STD.append(df)
        elif re.search('PPR', URL):
            all_RB_PPR.append(df)

    #renaming the columns for WRs
    elif re.search('wr', URL):
        df.columns = ['Rank', 'Player', 'Rec', 'TGT', 'RecYds', 'Y/R', 'LG', '20+', 'RecTD', 'RushAtt', 'RushYds', 'RushTD', 'FL', 'GP', 'FPTS', 'FPTS/G', 'OWN', 'Year']
        df=df.set_index('Rank').drop(labels=['OWN', '20+'], axis=1)
        df=to_numeric(df)
        if re.search('Standard', URL):
            all_WR_STD.append(df)
        elif re.search('PPR', URL):
            all_WR_PPR.append(df)
            
    #renaming the columns for TEs
    elif re.search('te', URL):
        df.columns = ['Rank', 'Player', 'Rec', 'TGT', 'RecYds', 'Y/R', 'LG', '20+', 'RecTD', 'RushAtt', 'RushYds', 'RushTD', 'FL', 'GP', 'FPTS', 'FPTS/G', 'OWN', 'Year']
        df=df.set_index('Rank').drop(labels=['OWN', '20+', 'RushAtt', 'RushYds', 'RushTD'], axis=1)
        df=to_numeric(df)
        if re.search('Standard', URL):
            all_TE_STD.append(df)
        elif re.search('PPR', URL):
            all_TE_PPR.append(df)
        
    #renaming the columns for Ks
    elif re.search('k', URL):
        df.columns = ['Rank', 'Player', 'FG', 'FGA', 'PCT(%)', 'LG', '1-19', '20-29', '30-39', '40-49', '50+', 'XPT', 'XPA', 'GP', 'FPTS', 'FPTS/G', 'OWN', 'Year']
        df=df.set_index('Rank').drop(labels=['OWN'], axis=1)
        df=to_numeric(df)
        all_K.append(df)
    
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
        row[1] = re.sub(r'\s\(.*','', row[1])                                               #takes out the team initals using regex
        l.append(row)

    df = pd.DataFrame(l, columns=column_names)

    df = renaming_columns(df, URL)                                                            #renames the columns, adds the year, appends the DataFrames to a collective list for each position

end_year = 2020
start_year = 2015
for year in range(end_year, start_year, -1):
    fantasy_pros_scrape(f'https://www.fantasypros.com/nfl/stats/qb.php?year={year}&scoring=Standard')
    fantasy_pros_scrape(f'https://www.fantasypros.com/nfl/stats/rb.php?year={year}&scoring=Standard')
    fantasy_pros_scrape(f'https://www.fantasypros.com/nfl/stats/rb.php?year={year}&scoring=PPR')
    fantasy_pros_scrape(f'https://www.fantasypros.com/nfl/stats/wr.php?year={year}&scoring=Standard')
    fantasy_pros_scrape(f'https://www.fantasypros.com/nfl/stats/wr.php?year={year}&scoring=PPR')
    fantasy_pros_scrape(f'https://www.fantasypros.com/nfl/stats/te.php?year={year}&scoring=Standard')
    fantasy_pros_scrape(f'https://www.fantasypros.com/nfl/stats/te.php?year={year}&scoring=PPR')
    fantasy_pros_scrape(f'https://www.fantasypros.com/nfl/stats/k.php?year={year}&scoring=Standard')

##### ALL Postions #####
QB = pd.concat(all_QB).set_index(['Year','Player'])
RB_STD = pd.concat(all_RB_STD).set_index(['Year','Player'])
RB_PPR = pd.concat(all_RB_PPR).set_index(['Year','Player'])
WR_STD = pd.concat(all_WR_STD).set_index(['Year','Player'])
WR_PPR = pd.concat(all_WR_PPR).set_index(['Year','Player'])
TE_STD = pd.concat(all_TE_STD).set_index(['Year','Player'])
TE_PPR = pd.concat(all_TE_PPR).set_index(['Year','Player'])
K = pd.concat(all_K).set_index(['Year','Player'])

#example graphs
K.hvplot(x='FG', y='XPT', width=1200, height=800, kind='scatter', c='FPTS', colormap='viridis') #FG to XPTs
