#! Python3
#LogisticR.py - run a logistics regression on the college basketball data scraped from sport reference.com

import preprocess
from sklearn import linear_model
from sklearn import metrics
import numpy
X_train, y_train, X_test, y_test = preprocess.get_data()
y_train = numpy.array(y_train)
y_test = numpy.array(y_test)

clf = linear_model.LogisticRegression(fit_intercept=False)
clf.fit(X_train, y_train)

prediction = clf.predict(X_test)
pred2 = clf.predict(X_train)

print(prediction)
print(metrics.accuracy_score(prediction, y_test))
print('\n')
print(pred2)
print(metrics.accuracy_score(pred2, y_train))

