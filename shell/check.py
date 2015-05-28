#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
ys = []
for line in open("valid.txt.debug"):
    id,p,y = line.strip().split(",")
    ys.append(int(y))

N = 20
k = len(ys)/N
for i in range(N):
    s = sum(ys[i*k : (i+1)*k])
    n = len(ys[i*k : (i+1)*k])
    print s/float(n)
