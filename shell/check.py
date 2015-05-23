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

k = len(ys)/10
for i in range(10):
    s = sum(ys[i*k : (i+1)*k])
    n = len(ys[i*k : (i+1)*k])
    print s/float(n)
