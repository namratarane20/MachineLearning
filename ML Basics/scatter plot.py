#!/usr/bin/env python
# coding: utf-8

# In[9]:


import matplotlib.pyplot as plt
x = [2,7,4,6,3,2,5,9,1,8]
y=  [6,3,9,1,5,2,8,4,2,1]
plt.scatter(x,y,label="Stars",color='red',s=30,marker='*')
plt.xlabel('x-axis')
plt.ylabel('y-axis')
plt.title('scatter plot')
plt.legend()
plt.show()

