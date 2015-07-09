#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified:

"""docstring
"""

__revision__ = '0.1'
from enrollment import *
from label import *
from cdate import *
from lastday import *
from weekend import *
import sys
class Correction:
    def __init__(self, enrollmentfile,debug = False):
        self.enrollment = Enrollment("../data/merge/enrollment.csv")
        self.enrollment_train = Enrollment("../data/train/enrollment_train.csv")

        self.label = Label()
        self.cdate = Cdate()
        self.debug = debug
        self.lastdayinfo = LastDayInfo()
        self.lastdayinfo.load_id_days()

    def get_features(self, id):
        username, course_id = self.enrollment.enrollment_info.get(id)
        enr_ids = self.enrollment_train.user_enrollment_id.get(username, [])
        whole_enr_ids = self.enrollment.user_enrollment_id.get(username, [])
        dropdays = []
        nodropdays = []
        dropdays1 = []
        nodropdays1 = []
        dropnum = 0
        nodropnum = 0
        weekend = Week()
        _end = self.cdate.get_end(course_id)
        days = self.lastdayinfo.get_days(id)
        if self.debug:
            print "id,_end,course_id,days"
            print id,_end,course_id,days
        lostdays = []
        for _id in whole_enr_ids:
            if _id == id:
                continue
            _username, _course_id = self.enrollment.enrollment_info.get(_id)
            days = self.lastdayinfo.get_days(_id)
            end = self.cdate.get_end(_course_id)
            if len(days) < 1:
                continue
            _y = self.label.get(_id)
            if _y == "0":
                continue
            lastday = days[-1]
            diff = weekend.diff(end, lastday)
            if diff < 8:
                continue
            for i in range(1, diff+1):
                lostdays.append(weekend.getnd(lastday, i))
            if self.debug:
                print "lastday,days,end,lostdays"
                print lastday,days,end,lostdays
        for _id in enr_ids:
            if _id == id:
                continue
            _y = self.label.get(_id)
            _username, _course_id = self.enrollment.enrollment_info.get(_id)
            days = self.lastdayinfo.get_days(_id)
            end = self.cdate.get_end(_course_id)
            if self.debug:
                print "_id,_y,days,end"
                print _id,_y,days,end
            if _y == "1":
                for i in range(1, 11):
                    nday = weekend.getnd(end, i)
                    dropdays.append(nday)
                dropnum = dropnum + 1
                if len(days) < 1:
                    continue
                lastday = days[-1]
                diff = weekend.diff(end, lastday)
                for i in range(1, diff+1):
                    if self.debug:
                        print weekend.getnd(lastday, i)
                    dropdays1.append(weekend.getnd(lastday, i))
            else:
                nodropnum = nodropnum + 1
                for i in range(1, 11):
                    nday = weekend.getnd(end, i)
                    nodropdays.append(nday)
                if len(days) < 1:
                    continue
                lastday = days[-1]
                diff = weekend.diff(end, lastday)
                for i in range(1, diff+1):
                    if self.debug:
                        print weekend.getnd(lastday, i)
                    nodropdays1.append(weekend.getnd(lastday, i))
        if self.debug:
            print "dropdays",dropdays
            print "nodropdays", nodropdays
            print "lostdays",lostdays
        k1 = self.k_get_features(_end, dropdays)
        k2 = self.k_get_features(_end, nodropdays)
        k3 = self.k_get_features(_end, lostdays)
        k4 = self.k_get_features(_end, dropdays1 + dropdays)
        k5 = self.k_get_features(_end, nodropdays1 + nodropdays)
        if self.debug:
            print k3,"k3"
        f = [dropnum, nodropnum, nodropnum/(dropnum+nodropnum+1.0), dropnum/(dropnum+nodropnum+1.0)]
        f = ["%s" % k for k in f]
        f.append(k1)
        f.append(k2)
        f.append(k3)
        f.append(k4)
        f.append(k5)
        return ",".join(f), nodropdays

    def k_get_features(self,end,daylist):
        M = 15
        N = 21
        k = [0] * (M + N + (M + N)/3)
        weekend = Week()
        for day in daylist:
            idx = weekend.diff(end, day)
            #print "end",end, day,idx
            if idx >= -N and idx < M:
                idx = idx + N
                k[idx] = 1 + k[idx]
                k[idx/3 + N + M] = 1 + k[idx/3 + N + M]
        k = ",".join(["%d" % i for i in k])
        if self.debug:
            print k
        return k

if __name__ == "__main__":
    cor = Correction("../data/train/enrollment_train.csv",True)
    id="4936"
    print cor.get_features(sys.argv[1])
    """
    for i in range(1, 100):
        print cor.get_features(str(i))
    """
