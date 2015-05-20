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
        fout = open("conf/last_day", "w")
        for id in enrollment.ids:
            ccc += 1
            if ccc % 5000 == 0:
                print ccc
            infos = log.enrollment_loginfo.get(id, [])
            buffer = []
            username, course_id = enrollment.enrollment_info.get(id)
            _day = ""
            for info in infos:
                ##time,source,event,o
                day = info[0].split("T")[0]
                if day != _day:
                    buffer = []
                buffer.append(info)
                _day = day
            fout.write("%s\t%s\n" % (course_id,_day))

if __name__ == "__main__":
    userinfo = Module()
    userinfo.build()
