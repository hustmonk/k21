#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
import math
import sys
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
kmax = {}
filter_trans = {}
def fit(courses, X):
    fnum = len(X[0])
    for i in range(fnum):
        for j in range(len(X)):
            x = X[j]
            course = courses[j]
            if x[i] > 0.001:
                if course not in kmax:
                    kmax[course] = [0] * 1000
                if kmax[course][i] < x[i]:
                    kmax[course][i] = x[i]

def transfer(course, x):
    x1 = []
    for i in range(len(x)):
        if i not in filter_trans:
            if kmax[course][i] == 0:
                x1.append(0.0)
            else:
                x1.append(x[i]/kmax[course][i])
        x1.append(x[i])
    return x1
def read(filename, isFit):
    X = []
    Y = []
    ids = []
    courses = []
    for line in open("../shell/" + filename):
        arr = line.strip().replace("inf","1").split(",")
        y = int(arr[0])
        ids.append(arr[1])
        courses.append(arr[2])
        x = [ math.sqrt(math.fabs(float(k))) for k in arr[3:]]
        X.append(x)
        Y.append(y)
        """
        if len(X) > 1000:
            break
        """
    if isFit:
        fit(courses, X)
    fout = open(filename+".transfer", "w")
    for i in range(len(Y)):
        x = transfer(courses[i], X[i])
        fout.write("%d,%s,%s,%s\n" % (Y[i],ids[i],courses[i],",".join(["%.2f" % k  for k in x]) ))
    fout.close()
read("train.txt", 1)
read("train2.txt", 0)
read("train1.txt", 0)
read("test.txt", 0)

