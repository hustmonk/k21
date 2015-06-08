#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'

import sys
import math

ps = []
ys = []
psd = {}
for line in open("valid.txt.1.debug"):
    id,p,y = line.split(",")
    ys.append(int(y))
    ps.append(float(p))
    #psd[id] = float(p) * 1.02
    psd[id] = float(p)
for line in open("valid.txt.2.debug"):
    id,p,y = line.split(",")
    ys.append(int(y))
    ps.append(float(p))
    psd[id] = float(p)
for line in open("../tovw/train2.txt.pred"):
    p, id = line.strip().split(" ")
    p = (float(p) + 1 )/2.0
    psd[id] = psd[id] * p

ps = []
ys = []
for line in open("valid.txt.debug"):
    id,p,y = line.split(",")
    ys.append(int(y))
    ps.append(float(p) * psd[id])
    #ps.append(psd[id])
from sklearn import metrics
roc_auc = metrics.roc_auc_score(ys, ps)
print roc_auc
