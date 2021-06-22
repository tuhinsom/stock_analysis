import datetime
import os
from os import path

import pandas as pd
import json

curr_year_till_date_stocks_file = r'Export_DataFrame.json'

main_df = None
if(path.exists(curr_year_till_date_stocks_file)):
    main_df = pd.read_json(curr_year_till_date_stocks_file)
    main_df['TIMESTAMP']= pd.to_datetime(main_df['TIMESTAMP'])
    main_df['DIFF']= main_df['PREVCLOSE'] - main_df['CLOSE']

if(main_df is not None):
	# print(main_df.info())

	# (4498, 5) records from '2020-06-15' to '2020-06-19'
	# print(main_df[(main_df['TIMESTAMP'] > '2020-06-15') & (main_df['TIMESTAMP'] < '2020-06-19')])
	# print(main_df[(main_df['TIMESTAMP'] >= '2020-06-15') & (main_df['TIMESTAMP'] <= '2020-06-19')].groupby(['SYMBOL','TIMESTAMP']).head(10))
	print(main_df[(main_df['TIMESTAMP'] >= '2020-06-12') & (main_df['TIMESTAMP'] <= '2020-06-19') & (main_df['SYMBOL'] == 'TITAN')].sort_values(by=['SYMBOL']).head(10))