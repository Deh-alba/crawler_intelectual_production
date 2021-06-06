import scrapy
from urllib.parse import urlparse
import json
from crawler_intelectual_production.items import CrawlerIntelectualProductionItem
import pandas as pd 


class intelectual_production(scrapy.Spider):
    name = "intelectual_production"
     
    def start_requests(self):
        urls = list()

        df = pd.read_json('test.json')['site_id'].astype(int)
        df = df.append(pd.Series(range(80000,900000)), ignore_index=True)
        df = df.drop_duplicates(keep=False)

        # get 80000 to 900000
        for i in df:
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
            intel_prod_data['id_status'] = True
            table = response.xpath('//*[@id="form"]/div[2]/div/div/div/div/div/table/tbody/*')
            list_aut=list()
            for autor in table:
                 list_aut.append(autor.css('span::text')[1].get())

            intel_prod_data["autors"] = list_aut
        else:
            intel_prod_data['id_status'] = False
            intel_prod_data['site_id'] = response.url.split('=')[2]

            yield intel_prod_data   
