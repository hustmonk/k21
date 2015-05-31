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
from transfer import *
from lastdayfeature import *
from day_level_feafure import *
from alldayfeature import *
from lastday import *
from wholesitefeature import *
from lastday5recordfeature import *
week = Week()
lastdayfeature = LastDayFeature()
lastdayfeature.load()
daylevel = DayLevelInfo()
daylevel.load()
lastdayinfo = LastDayInfo()
lastdayinfo.load_id_days()
alldayfeature = AllDayFeature()
alldayfeature.load()
lastday5recordfeature = LastDay5RecordFeature()
lastday5recordfeature.load()
coursetimeinfo = CourseTimeInfo()
enrollment_filename = sys.argv[2]
featrue_filename = sys.argv[3]
enrollment_train = Enrollment(enrollment_filename)
enrollment = Enrollment("../data/merge/enrollment.csv")
label = Label()
userinfo = Userinfo()
userinfo.load()
transfer_day = Transfer()
transfer_day.load()
wholesitefeature = WholeSiteFeature()
wholesitefeature.load()
ids = enrollment_train.ids
import math
def transfer(v):
    return math.log(v+1)

def get_features(id):
    y = label.get(id)
    username, course_id = enrollment.enrollment_info.get(id)

    course_id_vec = [0] * COURSE_VEC_NUM
    course_id_vec[coursetimeinfo.get_course_id(course_id)] = 1

    days = lastdayinfo.get_days(id)

    is_last_vec = [0] * IS_LAST_VEC_NUM #0 not last, 1-5, 6 more than 5
    is_pre_vec = [0] * IS_LAST_VEC_NUM #0 not last, 1-5, 6 more than 5
    is_next_vec = [0] * IS_LAST_VEC_NUM #0 not last, 1-5, 6 more than 5
    next_daynum_vec = [0] * IS_LAST_VEC_NUM
    if len(days) < 2:
        is_last_vec[0] = 1
        is_pre_vec[0] = 1
    else:
        last_day = days[-1]
        isCC = 0
        _diff = 100
        for day in days[:-1]:
            diff = week.diff(last_day, day) / 2 + 1
            if diff < (IS_LAST_VEC_NUM-1):
                is_last_vec[diff] = 1
                isCC = isCC + 1
                if diff < _diff:
                    _diff = diff
        if isCC == 0:
            is_last_vec[IS_LAST_VEC_NUM-1] = 1
            _diff = IS_LAST_VEC_NUM-1
        is_pre_vec[_diff] = 1
    alldays = userinfo.get_days(username)
    daynum = 0
    if len(days) > 0:
        for day in alldays:
            diff = week.diff(day,days[-1]) / 2
            if diff > 0  and diff < IS_LAST_VEC_NUM-1:
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
    f_user_site = wholesitefeature.get_features(username)
    f_days = [0] * DAYS_VEC_NUM
    f_all_days = [0] * DAYS_VEC_NUM
    f_last_5_record = "0"#lastday5recordfeature.get_features(id)
    f = [0] * 165
    f[0] = transfer(len(enrollment.course_info.get(course_id, [])))
    f[1] = transfer(len(enrollment.user_info.get(username, [])))
    f[2] = transfer(len(days))
    f[3] = transfer(len(alldays))
    dy_num = len(days)
    if dy_num > DAYS_VEC_NUM-1:
        dy_num = DAYS_VEC_NUM-1
    f_days[dy_num] = 1
    dy_num = len(alldays)
    if dy_num > DAYS_VEC_NUM-1:
        dy_num = DAYS_VEC_NUM-1
    f_all_days[dy_num] = 1
    fv_no_transfer = [transfer_vec]
    start = 4
    for vs in fv_no_transfer:
        for (i, v) in enumerate(vs):
            f[start+i] = v
        start = start + len(vs)

    fv = [course_id_vec,is_last_vec, use_vec, is_next_vec,next_daynum_vec,is_pre_vec,f_days,f_all_days]
    for vs in fv:
        for (i, v) in enumerate(vs):
            f[start+i] = transfer(v)
        start = start + len(vs)
    fs = "%s,%s,%s,%s,%s,%s,%s,-%s,%s\n" % (y, id, course_id, f_common, f_last_day, f_day_level, ",".join(["%.2f" % k for k in f]), f_last_5_record, f_user_site)
    return fs
def filed():
    fout = open(featrue_filename,"w")
    ccc = 0
    for id in ids:
        fs = get_features(id)
        ccc += 1
        if ccc % 5000 == 0:
            print ccc
        fout.write(fs)
def single(id):
    print get_features(id)

#single("184324")
filed()

