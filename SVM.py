#! Python3 
# SVM.py - uses support vector machine to attempt predcit NCAA tournament results trained on the data from past years.

import preprocess as pre
from sklearn import svm
import sklearn.metrics as met
import numpy as np



def train_model():
    X_train, y_train, X_test, y_test = pre.get_data()
    clf = svm.SVC(kernel='rbf', C=1)
    clf.fit(X_train, y_train)
    print(X_test)
    return clf



