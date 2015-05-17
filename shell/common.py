#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'

event_key = "access,discussion,nagivate,page_close,problem,video,wiki".split(",")
category_key = "video,vertical,static_tab,sequential,problem,peergrading,outlink,html,discussion,dictation,course_info,course,combinedopenended,chapter,about".split(",") #16
category_map = {}
event_map = {}
for k in event_key:
    event_map[k] = len(event_map)

for k in category_key:
    category_map[k] = len(category_map)

def get_event_idx(k):
    return event_map[k]
def get_category_idx(k):
    return category_map[k]

EVENT_VEC_NUM = 7
CATEGORY_VEC_NUM = 17
WEEKDAY_VEC_NUM = 7
HOUR_VEC_NUM = 12
CIDX_VEC_NUM = 10
CIDX_BY_STAT_VECT_NUM = 10
LAST_CIDX_VEC_NUM = 10
COURSE_VEC_NUM = 39
IS_LAST_VEC_NUM = 7
#EVENT_VEC_NUM = 7
#CATEGORY_VEC_NUM = 17
#WEEKDAY_VEC_NUM = 7
#HOUR_VEC_NUM = 12
#CIDX_VEC_NUM = 10
