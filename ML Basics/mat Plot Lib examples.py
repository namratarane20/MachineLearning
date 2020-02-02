#!/usr/bin/env python
# coding: utf-8

# In[48]:


import matplotlib.pyplot as plt
x= [1,2,3,4,5,6,7,8]
y= [1,4,6,5,7,8,9,1]
plt.plot(x,y)
plt.xlabel('x data')
plt.ylabel('y data')
plt.title('my data is ploted here')
plt.show()




# In[53]:


import numpy as np
newX=np.random.randint(0,100,10)
newY = np.random.randint(0,100,10)
print(newX)
print(newY)
plt.plot(newX,newY)
plt.xlabel('random X')
plt.ylabel('random Y')
plt.title('this is random data plotting')
plt.show()

