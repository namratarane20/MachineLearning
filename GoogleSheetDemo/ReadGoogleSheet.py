# program to read data from google sheet and add records same google sheet.
import gspread
from df2gspread import df2gspread as d2g
# import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
def readSheet():
    scope= ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
    credentials =ServiceAccountCredentials.from_json_keyfile_name('newCred.json', scope)
    gc =gspread.authorize(credentials)
    gc.create("my new sheet ")

    wks =gc.open("Lobsters trial Sheet").sheet1
    # wks.insert_row(['username','user desi','user mail id','new age'])
    # gc.create('my new sheet')
    # wks.add_rows(['hellow','hello','helllo','heloo'])

    data = wks.get_all_values()
    print('my all google sheet data----',data, type(data))
    print()
    print()
    headers = data.pop(0)
    dataFrame =pd.DataFrame(data,columns=headers)
    print('My google sheet records=========')
    print(dataFrame)


    # dataFrame['newCol']=['val0','val1','val2','val3','val4','val5','val6']



    # d2g.upload(dataFrame, spreadsheet_key, wks_name, credentials=credentials, row_names=True)
    # print('dataframe after adding====================================')
    # print(dataFrame)
readSheet()