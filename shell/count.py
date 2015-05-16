#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'

fin = open("train2.txt")

header = fin.next().strip().split(",")
counts = []
drop = []
for i in range(len(header)):
    counts.append({})
    drop.append({})
for line in fin:
    arr = line.strip().split(",")
    label = arr[0]
    for i in range(1, len(header)):
        key = arr[i]

        counts[i][key] = counts[i].get(key, 0) + 1
        if label == '1':
            drop[i][key] = drop[i].get(key, 0) + 1

for i in range(1, len(header)):
    #print header[i],len(counts[i]),"x"
    for (k,v) in counts[i].items():
        print k,v,drop[i].get(k, 0) / float(v)
