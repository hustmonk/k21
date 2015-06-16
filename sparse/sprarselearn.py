#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
import math
import sys
#from model import *
from xgboost_class import *
from scipy.sparse import *
from scipy import *
#from randomforest import *
#from net6 import *
def read(filename):
    X1 = []
    X2 = []
    v = []
    Y = []
    ids = []
    idx = 0
    max_iday = 0
    for line in open(filename):
        arr = line.strip().split(",")
        y = int(arr[0])
        ids.append(arr[1])
        iday = int(arr[3]) + 1
        if iday > 5 and iday < 7:
            iday = 5
        elif iday >= 7:
            iday = 6
            #iday = int(math.sqrt(iday - 5)) + 5
        if iday > max_iday:
            max_iday = iday
        arr = arr[3:]
        for i in range(len(arr)):
            if float(arr[i]) > 0.0001:
                X1.append(idx)
                X2.append(i)
                v.append(float(arr[i]))
                X1.append(idx)
                X2.append(i + iday * len(arr[i]))
                v.append(float(arr[i]))
        Y.append(y)
        idx += 1
        """
        if len(Y) > 2000:
            break
        """
    print max_iday
    X = csr_matrix((array(v),(array(X1),array(X2))), shape=(idx,len(arr) * max_iday))
    return X,Y,ids

X_train, y_train, ids_train = read(sys.argv[1])
X_test, y_test, ids_test = read(sys.argv[2])
out_file = sys.argv[3]
is_valid = int(sys.argv[4])
model = Model()
print "model"
model.train(X_train, y_train, X_test, ids_test, y_test, out_file, is_valid)
