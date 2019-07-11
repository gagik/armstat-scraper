import scrapy
import urllib
import logging
from scrapy.http.request.form import FormRequest

class ArmStatScraper(scrapy.Spider):
    name = 'armstat-scraper'
    start_urls = ['http://armstatbank.am/pxweb/hy/ArmStatBank/?rxid=ef3a1ac5-f82c-471b-a817-39c4fb0f703c']
    download_delay = 1.5
    def parse(self, response):
        ids_re = r'__doPostBack\(\'(.*)\'\)'
        for id in response.css('.AspNet-TreeView-Root a').re(ids_re):
            requestInfo = urllib.parse.unquote(id).split("','")
            formdata = {
                '__EVENTTARGET': requestInfo[0], 
                '__EVENTARGUMENT': requestInfo[1],
            }
            request = FormRequest.from_response(response=response,
                                                formdata=formdata,
                                                callback=self.takeEachParty,
                                                dont_click=True)
            yield request

    def takeEachParty(self, response):
        sections = response.css('.AspNet-TreeView-Parent a::text').extract()
        for section in sections:
            print(section.strip())