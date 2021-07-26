#first week homework at HSE cours of ML
#programmer fraIoann i_ingar@mail.ru
#written 25/07/2021
#dataset titanic from kaggle.com/datasets was used here

import pandas as pd
from collections import Counter

def writer (i, ans):
    #function writes an answer to .txt file in the work directory
    #function gets number of answer and information have to be written
    #and save answer .txt file with suitable index
    #let's open file, insert answer number as file index, 
    #write  and close the file
    MyFile = open('Answer_{index}.txt'.format(index = i), 'w')
    print(ans, file=MyFile, end="")
    MyFile.close()

#reading from csv series oriented by passenger ID
data = pd.read_csv('train.csv', index_col = 'PassengerId')


#filtration, for example, could be done by two methods
male = data.Sex.isin(['male']).size
female = data[data['Sex'] == 'female'].Sex.size
#for uniform use a writer function all values converted to string
answer = str(male) + ' ' + str(female)
writer(1, answer)

#calculate a percentage of survivors and 1t class passengers
#two methods of filtration are presented as above
survived_ratio = data.Survived.isin([1]).size / data.Survived.size *100
survived_ratio = round(survived_ratio, 2)
writer(2, survived_ratio)

first_class_ratio = data[data['Pclass'] == 1].Pclass.size / data.Pclass.size *100
first_class_ratio = round(first_class_ratio, 2)
writer(3, first_class_ratio)

#calculate age series mean and median
mean_age = data['Age'].mean()
median_age = data['Age'].median()
answer = str(mean_age) + ' ' + str(median_age)
writer(4, answer)

#let's see the Pirson correlation coef between number of sibs/sisters/partners
#and parents/children
corr_coef = data.SibSp.corr(data.Parch)
writer(5, corr_coef)

#below we try to find most common female name
#first let's filter only female passengers
#next try to define a special marks associated with thouse names
'''note that Mrs. and Miss. are not enough! thus we lose 5 woomen
in more common case better to use str.casefold() or str.lower()
during filtration because different registers could noise name series'''
#next filtering and chosing thirst female names and making a list 
#finally using a Counter, find a most common name
#another way is to chose and split strings with full names
#and count all names separately
names = data[data['Sex'] == 'female'].Name
marks = ['Mrs. ', 'Miss. ', 'Mme. ', 'Mlle. ', 'Dr. ']
names_list = []
for i in range(names.size):
    x = names.iloc[i]
    for mark in marks:
        if mark in x:
            x = x[x.find(mark) + len(mark):]
        elif '(' in x:
            x = x[x.find('(') + 1: x.find(')')]
        else:
            x = x
    names_list += x.split()[:1]   
name_found = Counter(names_list).most_common(1)[0][0]
writer(6, name_found)

      
