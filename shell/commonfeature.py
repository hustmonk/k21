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

class CommonFeature():
    def __init__(self):
        self.coursetimeinfo = CourseTimeInfo()
        self.obj = Obj()

    def get_features(self, infos, course_id):
        week = Week()
        event_count = [0] * EVENT_VEC_NUM
        weekday_count = [0] * WEEKDAY_VEC_NUM
        hour_count = [0] * HOUR_VEC_NUM
        cidx_count = [0] * CIDX_VEC_NUM
        cidx_by_stat_count = [0] * CIDX_VEC_NUM
        month_count = [0] * MONTH_VEC_NUM
        browser = 0
        server = 0
        for info in infos:
            day,timehms = info[0].split("T")
            if info[1] == "browser":
                browser += 1
            else:
                server += 1
            year,month,d = day.split("-")
            month_idx = (int(month) - 1) * 2 + int(d)/16
            month_count[month_idx] = 1

            event_idx = get_event_idx(info[2])
            event_count[event_idx] = event_count[event_idx] + 1

            weekday = week.get(day)
            weekday_count[weekday] = weekday_count[weekday] + 1

            hour = int(timehms[:2]) / 2
            hour_count[hour] = hour_count[hour] + 1
        
            cidx = self.obj.get_index(course_id, week.times(info[0]))
            cidx_count[cidx] = cidx_count[cidx] + 1

            cidx_by_stat = self.coursetimeinfo.get_index(course_id, week.times(info[0]))
            cidx_by_stat_count[cidx_by_stat] = cidx_by_stat_count[cidx_by_stat] + 1

        buf = []
        buf.append( "%.3f" % transfer(len(infos)))
        buf.append( ("%.3f" % transfer(browser)))
        buf.append( "%.3f" % transfer(server))
        buf.append( "%.3f" % ((browser+3.1)/(float(len(infos))+6.5)))
        fv = [event_count,weekday_count,hour_count,cidx_count,cidx_by_stat_count, month_count]
        for vs in fv:
            for (i, v) in enumerate(vs):
                buf.append( "%.3f" % transfer(v))
        return ",".join(buf)

