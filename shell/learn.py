#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'

def read(filename):
    X = []
    Y = []
    ids = []
    for line in open(filename):
        arr = line.strip().split(",")
        y = int(arr[0])
        ids.append(arr[1])
        x = [float(k) for k in arr[2:]]
        X.append(x)
        Y.append(y)
    return X,Y,ids

from sklearn import linear_model, decomposition, datasets
from sklearn.pipeline import Pipeline
from sklearn.grid_search import GridSearchCV
from sklearn import cross_validation
from sklearn import metrics
import logging
import logging.config
import sys
logging.config.fileConfig("log.conf")
logger = logging.getLogger("example")

X_train, y_train, ids_train = read(sys.argv[1])
X_test, y_test, ids_test = read(sys.argv[2])
is_valid=int(sys.argv[4])

clf = linear_model.LogisticRegression()
scores = cross_validation.cross_val_score(clf, X_train, y_train, cv=5)
logger.info(scores)
print scores
clf.fit(X_train, y_train)
preds = clf.predict(X_test)
preds = clf.predict_proba(X_test)
if is_valid:
    roc_auc = metrics.roc_auc_score(y_test, preds[:,1])
    logger.info(roc_auc)
    print roc_auc
fout = open(sys.argv[3], "w")
for i in range(len(ids_test)):
    fout.write("%s,%.3f\n" % (ids_test[i], preds[i,1]) )
fout.close()
if is_valid:
    fout = open(sys.argv[3]+".debug", "w")
    for i in range(len(ids_test)):
        fout.write("%s,%.3f,%d\n" % (ids_test[i], preds[i,1], y_test[i]) )
    fout.close()
