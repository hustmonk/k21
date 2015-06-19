#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified:

"""docstring
"""

__revision__ = '0.1'
import math
import sys
from model import *
kv = {}
for line in open("evals_result"):
    k,v = line[1:].strip().split("\t")
    if int(v) > 5:
        kv[int(k)+1] = len(kv)
print len(kv)
def read(filename):
    X = []
    Y = []
    ids = []
    for line in open(filename):
        arr = line.strip().split(",")
        y = int(arr[0])
        ids.append(arr[1])
        iday = int(arr[4])

        arr = [ math.sqrt(float(k)) for k in arr[3:]]
        x = [0] * (len(arr) + len(kv) * 2)
        for i in range(len(arr)):
            x[i] = arr[i]
        for i in range(len(arr)):
            if i in kv:
                if iday > 15:
                    x[len(arr) + kv[i]] = arr[i]
                else:
                    x[len(arr) + len(kv) + kv[i]] = arr[i]
        X.append(x)
        Y.append(y)
        """
        if len(X) > 2000:
            break
        """
    return X,Y,ids

X_train, y_train, ids_train = read(sys.argv[1])
X_test, y_test, ids_test = read(sys.argv[2])
out_file = sys.argv[3]
is_valid = int(sys.argv[4])
model = Model()
print "model"
model.train(X_train, y_train, X_test, ids_test, y_test, out_file, is_valid)
