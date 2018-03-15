#! Python3 
# desTree.py -  uses as desicion tree classifier to attempt to predict NCAA tournament results. trains on data from 1939 - 2017

from sklearn import tree
import sklearn.metrics as met
import numpy
import models.preprocess as pre
X_train, y_train, X_test, y_test = pre.get_data()
def train_model():
    
    clf = tree.DecisionTreeClassifier(min_samples_split=500)
    clf.fit(X_train, y_train)
    return clf

model = train_model()

# preds = model.predict(X_test)
# print(met.accuracy_score(y_test, preds))


