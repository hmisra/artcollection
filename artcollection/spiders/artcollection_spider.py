import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from artcollection.items import ArtcollectionItem
import re



class ArtcollectionSpider(scrapy.Spider):
    TAG_RE = re.compile(r'<[^>]+>')

    def remove_tags(self, text):
        return self.TAG_RE.sub('', text)

    name = "artspider"
    allowed_domains = ["tate.org.uk"]
    start_urls = [
        "http://www.tate.org.uk/art/search?limit=100&type=artwork&wdr=1700-2015&wi=1&wot=6",
    ]

    def parse(self, response):

        for i in range(100):
            url=response.css('#zone-content > div.container-16 > div > div > div.ajax-holder > div > div > div.search-background.grid.with-filters > ul > li:nth-child('+str(i)+') > div > div.grid-item-image > a::attr(href)').extract()
            image = response.css('#zone-content > div.container-16 > div > div > div.ajax-holder > div > div > div.search-background.grid.with-filters > ul > li:nth-child('+str(i)+') > div > div.grid-item-image > a > img::attr(src)').extract()
            item=ArtcollectionItem()
            nexturl=response.css('#zone-content > div.container-16 > div > div > div.ajax-holder > div > div > div.listFoot > div > ul > li.pager-next > a::attr(href)').extract()
            if len(nexturl)!=0:
                yield scrapy.Request("http://www.tate.org.uk"+nexturl[0],callback=self.parse)
            if len(url)!=0 and len(image)!=0:
                valueurl="http://www.tate.org.uk"+url[0]
                item['image']="http://www.tate.org.uk"+image[0]
                item['url']=valueurl
                request = scrapy.Request(valueurl,callback=self.parse_item)
                request.meta['item'] = item
                yield request

    # function to extract information from painting page
    def parse_item(self, response):

        item = response.meta['item']
        title=response.css('#region-header-second > div > h1 > span.title-row > span.title').xpath('./text()').extract()
        artist=response.css('#region-sidebar-artwork > div > div > div > div > div > div.infoArtists.infoFirstRow > div > a > span').xpath('./text()').extract()
        artistlife = response.css('#region-sidebar-artwork > div > div > div > div > div > div.infoArtists.infoFirstRow > div > span').xpath('./text()').extract()
        date = response.css('#region-sidebar-artwork > div > div > div > div > div > div:nth-child(3) > span.infoValue.infoDate > span').xpath('./text()').extract()
        medium = response.css('#region-sidebar-artwork > div > div > div > div > div > div:nth-child(4) > span.infoValue.infoMedium').xpath('./text()').extract()
        dimensions = response.css ('#region-sidebar-artwork > div > div > div > div > div > div:nth-child(5) > span.infoValue.infoSize').xpath('./text()').extract()
        collection = response.css('#region-sidebar-artwork > div > div > div > div > div > div.infoRow.infoOwner > div').xpath('./text()').extract()
        acquisition = response.css('#region-sidebar-artwork > div > div > div > div > div > div:nth-child(7) > span.infoValue.infoCredit').xpath('./text()').extract()
        reference = response.css('#region-sidebar-artwork > div > div > div > div > div > div:nth-child(8) > div > span > span').xpath('./text()').extract()
        if len(title)!=0 and len(artist)!=0 and len(artistlife)!=0 and len(date)!=0 and len(medium)!=0 and len(dimensions)!=0 and len(collection)!=0 and len(acquisition)!=0 and len(reference)!=0:
            item['artist']=artist[0]
            item['title']=title[0]
            item['date']=date[0]
            item['medium']=medium[0]
            item['dimensions']=dimensions[0]
            item['artistlife']=artistlife[0]
            item['collection']=collection[0]
            item['acquisition']=acquisition[0]
            item['reference']=reference[0]
            artistbiourl=response.css('#region-sidebar-artwork > div > div > div > div > div > div.infoArtists.infoFirstRow > div > a::attr(href)').extract()
            infourl=response.css('#zone-content > div.zone-content.clearfix.container-16.artwork-text > div.clearfix.artwork-texts-menu.grid-4 > ul > li:nth-child(1) > a::attr(href)').extract()
            if len(artistbiourl)!=0:
                request = scrapy.Request("http://www.tate.org.uk"+artistbiourl[0],callback=self.parse_artist)
                request.meta['item'] = item
                yield request
            if len(infourl)!=0:
                request=scrapy.Request('http://www.tate.org.uk'+infourl[0],callback=self.parse_info)
                request.meta['item']=item
                yield request

    # function to extract artist biography
    def parse_artist(self, response):

        item = response.meta['item']
        artistbio=response.css('#zone-content > div.zone-content.clearfix.equal-height-container.container-16.artist-text-block > div.grid-12.region.main-content.equal-height-element > div > div > div.field-name-body > article > div > div > div').extract()
        if len(artistbio)!=0:
            item['artistbio']=re.sub(' +',' ',self.remove_tags(artistbio[0]))
            return item

    # function to extract the painting summary
    def parse_info(self, response):
        item = response.meta['item']
        info=response.css('#region-content > div > div > div > div.field-name-body > article > div').extract()
        if len(info)!=0:
            item['info']=re.sub(' +',' ',self.remove_tags(info[0]))
            return item
