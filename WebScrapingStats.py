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

### PASSING ###

#top 50 passing stats 2020
passing2020_25 = 'https://www.nfl.com/stats/player-stats/category/passing/2020/REG/all/passingyards/desc'
passing2020_50 = 'https://www.nfl.com/stats/player-stats/category/passing/2020/REG/all/passingYards/DESC?aftercursor=0000001900000000008500100079000840a47800000000006e00000005000000045f74626c00000010706572736f6e5f7465616d5f737461740000000565736249640000000957454e36313537373000000004726f6c6500000003504c5900000008736561736f6e496400000004323032300000000a736561736f6e5479706500000003524547f07fffffe6f07fffffe6dfa1ba79872e6c9d5e6282cd124308e70004'
all_passing2020 = [passing2020_25, passing2020_50]
passing_2020 = nfl_stats_scrape(all_passing2020)

#top 50 passing stats 2019
passing2019_25 = 'https://www.nfl.com/stats/player-stats/category/passing/2019/REG/all/passingyards/desc'
passing2019_50 = 'https://www.nfl.com/stats/player-stats/category/passing/2019/REG/all/passingYards/DESC?aftercursor=0000001900000000008500100079000840a7a000000000006e00000005000000045f74626c00000010706572736f6e5f7465616d5f737461740000000565736249640000000944415234363631343100000004726f6c6500000003504c5900000008736561736f6e496400000004323031390000000a736561736f6e5479706500000003524547f07fffffe6f07fffffe6389bd3f93412939a78c1e6950d620d060004'
all_passing2019 = [passing2019_25, passing2019_50]
passing_2019 = nfl_stats_scrape(all_passing2019)

#top 50 passing stats 2018
passing2018_25 = 'https://www.nfl.com/stats/player-stats/category/passing/2018/REG/all/passingyards/desc'
passing2018_50 = 'https://www.nfl.com/stats/player-stats/category/passing/2018/REG/all/passingYards/DESC?aftercursor=0000001900000000008500100079000840a40c00000000006e00000005000000045f74626c00000010706572736f6e5f7465616d5f737461740000000565736249640000000944414c36353939303000000004726f6c6500000003504c5900000008736561736f6e496400000004323031380000000a736561736f6e5479706500000003524547f07fffffe6f07fffffe623180417c19bbf751691912234060a980004'
all_passing2018 = [passing2018_25, passing2018_50]
passing_2018 = nfl_stats_scrape(all_passing2018)

### RUSHING ###

#top 50 rushing stats 2020
rushing2020_25 = 'https://www.nfl.com/stats/player-stats/category/rushing/2020/REG/all/rushingyards/desc'
rushing2020_50 = 'https://www.nfl.com/stats/player-stats/category/rushing/2020/REG/all/rushingYards/DESC?aftercursor=0000001900000000008500100079000840857800000000006e00000005000000045f74626c00000010706572736f6e5f7465616d5f737461740000000565736249640000000953494e31383639313900000004726f6c6500000003504c5900000008736561736f6e496400000004323032300000000a736561736f6e5479706500000003524547f07fffffe6f07fffffe64de1d501a1e1179aa2471f5c05c264300004'
all_rushing2020 = [rushing2020_25, rushing2020_50]
rushing_2020 = nfl_stats_scrape(all_rushing2020)

#top 50 rushing stats 2019
rushing2019_25 = 'https://www.nfl.com/stats/player-stats/category/rushing/2019/REG/all/rushingyards/desc'
rushing2019_50 = 'https://www.nfl.com/stats/player-stats/category/rushing/2019/REG/all/rushingYards/DESC?aftercursor=0000001900000000008500100079000840883800000000006e00000005000000045f74626c00000010706572736f6e5f7465616d5f737461740000000565736249640000000953494e31383639313900000004726f6c6500000003504c5900000008736561736f6e496400000004323031390000000a736561736f6e5479706500000003524547f07fffffe6f07fffffe691de5008d799f9ba761cb0a998ca30040004'
all_rushing2019 = [rushing2019_25, rushing2019_50]
rushing_2019 = nfl_stats_scrape(all_rushing2019)

