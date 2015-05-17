#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
from weekend import *
from common import *
week = Week()

class Obj:
    def __init__(self):
        #course_id,module_id,category,children,start
        self.course_modules = {}
        self.module_info = {}
        self.parent = {}
        self.course_timeinfo = {}
        for line in open("../data/object.csv"):
            course_id,module_id,category,children,start = line.strip().split(",")
            children = children.split(" ")
            if len(children) > 0:
                for child in children:
                    self.parent[child] = module_id
            self.module_info[module_id] = [course_id,category,children,start]
            if line.find("chapter") > 0 and line.find("null") < 0:
                if course_id not in self.course_timeinfo:
                    self.course_timeinfo[course_id] = [week.times(start)]
                else:
                    self.course_timeinfo[course_id].append(week.times(start))
        #time
        self.course_start_end = {}
        for (k,v) in self.course_timeinfo.items():
            v = sorted(v)
            start = v[0] - 86400
            end = v[-1] + 86400
            #print v
            self.course_start_end[k] = [start, end]
        self.course_root_module = {}
        self.module_depth = {}
        for module_id in self.module_info:
            if module_id not in self.parent:
                course_id = self.module_info[module_id][0]
                if course_id not in self.course_root_module:
                    self.course_root_module[course_id] = [module_id]
                else:
                    self.course_root_module[course_id].append(module_id)
                self.module_depth[module_id] = 1
        while True:
            count = 0
            for module_id in self.module_info:
                if module_id not in self.module_depth:
                    if count == 1:
                        print module_id
                    count += 1
                else:
                    continue
                if self.parent[module_id] in self.module_depth:
                    self.module_depth[module_id] = self.module_depth[self.parent[module_id]] + 1
            if count == 0:
                break

    def get_index(self, id, timestampe):
        start,end = self.course_start_end[id]
        if timestampe < start:
            return 0
        elif timestampe > end:
            return CIDX_VEC_NUM-1
        return int((timestampe - start) * (CIDX_VEC_NUM - 2) / (end - start)) + 1


if __name__ == "__main__":
    obj = Obj()
