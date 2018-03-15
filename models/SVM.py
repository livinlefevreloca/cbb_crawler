#! Python3 
# SVM.py - uses support vector machine to attempt predcit NCAA tournament results trained on the data from past years.

import models.preprocess as pre
from sklearn import svm
import sklearn.metrics as met
import numpy as np

X_train, y_train, X_test, y_test = pre.get_data()

def train_model():
   
    clf = svm.SVC(kernel='sigmoid', C=0.01)
    clf.fit(X_train, y_train)
    return clf
    
    
model = train_model()




