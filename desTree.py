#! Python3 
# desTree.py -  uses as desicion tree classifier to attempt to predict NCAA tournament results. trains on data from 1939 - 2017

from sklearn import tree
import sklearn.metrics as met
import numpy
import preprocess as pre

X_train, y_train, X_test, y_test = pre.get_data()
acc = []
for i in range(2,500):
    clf = tree.DecisionTreeClassifier(min_samples_split=i)
    clf.fit(X_train, y_train)

    prediction = clf.predict(X_test)

    acc.append(met.accuracy_score(prediction, y_test))


print(acc)
print(max(acc), acc.index(max(acc)))