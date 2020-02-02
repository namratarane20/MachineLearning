#!/usr/bin/env python
# coding: utf-8

# In[17]:


import matplotlib.pyplot as plt
import numpy as np
states =['maha','andhra','mp','karnataka','up','kerala']
quantity = [70,30,20,40,55,20]
color = ['red','orange','blue','yellow','green','m']
plt.pie(quantity,labels=states,colors=color,startangle=90,shadow=True,explode=(0,0,0,0.2,0,0),autopct='%1.2f%%')
plt.legend()
plt.show()

