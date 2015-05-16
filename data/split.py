#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
fin = open("train/enrollment_train.csv")
header = fin.next()

fout1 = open("train1/enrollment_train.csv", "w")
fout2 = open("train2/enrollment_train.csv", "w")
fout1.write(header)
fout2.write(header)
cc = 0
id1 = set()
id2 = set()
for line in fin:
    if cc % 5 == 4:
        fout2.write(line)
        id2.add(line.split(",")[0])
    else:
        fout1.write(line)
        id1.add(line.split(",")[0])
    cc = cc + 1

fout1.close()
fout2.close()

fin = open("train/log_train.csv")
header = fin.next()
fout1 = open("train1/log_train.csv", "w")
fout2 = open("train2/log_train.csv", "w")
fout1.write(header)
fout2.write(header)
for line in fin:
    id = line.split(",")[0]
    if id in id2:
        fout2.write(line)
    else:
        fout1.write(line)
fout1.close()
fout2.close()
