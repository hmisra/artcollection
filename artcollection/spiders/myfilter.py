import os

from scrapy.dupefilter import RFPDupeFilter
from scrapy.utils.request import request_fingerprint

class CustomFilter(RFPDupeFilter):
    def __getid(self, url):
        mm = url.split("page=")[1] #or something like that
        return mm

    def request_fingerprint(self, request):
        fp = self.__getid(request.url)
        if fp in self.fingerprints:
            return True
        self.fingerprints.add(fp)
        if self.file:
            self.file.write(fp + os.linesep)
