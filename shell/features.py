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
from moreinfo import *
from statistic import *
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
moreinfo = MoreDayFeature()
moreinfo.load()
statistic = StatisticInfo()
statistic.load()
import math
def transfer(v):
    return math.log(v+1)

def get_features(id,IS_DEBUG=False):
    y = label.get(id)
    username, course_id = enrollment.enrollment_info.get(id)

    course_id_vec = [0] * COURSE_VEC_NUM
    course_id_vec[coursetimeinfo.get_course_id(course_id)] = 1

    days = lastdayinfo.get_days(id)

    is_last_vec = [0] * IS_LAST_VEC_NUM #0 not last, 1-5, 6 more than 5
    is_pre_vec = [0] * IS_LAST_VEC_NUM #0 not last, 1-5, 6 more than 5
    is_next_vec = [0] * IS_LAST_VEC_NUM #0 not last, 1-5, 6 more than 5
    next_daynum_vec = [0] * IS_LAST_VEC_NUM
    gap_vec = [0] * IS_LAST_VEC_NUM
    if len(days) < 2:
        is_last_vec[0] = 1
        is_pre_vec[0] = 1
    else:
        last_day = days[-1]
        isCC = 0
        _diff = 100
        for i in range(len(days)-1):
            diff = week.diff(days[i+1], days[i])
            if diff > (IS_LAST_VEC_NUM-1):
                diff = (IS_LAST_VEC_NUM-1)
            gap_vec[diff] = gap_vec[diff] + 1
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
    whole_site_pre_vec = [0] * IS_LAST_VEC_NUM
    whole_site_post_vec = [0] * IS_LAST_VEC_NUM
    whole_site_pre_enrollment_vec = [0] * IS_LAST_VEC_NUM
    whole_site_post_enrollment_vec = [0] * IS_LAST_VEC_NUM

    whole_site_pre_enrollment_id_vec = [0] * COURSE_VEC_NUM
    whole_site_post_enrollment_id_vec = [0] * COURSE_VEC_NUM
    k1,k2 = moreinfo.get_enrollment_features(username,id)
    kids1, kids2 = moreinfo.get_enrollment_ids(username,id)
    for k in kids1:
        _username, k = enrollment.enrollment_info.get(k)
        whole_site_pre_enrollment_id_vec[coursetimeinfo.get_course_id(k)] = 1
    for k in kids2:
        _username, k = enrollment.enrollment_info.get(k)
        whole_site_post_enrollment_id_vec[coursetimeinfo.get_course_id(k)] = 1
    if k1 > IS_LAST_VEC_NUM - 1:
        k1 = IS_LAST_VEC_NUM - 1
    if k2 > IS_LAST_VEC_NUM - 1:
        k2 = IS_LAST_VEC_NUM - 1
    #print k1, k2, kids1, kids2
    whole_site_pre_enrollment_vec[k1] = 1
    whole_site_post_enrollment_vec[k2] = 1
    pre_num = 0
    post_num = 0
    lastday = ""
    if len(days) > 0:
        lastday = days[-1]
        for day in alldays:
            diff = week.diff(day,days[-1]) / 2
            if diff > 0:
                post_num = post_num + 1
            else:
                pre_num = pre_num + 1
            if diff > 0  and diff < IS_LAST_VEC_NUM-1:
                is_next_vec[diff] = 1
                daynum += 1
        if daynum >= IS_LAST_VEC_NUM:
            daynum = IS_LAST_VEC_NUM - 1
    else:
        print id,"X"
    if daynum == 0:
        is_next_vec[IS_LAST_VEC_NUM-1] = 1
    if post_num > IS_LAST_VEC_NUM-1:
        post_num = IS_LAST_VEC_NUM-1
    if pre_num > IS_LAST_VEC_NUM-1:
        pre_num = IS_LAST_VEC_NUM-1
    if IS_DEBUG:
        print "post_num,",post_num,"pre_num",pre_num
    whole_site_pre_vec[pre_num] = 1
    whole_site_post_vec[post_num] = 1
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
    f_statistic = statistic.get_features(lastday, course_id)
    f_days = [0] * DAYS_VEC_NUM
    f_all_days = [0] * DAYS_VEC_NUM
    f_enrollment_num_vec = [0] * MAX_ENROLLMENT_VEC_NUM
    f_last_5_record = "0"#lastday5recordfeature.get_features(id)
    enrollment_num = len(enrollment.user_info.get(username, []))
    if enrollment_num > MAX_ENROLLMENT_VEC_NUM - 1:
        enrollment_num = MAX_ENROLLMENT_VEC_NUM - 1
    f_enrollment_num_vec[enrollment_num] = 1

    dy_num = len(days)
    if dy_num > DAYS_VEC_NUM-1:
        dy_num = DAYS_VEC_NUM-1
    f_days[dy_num] = 1
    dy_num = len(alldays)
    if dy_num > DAYS_VEC_NUM-1:
        dy_num = DAYS_VEC_NUM-1
    f_all_days[dy_num] = 1

    f = [0] * 305
    f[0] = transfer(len(enrollment.course_info.get(course_id, [])))
    f[1] = transfer(enrollment_num)
    f[2] = transfer(len(days))
    f[3] = transfer(len(alldays))

    fv_no_transfer = [transfer_vec]
    fv_no_transfer_debug = ["transfer_vec"]
    start = 4
    for j in range(len(fv_no_transfer)):
        vs = fv_no_transfer[j]
        if IS_DEBUG:
            print fv_no_transfer_debug[j],vs
        for (i, v) in enumerate(vs):
            f[start+i] = v
        start = start + len(vs)

    fv = [course_id_vec,is_last_vec, use_vec, is_next_vec,next_daynum_vec,is_pre_vec,f_days,f_all_days,whole_site_pre_vec,whole_site_post_vec,gap_vec, f_enrollment_num_vec, whole_site_pre_enrollment_vec, whole_site_post_enrollment_vec, whole_site_pre_enrollment_id_vec, whole_site_post_enrollment_id_vec]
    fv_debug = ["course_id_vec","is_last_vec", "use_vec", "is_next_vec","next_daynum_vec","is_pre_vec","f_days","f_all_days","whole_site_pre_vec","whole_site_post_vec","gap_vec", "f_enrollment_num_vec", "whole_site_pre_enrollment_vec", "whole_site_post_enrollment_vec", "whole_site_pre_enrollment_id_vec", "whole_site_post_enrollment_id_vec"]
    for j in range(len(fv)):
        vs = fv[j]
        if IS_DEBUG:
            print fv_debug[j],vs
        for (i, v) in enumerate(vs):
            f[start+i] = transfer(v)
        start = start + len(vs)
    if IS_DEBUG:
        print start
    f = ",".join(["%.2f" % k for k in f])
    fs = "%s,%s,%s,%d,-%s,-%s,-%s,-%s,-%s,-%s,-%s\n" % (y, id, course_id, len(days),f_common, f_last_day, f_day_level, f_last_5_record, f_user_site, f,f_statistic)
    #fs = "%s,%s,%s,%d,%s\n" % (y, id, course_id, len(days), f_last_day )
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
def single(id, True):
    print get_features(id, True)

#single("199364", True)
filed()

