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

# print feature idx:
fout = open("conf/feature.description", "w")

fout.write("0 #len of enrollment log info\n")
fout.write("1 #same course id, enrollment num\n")
fout.write("2 #same username, enrollment num\n")
fout.write("3 browser num\n")
fout.write("4 server num\n")
fout.write("5 browser ratio\n")
fout.write("[6-12] " + ",".join(event_key) + "\n")
fout.write("[13-29] " + ",".join(category_key) + "\n")
fout.write("[30-36] weekday" + "\n")
fout.write("[37-48] hour info" + "\n")
fout.write("[49-58] cidx info" + "\n")
fout.write("[59-97] course id info" + "\n")
fout.write("98 uniuq day " + "\n")
fout.write("[99-108] last_cidx info" + "\n")
fout.write("[109-115] last day info" + "\n")
fout.close

fout = open(featrue_filename,"w")
ccc = 0
for id in ids:
    ccc += 1
    if ccc % 10000 == 0:
        print ccc
    y = label.get(id)
    infos = log.enrollment_loginfo.get(id, [])
    f = [0] * 179
    f[0] = transfer(len(infos))
    username, course_id = enrollment.enrollment_info.get(id)
    #f[1] = transfer(len(enrollment.course_info.get(course_id, [])))
    f[2] = transfer(len(enrollment.user_info.get(username, [])))

    #time,source,event,o
    #source: browser,server
    #event:access,discussion,nagivate,page_close,problem,video,wiki
    #category:video,vertical,static_tab,sequential,problem,peergrading,outlink,html,discussion,dictation,course_info,course,combinedopenended,chapter,about
    #time:2014-06-13T09:52:49
    browser = 0
    server = 0
    event_count = [0] * 7
    category_count = [0] * 17
    weekday_count = [0] * 7
    hour_count = [0] * 12
    cidx_count = [0] * 10
    cidx_by_stat_count = [0] * 10
    last_cidx_count = [0] * 10
    course_id_vec = [0] * 39
    course_id_vec[coursetimeinfo.get_course_id(course_id)] = 1
    is_last_vec = [0] * 7 #0 not last, 1-5, 6 more than 5
    days = set()
    info_by_day = {}
    last_cidx = 0
    for info in infos:
        day,timehms = info[0].split("T")
        if day not in info_by_day:
            info_by_day[day] = {}
            info_by_day[day]["category"] = set()
            info_by_day[day]["event"] = set()
        if info[1] == "browser":
            browser += 1
            info_by_day[day]["browser"] = 1
        else:
            server += 1
            info_by_day[day]["server"] = 1
        mod_info = obj.module_info.get(info[3])
        if mod_info != None:
            category = mod_info[1]
            category_idx = get_category_idx(category)
            info_by_day[day]["category"].add(category_idx)

            category_count[category_idx] = category_count[category_idx] + 1
        else:
            category_count[16] = category_count[16] + 1

        event_idx = get_event_idx(info[2])
        event_count[event_idx] = event_count[event_idx] + 1
        info_by_day[day]["event"].add(event_idx)

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
    day_event_count = [0] * 7
    day_category_count = [0] * 17
    day_weekday_count = [0] * 7
    day_hour_count = [0] * 12
    day_cidx_count = [0] * 10
    for (day, info) in info_by_day.items():
        for k in info["event"]:
            day_event_count[k] = day_event_count[k] + 1
        for k in info["category"]:
            day_category_count[k] = day_category_count[k] + 1
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
    f[3] = transfer(browser)
    f[4] = transfer(server)
    f[5] = (browser+3.1)/(float(len(infos))+6.5)
    for i in range(7):
        f[6+i] = transfer(event_count[i])
    for i in range(17):
        f[13+i] = transfer(category_count[i])
    for i in range(7):
        f[30+i] = transfer(weekday_count[i])
    for i in range(12):
        f[37+i] = transfer(hour_count[i])
    for i in range(10):
        f[49+i] = transfer(cidx_count[i])
    for i in range(39):
        f[59+i] = transfer(course_id_vec[i])
    f[98] = transfer(len(days))
    for i in range(10):
        f[99+i] = transfer(last_cidx_count[i])
    for i in range(7):
        f[109+i] = transfer(is_last_vec[i])

    for i in range(7):
        f[116+i] = transfer(day_event_count[i])
    for i in range(17):
        f[123+i] = transfer(day_category_count[i])
    for i in range(7):
        f[140+i] = transfer(day_weekday_count[i])
    for i in range(12):
        f[147+i] = transfer(day_hour_count[i])
    for i in range(10):
        f[159+i] = transfer(day_cidx_count[i])
    for i in range(10):
        f[169+i] = transfer(cidx_by_stat_count[i])

    fout.write("%s,%s,%s\n" % (y, id, ",".join(["%.2f" % k for k in f])))
