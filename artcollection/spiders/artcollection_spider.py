import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from artcollection.items import ArtcollectionItem

class ArtcollectionSpider(CrawlSpider):
    name = "artspider"
    allowed_domains = ["tate.org.uk"]
    start_urls = [
        "http://www.tate.org.uk/art/search?limit=100",
    ]
    rules = (
        Rule(LinkExtractor(allow=('page\=\d', )), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        '''navigate=[]
        for i in range(5):
            link=response.css('#zone-content > div.container-16 > div > div > div.ajax-holder > div > div > div.listFoot > div > ul > li:nth-child('+str(i)+') > a::attr(href)').extract()
            if len(link)>0:
                navigate.append(link)

        for pages in navigate:
            for urls in self.start_urls :
                if pages!=urls:
                    self.start_urls.append('http://www.tate.org.uk'+pages[0])
'''
        for i in  range(100):
            a=response.css('#zone-content > div.container-16 > div > div > div.ajax-holder > div > div > div.search-background.grid.with-filters > ul > li:nth-child('+str(i)+') > div > div.grid-item-text > div.artist').xpath('./text()').extract()
            b=response.css('#zone-content > div.container-16 > div > div > div.ajax-holder > div > div > div.search-background.grid.with-filters > ul > li:nth-child('+str(i)+') > div > div.grid-item-text > div.title-and-date > a > span').xpath('./text()').extract()
            c=response.css('#zone-content > div.container-16 > div > div > div.ajax-holder > div > div > div.search-background.grid.with-filters > ul > li:nth-child('+str(i)+') > div > div.grid-item-text > div.title-and-date > span').xpath('./text()').extract()
            d=response.css('#zone-content > div.container-16 > div > div > div.ajax-holder > div > div > div.search-background.grid.with-filters > ul > li:nth-child('+str(i)+') > div > div.grid-item-image > a > img::attr(src)').extract()
            if len(a)!=0 and len(b)!=0 and len(c)!=0 and len(d)!=0 and len(c[0])<5 and int(c[0])>1700:
                item=ArtcollectionItem()
                item['artist']=a[0]
                item['title']=b[0]
                item['date']=c[0]
                item['image']="www.tate.org.uk"+d[0]
                yield item
