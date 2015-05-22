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
week = Week()
coursetimeinfo = CourseTimeInfo()
log_filename = sys.argv[1]
enrollment_filename = sys.argv[2]
featrue_filename = sys.argv[3]
log = Log(log_filename)
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
    infos = log.enrollment_loginfo.get(id, [])
    username, course_id = enrollment.enrollment_info.get(id)

    #time,source,event,o
    #source: browser,server
    #event:access,discussion,nagivate,page_close,problem,video,wiki
    #category:video,vertical,static_tab,sequential,problem,peergrading,outlink,html,discussion,dictation,course_info,course,combinedopenended,chapter,about
    #time:2014-06-13T09:52:49
    course_id_vec = [0] * COURSE_VEC_NUM
    course_id_vec[coursetimeinfo.get_course_id(course_id)] = 1

    event_count = [0] * EVENT_VEC_NUM
    category_count = [0] * CATEGORY_VEC_NUM
    weekday_count = [0] * WEEKDAY_VEC_NUM
    hour_count = [0] * HOUR_VEC_NUM
    cidx_count = [0] * CIDX_VEC_NUM
    cidx_by_stat_count = [0] * CIDX_VEC_NUM
    days = set()
    info_by_day = {}
    browser = 0
    server = 0
    for info in infos:
        day,timehms = info[0].split("T")
        #weight = module.get_weight(info[3])
        weight = 1
        if day not in info_by_day:
            info_by_day[day] = {}
            info_by_day[day]["category"] = {}
            info_by_day[day]["event"] = {}
        if info[1] == "browser":
            browser += weight
            info_by_day[day]["browser"] = info_by_day[day].get("browser", 0) + weight
        else:
            server += weight
            info_by_day[day]["server"] = info_by_day[day].get("server", 0) + weight
        mod_info = obj.module_info.get(info[3])
        if mod_info != None:
            category = mod_info[1]
            category_idx = get_category_idx(category)
            info_by_day[day]["category"][category_idx] = info_by_day[day]["category"].get(category_idx, 0) + weight

            #category_count[category_idx] = category_count[category_idx] + weight
        #else:
            #category_count[16] = category_count[16] + weight

        event_idx = get_event_idx(info[2])
        event_count[event_idx] = event_count[event_idx] + weight
        info_by_day[day]["event"][event_idx] = info_by_day[day]["event"].get(event_idx, 0) + weight

        days.add(day)
        weekday = week.get(day)
        weekday_count[weekday] = weekday_count[weekday] + weight
        info_by_day[day]["weekday"] = weekday

        hour = int(timehms[:2]) / 2
        hour_count[hour] = hour_count[hour] + weight
        info_by_day[day]["hour"] = hour
        
        cidx = obj.get_index(course_id, week.times(info[0]))
        cidx_count[cidx] = cidx_count[cidx] + weight
        info_by_day[day]["cidx"] = cidx

        cidx_by_stat = coursetimeinfo.get_index(course_id, week.times(info[0]))
        cidx_by_stat_count[cidx_by_stat] = cidx_by_stat_count[cidx_by_stat] + weight
    days = sorted(days)

    day_event_count = [0] * EVENT_VEC_NUM
    day_category_count = [0] * CATEGORY_VEC_NUM
    day_weekday_count = [0] * WEEKDAY_VEC_NUM
    day_hour_count = [0] * HOUR_VEC_NUM
    day_cidx_count = [0] * CIDX_VEC_NUM
    for (day, info) in info_by_day.items():
        for (k,v) in info["event"].items():
            day_event_count[k] = day_event_count[k] + math.sqrt(v)
        #for (k,v) in info["category"].items():
            #day_category_count[k] = day_category_count[k] + math.sqrt(v)
        day_weekday_count[info["weekday"]] = day_weekday_count[info["weekday"]] + 1
        day_hour_count[info["hour"]] = day_hour_count[info["hour"]] + 1
        day_cidx_count[info["cidx"]] = day_cidx_count[info["cidx"]] + 1

    last_day_event_count = [0] * EVENT_VEC_NUM
    last_day_category_count = [0] * CATEGORY_VEC_NUM
    last_day_weekday_count = [0] * WEEKDAY_VEC_NUM
    last_day_hour_count = [0] * HOUR_VEC_NUM
    last_cidx_count = [0] * CIDX_VEC_NUM
    last_cidx_by_stat_count = [0] * CIDX_VEC_NUM
    last_browser = 0
    last_server = 0
    for info in infos:

        #weight = module.get_weight(info[3])
        weight = 1
        day,timehms = info[0].split("T")
        if day != days[-1]:
            continue
        if info[1] == "browser":
            last_browser += weight
        else:
            last_server += weight
        mod_info = obj.module_info.get(info[3])
        """
        if mod_info != None:
            category = mod_info[1]
            category_idx = get_category_idx(category)
            last_day_category_count[category_idx] = last_day_category_count[category_idx] + weight
        else:
            last_day_category_count[16] = last_day_category_count[16] + weight
        """

        event_idx = get_event_idx(info[2])
        last_day_event_count[event_idx] = last_day_event_count[event_idx] + weight

        weekday = week.get(day)
        last_day_weekday_count[weekday] = last_day_weekday_count[weekday] + weight

        hour = int(timehms[:2]) / 2
        last_day_hour_count[hour] = last_day_hour_count[hour] + weight

        cidx = obj.get_index(course_id, week.times(info[0]))
        cidx_by_stat = coursetimeinfo.get_index(course_id, week.times(info[0]))
        last_cidx_count[cidx] = last_cidx_count[cidx] + 1
        last_cidx_by_stat_count[cidx_by_stat] = last_cidx_by_stat_count[cidx_by_stat] + 1
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
    f = [0] * 304
    f[0] = transfer(len(infos))
    f[1] = transfer(len(enrollment.course_info.get(course_id, [])))
    f[2] = transfer(len(enrollment.user_info.get(username, [])))
    f[3] = transfer(browser)
    f[4] = transfer(server)
    f[5] = (browser+3.1)/(float(len(infos))+6.5)
    f[6] = transfer(len(days))
    f[7] = transfer(last_browser)
    f[8] = transfer(last_server)
    fv_no_transfer = [transfer_vec,next_daynum_vec]
    start = 9
    for vs in fv_no_transfer:
        for (i, v) in enumerate(vs):
            f[start+i] = v
        start = start + len(vs)

    fv = [event_count,category_count,weekday_count,hour_count,cidx_count,course_id_vec,last_cidx_count,is_last_vec,day_event_count,day_category_count,day_weekday_count,day_hour_count,day_cidx_count,cidx_by_stat_count,last_day_event_count,last_day_category_count,last_day_weekday_count,last_day_hour_count, last_cidx_by_stat_count, use_vec, is_next_vec]
    for vs in fv:
        for (i, v) in enumerate(vs):
            f[start+i] = transfer(v)
        start = start + len(vs)

    fout.write("%s,%s,%s,%s\n" % (y, id, course_id, ",".join(["%.2f" % k for k in f])))
