#!/usr/bin/env python
# coding: utf-8

# In[1]:


var =0 
while var <=10:
    print('this is my var',var)
    var+=1
    


# In[3]:


string ='namrata ashok rane'
myitre = iter(string)
print(myitre)
print(next(myitre))


# In[4]:


string ='namrata ashok rane'
for char in iter(string):
    print(char)


# In[5]:


myList =['namrata','nikita','piyush','latiket']
for listItem in myList:
    for char in iter(listItem):
        print(char)

