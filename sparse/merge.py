#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""
import sys
__revision__ = '0.1'
fins = []
N = 60
for i in range(N):
    fin = open("merge/sub.csv"+str(i))
    fins.append(fin)
fout = open("merge.csv","w")
while fins[0]:
    ps = []
    for i in range(N):
        line = fins[i].readline()
        if line == "":
            sys.exit(-1)
        id,pred = line.strip().split(",")
        ps.append(float(pred))
    ps = [sum(ps[i*6:(i+1)*6])/6 for i in range(10) ]
    k = 1
    for i in ps:
        k = k * i
    fout.write("%s,%f\n" % (id, k))
