#! Python3
#LogisticR.py - run a logistics regression on the college basketball data scraped from sport reference.com

import models.preprocess as pre
from sklearn import linear_model
from sklearn import metrics
import numpy

def train_model():
    X_train, y_train, X_test, y_test = pre.get_data()
    y_train = numpy.array(y_train)
    y_test = numpy.array(y_test)

    clf = linear_model.LogisticRegression(fit_intercept=False)
    clf.fit(X_train, y_train)
    return clf

model = train_model()

