import scrapy
from bs4 import BeautifulSoup
from scrapy import Request


class AvSourceSpider(scrapy.Spider):
    name = 'av_source'
    allowed_domains = ['baza4.animevost.tv']
    query = {}
    result_genres = ''
    start_urls = ['http://baza4.animevost.tv/online/van_pis_sezon_1_1999_720_hd/37-1-0-399']
    custom_settings = {
        'ITEM_PIPELINES': {
            'animevost.pipelines.AnimevostPipeline2': 300,
        }
    }
    result = {}

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        if soup.find('div', {'class': 'player-box'}) is not None:
            if soup.find('div', {'class': 'player-box'}).find('iframe') is not None:
                genres = soup.find_all('ul', {'class': 'kino-lines'})
                for i in genres:
                    for r in i:
                        if 'Жанр:' in str(r.text):
                            self.result_genres = str(r.text).replace('Жанр: ', '').replace('По типу, ', '')
                self.result[response.url] = [soup.find('div', {'class': 'player-box'}).find('iframe').get('src'), self.result_genres]
            else:
                self.log('======================================')
                self.log('IFRAME NOT FIND !')
                self.log(response.url)
                self.log('======================================')
        else:
            self.log('======================================')
            self.log('PLAYER NOT FIND !')
            self.log(response.url)
            self.log('======================================')

        next_page = [i for i in self.query.keys()]

        while next_page:
            url_key = next_page.pop(0)
            value = self.query.pop(url_key)
            yield Request(value, callback=self.parse)

