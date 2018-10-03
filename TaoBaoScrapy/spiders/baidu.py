# -*- coding: utf-8 -*-
import json
import scrapy
from bs4 import BeautifulSoup
from scrapy.http import Request
from scrapy import Selector
from scrapy.http import FormRequest
from ..items import SongscrapyItem
from ..items import FilescrapyItem


class BaiduSpider(scrapy.Spider):
    name = 'baidu'
    allowed_domains = ['play.taihe.com', "music.taihe.com"]
    start_urls = ["http://music.taihe.com/artist/"]
    ignore_artist = list()
    songs_set = set()
    artist_name_set = set()

    def parse(self, response):

        ignore_artists = self.settings.get("IGNORE_ARTIST")
        artist_link = Selector(response=response).xpath(
            "//div[@class='hot-head clearfix']//dd//a[@class='cover-item-artist-name']/@href").extract()
        artists_name = Selector(response=response).xpath(
            "//div[@class='hot-head clearfix']//dd//a[@class='cover-item-artist-name']/text()").extract()

        bottom_artists_name = Selector(response=response).xpath("//ul[@class='clearfix']//li/a/text()").extract()
        bottom_artists_link = Selector(response=response).xpath("//ul[@class='clearfix']//li/a/text()").extract()

        bottom_artists_dict = dict(zip(bottom_artists_name, bottom_artists_link))
        artist_dict = dict(zip(artists_name, artist_link))
        artist_dict.update(bottom_artists_dict)
        for name, link in artist_dict.items():
            if name in ignore_artists:
                continue
            # print(name,link)
            url = f"http://music.taihe.com{link}"

            yield Request(url=url, callback=self.start_parse, meta={"name": name})

    def start_parse(self, response):
        li_list = Selector(response=response).xpath(
            "//li[@class='songlist-item clearfix ']//\
            div[@class='songlist-inline songlist-title']/span[@class='songname']/a[1]/@href").extract()

        singer_area = Selector(response=response).xpath("//p[@class='from']/span[1]/text()").extract()
        artist_name = Selector(response=response).xpath(("//span[@class='artist-name']/text()")).extract()

        try:
            _, addr = singer_area[0].rsplit(maxsplit=1)
        except Exception:
            addr = "未知"
        song_list_num = [s.split("/")[2] for s in li_list]
        song_list_str = ",".join(song_list_num)

        data_dict = {
            "songIds": song_list_str
        }

        yield FormRequest(url="http://play.taihe.com/data/music/songlink", formdata=data_dict,
                          callback=self.get_song_info_dict, meta={"area": addr, "artist_name": artist_name[0]})

        page = Selector(response=response).xpath("//div[@class='page-inner']//a[last()-1]/text()").extract()
        try:
            page_num = page[0]

            start_url = response.url

            ting_uid = start_url.rsplit("/", maxsplit=1)[1]

            for i in range(0, int(page_num) - 1):
                url = "http://music.taihe.com/data/user/getsongs?start=%s&size=15&ting_uid=%s\
                &.r=0.7306061573565991531499428670" % (i * 15, ting_uid)

                yield Request(url=url, callback=self.get_song_id_string)
        except IndexError:
            pass

    def get_song_id_string(self, response):
        body = response.body

        body = json.loads(body)
        html = body.get("data").get("html")

        soup = BeautifulSoup(html, 'lxml')

        a_s = soup.select("a[href^='/song']")

        song_id_list = [tag.get("href").split("/")[2] for tag in a_s]

        song_str = ",".join(song_id_list)

        data_dict = {
            "songIds": song_str
        }

        yield FormRequest(url="http://play.taihe.com/data/music/songlink/?id=1", formdata=data_dict,
                          callback=self.get_song_info_dict)

    def get_song_info_dict(self, response):
        addr = response.meta.get("area")
        body = response.body
        body = json.loads(body)
        song_list = body.get("data").get("songList")
        album_name = list()
        songs_url = []
        for song in song_list:
            song_name = song.get("songName")
            if song_name in self.songs_set:
                continue

            self.songs_set.add(song_name)
            song_album_name = song.get("albumName")
            author_name = song.get("artistName")
            song_id = song.get("songId")

            album_name.append(song_album_name + "," + author_name + "," + song_name)
            song_link = song.get("songLink")
            songs_url.append(song_link)

            yield SongscrapyItem(song_id=song_id, song_album_name=song_album_name, song_name=song_name,
                                 author_name=author_name, song_link=song_link, address=addr)

        # yield FilescrapyItem(file_urls=songs_url, files=album_name)
