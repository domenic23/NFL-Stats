import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd


#making a function to extract the stats from nfl.com
def nfl_stats_scrape(URL): #URL is a list of links. each link is a string

    html_table_lookup = 'table.d3-o-table.d3-o-table--detailed.d3-o-player-stats--detailed.d3-o-table--sortable' #NFL.com's html name for the tables they use
    df_list = [] #the list of DataFrames to be concatenated

    for link in URL: #iterates through the list of links 
        r = requests.get(link)
        stats = bs(r.content)
        table = stats.select(html_table_lookup)[0] #scrapes the table
        columns = table.find('thead').find_all('a') #finds the column names except for the first one because of the site code
        column_names = [c.string for c in columns] #makes the column names into a list
        player_names = table.find('thead').find('th') #finds the first column name because of the site code issue mentioned earlier
        player = player_names.string #parses the line of code to take out only the column name needed
        column_names.insert(0,player) #inserts the column name to the start of the list of column names

        #finds each players stats (each row of the table)
        table_rows = table.find('tbody').find_all('tr')
        l = []
        for tr in table_rows:
            td = tr.find_all('td')
            row = [str(tr.get_text()).strip() for tr in td]
            l.append(row)

        #creates a DataFrame with all the stats we want and appends that DataFrame to a list of DataFrames 
        df = pd.DataFrame(l, columns=column_names)
        df_list.append(df)
    
    result = pd.concat(df_list, ignore_index=True) #concatenates the list of DataFrames into 1 large DataFrame and returns it

    return result


#top 50 passing stats 2020 example
passing2020_25 = 'https://www.nfl.com/stats/player-stats/category/passing/2020/REG/all/passingyards/desc'
passing2020_50 = 'https://www.nfl.com/stats/player-stats/category/passing/2020/REG/all/passingYards/DESC?aftercursor=0000001900000000008500100079000840a47800000000006e00000005000000045f74626c00000010706572736f6e5f7465616d5f737461740000000565736249640000000957454e36313537373000000004726f6c6500000003504c5900000008736561736f6e496400000004323032300000000a736561736f6e5479706500000003524547f07fffffe6f07fffffe6dfa1ba79872e6c9d5e6282cd124308e70004'
all_passing2020 = [passing2020_25, passing2020_50]

passing_2020 = nfl_stats_scrape(all_passing2020)

#top 50 rushing stats 2020 example
rushing2020_25 = 'https://www.nfl.com/stats/player-stats/category/rushing/2020/REG/all/rushingyards/desc'
rushing2020_50 = 'https://www.nfl.com/stats/player-stats/category/rushing/2020/REG/all/rushingYards/DESC?aftercursor=0000001900000000008500100079000840857800000000006e00000005000000045f74626c00000010706572736f6e5f7465616d5f737461740000000565736249640000000953494e31383639313900000004726f6c6500000003504c5900000008736561736f6e496400000004323032300000000a736561736f6e5479706500000003524547f07fffffe6f07fffffe64de1d501a1e1179aa2471f5c05c264300004'
all_rushing2020 = [rushing2020_25, rushing2020_50]

rushing_2020 = nfl_stats_scrape(all_rushing2020)

#when trying to call 2 DataFrames at the same time like shown below, it only outputs the last DataFrame specified
passing_2020
rushing_2020