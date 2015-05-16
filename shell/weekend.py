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

if __name__ == "__main__":
    week = Week()
    print week.get("2015-05-16")
    print type(week.get("2015-05-16"))
