# rpogram to create google sheet and share it person through maid id,and read data from google sheet.

import gspread
import pandas as pd
from df2gspread import df2gspread as d2g
from oauth2client.service_account import ServiceAccountCredentials
def dataFrametoGooglesheet():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('newCred.json', scope)
    gc = gspread.authorize(credentials)

    # googleSheet = gc.create(" Emplyoyee data")
    # googleSheet.share(['namratarane33@gmail.com','service-account@importing-sheet.iam.gserviceaccount.com'],perm_type='user',role='writer')

    wks = gc.open(" Emplyoyee data").sheet1




    sheetRecords = wks.get_all_values()
    # headers = sheetRecords.pop(0)
    dataFrame = pd.DataFrame(sheetRecords)
    print('=============== my google sheet ====================')
    print(dataFrame)

    # wks = gc.open("added sheet").sheet1

    print('sheet created ')
    # data = wks.get_all_values()
dataFrametoGooglesheet()