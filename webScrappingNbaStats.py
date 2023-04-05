# Necessary imports for the scraping and data collection to work.
import pandas as pd
import requests
pd.set_option('display.max_columns', None)
import time
import numpy as np

# You can find the URL within the nba stats website:
# - Leaders > Official Leaders: find the stats that you want to work with (per game, totals, regular season, playoffs, etc)
# - Inspect the website and go to network (propably must refresh the page)
# - In the filters search for leagueLeader: this will be the url that we can manipulate later on
teste = 'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season=2012-13&SeasonType=Regular%20Season&StatCategory=PTS'

r1 = requests.get(url=teste).json()

# The table headers will be later used on our dataFrame.
table_headers = r1['resultSet']['headers']
table_headers

# Adjusting the content of the url in a dataFrame, with results and rows now aligned with the headers.
pd.DataFrame(r1['resultSet']['rowSet'], columns = table_headers)

# This is the base of our **for loop**, we have now 3 temporary dataframes that will later iterate through the years and the season types (in this case regular or playoffs).
temp_df1 = pd.DataFrame(r1['resultSet']['rowSet'], columns = table_headers)
temp_df2 = pd.DataFrame({'Year':['2012-13' for i in range(len(temp_df1))], 'Season_type':['Regular%20Season' for i in range(len(temp_df1))]})
temp_df3 = pd.concat([temp_df2, temp_df1], axis=1)
temp_df3

del temp_df1, temp_df2, temp_df3

# Adding years and season types to the columns of the dataframe.
df_cols = ['Year', 'Season_type'] + table_headers
pd.DataFrame(columns=df_cols)

# In this part, you can in your click your URL and then find _headers_, then in the lower part, search for your requisition headers, you will need this in the for loop.
headers = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
'Accept-Encoding':'gzip, deflate, br',
'Accept-Language':'pt-BR,pt;q=0.8,en-US;q=0.5,en;q=0.3',
'Connection':'keep-alive',
'Host':'stats.nba.com',
'Sec-Fetch-Dest':'document',
'Sec-Fetch-Mode':'navigate',
'Sec-Fetch-Site':'none',
'Sec-Fetch-User':'?1',
'TE':'trailers',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'
}

# The for loop works within each year and then each season type, the url will be searched through our string manipulation and the data concatenated in the **df**.
# In this case, regular season and playoffs in the latest 10 years were the parameters chosen, per game data. But this can be easily changed depending your demand.
df = pd.DataFrame(columns=df_cols)
season_types = ['Regular%20Season', 'Playoffs']
years = ['2012-13', '2013-14', '2014-15', '2015-16', '2016-17', '2017-18', '2018-19', '2019-20', '2020-21', '2021-22']

begin_loop = time.time()

for y in years:
  for s in season_types:
    api_url = 'https://stats.nba.com/stats/leagueLeaders?LeagueID=00&PerMode=PerGame&Scope=S&Season=' +y+ '&SeasonType=' +s+ '&StatCategory=PTS'
    r = requests.get(url=api_url, headers=headers).json()
    temp_df1 = pd.DataFrame(r['resultSet']['rowSet'], columns = table_headers)
    temp_df2 = pd.DataFrame({'Year':[y for i in range(len(temp_df1))],
                            'Season_type':[s for i in range(len(temp_df1))]})
    temp_df3 = pd.concat([temp_df2, temp_df1], axis=1)
    df = pd.concat([df, temp_df3], axis=0)
    print(f'Finished scraping data for the {y} {s}.')
    lag = np.random.uniform(low=5, high=40)
    print(f'Waiting {round(lag, 1)} seconds.')
    time.sleep(lag)

print(f'Process completed. Total run time {round((time.time()-begin_loop)/60,2)} min.')
df.to_excel('nba_player_data.xlsx', index=False)

# The output is a **xlsx** file that you can work with and proceed with the analysis.