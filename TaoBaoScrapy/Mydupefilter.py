# _*_ coding:utf-8 _*_
# __author__Zj__


#  自定制去重URL的类 需要在配置文件里指定
class ReptDupeFilter:

    def __init__(self):
        self.visit_urls = set()
        self.songs_name = set()

    @classmethod
    def from_settings(cls, settings):
        return cls()

    def request_seen(self, request):
        """
        去重 但是post的请求 不需要去重
        :param request:
        :return:
        """

        if request.url in self.visit_urls and request.method == "GET":
            return True
        self.visit_urls.add(request.url)
        return False

    def open(self):
        # print("open")# can return deferred
        pass

    def close(self, reason):
        # print("close")# can return a deferred
        pass

    def log(self, request, spider):  # log that a request has been filtered
        pass
