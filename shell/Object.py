#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'

class Obj:
    def __init__(self):
        #course_id,module_id,category,children,start
        self.course_modules = {}
        self.module_info = {}
        self.parent = {}
        for line in open("../data/object.csv"):
            course_id,module_id,category,children,start = line.strip().split(",")
            children = children.split(" ")
            if len(children) > 0:
                for child in children:
                    self.parent[child] = module_id
            self.module_info[module_id] = [course_id,category,children,start]
        
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

if __name__ == "__main__":
    obj = Obj()
