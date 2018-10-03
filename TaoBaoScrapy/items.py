# -*- coding: utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ImagescrapyItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()
    name = scrapy.Field()


class SongscrapyItem(scrapy.Item):
    name = "db"
    song_name = scrapy.Field()
    song_album_name = scrapy.Field()
    song_id = scrapy.Field()
    author_name = scrapy.Field()
    song_link = scrapy.Field()
    address = scrapy.Field()


class FilescrapyItem(scrapy.Item):
    name = "file_store"
    files = scrapy.Field()
    file_urls = scrapy.Field()
