#second week homework at HSE cours of ML
#programmer fraIoann i_ingar@mail.ru
#written 28/07/2021
#dataset Wine from 
#https://archive.ics.uci.edu/ml/machine-learning-databases/wine/wine.data 
#was used here

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import scale 
import pandas as pd

def writer (i, ans):
    #function writes an answer to .txt file in the work directory
    #function gets number of answer and information have to be written
    #and save answer .txt file with suitable index
    #let's open file, insert answer number as file index, 
    #write  and close the file
    MyFile = open('Answer_{index}.txt'.format(index = i), 'w')
    print(ans, file=MyFile, end="")
    MyFile.close()

def valid_score(X, Y):
    score = []
    for k in range(1, 51):
        kf = KFold(n_splits = 5, random_state = 42, shuffle = True)
        kNN = KNeighborsClassifier(n_neighbors = k)
        score.append(cross_val_score(kNN, X, Y, cv = kf, scoring = 'accuracy').mean())
    return score.index(max(score)), max(score)

data = pd.read_csv('wine.data', names = range(0, 14))
Y = data.iloc[:, 0]
X = data.iloc[:, 1:]

k, K = valid_score(X, Y)
writer(1, k)
writer(2, K)

k, K = valid_score(scale(X), Y)
answer = '{} {}'.format(k, K)
writer(3, k)
writer(4, K)

