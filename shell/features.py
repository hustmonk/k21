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
from lastdayfeature import *
from day_level_feafure import *
from alldayfeature import *
from lastday import *
week = Week()
lastdayfeature = LastDayFeature()
lastdayfeature.load()
daylevel = DayLevelInfo()
daylevel.load()
lastdayinfo = LastDayInfo()
lastdayinfo.load()
alldayfeature = AllDayFeature()
alldayfeature.load()
coursetimeinfo = CourseTimeInfo()
enrollment_filename = sys.argv[2]
featrue_filename = sys.argv[3]
enrollment_train = Enrollment(enrollment_filename)
enrollment = Enrollment("../data/merge/enrollment.csv")
obj = Obj()
label = Label()
userinfo = Userinfo()
userinfo.load()
module = Module()
module.load()
transfer_day = Transfer()
transfer_day.load()
ids = enrollment_train.ids
import math
def transfer(v):
    return math.log(v+1)

fout = open(featrue_filename,"w")
ccc = 0
for id in ids:
    ccc += 1
    if ccc % 5000 == 0:
        print ccc
    y = label.get(id)
    username, course_id = enrollment.enrollment_info.get(id)

    course_id_vec = [0] * COURSE_VEC_NUM
    course_id_vec[coursetimeinfo.get_course_id(course_id)] = 1

    days = lastdayinfo.get_days(id)

    is_last_vec = [0] * IS_LAST_VEC_NUM #0 not last, 1-5, 6 more than 5
    is_next_vec = [0] * IS_LAST_VEC_NUM #0 not last, 1-5, 6 more than 5
    next_daynum_vec = [0] * IS_LAST_VEC_NUM
    if len(days) < 2:
        is_last_vec[0] = 1
    else:
        last_day = days[-1]
        isCC = 0
        for day in days[:-1]:
            diff = week.diff(last_day, day)
            if diff < (IS_LAST_VEC_NUM-1):
                is_last_vec[diff] = 1
                isCC = isCC + 1
        if isCC == 0:
            is_last_vec[IS_LAST_VEC_NUM-1] = 1
    alldays = userinfo.get_days(username)
    daynum = 0
    if len(days) > 0:
        for day in alldays:
            diff = week.diff(day,days[-1]) - 1
            if diff >= 0  and diff < IS_LAST_VEC_NUM-1:
                is_next_vec[diff] = 1
                daynum += 1
        if daynum >= IS_LAST_VEC_NUM:
            daynum = IS_LAST_VEC_NUM - 1
    if daynum == 0:
        is_next_vec[IS_LAST_VEC_NUM-1] = 1
    next_daynum_vec[daynum] = 1

    use_vec = userinfo.get_features(username, course_id)
    if len(days) > 0:
        transfer_vec = transfer_day.get_features(days[-1])
    else:
        transfer_vec = transfer_day.get_features("")
    f_last_day = lastdayfeature.get_features(id)
    f_day_level = daylevel.get_features(id)
    f_common = alldayfeature.get_features(id)
    f = [0] * 109
    f[0] = transfer(len(enrollment.course_info.get(course_id, [])))
    f[1] = transfer(len(enrollment.user_info.get(username, [])))
    f[2] = transfer(len(days))
    fv_no_transfer = [transfer_vec]
    start = 3
    for vs in fv_no_transfer:
        for (i, v) in enumerate(vs):
            f[start+i] = v
        start = start + len(vs)

    fv = [course_id_vec,is_last_vec, use_vec, is_next_vec,next_daynum_vec]
    for vs in fv:
        for (i, v) in enumerate(vs):
            f[start+i] = transfer(v)
        start = start + len(vs)
    fout.write("%s,%s,%s,%s,%s,%s,%s\n" % (y, id, course_id, f_common, f_last_day, f_day_level, ",".join(["%.2f" % k for k in f])))
