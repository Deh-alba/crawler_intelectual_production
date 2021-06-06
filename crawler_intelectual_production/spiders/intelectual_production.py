import scrapy
from urllib.parse import urlparse
import json
from crawler_intelectual_production.items import CrawlerIntelectualProductionItem


class intelectual_production(scrapy.Spider):
    name = "intelectual_production"
     
    def start_requests(self):
        urls = list()
        
        # get 0 to 900000

        for i in range(900000):
            urls.append(
                "https://sucupira.capes.gov.br/sucupira/public/consultas/coleta/producaoIntelectual/viewProducaoIntelectual.jsf?popup=true&id_producao="+str(i)
            )
        

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)



    def parse(self, response):

        intel_prod_data = CrawlerIntelectualProductionItem()


        if len(response.xpath('//*[@id="form:nome"]/text()'))>0:
            intel_prod_data['title_production'] = response.xpath('//*[@id="form:nome"]/text()').extract_first()
            intel_prod_data['site_id'] = response.url.split('=')[2]
            intel_prod_data['year'] = response.xpath('//*[@id="form:periodo"]/text()').extract_first()
            intel_prod_data['university'] = response.xpath('//*[@id="form:ies"]/text()').extract_first()
            intel_prod_data['program'] = response.xpath('//*[@id="form:programa"]/text()').extract_first()
            intel_prod_data['type_production'] = response.xpath('//*[@id="form:subtipo"]/text()').extract_first()
            intel_prod_data['sub_type_production'] = response.xpath('//*[@id="form:periodo"]/text()').extract_first()
            table = response.xpath('//*[@id="form"]/div[2]/div/div/div/div/div/table/tbody/*')
            list_aut=list()
            for autor in table:
                 list_aut.append(autor.css('span::text')[1].get())

            intel_prod_data["autors"] = list_aut

            yield intel_prod_data   
