import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd


### TOP 25 PASSING STATS 2020 ###

r = requests.get('https://www.nfl.com/stats/player-stats/category/passing/2020/REG/all/passingyards/desc')
passing_stats_2020 = bs(r.content)

table_2020 = passing_stats_2020.select('table.d3-o-table.d3-o-table--detailed.d3-o-player-stats--detailed.d3-o-table--sortable')[0] #scrapes the table
pass_columns = table_2020.find('thead').find_all('a') # finds all the column names except for the first one because of the site code 
pass_column_names = [c.string for c in pass_columns] #makes the column names into a list
player_names_2020 = table_2020.find('thead').find('th') #finds the first column name because of the site code as mentioned earlier
player = player_names_2020.string #parses the line of code to take out only the column name needed
pass_column_names.insert(0,player) #inserts the column name to the start of the list of column names
#the column names are ready

table_rows_2020 = table_2020.find('tbody').find_all('tr') #finds each players stats (each row of the table)

l = []
for tr in table_rows_2020:
    td = tr.find_all('td')
    row = [str(tr.get_text()).strip() for tr in td]
    l.append(row)

#creates a DataFrame with all the stats we want
df_2020_passing = pd.DataFrame(l, columns=pass_column_names)


### TOP 25 PASSING STATS 2019 ###

r = requests.get('https://www.nfl.com/stats/player-stats/category/passing/2019/REG/all/passingyards/desc')
passing_stats_2019 = bs(r.content)

table_2019 = passing_stats_2019.select('table.d3-o-table.d3-o-table--detailed.d3-o-player-stats--detailed.d3-o-table--sortable')[0] #scrapes the table
pass_columns = table_2019.find('thead').find_all('a') # finds all the column names except for the first one because of the site code 
pass_column_names = [c.string for c in pass_columns] #makes the column names into a list
player_names = table_2019.find('thead').find('th') #finds the first column name because of the site code as mentioned earlier
player = player_names.string #parses the line of code to take out only the column name needed
pass_column_names.insert(0,player) #inserts the column name to the start of the list of column names
#the column names are ready

#finds each players stats (each row of the table) and creates a list of each players stats
table_rows = table_2019.find('tbody').find_all('tr') 
l = []
for tr in table_rows:
    td = tr.find_all('td')
    row = [str(tr.get_text()).strip() for tr in td]
    l.append(row)

#creates a DataFrame with all the stats we want
df_2019_passing = pd.DataFrame(l, columns=pass_column_names)


