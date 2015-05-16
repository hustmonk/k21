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
week = Week()
log_filename = sys.argv[1]
enrollment_filename = sys.argv[2]
featrue_filename = sys.argv[3]

log = Log(log_filename)
enrollment_train = Enrollment(enrollment_filename)
enrollment = Enrollment("../data/merge/enrollment.csv")
obj = Obj()
label = Label()
fout = open(featrue_filename,"w")
ids = enrollment_train.ids
import math
def transfer(v):
    return math.log(v+1)
event_key = "access,discussion,nagivate,page_close,problem,video,wiki".split(",")
category_key = "video,vertical,static_tab,sequential,problem,peergrading,outlink,html,discussion,dictation,course_info,course,combinedopenended,chapter,about".split(",") #16
for id in ids:
    y = label.get(id)
    infos = log.enrollment_loginfo.get(id, [])
    f = [0] * 37
    f[0] = transfer(len(infos))
    username, course_id = enrollment.enrollment_info.get(id)
    f[1] = transfer(len(enrollment.course_info.get(course_id, [])))
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
    for info in infos:
        if info[1] == "browser":
            browser += 1
        else:
            server += 1
        mod_info = obj.module_info.get(info[3])
        if mod_info != None:
            category = mod_info[1]
            for i in range(len(category_key)):
                if category == category_key[i]:
                    category_count[i] = category_count[i] + 1
        else:
            category_count[16] = category_count[16] + 1

        for i in range(len(event_key)):
            if info[2] == event_key[i]:
                event_count[i] = event_count[i] + 1
        day,timehms = info[0].split("T")
        weekday = week.get(day)
        weekday_count[weekday] = weekday_count[weekday] + 1
    f[3] = transfer(browser)
    f[4] = transfer(server)
    f[5] = (browser+3.1)/(float(len(infos))+6.5)
    for i in range(7):
        f[6+i] = transfer(event_count[i])
    for i in range(17):
        f[13+i] = transfer(category_count[i])
    for i in range(7):
        f[30+i] = transfer(weekday_count[i])


    fout.write("%s,%s,%s\n" % (y, id, ",".join(["%.2f" % k for k in f])))
