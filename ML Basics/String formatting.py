#!/usr/bin/env python
# coding: utf-8

# In[5]:


name = 'namrata'
add = 'banglore'
msg = name+ ' at '+ add +'this is add'
print(msg)


# In[7]:


msg2 ='{} {}.hoe are you ?'.format(name , add)
print(msg2)


# In[11]:


msg3 = 'getais is =='.format(name , add)
print(msg3)


# In[14]:


msg4 = f'{name} at {add}.how are you {name}'
print(msg4)


# In[15]:


msg4 = f'{name} , {add}.how are you {name}'
print(msg4)


# In[17]:


print(msg4)


# In[19]:


print(msg4.lower())
print(msg4.upper())
print(msg4.__len__())
print(len(msg4))
print(msg4.count('n'))
print(msg4.find('how'))
print(msg4[10])
print(msg4[0:10])

