#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
from weekend import *
from common import *
import cPickle as pickle
import math
class Transfer():
    def build(self):
        week = Week()
        total = {}
        for line in open("conf/user.info"):
            id,num,days = line.strip().split("\t")
            days = sorted(days.split(","))
            for i in range(len(days)-1):
                day1 = days[i]
                day2 = days[i+1]

                if day1 not in total:
                    total[day1] = [0] * TRANSFER_VEC_NUM
                diff = week.diff(day2, day1) - 1
                if diff > TRANSFER_VEC_NUM-1:
                    diff = TRANSFER_VEC_NUM-1
                total[day1][diff] = total[day1][diff] + 1

        ratio = {}
        for (d, info) in total.items():
            s = sum(info)
            info = [float(i)/s for i in info]
            ratio[d] = info
        modelFileSave = open('conf/transfer.model', 'wb')
        pickle.dump(ratio, modelFileSave)
        modelFileSave.close()

    def load(self):
        modelFileLoad = open('conf/transfer.model', 'rb')
        self.ratio = pickle.load(modelFileLoad)
        self.default = [0.2/TRANSFER_VEC_NUM]*TRANSFER_VEC_NUM
        self.default[TRANSFER_VEC_NUM-1] = 1 - 0.2/TRANSFER_VEC_NUM * (TRANSFER_VEC_NUM-1)

    def get_features(self, day):
        if day in self.ratio:
            return self.ratio[day]
        else:
            return self.default

if __name__ == "__main__":
    transfer = Transfer()
    transfer.build()
    transfer.load()
    print [math.log(k+1) for k in transfer.get_features("2013-12-31")]
    print sum([math.log(k+1) for k in transfer.get_features("2013-12-31")])
    print transfer.get_features("2013-12-31")
    print sum(transfer.get_features("2013-12-31"))
    print transfer.get_features("2013-12-41")
    print [math.log(k+1) for k in transfer.get_features("2013-12-41")]
