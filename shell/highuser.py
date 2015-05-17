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
week = Week()
coursetimeinfo = CourseTimeInfo()
log = Log("../data/merge/log.csv")
enrollment = Enrollment("../data/merge/enrollment.csv")
obj = Obj()
total = {}
ccc = 0
for id in enrollment.ids:
    ccc += 1
    if ccc % 5000 == 0:
        print ccc
    infos = log.enrollment_loginfo.get(id, [])
    username, course_id = enrollment.enrollment_info.get(id)

    for info in infos:
        if info[0].find("T") < 0:
            continue
        day,timehms = info[0].split("T")
        if username not in total:
            total[username] = set()
        total[username].add(day)
fout = open("conf/user.info", "w")
for (u, info) in total.items():
    fout.write("%s\t%d\t%s\n" % (u, len(info), ",".join(info)))
