#!/usr/bin/env python
# coding: utf-8

# In[1]:


for i in range(0,10):
    print(i)


# In[4]:


for i in range(0,11):
    print("num is ======{} square is====== {} cube is====== {}".format(i,i*i,i*i*i))
    


# In[8]:


def function1():
    name = str(input('ennter your name '))
    age = int(input('enter your age '))
    print('name = ',name)
    print( 'and age is ',age)
function1()


# In[12]:


def function1():
    name = str(input('ennter your name '))
    age = int(input('enter your age '))
    print('name = ',name)
    print( 'and age is ',age)
function1()


# In[14]:


def multipy():
    num1 = int(input('enter 1 st num'))
    num2 = int(input('enter 2nd st num'))
    mul = num1 * num2
    return mul
multipy()


# In[16]:


def multipy():
    num1 = int(input('enter 1 st num'))
    num2 = int(input('enter 2nd st num'))
    mul = num1 * num2
    return mul
multiplication = multipy()
print('function value is ===',multiplication)


# In[17]:


def multipy(num1,num2):
    
    mul = num1 * num2
    print('multiplocation is',mul)
multipy(70,3)

   

