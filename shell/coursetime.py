#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
from weekend import *
week = Week()
class CourseTimeInfo:
    def __init__(self):
        self.timeinfo = {}
        self.course_id = {}
        for line in open("conf/course.time.info"):
                id, times = line.strip().split("\t")
                times = times.split(",")
                self.timeinfo[id] = [float(k)  for k in times[1:]]
                """
                for k in self.timeinfo[id]:
                    print id, week.stypetime(k)
                """
                self.course_id[id] = len(self.course_id)


    def get_index(self, id, timestampe):
        infos = self.timeinfo[id]
        for i in range(len(infos)):
            if timestampe < infos[i]:
                return i
        return 9
    
    def get_course_id(self, id):
        return self.course_id.get(id)

if __name__ == "__main__":
    ct = CourseTimeInfo()
