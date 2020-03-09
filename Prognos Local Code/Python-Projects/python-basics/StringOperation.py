import re
def extract():
        str1="123@#$ABCDEFnarata"
        print('this is initial string',str)
        res1 = "".join(re.split("[^a-zA-Z]*",str1))
        print('this is my extracted string',res1)

        print(str1.replace('@' ,'I AM HERE'))

extract()