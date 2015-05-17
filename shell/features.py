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
log_filename = sys.argv[1]
enrollment_filename = sys.argv[2]
featrue_filename = sys.argv[3]
log = Log(log_filename)
enrollment_train = Enrollment(enrollment_filename)
enrollment = Enrollment("../data/merge/enrollment.csv")
obj = Obj()
label = Label()
ids = enrollment_train.ids
import math
def transfer(v):
    return math.log(v+1)

fout = open(featrue_filename,"w")
ccc = 0
for id in ids:
    ccc += 1
    if ccc % 10000 == 0:
        print ccc
    y = label.get(id)
    infos = log.enrollment_loginfo.get(id, [])
    f = [0] * 179
    username, course_id = enrollment.enrollment_info.get(id)

    #time,source,event,o
    #source: browser,server
    #event:access,discussion,nagivate,page_close,problem,video,wiki
    #category:video,vertical,static_tab,sequential,problem,peergrading,outlink,html,discussion,dictation,course_info,course,combinedopenended,chapter,about
    #time:2014-06-13T09:52:49
    browser = 0
    server = 0
    event_count = [0] * EVENT_VEC_NUM
    category_count = [0] * CATEGORY_VEC_NUM
    weekday_count = [0] * WEEKDAY_VEC_NUM
    hour_count = [0] * HOUR_VEC_NUM
    cidx_count = [0] * CIDX_VEC_NUM
    cidx_by_stat_count = [0] * CIDX_BY_STAT_VECT_NUM
    last_cidx_count = [0] * LAST_CIDX_VEC_NUM
    course_id_vec = [0] * COURSE_VEC_NUM
    course_id_vec[coursetimeinfo.get_course_id(course_id)] = 1
    is_last_vec = [0] * IS_LAST_VEC_NUM #0 not last, 1-5, 6 more than 5
    days = set()
    info_by_day = {}
    last_cidx = 0
    for info in infos:
        day,timehms = info[0].split("T")
        if day not in info_by_day:
            info_by_day[day] = {}
            info_by_day[day]["category"] = {}
            info_by_day[day]["event"] = {}
        if info[1] == "browser":
            browser += 1
            info_by_day[day]["browser"] = info_by_day[day].get("browser", 0) + 1
        else:
            server += 1
            info_by_day[day]["server"] = info_by_day[day].get("server", 0) + 1
        mod_info = obj.module_info.get(info[3])
        if mod_info != None:
            category = mod_info[1]
            category_idx = get_category_idx(category)
            info_by_day[day]["category"][category_idx] = info_by_day[day]["category"].get(category_idx, 0) + 1

            category_count[category_idx] = category_count[category_idx] + 1
        else:
            category_count[16] = category_count[16] + 1

        event_idx = get_event_idx(info[2])
        event_count[event_idx] = event_count[event_idx] + 1
        info_by_day[day]["event"][event_idx] = info_by_day[day]["event"].get(event_idx, 0) + 1

        days.add(day)
        weekday = week.get(day)
        weekday_count[weekday] = weekday_count[weekday] + 1
        info_by_day[day]["weekday"] = weekday

        hour = int(timehms[:2]) / 2
        hour_count[hour] = hour_count[hour] + 1
        info_by_day[day]["hour"] = hour
        
        cidx = obj.get_index(course_id, week.times(info[0]))
        cidx_count[cidx] = cidx_count[cidx] + 1
        info_by_day[day]["cidx"] = cidx
        if cidx > last_cidx:
            last_cidx = cidx

        cidx_by_stat = coursetimeinfo.get_index(course_id, week.times(info[0]))
        cidx_by_stat_count[cidx_by_stat] = cidx_by_stat_count[cidx_by_stat] + 1
    day_event_count = [0] * EVENT_VEC_NUM
    day_category_count = [0] * CATEGORY_VEC_NUM
    day_weekday_count = [0] * WEEKDAY_VEC_NUM
    day_hour_count = [0] * HOUR_VEC_NUM
    day_cidx_count = [0] * CIDX_VEC_NUM
    for (day, info) in info_by_day.items():
        for (k,v) in info["event"].items():
            day_event_count[k] = day_event_count[k] + math.sqrt(v)
        for (k,v) in info["category"].items():
            day_category_count[k] = day_category_count[k] + math.sqrt(v)
        day_weekday_count[info["weekday"]] = day_weekday_count[info["weekday"]] + 1
        day_hour_count[info["hour"]] = day_hour_count[info["hour"]] + 1
        day_cidx_count[info["cidx"]] = day_cidx_count[info["cidx"]] + 1

    last_cidx_count[last_cidx] = last_cidx_count[last_cidx] + 1
    if len(days) < 2:
        is_last_vec[0] = 1
    else:
        days = sorted(days)
        diff = week.diff(days[-1],days[-2])
        if diff > 5:
            is_last_vec[6] = 1
        else:
            is_last_vec[diff] = 1
    f[0] = transfer(len(infos))
    f[1] = transfer(len(enrollment.course_info.get(course_id, [])))
    f[2] = transfer(len(enrollment.user_info.get(username, [])))
    f[3] = transfer(browser)
    f[4] = transfer(server)
    f[5] = (browser+3.1)/(float(len(infos))+6.5)
    f[6] = transfer(len(days))
    fv = [event_count,category_count,weekday_count,hour_count,cidx_count,course_id_vec,last_cidx_count,is_last_vec,day_event_count,day_category_count,day_weekday_count,day_hour_count,day_cidx_count,cidx_by_stat_count]
    start = 7
    for vs in fv:
        for (i, v) in enumerate(vs):
            f[start+i] = transfer(v)
        start = start + len(vs)

    fout.write("%s,%s,%s\n" % (y, id, ",".join(["%.2f" % k for k in f])))
