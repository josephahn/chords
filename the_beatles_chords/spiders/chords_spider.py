from scrapy import Spider, Request
from the_beatles_chords.items import TheBeatlesChordsItem
import re
import json

class TheBeatlesChordsSpider(Spider):
    name = 'the_beatles_chords_spider'
    start_urls = ['https://www.ultimate-guitar.com/artist/the_beatles_1916?filter=chords']

    def parse(self, response):
        data = response.css('div.js-store::attr(data-content)').get()
        pages = json.loads(data)['store']['page']['data']['pagination']['pages']
        page_urls = list(map(lambda p: p['url'], pages))

        for url in page_urls:
            yield response.follow(url, callback=self.parse_page)

    def parse_page(self, response):
        data = response.css('div.js-store::attr(data-content)').get()
        tabs = json.loads(data)['store']['page']['data']['other_tabs']
        tab_urls = list(map(lambda t: t['tab_url'], tabs))

        for url in tab_urls:
            yield Request(url=url, callback=self.parse_tab)

    def parse_tab(self, response):
        data = response.css('div.js-store::attr(data-content)').get()
        json_data = json.loads(data)

        name = json_data['store']['page']['data']['tab']['song_name']
        content = json_data['store']['page']['data']['tab_view']['wiki_tab']['content']
        chords = re.findall('\[ch\](.*?)\[\/ch\]', content)

        item = TheBeatlesChordsItem()
        item['name'] = name
        item['chords'] = chords

        yield item


