#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""
import sys
__revision__ = '0.1'
for line in open("train2/enrollment_train.csv"):
    id = line.split(",")[0]
    if id == sys.argv[1]:
        print line.strip()
        cid = line.strip().split(",")[-1]
for line in open("train2/log_train.csv"):
    id = line.split(",")[0]
    if id == sys.argv[1]:
        print line.strip()

print cid
debug = []
for line in open("object.csv"):
    if line.find("chapter") < 0:
        continue
    if line.find(cid) >= 0:

        debug.append(line.strip().split(",")[-1])

print "\n".join(sorted(debug))

import pickle
modelFileLoad = open('../shell/valid.model', 'rb')
clf = pickle.load(modelFileLoad)

for line in open("../shell/train2.txt"):
    arr = line.split(",")
    if arr[1] == sys.argv[1]:
        feature = [float(k) for k in arr[3:]]
        #print feature, clf.coef_
        #print feature, type(clf.coef_)
        print len(feature)
        continue
        for i in range(len(feature)):
            x = feature[i] * clf.coef_[0, i]
            print i, feature[i], clf.coef_[0, i],feature[i] * clf.coef_[0, i]
