class Dictinaries:
    stud={'name':'namarat','id':'tc114'}
dictObj= Dictinaries()
print(dictObj.stud.items())
print(dictObj.stud.keys())
print(dictObj.stud.values())
print(dictObj.stud.copy())

# print one bye one keys
stud={'name':'namarat','id':'tc114'}
for i in stud.keys():
   # print('this is keys extrcted sparately')
    print(i)
