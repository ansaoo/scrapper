
import scrapy


class TrailerSpider(scrapy.Spider):
    name = "url"

    start_urls = ['https://ww1.zone-telechargement.ws/13108-mentalist-saison-2-hd-720p-french.html',
                  'https://ww1.zone-telechargement.ws/13110-mentalist-saison-3-hdtv-french.html',
                  'https://ww1.zone-telechargement.ws/13140-mentalist-saison-4-hd-720p-french.html',
                  'https://ww1.zone-telechargement.ws/13144-mentalist-saison-5-hd-720p-french.html',
                  'https://ww1.zone-telechargement.ws/13149-mentalist-saison-6-hd-720p-french.html',
                  'https://ww1.zone-telechargement.ws/13190-mentalist-saison-7-hd-1080p-french.html']

    def parse(self, response):
        yield {
            'url': [href.strip() for href in response.css('div.postinfo a::attr(href)').extract()]
        }
