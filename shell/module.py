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
import math
import pickle
class Module:
    def build(self):
        week = Week()
        coursetimeinfo = CourseTimeInfo()
        log = Log("../data/merge/log.csv")
        enrollment = Enrollment("../data/merge/enrollment.csv")
        obj = Obj()
        moduler_stat = {}
        ccc = 0
        for id in enrollment.ids:
            ccc += 1
            if ccc % 5000 == 0:
                print ccc
            infos = log.enrollment_loginfo.get(id, [])
            for info in infos:
                ##time,source,event,o
                o = info[3]
                moduler_stat[o] = moduler_stat.get(o, 0) + 1

        modelFileSave = open('conf/modular.info.model', 'wb')
        pickle.dump(moduler_stat, modelFileSave)
        modelFileSave.close()

    def load(self):
        modelFileLoad = open('conf/modular.info.model', 'rb')
        self.moduler_stat = pickle.load(modelFileLoad)
        self.week = Week()
        self.obj = Obj()
        """
        for (k, v) in self.moduler_stat.items():
            print k,v,self.get_weight(k)
        """
    
    def get_weight(self, o):
        return 3/math.sqrt(self.moduler_stat.get(o)+1)

if __name__ == "__main__":
    userinfo = Module()
    #userinfo.build()
    userinfo.load()
    print userinfo.get_weight("bLd0qFlUenJjVXjJFYxr4hHl3GiZeCjn")
    
