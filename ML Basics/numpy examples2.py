#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
np.arange(0,20,2)


# In[ ]:


np.zeros((3,6))


# In[ ]:


np.ones((4,6))


# In[ ]:


np.random.randint(1,100,(6,6))


# In[ ]:


import numpy as np
np.random.randint(0,100,10)


# In[59]:


np.random.seed(1)
np.random.randint(0,100,10)


# In[8]:


import numpy as np
np.random.seed(1)
np.random.randint(0,100,10)


# In[9]:


np.random.seed(1)
myArray=np.random.randint(0,100,32)
print('this is my randon ones time array=========',myArray)
print('this is the maximum numner form my array==',myArray.max())
print('this is the minimum number from array=====',myArray.min())
print('this is the mean value of my array========',myArray.mean())
print('index  value of maximum numberin arary====',myArray.argmax())
print('index  value of manimum numberin arary====',myArray.argmin())
print('add the array in matrix form like ========',myArray.reshape(4,8))


# In[10]:


np.random.seed() # if we didnt menton any number as seed parameter our values will change continuesly it will not take once tiem random number
np.random.randint(0,100,100).reshape(10,10)


# In[11]:


matrix =np.random.randint(0,100,100).reshape(10,10)
matrix


# In[22]:


print(matrix[5,4])
print(matrix[3,7])

print(matrix[8,6])
print(matrix[:,0])#it will take 0 th  position coloumn.
print(matrix[:,3])#it will take 3 rd position coiulmn.
print(matrix[0,:])# it will take 0 th positon row.
print(matrix[7,:])# it will take 7th postion row.
print(matrix[0:3,0:5])# it will print the matrix row 3 and col 5

