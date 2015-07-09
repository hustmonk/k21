#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'
import time
class Week:
    def get(self, day):
        t1=time.mktime(time.strptime(day,'%Y-%m-%d'))
        return int(time.strftime("%w",time.gmtime(int(t1) + 8*60*60)))

    def diff(self, day1, day2):
        d1 = self.timestamp(day1)
        d2 = self.timestamp(day2)
        return int((d1-d2)/(self.timestamp("2014-06-07") - self.timestamp("2014-06-06")))

    def timestamp(self, timestr):
        t1=time.mktime(time.strptime(timestr,'%Y-%m-%d'))
        return t1

    def times(self, timestr):
        if timestr.find("T")>0:
            t1=time.mktime(time.strptime(timestr,'%Y-%m-%dT%H:%M:%S'))
        else:
            t1=time.mktime(time.strptime(timestr,'%Y-%m-%d'))
        return t1

    def stypetime(self, times):
        timeArray = time.localtime(times)
        otherStyleTime = time.strftime("%Y-%m-%dT%H:%M:%S", timeArray)
        return otherStyleTime
    
    def getnd(self, day, i):
        k = self.times(day)
        k = k + (self.timestamp("2014-06-07") - self.timestamp("2014-06-06")) * i
        timeArray = time.localtime(k)
        otherStyleTime = time.strftime("%Y-%m-%d", timeArray)
        return otherStyleTime


if __name__ == "__main__":
    week = Week()
    print week.get("2015-05-16")
    print type(week.get("2015-05-16"))
    print week.times("2015-05-16T07:08:09")
    print type(week.times("2015-05-16T07:08:09"))
    print week.stypetime(week.times("2015-05-16T07:08:09"))
    print week.diff("2015-05-16","2015-05-14")
    print week.diff('2014-07-11', '2014-07-05'),"X"
    print week.timestamp("2014-06-07") -  week.timestamp("2014-06-06")
    print week.times("2013-12-24T14:17:14")
    for i in range(-10, 10):
        print week.getnd("2014-06-07", i),i
