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

    def times(self, timestr):
        t1=time.mktime(time.strptime(timestr,'%Y-%m-%dT%H:%M:%S'))
        return t1

    def stypetime(self, times):
        timeArray = time.localtime(times)
        otherStyleTime = time.strftime("%Y-%m-%dT%H:%M:%S", timeArray)
        return otherStyleTime

if __name__ == "__main__":
    week = Week()
    print week.get("2015-05-16")
    print type(week.get("2015-05-16"))
    print week.times("2015-05-16T07:08:09")
    print type(week.times("2015-05-16T07:08:09"))
    print week.stypetime(week.times("2015-05-16T07:08:09"))
