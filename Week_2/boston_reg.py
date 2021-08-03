#second week homework at HSE cours of ML
#programmer fraIoann i_ingar@mail.ru
#written 03/08/2021


from sklearn import datasets
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import scale 
import numpy

def writer (i, ans):
    #function writes an answer to .txt file in the work directory
    #function gets number of answer and information have to be written
    #and save answer .txt file with suitable index
    #let's open file, insert answer number as file index, 
    #write  and close the file
    MyFile = open('Answer_{index}.txt'.format(index = i), 'w')
    print(ans, file = MyFile, end = "")
    MyFile.close()

#let's take a dataset boston from library and scale data
boston = datasets.load_boston()
boston.data = scale(boston.data)
#form an empty list to write cross correlation values
score = []
#make a fold for cross correlation
cv = KFold(n_splits = 5, random_state = 42, shuffle = True)
#iterate p (weights) - metrics parameter, call regression and cross correlation
for i in numpy.linspace(1, 10, num = 200):
    reg = KNeighborsRegressor(n_neighbors = 5, weights = 'distance',  p = i)
    score.append(cross_val_score(reg, boston.data, boston.target, cv = cv, 
                                 scoring = 'neg_mean_squared_error').mean())

best_score, num = max(score), score.index(max(score))
#we write a num + 1, 'cause indexes in list start from zero
writer(5, num + 1)