#top 50 rushing stats 2018
rushing2018_25 = 'https://www.nfl.com/stats/player-stats/category/rushing/2018/REG/all/rushingyards/desc'
rushing2018_50 = 'https://www.nfl.com/stats/player-stats/category/rushing/2018/REG/all/rushingYards/DESC?aftercursor=0000001900000000008500100079000840869000000000006e00000005000000045f74626c00000010706572736f6e5f7465616d5f7374617400000005657362496400000009474f5234313131373100000004726f6c6500000003504c5900000008736561736f6e496400000004323031380000000a736561736f6e5479706500000003524547f07fffffe6f07fffffe6ce7efc6cd468fdd6b52ad0199e454a1e0004'
all_rushing2018 = [rushing2018_25, rushing2018_50]
rushing_2018 = nfl_stats_scrape(all_rushing2018)

### RECEIVING ###

#top 50 receiving stats 2020
receiving2020_25 = 'https://www.nfl.com/stats/player-stats/category/receiving/2020/REG/all/receivingreceptions/desc'
receiving2020_50 = 'https://www.nfl.com/stats/player-stats/category/receiving/2020/REG/all/receivingReceptions/DESC?aftercursor=0000001900000000008500100079000840534000000000006e00000005000000045f74626c00000010706572736f6e5f7465616d5f737461740000000565736249640000000953414d36333332383500000004726f6c6500000003504c5900000008736561736f6e496400000004323032300000000a736561736f6e5479706500000003524547f07fffffe6f07fffffe645ebb01fc753cce25ebecff43a8c12a80004'
all_receiving2020 = [receiving2020_25, receiving2020_50]
receiving_2020 = nfl_stats_scrape(all_receiving2020)
receiving_2020 = receiving_2020.drop(columns='Rec YAC/R')

#top 50 receiving stats 2019
receiving2019_25 = 'https://www.nfl.com/stats/player-stats/category/receiving/2019/REG/all/receivingreceptions/desc'
receiving2019_50 = 'https://www.nfl.com/stats/player-stats/category/receiving/2019/REG/all/receivingReceptions/DESC?aftercursor=0000001900000000008500100079000840530000000000006e00000005000000045f74626c00000010706572736f6e5f7465616d5f7374617400000005657362496400000009464f5535363439373000000004726f6c6500000003504c5900000008736561736f6e496400000004323031390000000a736561736f6e5479706500000003524547f07fffffe6f07fffffe64e1657f75ee423642998069ba578dfcd0004'
all_receiving2019 = [receiving2019_25, receiving2019_50]
receiving_2019 = nfl_stats_scrape(all_receiving2019)
receiving_2019 = receiving_2019.drop(columns='Rec YAC/R')
#top 50 receiving stats 2018
receiving2018_25 = 'https://www.nfl.com/stats/player-stats/category/receiving/2018/REG/all/receivingreceptions/desc'
receiving2018_50 = 'https://www.nfl.com/stats/player-stats/category/receiving/2018/REG/all/receivingReceptions/DESC?aftercursor=0000001900000000008500100079000840530000000000006e00000005000000045f74626c00000010706572736f6e5f7465616d5f737461740000000565736249640000000948494c37373534343900000004726f6c6500000003504c5900000008736561736f6e496400000004323031380000000a736561736f6e5479706500000003524547f07fffffe6f07fffffe625b1f5ad2f52ff079546ce03cf3b3ac60004'
all_receiving2018 = [receiving2018_25, receiving2018_50]
receiving_2018 = nfl_stats_scrape(all_receiving2018)
receiving_2018 = receiving_2018.drop(columns='Rec YAC/R')
