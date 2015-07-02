#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
fins = []
fins.append([open("aveenv/merge.csv"), 1.1])
fins.append([open("xgboost/merge.csv"), 1])
fins.append([open("subenv/merge.csv"), 1])
fins.append([open("v1subenv/merge.csv"), 1.2])
N = sum([k[1] for k in fins])
fout = open("merge.csv","w")
while fins[0]:
    ps = []
    k = 1
    for i in range(len(fins)):
        line = fins[i][0].next()
        id,pred = line.strip().split(",")
        ps.append(float(pred) * fins[i][1])
        k = float(pred) * k
    #fout.write("%s,%f\n" % (id, sum(ps)/N))
    fout.write("%s,%f\n" % (id, k))
