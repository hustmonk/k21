#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified:

"""docstring
"""

__revision__ = '0.1'

from weekend import *
from common import *
import cPickle as pickle
from label import *
from lastday import *
from enrollment import *
import math
class StatisticInfo:
    def course(self, course_deafault, default):
        enrollment = Enrollment("../data/merge/enrollment.csv")
        userinfo = LastDayInfo()
        userinfo.load_id_days()
        label = Label()
        count = {}
        dropcount = {}
        for (id, days) in userinfo.id_days_infos.items():
            if label.contain(id) and len(days) > 0:
                lastday = days[-1]
                y = int(label.get(id))
                username, course_id = enrollment.enrollment_info.get(id)
                if course_id != course_deafault:
                    continue
                count[lastday] = count.get(lastday, 0) + 1
                dropcount[lastday] = dropcount.get(lastday, 0) + y
        ratio_day = {}
        for day in sorted(count):
            c = count[day] + 10
            d = dropcount[day] + default * 10
            ratio_day[day] = float(d)/float(c)
            print day,c,d, float(d)/float(c)

    def build(self):
        enrollment = Enrollment("../data/merge/enrollment.csv")
        userinfo = LastDayInfo()
        userinfo.load_id_days()
        label = Label()
        count = {}
        dropcount = {}
        coursecount = {}
        dropcoursecount = {}
        dropfirstcount = {}
        count_by_course = {}
        test_count_by_course = {}
        dropcount_by_course = {}
        cc = 0
        dropcc = 0
        for (id, days) in userinfo.id_days_infos.items():
            if label.contain(id) and len(days) > 0:
                lastday = days[-1]
                y = int(label.get(id))
                username, course_id = enrollment.enrollment_info.get(id)
                cc = cc + 1
                dropcc = dropcc + y
                if course_id not in count_by_course:
                    count_by_course[course_id] = {}
                    dropcount_by_course[course_id] = {}
                count_by_course[course_id][lastday] = count_by_course[course_id].get(lastday, 0) + 1
                dropcount_by_course[course_id][lastday] = dropcount_by_course[course_id].get(lastday, 0) + y
                """
                for day in days[:-1]:
                    count_by_course[course_id][day] = count_by_course[course_id].get(day, 0) + 1
                """

                count[lastday] = count.get(lastday, 0) + 1
                dropcount[lastday] = dropcount.get(lastday, 0) + y
                coursecount[course_id] = coursecount.get(course_id, 0) + 1
                dropcoursecount[course_id] = dropcoursecount.get(course_id, 0) + y
                if len(days) == 1:
                    dropfirstcount[course_id] = dropfirstcount.get(course_id, 0) + y
            else:
                if course_id not in test_count_by_course:
                    test_count_by_course[course_id] = {}
                test_count_by_course[course_id][lastday] = test_count_by_course[course_id].get(lastday, 0) + 1
                test_count_by_course[course_id]["x"] = test_count_by_course[course_id].get("x", 0) + 1
        default = float(dropcc)/cc

        ratio_course_id = {}
        ratio_day_by_course_id = {}
        first_day_by_course_id = {}
        for course_id in coursecount:
            c = coursecount[course_id]
            d = dropcoursecount[course_id]
            ratio_course_id[course_id] = float(d)/float(c)
            print "CC",course_id,d,c,float(d)/float(c),len(count_by_course[course_id]),len(test_count_by_course[course_id])
            #self.course(course_id, float(d)/float(c))
            default_course_id_ratio = float(d)/float(c)
            _ratio = {}
            for day in sorted(count_by_course[course_id]):
                if course_id not in first_day_by_course_id:
                    first_day_by_course_id[course_id] = day
                c1 = count_by_course[course_id][day]# + 5
                d1 = dropcount_by_course[course_id][day]# + default_course_id_ratio * 5
                _ratio[day] = float(d1)/float(c1)
                r1 = test_count_by_course[course_id][day]/float(test_count_by_course[course_id]["x"])
                print day,c1,d1,d1/float(c1),c1/float(c),test_count_by_course[course_id][day],r1, (c1/float(c))/r1
            ratio_day_by_course_id[course_id] = _ratio
            print ""
        ratio_day = {}
        for day in count:
            c = count[day] + 10
            d = dropcount[day] + default * 10
            ratio_day[day] = float(d)/float(c)
        ratio_course_id_first = {}
        for course_id in coursecount:
            c = coursecount[course_id]
            d = dropfirstcount[course_id]
            ratio_course_id_first[course_id] = float(d)/float(c)
        statistic = {}
        statistic["ratio_course_id_first"] = ratio_course_id_first
        statistic["ratio_day"] = ratio_day
        statistic["first_day_by_course_id"] = first_day_by_course_id
        statistic["ratio_course_id"] = ratio_course_id
        statistic["default"] = default
        statistic["ratio_day_by_course_id"] = ratio_day_by_course_id
        modelFileSave = open('_feature/statistic.info', 'wb')
        pickle.dump(statistic, modelFileSave)
        modelFileSave.close()

    def load(self):
        modelFileLoad = open('_feature/statistic.info', 'rb')
        statistic = pickle.load(modelFileLoad)
        self.default = statistic["default"]
        self.ratio_course_id_first = statistic["ratio_course_id_first"]
        self.ratio_day = statistic["ratio_day"]
        self.ratio_course_id = statistic["ratio_course_id"]
        self.ratio_day_by_course_id = statistic["ratio_day_by_course_id"]
        self.first_day_by_course_id = statistic["first_day_by_course_id"]

    def get_features(self, day, course_id, days,alldays):
        f = [0] * 169
        f[0] = self.ratio_course_id[course_id]
        f[1] = self.ratio_course_id_first[course_id]
        for i in range(21):
            if len(day) < 4:
                f[2+i] = self.default
            else:
                k = i - 10
                nd = week.getnd(day, k)
                f[2+i] = self.ratio_day.get(nd, self.default)
        start = 23
        if len(day) > 4:
            idx = week.diff(day, self.first_day_by_course_id[course_id])
            f[start + idx] = 1
        else:
            return ",".join(["%.3f" % k for k in f])
        start = 53
        for d in days:
            idx = week.diff(d, self.first_day_by_course_id[course_id])
            if idx >= 0 and idx < 30:
                f[start + idx] = 1
            if idx < 0:
                f[start + 30] = f[start + 30] + 1
        start = 84
        for d in days:
            idx = week.diff(d, self.first_day_by_course_id[course_id])
            if idx >= 0 and idx < 30:
                idx = idx / 3
                f[start + idx] = 1 + f[start + idx]
        start = 94
        for d in alldays:
            idx = week.diff(d, self.first_day_by_course_id[course_id])
            if idx < -15:
                f[start + 30] = f[start + 30] + 1
            elif idx < -10:
                f[start + 31] = f[start + 31] + 1
            elif idx < -7:
                f[start + 32] = f[start + 32] + 1
            elif idx < -3:
                f[start + 33] = f[start + 33] + 1
            elif idx < 0:
                f[start + 34] = f[start + 34] + 1
            elif idx < 30:
                f[start + idx] = 1
            elif idx < 33:
                f[start + 35] = f[start + 35] + 1
            elif idx < 36:
                f[start + 36] = f[start + 36] + 1
            elif idx < 40:
                f[start + 37] = f[start + 37] + 1
            elif idx < 45:
                f[start + 38] = f[start + 38] + 1
            else:
                f[start + 39] = f[start + 39] + 1
        start = 134

        idx = week.diff(day, self.first_day_by_course_id[course_id])
        if idx >= 0 and idx < 30:
            idx = idx / 3
            f[start + idx] = 1
        start = 144
        for d in alldays:
            idx = week.diff(d, self.first_day_by_course_id[course_id])
            if idx >= 0 and idx < 30:
                idx = idx / 3
                f[start + idx] = f[start + idx] + 1
        start = 154
        for d in days:
            idx = week.diff(d, self.first_day_by_course_id[course_id])
            if idx >= 0 and idx < 30:
                idx = idx / 6
                f[start + idx] = 1 + f[start + idx]
        start = 159
        for d in alldays:
            idx = week.diff(d, self.first_day_by_course_id[course_id])
            if idx >= 0 and idx < 30:
                idx = idx / 6
                f[start + idx] = 1 + f[start + idx]
        start = 164

        idx = week.diff(day, self.first_day_by_course_id[course_id])
        if idx >= 0 and idx < 30:
            idx = idx / 6
            f[start + idx] = 1
        """
        start = 83
        for i in range(5):
            default = self.ratio_course_id[course_id]
            if len(day) < 4:
                f[start+i] = default
            else:
                k = i - 2
                nd = week.getnd(day, k)
                f[start+i] = self.ratio_day_by_course_id[course_id].get(nd, default)
        """
        return ",".join(["%.3f" % k for k in f])
    def get_start_idx(self, day, course_id):
        if len(day) < 4:
            return 0
        return week.diff(day, self.first_day_by_course_id[course_id])
if __name__ == "__main__":
    statistic = StatisticInfo()
    statistic.build()
    statistic.load()
    #print statistic.get_features("2014-06-17", "V4tXq15GxHo2gaMpaJLZ3IGEkP949IbE")


