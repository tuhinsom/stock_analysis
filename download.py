import datetime
import os
from os import path

import urllib
from urllib.request import urlopen
from zipfile import ZipFile

import pandas as pd
import json
curr_year_till_date_stocks_file = r'Export_DataFrame.json'

if(path.exists(curr_year_till_date_stocks_file)):
    main_df = pd.read_json(curr_year_till_date_stocks_file)
else:        
    main_df = None


def updateDataframe(file_csv) :
    global main_df
    temp_df = pd.read_csv(file_csv)
    temp_df = temp_df[temp_df['SERIES'] == 'EQ']
    if(main_df is not None):
        main_df = pd.concat([main_df, temp_df[['SYMBOL', 'OPEN', 'CLOSE', 'PREVCLOSE', 'TIMESTAMP']]], ignore_index=True, sort=True)
        # main_df.append(temp_df[['SYMBOL', 'OPEN', 'CLOSE', 'PREVCLOSE', 'TIMESTAMP']], ignore_index=True)
    else :
        main_df = temp_df[['SYMBOL', 'OPEN', 'CLOSE', 'PREVCLOSE', 'TIMESTAMP']]
    # print(temp_df[['SYMBOL', 'OPEN', 'CLOSE', 'PREVCLOSE', 'TIMESTAMP']].head())





from os import path
data = {}
if(path.exists("config.json")):
    with open('config.json') as json_file:
        data = json.load(json_file)
        last_end_date = datetime.datetime.strptime(data['range_end_date'], '%Y/%m/%d').date()
        initdelta = datetime.timedelta(days=1)
        start_date = last_end_date + initdelta 
else:
    # end_date = datetime.date(2020, 1, 2) #temporary, actual will be till current date
    # range of dates to pull files from NSE
    start_date = datetime.date(2020, 1, 1)
    data['range_end_date'] = start_date.strftime("%Y") + '/' + start_date.strftime("%m") + '/' + start_date.strftime("%d")
    with open('config.json', 'w') as outfile:
        json.dump(data, outfile)

end_date = datetime.date.today()

delta = datetime.timedelta(days=1)

b = 0
while start_date <= end_date:
    if(start_date.strftime("%a") != 'Sun' and start_date.strftime("%a") != 'Sat') :
        b += 1
        csv_file = 'cm'+ start_date.strftime("%d") + start_date.strftime("%b").upper() + start_date.strftime("%Y") +'bhav.csv'
        zipurl = 'https://www1.nseindia.com/content/historical/EQUITIES/'+start_date.strftime("%Y")+'/'+ start_date.strftime("%b").upper() +'/'+ csv_file + '.zip'
        try: 
            # Download the file from the URL
            zipresp = urlopen(zipurl)
            # Create a new file on the hard drive
            tempzip = open("/home/tuhin/workspace/python/stock_analysis/tempfile.zip", "wb")
            # Write the contents of the downloaded file into the new file
            tempzip.write(zipresp.read())
            # Close the newly-created file
            tempzip.close()
            # Re-open the newly-created file with ZipFile()
            zf = ZipFile("tempfile.zip")
            # Extract its contents into <extraction_path>
            # note that extractall will automatically create the path
            zf.extractall(path = '/home/tuhin/workspace/python/stock_analysis')
            # close the ZipFile instance
            zf.close()
            updateDataframe(csv_file)
            # print(main_df.shape)
            
            # os.remove(csv_file)
        except urllib.request.HTTPError as exception: 
            print("exception downloading :" + csv_file) 
        
        print (csv_file)

    # break
    start_date += delta

main_df.to_json (curr_year_till_date_stocks_file)
print (b)


