import pandas as pd
def readCSV():
    dataFrame = pd.read_csv("C:/Users/namrata.ashok/Downloads/LobstersTeam.csv")
    print(dataFrame.drop(columns=['Country']))
    # print(dataFrame.sort_values('Country', ascending = True))
    # print(dataFrame.sort_values(['Name','Email']))
    # dataFrame['age']='90'
    # print(dataFrame)
    # myNameList = dataFrame.Name

    # myMailList = dataFrame.Email
    # mailList = list(myMailList)
    # newList = list(myNameList)
    # print(newList)
    # nameAndMailDict ={}
    # for name in newList:
    #     for mail in mailList:
    #         nameAndMailDict.update({name:mail})
    #
    # print(nameAndMailDict)
    # print(dataFrame.Name)
    # print(dataFrame[['Name','Email']])
    # print(dataFrame.head(2))
    # print(dataFrame.iloc[0])
    # print(dataFrame.iloc[1:4])
    # print(dataFrame)
    # print(dataFrame.iloc[3,1])



    # print(dataFrame.loc[dataFrame['Country']=='France'])
    # print(dataFrame.describe())



readCSV()