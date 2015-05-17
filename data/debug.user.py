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
