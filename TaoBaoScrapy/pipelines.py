# -*- coding: utf-8 -*-

import uuid
import traceback
from scrapy.pipelines.images import ImagesPipeline
from scrapy.pipelines.images import FilesPipeline
from scrapy.http import Request
from TaoBaoScrapy.utils.db_pool import get_session
from TaoBaoScrapy.store.db_store import Song


class TaobaoscrapyPipeline(object):
    session = None

    def process_item(self, item, spider):
        if spider.name == "baidu" and item.name == "db":
            try:
                print(item)
                song_obj = Song(**item)
                self.session.add(song_obj)
                self.session.commit()
            except Exception:
                traceback.print_exc()
                self.session.rollback()
        return item

    @classmethod
    def from_settings(cls, settings):
        print(settings)
        return cls()

    def open_spider(self, spider):
        self.session = get_session()
        return spider


class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        print("MyImagesPipeline", info.spider.name)

        return [Request(x, meta={"title": item["images"][item["image_urls"].index(x)]}) for x in
                item.get(self.images_urls_field, [])]

    def file_path(self, request, response=None, info=None):
        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('ImagesPipeline.image_key(url) and file_key(url) methods are deprecated, '
                          'please use file_path(request, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)

        # check if called from image_key or file_key with url as first argument
        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url

        # detect if file_key() or image_key() methods have been overridden
        if not hasattr(self.file_key, '_base'):
            _warn()
            return self.file_key(url)
        elif not hasattr(self.image_key, '_base'):
            _warn()
            return self.image_key(url)

        format_url = url[-3:]

        imgName = str(uuid.uuid4()) + "." + format_url

        return 'full/image/%s' % (imgName)


class MyFilesPipeline(FilesPipeline):

    def media_to_download(self, request, info):

        return super().media_to_download(request, info)

    def get_media_requests(self, item, info):
        # TODO  在这里也可以去重

        return [Request(x, meta={"name": item["files"][item["file_urls"].index(x)]}) for x in
                item.get(self.files_urls_field, [])]

    def file_path(self, request, response=None, info=None):
        def _warn():
            from scrapy.exceptions import ScrapyDeprecationWarning
            import warnings
            warnings.warn('FilesPipeline.file_key(url) method is deprecated, please use '
                          'file_path(request, response=None, info=None) instead',
                          category=ScrapyDeprecationWarning, stacklevel=1)

        # check if called from file_key with url as first argument
        if not isinstance(request, Request):
            _warn()
            url = request
        else:
            url = request.url

        # detect if file_key() method has been overridden
        if not hasattr(self.file_key, '_base'):
            _warn()
            return self.file_key(url)
        ## end of deprecation warning block

        albumName_name, author_name, song_name = request.meta.get("name").split(",")

        return 'music/%s/%s/%s.mp3' % (author_name, albumName_name, song_name)
