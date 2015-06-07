#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'

import sys
from log import *
from enrollment import *
from Object import *
from label import *
from weekend import *
from coursetime import *
from common import *
from highuser import *
import math
from module import *
from transfer import *
from lastday import *
from commonfeature import *
week = Week()
class ObjWeight:
    def build(self):
        print "start build ObjWeight..."
        self.label = Label()
        self.log = Log("../data/merge/log.csv")
        self.objs = {}
    def write(self, filename, fout):
        fout = open(fout,"w")
        enrollment = Enrollment(filename)
        ccc = 0
        for id in enrollment.ids:
            y = int(self.label.get(id))
            ccc += 1
            if ccc % 5000 == 0:
                print ccc
            infos = self.log.enrollment_loginfo.get(id, [])
            ks = {}
            for info in infos:
                obj = info[-1]
                if obj not in self.objs:
                    self.objs[obj] = "%s" % len(self.objs)
                k = self.objs[obj]
                ks[k] = ks.get(k, 0) + 1
            fs = []
            for (k,v) in ks.items():
                fs.append("%s:%.2f" % (k, math.sqrt(v)))
            fout.write("%s %s|f %s\n" %(y, id, " ".join(fs)))

        fout.close()

if __name__ == "__main__":
    daylevel = ObjWeight()
    daylevel.build()
    #daylevel.write("../data/train1/enrollment_train.csv", "../obj/train1.txt")
    #daylevel.write("../data/train2/enrollment_train.csv", "../obj/train2.txt")
    daylevel.write("../data/train/enrollment_train.csv", "../obj/train.txt")
    daylevel.write("../data/test/enrollment_test.csv", "../obj/test.txt")
