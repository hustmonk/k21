#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""
import sys
__revision__ = '0.1'
for line in open("train2/enrollment_train.csv"):
    arr = line.strip().split(",")
    id = line.split(",")[0]
    if arr[0] == sys.argv[1]:
        print line.strip()
        cid = arr[-1]
        uid = arr[1]
print "uinfo....."
for line in open("merge/enrollment.csv"):
    arr = line.strip().split(",")
    id = line.split(",")[0]
    if arr[1] == uid:
        print line.strip()
        uid = arr[1]
print "uinfo....."
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
        for i in range(len(feature)):
            x = feature[i] * clf.coef_[0, i]
            #if x > 1 or x < -1:
            print i, feature[i], clf.coef_[0, i],feature[i] * clf.coef_[0, i]
