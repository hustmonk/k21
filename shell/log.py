#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'

class Log:
    def __init__(self, filename):
        fin = open(filename)
        fin.next()
        self.enrollment_loginfo = {}
        for line in fin:
            #enrollment_id,username,course_id,time,source,event,object
            enrollment_id,time,source,event,o = line.strip().split(",")
            if enrollment_id not in self.enrollment_loginfo:
                self.enrollment_loginfo[enrollment_id] = [[time,source,event,o]]
            else:
                self.enrollment_loginfo[enrollment_id].append([time,source,event,o])


from label import *
if __name__ == "__main__":
    log = Log("../data/train/log_train.csv")
    fout = open("conf/_id_days", "w")
    label = Label()
    count = {}
    c1ount = {}
    for (k, infos) in log.enrollment_loginfo.items():
        days = set()
        for info in infos:
            day = info[0][:10]
            days.add(day)
        fout.write("%s\t%d\t%s\t%s\n" % (k, len(days), label.get(k), sorted(days)))
        count[len(days)] = count.get(len(days), 0) + 1
        c1ount[len(days)] = c1ount.get(len(days), 0) + int(label.get(k))
    for (k, v) in count.items():
        print k, v, c1ount[k]/float(v)


