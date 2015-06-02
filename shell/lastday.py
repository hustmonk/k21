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
import cPickle as pickle
class LastDayInfo:
    def build(self):
        print "start LastDayInfo build..."
        week = Week()
        log = Log("../data/merge/log.csv")
        enrollment = Enrollment("../data/merge/enrollment.csv")
        ccc = 0
        last_infos = {}
        id_days_infos = {}
        for id in enrollment.ids:
            days = set()
            ccc += 1
            if ccc % 5000 == 0:
                print ccc
            infos = log.enrollment_loginfo.get(id, [])
            buf = []
            _day = ""
            for info in infos:
                ##time,source,event,o
                day = info[0].split("T")[0]
                days.add(day)
                if day != _day:
                    buf = []
                buf.append(",".join(info))
                _day = day
            last_infos[id] = buf
            days = sorted(days)
            id_days_infos[id] = days
        modelFileSave = open('_feature/last.day.log', 'wb')
        pickle.dump(last_infos, modelFileSave)
        modelFileSave.close()
        modelFileSave = open('_feature/id_days.info', 'wb')
        pickle.dump(id_days_infos, modelFileSave)
        modelFileSave.close()
        print "LastDayInfo build over"

    def load(self):
        modelFileLoad = open('_feature/last.day.log', 'rb')
        self.last_infos = pickle.load(modelFileLoad)
        modelFileLoad = open('_feature/id_days.info', 'rb')
        self.id_days_infos = pickle.load(modelFileLoad)

    def load_id_days(self):
        modelFileLoad = open('_feature/id_days.info', 'rb')
        self.id_days_infos = pickle.load(modelFileLoad)

    def get_info(self, id):
        return [k.split(",") for k in self.last_infos[id]]

    def get_days(self, id):
        return self.id_days_infos[id]

if __name__ == "__main__":
    userinfo = LastDayInfo()
    userinfo.build()
    #userinfo.load()
    #print userinfo.get_info("1")
