import scrapy
from scrapy import Request
from bs4 import BeautifulSoup
import hashlib


class AvSpider(scrapy.Spider):
    name = 'av'
    allowed_domains = ['baza4.animevost.tv']
    start_urls = ['http://baza4.animevost.tv/']
    dict_anime = {}
    visited = []
    custom_settings = {
            'ITEM_PIPELINES':{
            'animevost.pipelines.AnimevostPipeline1': 300,
        }
    }


    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        if soup.findAll('div', {'class': 'kino-item'}) is not None:
            for item in soup.findAll('div', {'class': 'kino-item'}):
                if item.find('ul', {'class': 'kino-lines'}) is not None:
                    if 'Игры' not in item.find('ul', {'class': 'kino-lines'}).text:
                        if item.find('a', {'class': 'kino-h'}).get('href') is not None and \
                                item.find('a', {'class': 'kino-h'}).get('href') is not None:
                            self.dict_anime[str(item.find('a', {'class': 'kino-h'}).text).replace('\n', '')] = [
                                item.find('a', {'class': 'kino-h'}).get('href'),
                                str(hashlib.md5(str(response.body).encode()).hexdigest())]
                        else:
                            self.log('======================================')
                            self.log("HREF OR TITLE IS NONE!")
                            self.log('======================================')
                else:
                    self.log('======================================')
                    self.log('K-LABEL')
                    self.log(str(item.find('div', {'class': 'kino-lines'}).find('a')))
                    self.log('======================================')
                    if item.find('a', {'class': 'kino-h'}).get('href') is not None and \
                            item.find('a', {'class': 'kino-h'}).get('href') is not None:
                        self.dict_anime[str(item.find('a', {'class': 'kino-h'}).text).replace('\n', '')] = [
                            item.find('a', {'class': 'kino-h'}).get('href'),
                            str(hashlib.md5(str(response.body).encode()).hexdigest())]
                    else:
                        self.log('======================================')
                        self.log("HREF OR TITLE IS NONE!")
                        self.log('======================================')

        else:
            self.log('======================================')
            self.log('kino-item IS NONE!')
            self.log('======================================')

        next_page = [str(i.get('href')) for i in soup.find('div', {'class': 'pagi-nav'}).findAll('a') if str(i.get('href')) not in self.visited]

        while next_page:
            url = next_page.pop(0)
            if url not in self.visited:
                self.visited.append(str(url))
                if url[0] == '/':
                    url = 'http://baza4.animevost.tv' + url
                next_page.append(response.urljoin(url))
                yield Request(url, callback=self.parse)

