#!/usr/bin/env python
# -*- coding: GB2312 -*-
# Last modified: 

"""docstring
"""

__revision__ = '0.1'

# print feature idx:
fout = open("conf/feature.description", "w")

fout.write("0 #len of enrollment log info\n")
fout.write("1 #same course id, enrollment num\n")
fout.write("2 #same username, enrollment num\n")
fout.write("3 browser num\n")
fout.write("4 server num\n")
fout.write("5 browser ratio\n")
fout.write("[6-12] " + ",".join(event_key) + "\n")
fout.write("[13-29] " + ",".join(category_key) + "\n")
fout.write("[30-36] weekday" + "\n")
fout.write("[37-48] hour info" + "\n")
fout.write("[49-58] cidx info" + "\n")
fout.write("[59-97] course id info" + "\n")
fout.write("98 uniuq day " + "\n")
fout.write("[99-108] last_cidx info" + "\n")
fout.write("[109-115] last day info" + "\n")
fout.close

