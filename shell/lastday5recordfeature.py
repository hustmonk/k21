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
import cPickle as pickle
week = Week()
class LastDay5RecordFeature:
    def build(self):
        print "start build LastDayFeature..."
        enrollment = Enrollment("../data/merge/enrollment.csv")
        last_day_info = LastDayInfo()
        last_day_info.load()
        commonfeature = CommonFeature()
        ccc = 0
        fs = {}

        for id in enrollment.ids:
            ccc += 1
            if ccc % 5000 == 0:
                print ccc
            infos = last_day_info.get_info(id)
            username, course_id = enrollment.enrollment_info.get(id)
            f = commonfeature.get_features(infos[-5:], course_id)
            fs[id] = f
        modelFileSave = open('_feature/lastday.5.info.model', 'wb')
        pickle.dump(fs, modelFileSave)
        modelFileSave.close()
        print "build LastDayFeature over!"

    def load(self):
        modelFileLoad = open('_feature/lastday.5.info.model', 'rb')
        self.fs = pickle.load(modelFileLoad)

    def get_features(self, id):
        return self.fs[id]

if __name__ == "__main__":
    daylevel = LastDay5RecordFeature()
    daylevel.build()
    daylevel.load()
    print daylevel.get_features("1")
