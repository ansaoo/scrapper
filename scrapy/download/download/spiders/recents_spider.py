
import scrapy
import re
from dateutil import parser
import datetime


class RecentSpider(scrapy.Spider):
        name = "recents"

#        start_urls = ["https://www.themoviedb.org/movie/upcoming/"]
#         start_urls = ['http://www.allocine.fr/film/sorties-semaine/']
#         start_urls = ['http://www.allocine.fr/film/agenda/sem-2017-10-11/',
#                       'http://www.allocine.fr/film/agenda/sem-2017-11-01/'
#                       ]

        def start_requests(self):
            urls = [
                # 'http://www.allocine.fr/film/agenda/sem-2017-12-13/',
                # 'http://www.allocine.fr/film/agenda/sem-2017-12-20/',
                # 'http://www.allocine.fr/film/agenda/sem-2017-12-27/',
                # 'http://www.allocine.fr/film/agenda/sem-2018-01-03/',
                # 'http://www.allocine.fr/film/agenda/sem-2018-01-10/',
                # 'http://www.allocine.fr/film/agenda/sem-2018-01-17/',
                # 'http://www.allocine.fr/film/agenda/sem-2018-01-24/',
                # 'http://www.allocine.fr/film/agenda/sem-2018-01-31/',
                # 'http://www.allocine.fr/film/agenda/sem-2018-02-07/',
                # 'http://www.allocine.fr/film/agenda/sem-2018-02-14/',
                # 'http://www.allocine.fr/film/agenda/sem-2018-02-21/',
                # 'http://www.allocine.fr/film/agenda/sem-2018-02-28/',
                # 'http://www.allocine.fr/film/agenda/sem-2018-03-07/',
                # 'http://www.allocine.fr/film/agenda/sem-2018-03-14/',
                # 'http://www.allocine.fr/film/agenda/sem-2018-03-21/',
                # 'http://www.allocine.fr/film/agenda/sem-2018-03-28/',
                'http://www.allocine.fr/film/agenda/sem-2018-04-04/',
                'http://www.allocine.fr/film/agenda/sem-2018-04-11/',
                'http://www.allocine.fr/film/agenda/sem-2018-04-18/',
                ]
            for url in urls:
                yield scrapy.Request(url=url, callback=self.parse)
        
        def parse(self, response):
            def parse_date(date, to_str=False):
                mapping = {'janvier': 'january',
                           'février': 'february',
                           'mars': 'march',
                           'avril': 'april',
                           'mai': 'may',
                           'juin': 'june',
                           'juillet': 'july',
                           'août': 'august',
                           'septembre': 'september',
                           'octobre': 'october',
                           'novembre': 'november',
                           'décembre': 'december'}
                for key in mapping.keys():
                    if key in date:
                        date = date.replace(key, mapping[key])
                date = parser.parse(date, fuzzy=True)
                return datetime.datetime.strftime(date, '%Y-%m-%dT%H:%M:%S.000Z+0000') if to_str else date

            def avg(rate_list):
                return sum([float(elem.strip().replace(',', '.'))
                            for elem in rate_list]) / len(rate_list) if len(rate_list) != 0 else 0

            regex = '(.*)cfilm=(?P<cfilm>[0-9]*).html'
            for quote in response.css('div.card.card-entity.card-entity-list.cf'):
                res = re.match(regex, quote.css('h2.meta-title a::attr(href)').extract_first())
                yield {
                        'title': quote.css('h2.meta-title a::text').extract_first(),
                        'eventDate': parse_date(quote.css('div.meta-body-item.meta-body-info span::text').extract_first(), to_str=True),
                        'kind': quote.css('div.meta-body-item.meta-body-info span::text').extract()[3:],
                        'dirs': quote.css('div.meta-body-item.meta-body-direction.light span::text').extract(),
                        'actors': quote.css('div.meta-body-item.meta-body-actor.light span::text').extract(),
                        'id': {'allocine': res.groupdict()['cfilm'], 'name_attr': 'cfilm'} if res else None,
                        'rate': avg(quote.css('span.stareval-note::text').extract()),
                        'synopsis': {'fr': quote.css('div.synopsis::text').extract_first().strip()},
                        'estimation': 0
                        }
            for href in response.css('h2.meta-title a::attr(href)'):
                yield response.follow(href, callback=self.parse_trailer)

        def parse_trailer(self, response):
            regex = '(.*)cmedia=(?P<cmedia>[0-9]*)&cfilm=(?P<cfilm>[0-9]*).html'
            for href in response.css('a::attr(href)').extract():
                res = re.match(regex, href)
                if href.startswith('/video/player'):
                    yield {
                        'trailers': {'src': 'http://www.allocine.fr/_video/iblogvision.aspx?cmedia=',
                                     'values': [res.groupdict()['cmedia']]} if res else None,
                        'id': {'allocine': res.groupdict()['cfilm'], 'name_attr': 'cfilm'} if res else None
                    }
