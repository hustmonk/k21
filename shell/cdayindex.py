class Cdayindex:
    def __init__(self):
        self.cdict = {}
        for line in open("dayindex/kdayindex.conf"):
            self.cdict[line.strip()] = len(self.cdict)

    def get_features(self, daynum, dayindex):
        k = [0] * (len(self.cdict) + 1)
        key = str(daynum) + "_" + str(dayindex)
        if key in self.cdict:
            k[self.cdict[key]] = 1
        else:
            k[len(self.cdict)] = 1
        return ",".join(["%s" % i for i in k])

if __name__ == "__main__":
    cdayindex = Cdayindex()
    print cdayindex.get_features(4, 19)



