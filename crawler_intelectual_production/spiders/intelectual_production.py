import scrapy
from crawler_intelectual_production.items import CrawlerIntelectualProductionItem
import pandas as pd 

# 
class intelectual_production(scrapy.Spider):
    name = "intelectual_production"
     
    def start_requests(self):
        urls = list()
        
        # Open json file with downloaded  production, get the index and trasnform float numbers in int64
        # df = pd.read_json('test.json')['site_id'].astype(int)
        
        # create range of index that i will crawling, and merge with downloaded index production in the last turn that i runed the crawler 
        # df = df.append(pd.Series(range(130627,900000)), ignore_index=True)
        df = pd.Series(range(130627,900000))

        # Drop all index duplicates for criate dataframe with only not crawled index
        df = df.drop_duplicates(keep=False)

        # create all links that i will crawling  
        for i in df:
            url = "https://sucupira.capes.gov.br/sucupira/public/consultas/coleta/producaoIntelectual/viewProducaoIntelectual.jsf?popup=true&id_producao="+str(i)
            yield scrapy.Request(url=url, callback=self.parse)



    def parse(self, response):

        # instanciate item calass
        intel_prod_data = CrawlerIntelectualProductionItem()

        # teste if de addres crawled had information 
        # if YES, get the information, set id_status with True and call yield 
        # else set id_status with False and call yield
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
            yield intel_prod_data
        else:
            intel_prod_data['id_status'] = False
            intel_prod_data['site_id'] = response.url.split('=')[2]

            yield intel_prod_data   
